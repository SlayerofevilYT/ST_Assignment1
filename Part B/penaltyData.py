import pandas as pd
from datetime import datetime

df = pd.read_csv('penalty_data_set_2.csv')

dateSearchTerm = input("Enter a search date (dd/mm/yyyy): ")
#keywordSearchTerm = input("Enter a search term: ")

try:
    searchDate = datetime.strptime(dateSearchTerm, '%d/%m/%Y')
except ValueError:
    print("Invalid date format")
    exit()

#result = df[df.apply(lambda row: row.astype(str).str.contains(keywordSearchTerm).any(), axis = 1)]

df['OFFENCE_MONTH'] = pd.to_datetime(df['OFFENCE_MONTH'], format='%d/%m/%Y')

result = df[df['OFFENCE_MONTH'] == searchDate]

if not result.empty:
    print("Search results:")
    print(result)
else:
    print("No matching records found.")
