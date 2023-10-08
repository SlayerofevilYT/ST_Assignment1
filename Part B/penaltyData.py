import wx
import wx.grid
import wx.xrc
import wx.adv
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
from main import Frame1 as Frame1
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure

matplotlib.use('WXAgg')

# Load the CSV file into a pandas DataFrame
resetBool = False
EVEN_ROW_COLOUR = '#CCE6FF'
GRID_LINE_COLOUR = '#ccc'


# print("All searches are able to beleft blank. Press enter if you do not want use the search parameters.")

# Prompt the user for a search date
# start_date_input = input("Enter a start date (dd/mm/yyyy): ")
# end_date_input = input("Enter an end date (dd/mm/yyyy): ")
# keyword = input("Enter a keyword to search for or leave it blank: ")

# if keyword:  # WILL NEED TO CHANGE FOR UI, Right now it just asks for the specific name of the column you want to search in
#    keyword_search_column = input("Enter the column you would like to search for a keyword in: ")

class LoadData(wx.grid.GridTableBase):
    def __init__(self, data=None):
        wx.grid.GridTableBase.__init__(self)
        self.headerRows = 1
        self.data = data

    def GetNumberRows(self):
        return len(self.data.index)

    def GetNumberCols(self):
        return len(self.data.columns)

    def GetValue(self, row, col):
        return self.data.iloc[row, col]

    def SetValue(self, row, col, value):
        self.data.iloc[row, col] = value

    # For better visualisation
    def GetColLabelValue(self, col):
        return self.data.columns[col]

    def GetAttr(self, row, col, prop):
        attr = wx.grid.GridCellAttr()
        if row % 2 == 1:
            attr.SetBackgroundColour(EVEN_ROW_COLOUR)
        return attr


class MyFrame(Frame1):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.df = pd.read_csv('penalty_data_set_2.csv', index_col=0, low_memory=False)
        self.editedDF = self.df
        self.table = LoadData(self.df)
        self.m_grid_data.SetTable(self.table, takeOwnership=True)

        self.Show(True)
        self.Layout()

        self.search_filters = []

    def wxdate2pydate(self, date):
        assert isinstance(date, wx.DateTime)
        if date.IsValid():
            year = date.GetYear()
            month = date.GetMonth() + 1
            day = date.GetDay()

            # Format day, month, and year as strings
            formatted_day = "{:02d}".format(day)  # Format day with leading zeros
            formatted_month = "{:02d}".format(month)  # Format month with leading zeros
            formatted_year = "{:04d}".format(year)  # Format year with four digits

            # Create a Python datetime.datetime object with the formatted date components
            formatted_date = datetime(int(formatted_year), int(formatted_month), int(formatted_day))
            return formatted_date
        else:
            return None

    def DateSearch(self, event):
        if resetBool == True:
            temp_df1 = self.df
        elif resetBool == False:
            temp_df1 = self.editedDF

        temp_df1['OFFENCE_MONTH'] = pd.to_datetime(temp_df1['OFFENCE_MONTH'], format='%d/%m/%Y')

        wx_min_date = self.m_datePicker_start.GetValue()
        wx_max_date = self.m_datePicker_end.GetValue()

        min_date = self.wxdate2pydate(wx_min_date)
        max_date = self.wxdate2pydate(wx_max_date)

        if min_date <= max_date:
            temp_df = temp_df1[(temp_df1['OFFENCE_MONTH'] >= min_date) & (temp_df1['OFFENCE_MONTH'] <= max_date)]
            temptable = LoadData(temp_df)
        else:
            #print("Invalid date")
            temptable = LoadData(self.df)

        self.m_grid_data.ClearGrid()
        self.m_grid_data.SetTable(temptable,True)
        self.Layout()

        self.editedDF = temp_df

    def KeywordSearch(self):
        if resetBool == True:
            if keyword:
                search_result = df[df.str.contains(keyword, case=False)]
                temptable = LoadData(search_result)
        elif resetBool == False:
            if keyword:
                editedDF = editedDF[(editedDF.str.contains(keyword, case=False))]
                temptable = LoadData(editedDF)
        else:
            search_result = df
            temptable = LoadData(search_result)

        self.m_grid_data.ClearGrid()
        self.m_grid_data.SetTable(temptable, True)
        self.Layout()


    def CameraDetected(self):
        if resetBool == True:
            if keyword:
                df = df[df['OFFENCE_DESC'].str.contains('Camera Detected', case=False)]
        elif resetBool == False:
            if keyword:
                editedDF = editedDF[editedDF['OFFENCE_DESC'].str.contains('Camera Detected', case=False)]

        self.m_grid_data.ClearGrid()
        self.m_grid_data.SetTable(temptable, True)
        self.Layout()


    def ToggleReset(self):
        if resetBool is True:
            resetBool == False
        elif resetBool is False:
            resetBool == True


'''
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
'''

if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()