import pandas as pd
import os
from config import client
from prompts import get_eda_prompt

# Read the mental health dataset
file_path = os.path.join(os.path.dirname(__file__), "data.csv")

def generate_eda_report(file_path):
    print("Loading data")
    df = pd.read_csv(file_path)
    
    # Extracting a sample of data for the model to analyze
    sample_data = df.sample(15, random_state=42).to_dict(orient='records')

    print("Generating EDA Prompt")
    prompt = get_eda_prompt(sample_data)
    
    print("Sending Request to Gemini API")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text

if __name__ == "__main__":
    try:
        eda_report = generate_eda_report(file_path)
        print("\n--- EDA REPORT ---\n")
        print(eda_report)
        print("\n------------------\n")
        
    except FileNotFoundError:
        print(f"Error: Could not find the dataset at {file_path}.")
        print("Please make sure you have 'data.csv' in the 'src' directory.")
    except Exception as e:
        print(f"An error occurred: {e}")
