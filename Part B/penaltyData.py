import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('penalty_data_set_2.csv')

print("All searches are able to be left blank. Press enter if you do not want use the search parameters.")

# Prompt the user for a search date
start_date_input = input("Enter a start date (dd/mm/yyyy): ")
end_date_input = input("Enter an end date (dd/mm/yyyy): ")
keyword = input("Enter a keyword to search for or leave it blank: ")

# Specify the name of the column you want to search in
column_name = 'OFFENCE_MONTH'


# Convert the start and end date strings to datetime objects if they were provided
if start_date_input:
    try:
        start_date = datetime.strptime(start_date_input, "%d/%m/%Y")
    except ValueError:
        print("Invalid start date format. Please use the format dd/mm/yyyy.")
        exit()
else:
    start_date = datetime.min  # Set to the minimum possible datetime if there was no date provided

if end_date_input:
    try:
        end_date = datetime.strptime(end_date_input, "%d/%m/%Y")
    except ValueError:
        print("Invalid end date format. Please use the format dd/mm/yyyy.")
        exit()
else:
    end_date = datetime.max  # Set to the maximum possible datetime if there was no date provided


if start_date <= end_date:
    result = df[
        (df[column_name].apply(lambda date_str: start_date <= datetime.strptime(date_str, "%d/%m/%Y") <= end_date))
    ]
else:
    result = df  # If start date is greater than end date, select all rows

if keyword:
    result = result[result['OFFENCE_DESC'].str.contains(keyword, case = False)]

# Display the search results
if not result.empty:
    print("Search results:")
    print(result)

    dates = pd.to_datetime(result[column_name], format="%d/%m/%Y")
    values = result[column_name].to_numpy()

    # Continue with matplotlib graphs

else:
    print("No matching records found.")

