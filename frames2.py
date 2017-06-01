import wx
from wx.lib.pubsub import Publisher
import pygame, sys
from pygame.locals import *
import pygame.camera
import picamera
from datetime import datetime
import subprocess
import time
import os
variable1 = 0

 
########################################################################
class SideView(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, variable1):
        """Constructor"""
        self.variable1 = variable1
        wx.Frame.__init__(self, None, wx.ID_ANY, "Sideview Camera")
        panel = wx.Panel(self)
        
        closeBtn = wx.Button(panel, label="Back to Patient Info")
        closeBtn.Bind(wx.EVT_BUTTON, self.BacktoPatInfo)
        camBtn = wx.Button(panel, label ="Take Sideview Photo")
        camBtn.Bind(wx.EVT_BUTTON, self.takephotocam)
        self.Bind(wx.EVT_CLOSE, self.on_close)
 
        sizer = wx.GridSizer(2,2,5,5)
        sizer.Add(closeBtn, 0, wx.EXPAND)
        sizer.Add(camBtn, 0, wx.EXPAND)


        
        panel.SetSizer(sizer)

    def on_close(self, event):
        self.Destroy()
        sys.exit(0)
    #######################################################################
    def takephotocam(self, event):
        """Operation to take photo"""
        pygame.init()
        pygame.camera.init()

        cam = pygame.camera.Camera("/dev/video0",(352,288))
        cam.start()
        image= cam.get_image()
        filename = str(self.variable1) + " Sideview.jpg"
        filename2 =str(self.variable1)
        npath ="/home/pi/FootCam/" + str(filename2)
        if not os.path.isdir(npath):
            os.makedirs(npath)
        pygame.image.save(image, npath + "/" + filename)
            

    #----------------------------------------------------------------------
    def BacktoPatInfo(self, event):
        """Close camera windows and restart with new patient"""
        self.Hide()
        PatInfo = MainFrame()
        PatInfo.Show()

########################################################################
class MainPanel(wx.Panel):
    """"""
    variable1 = 0
    #----------------------------------------------------------------------
    def __init__(self, parent, variable1):
        """Patient information Panel"""
        wx.Panel.__init__(self, parent=parent)
        MainPanel.variable1 = variable1 + 2
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
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
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
        
        if self.patnum.GetValue() :
            variable1 = int(self.patnum.GetValue())
            filename2 =str(variable1)
            npath ="/home/pi/FootCam/" + str(filename2)
            if not os.path.isdir(npath):
                os.makedirs(npath)
            Fname = str(self.patnum.GetValue()) + " " + str(datetime.strftime(datetime.now(), '%Y-%m-%d'))+".txt"
            Fhand = open(npath + "/" + Fname, "w")
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

        new_frame3 = BottomView(variable1)
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
        
    def on_close(self, event):
        self.Destroy()
        sys.exit(0)
 
########################################################################
class MainFrame(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Foot Camera program")
        panel = MainPanel(self, variable1)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def hideFrame(self,event):
        """"""
        self.frame.Hide()
        new_frame = MainPanel()
        new_frame.Show()

    def showFrame(self):
        frame = self.GetParent()
        frame.Show()
        
    def on_close(self, event):
        self.Destroy()
        sys.exit(0)
########################################################################

class BackView(wx.Frame):
    """Backview of Camera interface"""
    
    def __init__(self, variable1):
        self.variable1 = variable1
        wx.Frame.__init__(self, None, wx.ID_ANY, "Backview Camera" )
        panel = wx.Panel(self)
        sideBtn = wx.Button(panel, label= "To Sideview camera")
        sideBtn.Bind(wx.EVT_BUTTON, self.hideFrame4)
        BckBtn = wx.Button(panel, label = " Take photo Backview")
        BckBtn.Bind(wx.EVT_BUTTON, self.takephotocam2)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        sizer = wx.GridSizer(2,2,5,5)
        sizer.Add(sideBtn, 0, wx.EXPAND)
        sizer.Add(BckBtn, 0, wx.EXPAND)
        panel.SetSizer(sizer)

    def hideFrame4(self,event):
        """Close BAckview and open sideview"""
        self.Hide()
        new_frame4= SideView(self.variable1)
        new_frame4.Show()

    def takephotocam2(self, event):
        """Operation to take photo"""
        pygame.init()
        pygame.camera.init()

        cam = pygame.camera.Camera("/dev/video0",(352,288))
        cam.start()
        image= cam.get_image()
        imgname = str(self.variable1) + " Backview.jpg"
        filename2 =str(self.variable1)
        npath ="/home/pi/FootCam/" + str(filename2)
        if not os.path.isdir(npath):
            os.makedirs(npath)
        pygame.image.save(image,npath + "/" +imgname)
        cam.stop()

    def on_close(self, event):
        self.Destroy()
        sys.exit(0)
        
class BottomView(wx.Frame):
    """"""
    def __init__(self,variable1):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Bottomview camera")
        panel = wx.Panel(self)
        self.variable1 = variable1
        #self.Image = wx.StaticBitmap(self, bitmap=wx.EmptyBitmap())
        backBtn = wx.Button(panel, label="To Backview camera")
        backBtn.Bind(wx.EVT_BUTTON, self.hideFrame2)
        picamBtn = wx.Button(panel, label = " Take Bottomview photo")
        picamBtn.Bind(wx.EVT_BUTTON, self.camerapi)
        
        sizer = wx.GridSizer(2,2,5,5)
        #sizer.Add(self.Image, 0, wx.EXPAND)
        sizer.Add(backBtn, 0, wx.EXPAND)
        sizer.Add(picamBtn, 0, wx.EXPAND)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
    def hideFrame2(self,event):
        """close Bottomview and open backview"""
        self.Hide()
        new_frame2 = BackView(self.variable1)
        new_frame2.Show()

    def camerapi(self,event):
        camera = picamera.PiCamera()
        camera.resolution = (2592, 1944)
        camera.drc_strength = 'high'
        time.sleep(2)
        filename = str(self.variable1) + ' Bottomview.jpg'
        filename2 =str(self.variable1)
        npath ="/home/pi/FootCam/" + str(filename2)
        if not os.path.isdir(npath):
            os.makedirs(npath)
        camera.capture(npath + "/" + filename)
        camera.close()
        
    def on_close(self, event):
        self.Destroy()
        sys.exit(0)
        



#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
