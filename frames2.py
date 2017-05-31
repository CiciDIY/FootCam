import wx
from wx.lib.pubsub import Publisher
import pygame, sys
from pygame.locals import *
import pygame.camera
import picamera
from datetime import datetime

 
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
        camBtn = wx.Button(panel, label ="Take Sideview Photo")
        camBtn.Bind(wx.EVT_BUTTON, self.takephotocam)
 
        sizer = wx.GridSizer(2,2,5,5)
        sizer.Add(closeBtn, 0, wx.EXPAND)
        sizer.Add(camBtn, 0, wx.EXPAND)
        
        panel.SetSizer(sizer)
    #######################################################################
    def takephotocam(self, event):
        """Operation to take photo"""
        pygame.init()
        pygame.camera.init()

        cam = pygame.camera.Camera("/dev/video0",(352,288))
        cam.start()
        image= cam.get_image()
        filename = "101.jpg"
        pygame.image.save(image, "sideviewphoto.jpg")
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
        self.pntext = wx.StaticText(self, -1, "Patient Number")
        self.patsur = wx.TextCtrl(self, value = "")
        self.surtext = wx.StaticText(self, -1, "Patient Surname")
        self.patdb = wx.TextCtrl(self, value = "")
        self.dbtext = wx.StaticText(self, -1, "Patient date of birth")
        self.patweight = wx.TextCtrl(self, value = "")
        self.weighttext = wx.StaticText(self, -1, "Patient weight")
        self.patheight = wx.TextCtrl(self, value = "")
        self.heighttext = wx.StaticText(self, -1, "Patient height")
        
        bottomBtn = wx.Button(self, label="To Bottomview camera")
        bottomBtn.Bind(wx.EVT_BUTTON, self.hideFrame3)
 
        sizer = wx.GridSizer(7, 2, 5, 5)
        
        sizer.Add(self.patnum, 0, wx.EXPAND)
        sizer.Add(self.pntext, 0, wx.EXPAND)
        sizer.Add(self.patsur,  0, wx.EXPAND)
        sizer.Add(self.surtext, 0, wx.EXPAND)
        sizer.Add(self.patdb,  0, wx.EXPAND)
        sizer.Add(self.dbtext, 0, wx.EXPAND)
        sizer.Add(self.patweight, 0, wx.EXPAND)
        sizer.Add(self.weighttext, 0, wx.EXPAND)
        sizer.Add(self.patheight,  0, wx.EXPAND)
        sizer.Add(self.heighttext, 0, wx.EXPAND)
        sizer.Add(bottomBtn,  0, wx.EXPAND)
        self.SetSizer(sizer)

    def hideFrame3(self,event):
        """Close Patient information Panel and open Bottom Camera Panel"""
        self.frame.Hide()
        new_frame3 = BottomView()
        new_frame3.Show()
        if self.patnum.GetValue() :
            Fname = str(self.patnum.GetValue()) + " " + str(datetime.strftime(datetime.now(), '%Y-%m-%d'))+".txt"
            Fhand = open(Fname, "w")
            Fhand.write("Patient Number: " + str(self.patnum.GetValue()))
            Fhand.write("\n")
        if self.patsur.GetValue():
            Fhand.write("Patient surname: " + str(self.patsur.GetValue()))
            Fhand.write("\n")
        if self.patdb.GetValue():
            Fhand.write("Patient date of Birth: " + str(self.patdb.GetValue()))
            Fhand.write("\n")
        if self.patweight.GetValue():
            Fhand.write("Patient weight: " + str(self.patweight.GetValue()))
            Fhand.write("\n")
        if self.patheight.GetValue():
            Fhand.write("Patient height: " + str(self.patheight.GetValue()))
            Fhand.write("\n")
            Fhand.close()
            
            
            

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
        wx.Frame.__init__(self, None, wx.ID_ANY, "Foot Camera program")
        panel = MainPanel(self)

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
        
        sideBtn = wx.Button(panel, label= "To Sideview camera")
        sideBtn.Bind(wx.EVT_BUTTON, self.hideFrame4)
        BckBtn = wx.Button(panel, label = " Take photo Backview")
        BckBtn.Bind(wx.EVT_BUTTON, self.takephotocam2)

        sizer = wx.GridSizer(2,2,5,5)
        sizer.Add(sideBtn, 0, wx.EXPAND)
        sizer.Add(BckBtn, 0, wx.EXPAND)
        panel.SetSizer(sizer)

    def hideFrame4(self,event):
        """Close BAckview and open sideview"""
        self.Hide()
        new_frame4= SideView()
        new_frame4.Show()

    def takephotocam2(self, event):
        """Operation to take photo"""
        pygame.init()
        pygame.camera.init()

        cam = pygame.camera.Camera("/dev/video0",(352,288))
        cam.start()
        image= cam.get_image()
        pygame.image.save(image,'Backview.jpg')
        cam.stop()
        
class BottomView(wx.Frame):
    """"""
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Bottomview camera")
        panel = wx.Panel(self)
        
        backBtn = wx.Button(panel, label="To Backview camera")
        backBtn.Bind(wx.EVT_BUTTON, self.hideFrame2)
        picamBtn = wx.Button(panel, label = " Take Bottomview photo")
        picamBtn.Bind(wx.EVT_BUTTON, self.camerapi)
        
        sizer = wx.GridSizer(2,2,5,5)
        sizer.Add(backBtn, 0, wx.EXPAND)
        sizer.Add(picamBtn, 0, wx.EXPAND)
        panel.SetSizer(sizer)
        
    def hideFrame2(self,event):
        """close Bottomview and open backview"""
        self.Hide()
        new_frame2 = BackView()
        new_frame2.Show()

    def camerapi(self,event):
        camera = picamera.PiCamera()
        camera.capture('BottomView.jpg')
        camera.close()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
