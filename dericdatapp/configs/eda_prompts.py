from ..utils import load_template

# A dictionary to map function names to their specific text
EDA_FUNCTION_PROMPTS = {
    "analyze_numerical_statistics": {
        "header": load_template("eda_num_stats_h.txt"),
        "footer": "--- STATISTICAL SUMMARY END ---"
    },
    "analyze_categorical_statistics": {
        "header": load_template("eda_cat_stats_h.txt"),
        "footer": "--- STATISTICAL SUMMARY END ---"
    },
}