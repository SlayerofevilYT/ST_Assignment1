# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv
import wx.grid


###########################################################################
## Class Frame1
###########################################################################

class Frame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"NSW Traffic Penalty Data", pos=wx.DefaultPosition,
                          size=wx.Size(1492, 1000), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        wSizer1 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.m_togglereset = wx.ToggleButton(self, wx.ID_ANY, u"Reset Search", wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer1.Add(self.m_togglereset, 0, wx.ALL, 5)

        self.m_button8 = wx.Button(self, wx.ID_ANY, u"Video Data", wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer1.Add(self.m_button8, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 50)

        self.m_text_search = wx.TextCtrl(self, wx.ID_ANY, u"Keyword\n\n", wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer1.Add(self.m_text_search, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 50)

        self.m_button_search_submit = wx.Button(self, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer1.Add(self.m_button_search_submit, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 50)

        self.m_toggleBtn2 = wx.ToggleButton(self, wx.ID_ANY, u"Update Graphs", wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer1.Add(self.m_toggleBtn2, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 50)

        self.m_static_startdate = wx.StaticText(self, wx.ID_ANY, u"Starting Date", wx.DefaultPosition, wx.DefaultSize,
                                                0)
        self.m_static_startdate.Wrap(-1)

        wSizer1.Add(self.m_static_startdate, 0, wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_datePicker_start = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition,
                                                        wx.DefaultSize, wx.adv.DP_DEFAULT)
        wSizer1.Add(self.m_datePicker_start, 0, wx.ALL, 5)

        self.m_static_enddata = wx.StaticText(self, wx.ID_ANY, u"Ending Date", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_static_enddata.Wrap(-1)

        wSizer1.Add(self.m_static_enddata, 0, wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_datePicker_end = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition,
                                                      wx.DefaultSize, wx.adv.DP_DEFAULT)
        wSizer1.Add(self.m_datePicker_end, 0, wx.ALL, 5)

        self.m_button_date_submit = wx.Button(self, wx.ID_ANY, u"Submit", wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer1.Add(self.m_button_date_submit, 0, wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer5.Add(wSizer1, 0, wx.ALL | wx.EXPAND, 0)

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        self.m_grid_data = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid_data.CreateGrid(20, 25)
        self.m_grid_data.EnableEditing(False)
        self.m_grid_data.EnableGridLines(True)
        self.m_grid_data.EnableDragGridSize(False)
        self.m_grid_data.SetMargins(0, 0)

        # Columns
        self.m_grid_data.AutoSizeColumns()
        self.m_grid_data.EnableDragColMove(False)
        self.m_grid_data.EnableDragColSize(True)
        self.m_grid_data.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Rows
        self.m_grid_data.EnableDragRowSize(True)
        self.m_grid_data.SetRowLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Label Appearance

        # Cell Defaults
        self.m_grid_data.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        bSizer7.Add(self.m_grid_data, 0, wx.ALL, 5)

        bSizer5.Add(bSizer7, 1, wx.EXPAND, 5)

        wSizer2 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        wSizer2.Add(self.m_panel1, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel2 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        wSizer2.Add(self.m_panel2, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel3 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        wSizer2.Add(self.m_panel3, 1, wx.EXPAND | wx.ALL, 5)

        bSizer5.Add(wSizer2, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer5)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_togglereset.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleReset)
        self.m_button8.Bind(wx.EVT_BUTTON, self.VideoData)
        self.m_text_search.Bind(wx.EVT_TEXT, self.KeywordUpdate)
        self.m_text_search.Bind(wx.EVT_TEXT_ENTER, self.KeywordUpdate)
        self.m_button_search_submit.Bind(wx.EVT_BUTTON, self.KeywordSearch)
        self.m_toggleBtn2.Bind(wx.EVT_TOGGLEBUTTON, self.GraphUpdate)
        self.m_datePicker_start.Bind(wx.adv.EVT_DATE_CHANGED, self.StartDateUpdate)
        self.m_datePicker_end.Bind(wx.adv.EVT_DATE_CHANGED, self.EndDateUpdate)
        self.m_button_date_submit.Bind(wx.EVT_BUTTON, self.DateSearch)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def ToggleReset(self, event):
        event.Skip()

    def VideoData(self, event):
        event.Skip()

    def KeywordUpdate(self, event):
        event.Skip()

    def KeywordSearch(self, event):
        event.Skip()

    def GraphUpdate(self, event):
        event.Skip()

    def StartDateUpdate(self, event):
        event.Skip()

    def EndDateUpdate(self, event):
        event.Skip()

    def DateSearch(self, event):
        event.Skip()
