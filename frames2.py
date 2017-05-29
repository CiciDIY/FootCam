import wx
from wx.lib.pubsub import Publisher
import pygame, sys
from pygame.locals import *
import pygame.camera
import picamera
from time import sleep

 
########################################################################
class SideView(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Sideview Camera")
        panel = wx.Panel(self)
        closeBtn = wx.Button(panel, label="Back to Patient Info")
        closeBtn.Bind(wx.EVT_BUTTON, self.BacktoPatInfo)
        camBtn = wx.Button(panel, label ="Take side photo")
        camBtn.Bind(wx.EVT_BUTTON, self.takephotocam)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        flags = wx.ALL|wx.CENTER
        sizer.Add(camBtn, 0, flags, 5)
        sizer.Add(closeBtn, 0, flags, 5)
        panel.SetSizer(sizer)
    #######################################################################
    def takephotocam(self, event):
        """Operation to take photo"""
        pygame.init()
        pygame.camera.init()

        cam = pygame.camera.Camera("/dev/video0",(352,288))
        cam.start()
        image= cam.get_image()
        pygame.image.save(image,'101.jpg')

        cam.stop()

    #----------------------------------------------------------------------
    def BacktoPatInfo(self, event):
        """Close camera windows and restart with new patient"""
        self.Close()
        PatInfo = MainFrame()
        PatInfo.Show()
 
########################################################################
class MainPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Patient information Panel"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        Publisher().subscribe(self.showFrame, ("show.mainframe"))
        self.patnum = wx.TextCtrl(self, value = "")
        self.pntext = wx.StaticText(self, -1, "Patient number")
        self.patsur = wx.TextCtrl(self, value = "")
        self.surtext = wx.StaticText(self, -1, "Patient Surname")
        self.patdb = wx.TextCtrl(self, value = "")
        self.dbtext = wx.StaticText(self, -1, "Patient date of birth")
        self.patweight = wx.TextCtrl(self, value = "")
        self.weighttext = wx.StaticText(self, -1, "Patient weight")
        self.patheight = wx.TextCtrl(self, value = "")
        self.heighttext = wx.StaticText(self, -1, "Patient height")
        
        bottomBtn = wx.Button(self, label="To bottom view camera")
        bottomBtn.Bind(wx.EVT_BUTTON, self.hideFrame3)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.patnum, -1, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.pntext, -1, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.patsur, -1, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.surtext, -1, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.patdb, -1, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.dbtext, -1, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.patweight, -1, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.weighttext, -1, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.patheight, -1, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.heighttext, -1, wx.ALL|wx.CENTER, 5)
        sizer.Add(bottomBtn, 0, wx.ALL|wx.CENTER, 5)
        self.SetSizer(sizer)

    def hideFrame3(self,event):
        """Close Patient information Panel and open Bottom Camera Panel"""
        self.frame.Hide()
        new_frame3 = BottomView()
        new_frame3.Show()

    #----------------------------------------------------------------------
    def hideFrame(self, event):
        """"""
        self.frame.Hide()
        new_frame = OtherFrame()
        new_frame.Show()
 
    #----------------------------------------------------------------------
    def showFrame(self, msg):
        """"""

        frame = self.GetParent()
        frame.Show()
 
########################################################################
class MainFrame(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Foot Cam program")
        panel = MainPanel(self)

class startsection(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent)
        self.frame = parent

        Publisher().subscribe(self.showFrame, ("show.mainframe"))
        startBtn = wx.Button(self, label="Start Program")
        startBtn.Bind(wx.EVT_BUTTON, self.hideFrame)

        sizer= wx.BoxSizer(wx.Vertical)
        sizer.Add(startBtn, 0, wx.ALL|wx.CENTER, 5)
        self.SetSizer(sizer)

    def hideFrame(self,event):
        """"""
        self.frame.Hide()
        new_frame = MainPanel()
        new_frame.Show()

    def showFrame(self):
        frame = self.GetParent()
        frame.Show
########################################################################

class BackView(wx.Frame):
    """Backview of Camera interface"""
    
    def __init__(self):
        
        wx.Frame.__init__(self, None, wx.ID_ANY, "Backview Camera" )
        panel = wx.Panel(self)
        
        sideBtn = wx.Button(self, label= "To sideview camera")
        sideBtn.Bind(wx.EVT_BUTTON, self.hideFrame4)
        BckBtn = wx.Button(self, label = " Take photo backview")
        BckBtn.Bind(wx.EVT_BUTTON, self.takephotocam2)

        sizer = wx.BoxSizer(wx.VERTICAL)
        flags = wx.ALL|wx.CENTER
        sizer.Add(sideBtn, 0, flags, 5)
        sizer.Add(BckBtn, 0, flags, 5)
        panel.SetSizer(sizer)

    def hideFrame4(self,event):
        """Close BAckview and open sideview"""
        self.frame.Hide()
        new_frame4= SideView()
        new_frame4.Show()

    def takephotocam2(self, event):
        """Operation to take photo"""
        pygame.init()
        pygame.camera.init()

        cam = pygame.camera.Camera("/dev/video0",(352,288))
        cam.start()
        image= cam.get_image()
        pygame.image.save(image,'101.jpg')

        cam.stop()
class BottomView(wx.Frame):
    """"""
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "BottomView Camera")
        panel = wx.Panel(self)
        
        backBtn = wx.Button(self, label="To backview camera")
        backBtn.Bind(wx.EVT_BUTTON, self.hideFrame2)
        picamBtn = wx.Button(panel, label = " Take Bottom view photo")
        picamBtn.Bind(wx.EVT_BUTTON, self.camerapi)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        flags = wx.ALL|wx.CENTER
        sizer.Add(backBtn, 0, flags, 5)
        sizer.Add(picamBtn, 0, flags, 5)
        panel.SetSizer(sizer)
        
    def hideFrame2(self,event):
        """close Bottomview and open backview"""
        self.frame.Hide()
        new_frame2 = BackView()
        new_frame2.Show()

    def camerapi(self,event):
        camera = picamera.PiCamera()
        camera.capture('image.jpg')

        camera.start_preview()
        camera.vflip = True
        camera.hflip = True
        camera.brightness = 60
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
