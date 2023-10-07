import wx
import wx.grid
import wx.xrc
import wx.adv
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure

from main import Frame1 as Frame1

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('penalty_data_set_2.csv')

print("All searches are able to be left blank. Press enter if you do not want use the search parameters.")

# Prompt the user for a search date
start_date_input = input("Enter a start date (dd/mm/yyyy): ")
end_date_input = input("Enter an end date (dd/mm/yyyy): ")
keyword = input("Enter a keyword to search for or leave it blank: ")

if keyword:  # WILL NEED TO CHANGE FOR UI, Right now it just asks for the specific name of the column you want to search in
    keyword_search_column = input("Enter the column you would like to search for a keyword in: ")

# Specify column names
dates_column_name = 'OFFENCE_MONTH'
penalty_value_column_name = 'FACE_VALUE'


class MyFrame(Frame1):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.Layout()
        self.Show(True)

    def DateSearch():
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
                result = df[(df[dates_column_name].apply(
                    lambda date_str: start_date <= datetime.strptime(date_str, "%d/%m/%Y") <= end_date))]
            else:
                result = df  # If start date is greater than end date, select all rows

            return result

    def KeywordSearch(result):
        if result.isna:
            if keyword:
                result = result[result[keyword_search_column].str.contains(keyword,
                                                                           case=False)]  # If result and keyword are not null, search through result[]
        elif result:
            if keyword:
                result = df[(df[keyword_search_column].str.contains(keyword,
                                                                    case=False))]  # If result is null but keyword is not, search through df[]

        return result

    def DisplayResults(result):
        # Display the search results
        if not result.empty:
            print("Search results:")
            print(result)

            dates = pd.to_datetime(result[dates_column_name], format="%d/%m/%Y")
            values = result[dates_column_name].to_numpy()

            # Continue with matplotlib graphs

        else:
            print("No matching records found.")

    def AverageCost(result):
        average_cost = result[penalty_value_column_name].mean()

        return average_cost

    def StartSearch():
        dateResult = DateSearch()
        keywordResult = KeywordSearch(dateResult)
        average_cost = AverageCost(keywordResult)
        DisplayResults(keywordResult)

        # print("The average cost for these penalties are: " + average_cost)

    StartSearch()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
