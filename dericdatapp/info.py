def info():
    """Prints the capabilities of dericlens."""
    print("""--- dericdatapp: Data Preparation ---
    
    [Exploratory Data Analysis]
    - Numerical statistics (.eda.analyze_numerical_statistics(df: pd.DataFrame))
    - Missing value (.eda.show_missing_values(df: pd.DataFrame))
    - Unique values 
      - All columns (.eda.show_unique_values_of_cat_columns(df: pd.DataFrame))
      - Specific columns (.eda.show_column_unique_values(df: pd.DataFrame, column_name: str))""")