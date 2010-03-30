# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
tododoc
'''

import pkg_resources
import wx
from garlicsim_wx.general_misc.third_party import aui

import garlicsim
from garlicsim_wx.widgets import WorkspaceWidget

from . import images as __images_package
images_package = __images_package.__name__


class PlaybackControls(wx.Panel, WorkspaceWidget):
    #DoGetBestSize = lambda self: wx.Size(180, 96)
    def __init__(self, frame):
        wx.Panel.__init__(self, frame, -1, size=(180, 96),
                          style=wx.SUNKEN_BORDER)
        aui_pane_info = aui.AuiPaneInfo().\
            Caption('PLAYBACK CONTROLS').\
            CloseButton(False).\
            Fixed().\
            BestSize(180, 96).MinSize(180, 96).MaxSize(180, 96)
        WorkspaceWidget.__init__(self, frame, aui_pane_info)
        
        self.Bind(wx.EVT_SIZE, self.on_size)
        
        
        bitmap_list = ['to_start', 'previous_node', 'play',
                                'next_node', 'to_end', 'pause',
                                'finalize']
        
        bitmaps_dict = self.bitmap_dict = {}
        for bitmap_name in bitmap_list:
            path = pkg_resources.resource_filename(images_package,
                                                   bitmap_name + '.png')
            self.bitmap_dict[bitmap_name] = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)


        v_sizer = self.v_sizer = wx.BoxSizer(wx.VERTICAL)


        b1 = wx.Button(self, -1, size=(180, 30))
        v_sizer.Add(b1, 0)


        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
                           
        self.button_to_start = wx.BitmapButton(
            self, -1, bitmaps_dict['to_start'], size=(30, 50)
        )
        self.button_previous_node = wx.BitmapButton(
            self, -1, bitmaps_dict['previous_node'], size=(30, 50)
        )
        self.button_play = wx.BitmapButton(
            self, -1, bitmaps_dict['play'], size=(60, 50)
        )
        self.button_next_node= wx.BitmapButton(
            self, -1, bitmaps_dict['next_node'], size=(30, 50)
        )
        self.button_to_end = wx.BitmapButton(
            self, -1, bitmaps_dict['to_end'], size=(30, 50)
        )
        
        # Some buttons should be grayed out depending on the path!
        
        
        self.Bind(wx.EVT_BUTTON, self.on_button_to_start,
                  source=self.button_to_start)
        
        self.Bind(wx.EVT_BUTTON, self.on_button_previous_node,
                  source=self.button_previous_node)
        
        self.Bind(wx.EVT_BUTTON, self.on_button_to_start,
                  source=self.button_to_start)
        
        self.Bind(wx.EVT_BUTTON, self.on_button_next_node,
                  source=self.button_next_node)
        
        self.Bind(wx.EVT_BUTTON, self.on_button_to_end,
                  source=self.button_to_end)
        
        button_line = (
            self.button_to_start,
            self.button_previous_node,
            self.button_play,
            self.button_next_node,
            self.button_to_end
        )
        
        for button in button_line:
            h_sizer.Add(button, 0)
        v_sizer.Add(h_sizer,)


        b3 = wx.Button(self, -1, size=(180, 16))
        v_sizer.Add(b3, 1)


        self.SetSizer(v_sizer)
        v_sizer.Layout()
        


    def on_size(self, e=None):
        self.Refresh()
        if e is not None:
            e.Skip()
            
    def update_buttons_status(self, e=None):
        if self.gui_project.path is None:
            self.button_to_start.Disable()
            self.button_previous_node.Disable()
            self.button_play.Disable()
            self.button_next_node.Disable()
            self.button_to_end.Disable()
        
        elif self.gui_project.active_node is None:
            self.button_previous_node.Disable()
            self.button_next_node.Disable()
            self.button_play.Disable()
            
        else:
            self.button_play.Enable()
            
            if self.gui_project.active_node.parent is not None:
                self.button_previous_node.Enable()
                self.button_to_start.Enable()
            else:
                self.button_previous_node.Disable()
                self.button_to_start.Disable()
                
            if self.gui_project.active_node.children:
                self.button_next_node.Enable()
                self.button_to_end.Enable()
            else:
                self.button_next_node.Disable()
                self.button_to_end.Disable()
        
    def OnPaint(self, e):
        self.update_buttons_status()
        wx.Panel.OnPaint(self, e)
        
    def on_button_to_start(self, e=None):
        try:
            if self.gui_project.path is None: return
            start_node = self.gui_project.path[0]
            self.gui_project.set_active_node(start_node)
        except garlicsim.data_structures.path.PathOutOfRangeError:
            return
        
    def on_button_to_end(self, e=None):
        try:
            if self.gui_project.path is None: return
            end_node = self.gui_project.path[-1]
            self.gui_project.set_active_node(end_node)
        except garlicsim.data_structures.path.PathOutOfRangeError:
            return
    
    def on_button_previous_node(self, e=None):
        if self.gui_project.active_node is None: return
        previous_node = self.gui_project.active_node.parent
        if previous_node is not None:
            self.gui_project.set_active_node(previous_node)
        
                
    def on_button_next_node(self, e=None):
        if self.gui_project.active_node is None: return
        try:
            next_node = \
                self.gui_project.path.next_node(self.gui_project.active_node)
            self.gui_project.set_active_node(next_node)
        except garlicsim.data_structures.path.PathOutOfRangeError:
            return
        
        