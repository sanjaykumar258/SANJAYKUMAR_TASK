def get_eda_prompt(sample_data):
    return f"""
    Analyze this dataset sample and give a very short EDA summary.

    Include only:
    - What the data is about (1 line)
    - Any issues (missing values, errors, outliers)
    - Main issue (most important problem)
    - Simple suggestion to fix it

    Keep it clear, easy to read, and under 6 bullet points.

    Data:
    {sample_data}
    """
