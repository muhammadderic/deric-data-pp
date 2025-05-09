# Project Name

## Project Description
This package serves as a diagnostic bridge between raw data and actionable insight by automating the initial interrogation of datasets. It enforces a rigorous, standardized approach to data profiling, ensuring that structural anomalies and statistical distributions are exposed before any modeling begins.

## Features
* Exploratory Data Analysis
* Raw Code View Support
* Prompt Preview

## Colab Usage Instructions
### General
```python
!pip install git+https://github.com/muhammadderic/deric-data-pp.git --quiet

import dericdatapp.eda as dda
num_cols, cat_cols, other_cols = classify_dataframe_columns(df)
dda.analyze_numerical_statistics(df, num_cols)
dda.analyze_categorical_statistics(df, cat_cols)
dda.show_missing_values(df)
dda.show_unique_values_of_cat_columns(df)
dda.show_column_unique_values(df, column_name)
```

### Raw Code Support
To view the underlying logic of any dericdatapp function directly within your notebook, use the .raw() method attached to the function.

Example 1: View Full Source Code
This will display the complete function, including its docstrings and internal comments.

```python
import dericdatapp as ddp
# Display the full implementation of the classifier
ddp.eda.classify_dataframe_columns.raw()
```

Example 2: View Pure Logic (No Comments)
If you want to see just the executable code without the documentation or commentary, pass pure=True.

```python
import dericdatapp as ddp
# Display only the functional code
ddp.eda.classify_dataframe_columns.raw(pure=True)
```

Summary of the Feature
The .raw() utility is a built-in introspection tool designed for transparency and education. It allows users to instantly audit the preprocessing logic or copy specific code snippets for customization without leaving the Google Colab environment or browsing external repositories.

### Prompt Preview
This feature lets you wrap your analysis output with a smart instruction (prompt) so it can be directly used by an LLM.

```python
import dericdatapp as ddp
# Display only the functional code
ddp.eda.analyze_numerical_statistics(df).prompt()
```

It will:
- Show a header → explains how to interpret the data (for AI)
- Show your analysis result
- Show a footer → tells what kind of output is expected

## Project Structure
```
project-name/
│── dericdatapp/
│   ├── eda.py
│   ├── info.py
|   |
│   ├── configs
│   ├── utils
│   └── templates
└── pyproject.toml
```

## Contributing Guidelines
1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Submit a pull request

## License
This project is licensed under the MIT License.

**Developed by muhammadderic**  
[My GitHub Profile](https://github.com/muhammadderic)