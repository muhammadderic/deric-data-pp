import pandas as pd

def analyze_numerical_statistics(df: pd.DataFrame):
    """
    Compute and display descriptive statistics for numerical features.

    Parameters:
    - df (pd.DataFrame): Dataset containing numerical variables.

    Returns:
    - None: This function prints a summary directly to the console.
    """

    # 1. Correct type selection for all numbers
    numerical_cols = df.select_dtypes(include=["number"]).columns
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
    print("-" * 31)
    print("DERICDATAPP: NUMERICAL ANALYSIS")
    print("-" * 31)

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


def show_unique_values_of_cat_columns(df: pd.DataFrame, column_name: str):
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