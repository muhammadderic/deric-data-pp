import pandas as pd

from .utils import add_raw_support, custom_prompt, get_prompt
# from .configs import EDA_FUNCTION_PROMPTS

# EDA_NUM_STATS_H = open("templates/eda_num_stats_h.txt").read()

# Extract the specific text for each function
# num_stats_text = EDA_FUNCTION_PROMPTS.get("analyze_numerical_statistics", {})

@add_raw_support
def classify_dataframe_columns(df: pd.DataFrame):
    """
    Separates dataframe columns into numerical, categorical, and other types.

    Parameters:
    df (pd.DataFrame): The dataset to analyze.

    Returns:
    tuple: (numerical_cols, categorical_cols, other_cols) as lists of strings.
    """
    
    # 1. Identify Numerical Columns (Integers and Floats)
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    # 2. Identify Categorical Columns (Objects and Categorical types)
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 3. Identify Other Columns (Datetime, Timedelta, Bool, etc.)
    # We exclude 'number', 'object', and 'category' to find the rest
    other_cols = df.select_dtypes(exclude=['number', 'object', 'category']).columns.tolist()

    # Print Summary Table-style counts
    print("--- Column Type Summary ---")
    print(f"Numerical Columns:   {len(num_cols)}")
    print(f"Categorical Columns: {len(cat_cols)}")
    print(f"Other Columns:       {len(other_cols)}")
    
    # Show specific types for 'Other' if they exist
    if other_cols:
        print("\nDetails for 'Other' Data Types:")
        for col in other_cols:
            print(f"- {col}: {df[col].dtype}")
    
    return num_cols, cat_cols, other_cols


@add_raw_support
@custom_prompt(
    header=get_prompt("eda_num_stats_h"),
    footer="--- STATISTICAL SUMMARY END ---",
)
def analyze_numerical_statistics(df: pd.DataFrame, numerical_cols):
    """
    Compute and display descriptive statistics for numerical features.

    Parameters:
    - df (pd.DataFrame): Dataset containing numerical variables.
    - numerical_cols (list of str): List of numerical column names to analyze.

    Returns:
    - None: This function prints a summary directly to the console.
    """

    # 1. Correct type selection for all numbers
    numerical_stats = {} 

    for col in numerical_cols:
        # Skip if all values are NaN to avoid calculation errors
        if df[col].isna().all():
            numerical_stats[col] = {'error': 'all_null'}
            continue

        # Pre-calculate quantiles to keep the 'stats' dictionary clean
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        stats = {
            'mean': round(df[col].mean(), 4),
            'median': round(df[col].median(), 4),
            'std_dev': round(df[col].std(), 4),
            'variance': round(df[col].var(), 4), # Useful for ML Info/Entropy
            'min': round(df[col].min(), 4),
            'max': round(df[col].max(), 4),
            'range': round(df[col].max() - df[col].min(), 4),
            'missing_count': int(df[col].isna().sum()),
            'missing_percentage': round(df[col].isna().sum() / len(df) * 100, 2),
            'q1': round(q1, 4),
            'q3': round(q3, 4),
            'iqr': round(iqr, 4)
        }
        numerical_stats[col] = stats

    # 2. Printing Section
    for col, stats in numerical_stats.items():
        if 'error' in stats:
            print(f"\n{col}: [!] ALL VALUES ARE NULL - SKIPPING")
            continue

        print(f"\n{col}:")
        print(f"  Central: Mean: {stats['mean']} | Median: {stats['median']}")
        print(f"  Spread:  Std Dev: {stats['std_dev']} | Var: {stats['variance']} | Range: {stats['range']}")
        print(f"  Values:  Min: {stats['min']} | Max: {stats['max']}")
        print(f"  Quality: Missing: {stats['missing_count']} ({stats['missing_percentage']}%)")
        print(f"  Tiers:   Q1: {stats['q1']} | Q3: {stats['q3']} | IQR: {stats['iqr']}")

    return None


