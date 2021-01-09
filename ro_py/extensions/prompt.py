"""

This extension houses functions that allow human verification prompts for interactive applications.

"""


import wx
from wx import html2
import os
import asyncio
import pytweening
import trio
import greenback


async def initialize():
    await greenback.ensure_portal()


async def user_login(client, username, password, key=None):
    if key:
        return await client.user_login(username, password, key)
    else:
        return await client.user_login(username, password)


class RbxLogin(wx.Frame):
    """
    wx.Frame wrapper for Roblox authentication.
    """
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((512, 512))
        self.SetTitle("Login with Roblox")
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.SetIcon(wx.Icon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "appicon.png")))

        self.username = None
        self.password = None
        self.client = None
        self.status = False

        root_sizer = wx.BoxSizer(wx.VERTICAL)

        self.inner_panel = wx.Panel(self, wx.ID_ANY)
        root_sizer.Add(self.inner_panel, 1, wx.ALL | wx.EXPAND, 100)

        inner_sizer = wx.BoxSizer(wx.VERTICAL)

        inner_sizer.Add((0, 20), 0, 0, 0)

        login_label = wx.StaticText(self.inner_panel, wx.ID_ANY, "Please log in with your username and password.",
                                    style=wx.ALIGN_CENTER_HORIZONTAL)
        inner_sizer.Add(login_label, 1, 0, 0)

        self.username_entry = wx.TextCtrl(self.inner_panel, wx.ID_ANY, "\n")
        self.username_entry.SetFont(
            wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.username_entry.SetFocus()
        inner_sizer.Add(self.username_entry, 1, wx.BOTTOM | wx.EXPAND | wx.TOP, 4)

        self.password_entry = wx.TextCtrl(self.inner_panel, wx.ID_ANY, "", style=wx.TE_PASSWORD)
        self.password_entry.SetFont(
            wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        inner_sizer.Add(self.password_entry, 1, wx.BOTTOM | wx.EXPAND | wx.TOP, 4)

        self.log_in_button = wx.Button(self.inner_panel, wx.ID_ANY, "Login")
        inner_sizer.Add(self.log_in_button, 1, wx.ALL | wx.EXPAND, 0)

        inner_sizer.Add((0, 20), 0, 0, 0)

        self.web_view = wx.html2.WebView.New(self, wx.ID_ANY)
        self.web_view.Hide()
        self.web_view.EnableAccessToDevTools(False)
        self.web_view.EnableContextMenu(False)

        root_sizer.Add(self.web_view, 1, wx.EXPAND, 0)

        self.inner_panel.SetSizer(inner_sizer)

        self.SetSizer(root_sizer)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.login_click, self.log_in_button)
        self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATED, self.login_load, self.web_view)

    def login_load(self, event):
        _, token = self.web_view.RunScript("try{document.getElementsByTagName('input')[0].value}catch(e){}")
        if token == "undefined":
            token = False
        if token:
            self.web_view.Hide()
            lr = greenback.await_(user_login(
                self.client,
                self.username,
                self.password,
                token
            ))
            if ".ROBLOSECURITY" in self.client.requests.session.cookies:
                self.status = True
                self.Close()
            else:
                self.status = False
                wx.MessageBox(f"Failed to log in.\n"
                              f"Detailed information from server: {lr.json()['errors'][0]['message']}",
                              "Error", wx.OK | wx.ICON_ERROR)
                self.Close()

    def login_click(self, event):
        self.username = self.username_entry.GetValue()
        self.password = self.password_entry.GetValue()
        self.username.strip("\n")
        self.password.strip("\n")

        if not (self.username and self.password):
            # If either the username or password is missing, return
            return

        if len(self.username) < 3:
            # If the username is shorter than 3, return
            return

        # Disable the entries to stop people from typing in them.
        self.username_entry.Disable()
        self.password_entry.Disable()
        self.log_in_button.Disable()

        # Get the position of the inner_panel
        old_pos = self.inner_panel.GetPosition()
        start_point = old_pos[0]

        # Move the panel over to the right.
        for i in range(0, 512):
            wx.Yield()
            self.inner_panel.SetPosition((int(start_point + pytweening.easeOutQuad(i / 512) * 512), old_pos[1]))

        # Hide the panel. The panel is already on the right so it's not visible anyways.
        self.inner_panel.Hide()
        self.web_view.SetSize((512, 600))

        # Expand the window.
        for i in range(0, 88):
            self.SetSize((512, int(512 + pytweening.easeOutQuad(i / 88) * 88)))

        # Runs the user_login function.
        fd = greenback.await_(user_login(self.client, self.username, self.password))

        # Load the captcha URL.
        if fd:
            self.web_view.LoadURL(fd.url)
            self.web_view.Show()
        else:
            # No captcha needed.
            self.Close()


class RbxCaptcha(wx.Frame):
    """
    wx.Frame wrapper for Roblox authentication.
    """
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((512, 600))
        self.SetTitle("Roblox Captcha (ro.py)")
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.SetIcon(wx.Icon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "appicon.png")))

        self.status = False
        self.token = None

        root_sizer = wx.BoxSizer(wx.VERTICAL)

        self.web_view = wx.html2.WebView.New(self, wx.ID_ANY)
        self.web_view.SetSize((512, 600))
        self.web_view.Show()
        self.web_view.EnableAccessToDevTools(False)
        self.web_view.EnableContextMenu(False)

        root_sizer.Add(self.web_view, 1, wx.EXPAND, 0)

        self.SetSizer(root_sizer)

        self.Layout()

        self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATED, self.login_load, self.web_view)

    def login_load(self, event):
        _, token = self.web_view.RunScript("try{document.getElementsByTagName('input')[0].value}catch(e){}")
        if token == "undefined":
            token = False
        if token:
            self.web_view.Hide()
            self.status = True
            self.token = token
            self.Close()


class AuthApp(wx.App):
    """
    wx.App wrapper for Roblox authentication.
    """

    def OnInit(self):
        self.rbx_login = RbxLogin(None, wx.ID_ANY, "")
        self.SetTopWindow(self.rbx_login)
        self.rbx_login.Show()
        return True


class CaptchaApp(wx.App):
    """
    wx.App wrapper for Roblox captcha.
    """

    def OnInit(self):
        self.rbx_captcha = RbxCaptcha(None, wx.ID_ANY, "")
        self.SetTopWindow(self.rbx_captcha)
        self.rbx_captcha.Show()
        return True


def authenticate_prompt(client):
    """
    Prompts a login screen.
    Returns True if the user has sucessfully been authenticated and False if they have not.

    Parameters
    ----------
    client : ro_py.client.Client
        Client object to authenticate.

    Returns
    ------
    bool
    """
    app = AuthApp(0)
    app.rbx_login.client = client
    app.MainLoop()
    return app.rbx_login.status


def captcha_prompt(unsolved_captcha):
    """
    Prompts a captcha solve screen.
    First item in tuple is True if the solve was sucessful, and the second item is the token.

    Parameters
    ----------
    unsolved_captcha : ro_py.captcha.UnsolvedCaptcha
        Captcha to solve.

    Returns
    ------
    tuple of bool and str
    """
    app = CaptchaApp(0)
    app.rbx_captcha.web_view.LoadURL(unsolved_captcha.url)
    app.MainLoop()
    return app.rbx_captcha.status, app.rbx_captcha.toke


trio.run(initialize)
