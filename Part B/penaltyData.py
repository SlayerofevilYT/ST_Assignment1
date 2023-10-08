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

df = pd.read_csv('penalty_data_set_2.csv', low_memory=False)
editedDF = df

matplotlib.use('WXAgg')

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

        self.table = LoadData(editedDF)
        self.m_grid_data.SetTable(self.table, takeOwnership=True)

        self.filteredDF = editedDF
        self.resetBool = False

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
        if self.resetBool:
            temp_df = editedDF
        else:
            temp_df = self.filteredDF

        temp_df['OFFENCE_MONTH'] = pd.to_datetime(temp_df['OFFENCE_MONTH'], format='%d/%m/%Y')

        wx_min_date = self.m_datePicker_start.GetValue()
        wx_max_date = self.m_datePicker_end.GetValue()

        min_date = self.wxdate2pydate(wx_min_date)
        max_date = self.wxdate2pydate(wx_max_date)

        if min_date <= max_date:
            search_result = temp_df[(temp_df['OFFENCE_MONTH'] >= min_date) & (temp_df['OFFENCE_MONTH'] <= max_date)]

        if self.resetBool == False:
            self.filteredDF = editedDF

        self.UpdateGrid(search_result)

    def KeywordSearch(self, event):
        if self.resetBool:
            temp_df = editedDF
        else:
            temp_df = self.filteredDF

        keyword = self.m_text_search.GetValue()
        search_result = temp_df[temp_df['OFFENCE_DESC'].str.contains(keyword, case=False)]

        if self.resetBool == False:
            self.filteredDF = editedDF

        self.UpdateGrid(search_result)

    def VideoData(self, events):
        if self.resetBool:
            temp_df = editedDF
        else:
            temp_df = self.filteredDF

        search_result = temp_df[temp_df['OFFENCE_DESC'].str.contains('Camera', case=False)]

        if self.resetBool == False:
            self.filteredDF = editedDF

        self.UpdateGrid(search_result)

    def ToggleReset(self, events):
        if self.resetBool is True:
            self.resetBool == False
        elif self.resetBool is False:
            self.resetBool == True
            self.filteredDF = editedDF

    def UpdateGrid(self, data):
        # Helper method to update the grid with search results
        temptable = LoadData(data)
        self.m_grid_data.ClearGrid()
        self.m_grid_data.SetTable(temptable, True)
        self.Layout()

    def GraphUpdate(self, event):
        figure_score = self.plot_data(df)
        h, w = self.m_panel1.GetSize()
        figure_score.set_size_inches(h / figure_score.get_dpi(), w / figure_score.get_dpi())

        canvas = FigureCanvasWxAgg(self.m_panel1, -1, figure_score)
        canvas.SetSize(self.m_panel1.GetSize())

        self.Layout()

    def plot_data(self, df):
        if 'OFFENCE_MONTH' in df.keys() and 'MOBILE_PHONE_IND' in df.keys():
            # create dataframe using only relevant data
            dfMbPh = pd.DataFrame(df, columns=['OFFENCE_MONTH', 'MOBILE_PHONE_IND'])

            # convert the OFFENCE_MONTH to datetime
            dfMbPh['OFFENCE_MONTH'] = pd.to_datetime(dfMbPh['OFFENCE_MONTH'], dayfirst=True)

            # calling selected dates and converted to correct format
            wx_min_date = self.m_datePicker_start.GetValue()
            wx_max_date = self.m_datePicker_end.GetValue()
            min_date = self.wxdate2pydate(wx_min_date)
            max_date = self.wxdate2pydate(wx_max_date)

            # removing data outside of selected timeframe
            if min_date <= max_date:
                dfMbPh = dfMbPh[(dfMbPh['OFFENCE_MONTH'] >= min_date) & (dfMbPh['OFFENCE_MONTH'] <= max_date)]

            # add a column for YEAR of accident and MONTH of accident
            try:
                dfMbPh['YEAR'] = dfMbPh['OFFENCE_MONTH'].dt.year
                dfMbPh['MONTH'] = dfMbPh['OFFENCE_MONTH'].dt.month
            except:
                print("Dates Dont Exist")
                return
            # drop unnecessary date column
            dfMbPh.drop(columns=['OFFENCE_MONTH'], inplace=True)

            # dataframe w/ only mobile phone related incidents
            dfMbPhCountTemp = dfMbPh[dfMbPh['MOBILE_PHONE_IND'] == 'Y']

            # dataframe w/ count of incidents per month per year
            dfMbPhCount = dfMbPhCountTemp.groupby(['YEAR', 'MONTH'])['MOBILE_PHONE_IND'].count().reset_index(
                name='COUNT')

            # concat MONTH and YEAR and convert to datetime
            dfMbPhCount['DATE'] = dfMbPhCount['MONTH'].map(str) + '-' + dfMbPhCount['YEAR'].map(str)
            dfMbPhCount['DATE'] = pd.to_datetime(dfMbPhCount['DATE'], format='%m-%Y')
            # plot as line
            figure_score = Figure()
            ax = figure_score.add_subplot(3, 1, 1)
            ax.plot(dfMbPhCount['DATE'], dfMbPhCount['COUNT'])
            ax.set_xlabel("Year")
            ax.set_ylabel("Mobile Phone Penalties")
            ax.grid(linestyle='--')
        else:
            return

        if 'OFFENCE_MONTH' in df.keys() and 'FACE_VALUE' in df.keys() and 'TOTAL_NUMBER' in df.keys():
            # create dataframe using only relevant data
            dfAvFi = pd.DataFrame(df, columns=['OFFENCE_MONTH', 'FACE_VALUE', 'TOTAL_NUMBER'])
            # convert the OFFENCE_MONTH to datetime
            dfAvFi['OFFENCE_MONTH'] = pd.to_datetime(dfAvFi['OFFENCE_MONTH'], dayfirst=True)

            # calling selected dates and converted to correct format
            wx_min_date = self.m_datePicker_start.GetValue()
            wx_max_date = self.m_datePicker_end.GetValue()
            min_date = self.wxdate2pydate(wx_min_date)
            max_date = self.wxdate2pydate(wx_max_date)

            # removing data outside of selected timeframe
            if min_date <= max_date:
                dfAvFi = dfAvFi[(dfAvFi['OFFENCE_MONTH'] >= min_date) & (dfAvFi['OFFENCE_MONTH'] <= max_date)]

            # add a column for YEAR of accident and MONTH of accident
            try:
                dfAvFi['YEAR'] = dfAvFi['OFFENCE_MONTH'].dt.year
                dfAvFi['MONTH'] = dfAvFi['OFFENCE_MONTH'].dt.month
            except:
                print("Dates Dont Exist")
                return
            # dataframe w/ average fine price of every column
            dfAvFi['AVG'] = dfAvFi["FACE_VALUE"].multiply(df["TOTAL_NUMBER"], axis="index")

            # merging Month and Year into Date
            dfAvFi['DATE'] = dfAvFi['MONTH'].map(str) + '-' + dfAvFi['YEAR'].map(str)

            # drop unnecessary date column
            dfAvFi.drop(columns=['OFFENCE_MONTH'], inplace=True)
            dfAvFi.drop(columns=['FACE_VALUE'], inplace=True)
            dfAvFi.drop(columns=['MONTH'], inplace=True)
            dfAvFi.drop(columns=['YEAR'], inplace=True)

            # merging columns based on the same date
            aggregation_functions = {'TOTAL_NUMBER': 'sum', 'DATE': 'first', 'AVG': 'sum'}
            dfAvFi = dfAvFi.groupby('DATE', as_index=False).aggregate(aggregation_functions)
            dfAvFi['AVG'] = dfAvFi['AVG'].div(dfAvFi['TOTAL_NUMBER'])

            # convert the Date to datetime
            dfAvFi['DATE'] = pd.to_datetime(dfAvFi['DATE'], format='%m-%Y')

            # sorting the values by date
            dfAvFi.sort_values(by=['DATE'], inplace=True)

            # plot as line
            ax = figure_score.add_subplot(3, 1, 2)
            ax.plot(dfAvFi['DATE'], dfAvFi['AVG'])
            ax.set_xlabel("Year")
            ax.set_ylabel("Average Fine Amount")
            ax.grid(linestyle='--')
        else:
            return

        if 'OFFENCE_MONTH' in df.keys() and 'MOBILE_PHONE_IND' in df.keys():
            # create dataframe using only relevant data
            dfOffCD = pd.DataFrame(df, columns=['OFFENCE_CODE', 'OFFENCE_MONTH'])

            # convert the OFFENCE_MONTH to datetime
            dfOffCD['OFFENCE_MONTH'] = pd.to_datetime(dfOffCD['OFFENCE_MONTH'], dayfirst=True)

            # calling selected dates and converted to correct format
            wx_min_date = self.m_datePicker_start.GetValue()
            wx_max_date = self.m_datePicker_end.GetValue()
            min_date = self.wxdate2pydate(wx_min_date)
            max_date = self.wxdate2pydate(wx_max_date)

            # removing data outside of selected timeframe
            if min_date <= max_date:
                dfOffCD = dfOffCD[(dfOffCD['OFFENCE_MONTH'] >= min_date) & (dfOffCD['OFFENCE_MONTH'] <= max_date)]

            # adding a count and removing duplicate offence codes
            dfOffCD = dfOffCD.assign(COUNT=dfOffCD['OFFENCE_CODE'].map(dfOffCD['OFFENCE_CODE'].value_counts()))
            dfOffCD = dfOffCD.drop_duplicates(subset='OFFENCE_CODE', keep="first")
            # setting the count to 75 if the count is larger than 50
            dfOffCD['COUNT'].where(dfOffCD['COUNT'] <= 50, 75, inplace=True)
            # plot as line
            ax = figure_score.add_subplot(3, 1, 3)
            ax.bar(dfOffCD['OFFENCE_CODE'], dfOffCD['COUNT'])
            ax.set_xlabel("OFFENCE_CODE")
            ax.set_ylabel("Cases per offense code")
            ax.grid(linestyle='--')
        else:
            return
        return figure_score


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
