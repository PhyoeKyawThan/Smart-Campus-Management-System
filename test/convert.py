import pandas as pd

# Read the Excel file, all sheets
xlsx = pd.ExcelFile('test.xlsx')

# Create a dictionary to hold the data for all sheets
all_data = {}

# Loop through each sheet
for sheet_name in xlsx.sheet_names:
    # Read the sheet into a DataFrame
    df = pd.read_excel(xlsx, sheet_name=sheet_name)
    
    # Convert the DataFrame to a dictionary where each key is a column name
    # and each value is a list of rows as dictionaries
    column_dict = {}
    for col in df.columns:
        column_dict[col] = df[[col]].to_dict(orient='records')
    
    # Add to the all_data dictionary
    all_data[sheet_name] = column_dict

# Print the resulting dictionary
from json import dumps, loads

with open('data.json', 'w') as file:
    file.write(dumps(all_data))