@add_raw_support
@custom_prompt(
    header=get_prompt("eda_cat_stats_h"),
    footer="--- STATISTICAL SUMMARY END ---",
)
def analyze_categorical_statistics(df, categorical_cols, top_n=20):
    """
    Compute and display descriptive statistics for categorical features.

    Parameters:
    - df (pd.DataFrame): Dataset containing categorical variables.
    - categorical_cols (list of str): List of categorical column names to analyze.
    - top_n (int, optional): Number of top frequent categories to store (default=20).

    Returns:
    - None
    """

    categorical_stats = {}  # Local result storage

    for col in categorical_cols:

        freq_counts = df[col].value_counts()
        freq_percentages = df[col].value_counts(normalize=True) * 100

        distribution = {}
        for idx, (value, count) in enumerate(freq_counts.items()):
            if idx < top_n:
                percentage = freq_percentages[value]
                distribution[str(value)] = {
                    'count': int(count),
                    'percentage': round(percentage, 2)
                }

        stats = {
            'unique_values': df[col].nunique(),
            'missing_count': int(df[col].isna().sum()),
            'missing_percentage': round(df[col].isna().sum() / len(df) * 100, 2),
            'mode': str(df[col].mode()[0]) if not df[col].mode().empty else None,
            'mode_frequency': int(freq_counts.iloc[0]) if not freq_counts.empty else 0,
            'mode_percentage': round(freq_percentages.iloc[0], 2) if not freq_percentages.empty else 0,
            'top_distribution': distribution
        }

        categorical_stats[col] = stats

    # Print section moved inside function
    for col, stats in categorical_stats.items():
        print(f"\nField ({col}):")
        print(f"  Unique: {stats['unique_values']}")
        print(f"  Mode: '{stats['mode']}' ({stats['mode_percentage']}% of data)")
        print(f"  Missing: {stats['missing_count']} ({stats['missing_percentage']}%)")
        print(f"  Top 5 values:")

        for val, freq in list(stats['top_distribution'].items())[:5]:
            print(f"    '{val}': {freq['count']} rows ({freq['percentage']}%)")

    return None


@add_raw_support
def show_missing_values(df: pd.DataFrame):
    """
    Show null and blank value counts.

    Returns: 
    - None
    """

    summary = {}

    for col in df.columns:
        null_count = df[col].isnull().sum()
        blank_count = 0

        if df[col].dtype == "object":
            # Using .fillna("") ensures we don't get errors when stripping
            blank_count = (df[col].astype(str).str.strip() == "").sum()
        total_missing = int(null_count + blank_count)
        # Only store and print if there is actually something missing
        if total_missing > 0:
            summary[col] = {
                "null_values": int(null_count),
                "blank_values": int(blank_count),
                "total_missing": total_missing
            }

    # Printing Section
    print("Missing Value Summary:")
    for col, counts in summary.items():
        print(f"\nColumn: {col}")
        print(f"- null_values: {counts['null_values']}")
        print(f"- blank_values: {counts['blank_values']}")
        print(f"- total_missing: {counts['total_missing']}")

    return None


@add_raw_support
def show_unique_values_of_cat_columns(df: pd.DataFrame):
    """
    Identifies all categorical columns and prints their unique value summaries.

    Parameters:
    df (pd.DataFrame): The dataset to analyze.

    Returns:
    - None
    """
    # Identify categorical columns (object or category types)
    cat_cols = df.select_dtypes(include=['object', 'category']).columns

    if len(cat_cols) == 0:
        print("No categorical columns found in the DataFrame.")
        return None

    print(f"Found {len(cat_cols)} categorical columns.\n")

    for col in cat_cols:
        unique_values = df[col].unique()
        unique_count = len(unique_values)
        total_rows = len(df)

        print(f"--- Field: '{col}' ---")
        print(f"Total Row Count: {total_rows}")
        print(f"Unique Value Count: {unique_count}")

        # Only print the list if it's manageable (15 or fewer)
        if unique_count <= 15:
            # We cast to list and handle potential NaN values for cleaner printing
            print(f"Unique Values: {list(unique_values)}")
        else:
            print(f"Unique Values: [Too many to display - {unique_count} items]")
        
        print()

    return None


def show_column_unique_values(df: pd.DataFrame, column_name: str):
    """
    Prints unique values only if count <= 15.

    Parameters:
    df (pd.DataFrame): The dataset to analyze.
    column_name (str): The name of the field to check for unique values.

    Returns:
    - None
    """
    unique_values = df[column_name].unique()
    unique_count = len(unique_values)
    total_rows = len(df)

    print(f"--- Total unique values for field: '{column_name}' ---")
    print(f"Total Row Count: {total_rows}")
    print(f"Unique Value Count: {unique_count}")

    # Only print the list if it's manageable (15 or fewer)
    if unique_count <= 15:
        print(f"Unique Values: {list(unique_values)}")
    else:
        print(f"Unique Values: [Too many to display - {unique_count} items]")

    return None