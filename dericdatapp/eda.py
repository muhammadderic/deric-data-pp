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