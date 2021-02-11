"""

This extension houses functions that allow human verification prompts for interactive applications.

"""


import sys
try:
    import wx
    import wxasync
    from wx import html2
    import pytweening
    from wx.lib.embeddedimage import PyEmbeddedImage
except ModuleNotFoundError:
    print("Please install wxPython, wxAsync and pytweening from pip to use the prompt extension.")
    sys.exit()

icon_image = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAhaSURBVGhDxZl5bFRVFMbPfTNtQRTF'
    b'uOAWVKKIylqptCBiNBQ1MURjQv8Qt8RoxCWKawTFGLdo4oIaY2LUGCUmBo3BAKJgtRTFQi3u'
    b'KBA1LhEXqMK0nb7n79w7M05f36zt1C+9c++7b/re+c757rnLGCkBQbvMkyq5XHxZw+UGyldm'
    b'guyzN/8nFEWgftGqC/Z1j1q55YrTa7jcKCNlgnRKkv/+juuPKOtob6T+FkJJ6iFDQQIYP5xq'
    b'K+WG1kfmriQKZ0tcVhOFmHj0xikBpVsSPO1rWi3U66k3SbXsNONoVRDFEJhovNingd+7mcsZ'
    b'kEhA4hUZJk2Y/B/0SUomRvEpPbKHvs9pfZgitJno/EI9qFAfFkK9icXFi9dMpX2l65IleHy3'
    b'NTYNjUIPRUl1UwxCi0u91MgtvGUlpLYGHbKWsiTYKrMpB/OtAaOYCLyK8fMDPylB4P/MRy1R'
    b'+Jko3C3D5Z6ih7CSTRcl6MtPvL2N1nrqD6m/IEJ/U5eEvAQwfj+qDuPFxyoBr2qY+D2JZRC4'
    b'DgIHcm8TWekE6/lSoG9Njx9tdxE/IztofUxRQprhvoFQF3VeFCIwRYzZRDOG5/m24c9LMB5m'
    b'QqINEvMZqK9ajw4EaoVGRgkpuniikW9ptVKvo/6Ieoc5VXrt/SwUInCtV1WzzO/5zxHISfxk'
    b'15ogMOe2Lmg0+G4VOj+nsK9KQDYhl+H20vclrXRCaCM6P1AXHMRn2gdkAePFxKrmGBNcZCZZ'
    b'j9xJ5u8qKh0UC32nziaaENQxRvaDUC3RvoF6BeOngyTQjALuyhkBvD+C6jNS6LFIxnWmoFkp'
    b'6E1qzq9DSnt40NMM6GuGbE5WZ+no/Fva8vltPII/JvA1qfcFxuuA1inqetcj9+GtX23YhwJq'
    b'kvPp6nwEZnjxakwKaSiFIMnINd5NROp4M5mUGMj9ZKShg8t8zfkIoP9o4xXMCQzoqlE0l7oe'
    b'eY4obEGnlYdGOil/8NkeSQCvHkB1Wlj7YfhEgTEyn+/PJgo6Au4kvH7+3DYIcFLtIOq/5orA'
    b'yeT7o6L03wdECAKa7B6Yvmh1NSRW4ZkVpNXKwhFoNlNyp9GZJl7NvdwSSkOjwFiZzoRwaapr'
    b'MXm7c1DTahhO/x/oR67XzBI0XixcpMxipHQoUfgSET1ZsSg4/e/is10v+xHACF3j1BbSfzbc'
    b'OqnmGJq3ux55lAG9k7mh8FRZKpx82nGUkoh8/Cno/8iC+g9B0yr/dzUOmMTD/0B9N5KrN1Pv'
    b'tdEYRkkv3gYCR8DKRxFFQPXPawrrPxuaVk28SufHJXU3rRFIvCnfSx1vmEzIL2FcPI+0dD2T'
    b'vQ0qDUreLRyb7SeIIkD+L837GTjOQVVqVWnmSi+Lrm2Ul81ENkNGyBvyYNnjQ63tZcbXFJpC'
    b'HwKE/yCqKaXovw+cPNa2PDzHNsKw6/tAxpYtI+cY1b9OYhbhCEwwnje6VP1bsFcgpeoastV1'
    b'9AeLPh3WDXalWQ6ctRn5KMIEzjCx0vWvMIbRFQQ7aX7jeiIxDu+P6b8tKQJO/2pYZgArwgRK'
    b'yv/ZYEbWagPL63yL6gb0z1o8dVUK1NJee6qhRzwZZAigfz0lKF//apUx2xtufUcTZj8EW2x1'
    b'TlnGK5z+t6D/v2wrhcxwgsBZePG98gkAY3T/tIOds57SreN6Y3fnru2fPNOUDDRv+PI688GF'
    b'ZSVSHT375DYIPOw6HLIlhP4HvKCvYSycxHMuY9f2InNDe82Bh3+Mc+aRRhVL7f42LNxCUDdr'
    b'/tI9cQj2URdf/JpWZes/A1anuqzQfbMu8sBwBge53zymEsV7HUThmZLnAbVSz5HEnvT1gSXw'
    b'45iRh1JN0pcPKiDk9yR0nTSGq0WuUx5CQj+kNF0c3HfbcMBu28pCOpiT0P8hZeX/IpBaJy0k'
    b'CuMx4jfEcG9qTVMcnJXv288Q0gRmDYL+c8Kuk2JVusu7Txbs0a6X0HRrUdtPp3/1bIu9DsGb'
    b'fvNqrc+QCnk/Dbf9jM+rP2zDuURBB4huP/U3hvzQSPnyI59f2OsQPGOCw6knDrr++4HtJzqi'
    b'cT9SGg6J9eyslhcc0E5qqv9O2wpBHzgZzxysYa40/N4ePZqcTPMq22HkbmLxZ97x4CIUqX+F'
    b'EkD/paSEgcFG2pg7iMKReHU78ng051hQ47vtyilS/wol0KjrGBfdykNneqKgsl3seuQJZtiv'
    b'Iw/FnP71EFc3QpFQq1eQq5uZgv70yETkbM0YsK8cIXtA7MUuJwrTUtq+y90JwQljE9/5x7Yi'
    b'kMkBLMKOJt/V0pzNnD0TX42H0AhCY71m10h5TupKhRev1sz0bhCYxtYFjfhP3mZAN9rT6DR0'
    b'WZiQhRB4ynX0R2QSa7h1Le4PjsfgOi7P4un11Cd4sWqrVtWxm/QGRkgjzsBuYgm+nM3OVCTT'
    b'wiOH2azvLONFUgcBt5aNQCSBMIgOhgcn8rAGLomQJXYcXvQ0Ki5CpRNKHdNvozkNErsh8SSr'
    b'p4X2kFLlk7S/Q0+EwF7qSBRFIAwIjcDYk7EXqVlCtSyhjzLIAib2+L3YtJz63e0eCCyFwGgs'
    b'2kwkjrAEErIc45vcN6NRFoEwIDQKi3XBPItyJoTs2or5RZO/i1AOQqnst5v7GoVtkLgWES2z'
    b'NxNyNQSete0cGBQCYUBoNBbrEUo6IZzqefGR4qG4iISgmc/v6VoOgSYI6NBtIQpTmQH0kCxz'
    b'hBKFihDIxgUP/Sa7fm8fg8HTuFRCM7B+HAOYPZbLcCo7QtFLuxES70LifL77OGUCBPL+cFVx'
    b'AmEQHXQVjGX8TOdSM5zWY+M1+8eTiU7dsNdvuHJugnR6Hsa/pf+TD0NOIAwIIZngJG0yu80h'
    b'AbxAFN5wdwtB5F91LAlTEJXvrgAAAABJRU5ErkJggg=='
)


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
        self.SetIcon(icon_image.GetIcon())

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

        wxasync.AsyncBind(wx.EVT_BUTTON, self.login_click, self.log_in_button)
        wxasync.AsyncBind(wx.html2.EVT_WEBVIEW_NAVIGATED, self.login_load, self.web_view)

    async def login_load(self, event):
        _, token = self.web_view.RunScript("try{document.getElementsByTagName('input')[0].value}catch(e){}")
        if token == "undefined":
            token = False
        if token:
            self.web_view.Hide()
            lr = await user_login(
                self.client,
                self.username,
                self.password,
                token
            )
            if ".ROBLOSECURITY" in self.client.requests.session.cookies:
                self.status = True
                self.Close()
            else:
                self.status = False
                wx.MessageBox(f"Failed to log in.\n"
                              f"Detailed information from server: {lr.json()['errors'][0]['message']}",
                              "Error", wx.OK | wx.ICON_ERROR)
                self.Close()

    async def login_click(self, event):
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
        fd = await user_login(self.client, self.username, self.password)

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
        self.SetIcon(icon_image.GetIcon())

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


class AuthApp(wxasync.WxAsyncApp):
    """
    wx.App wrapper for Roblox authentication.
    """

    def OnInit(self):
        self.rbx_login = RbxLogin(None, wx.ID_ANY, "")
        self.SetTopWindow(self.rbx_login)
        self.rbx_login.Show()
        return True


class CaptchaApp(wxasync.WxAsyncApp):
    """
    wx.App wrapper for Roblox captcha.
    """

    def OnInit(self):
        self.rbx_captcha = RbxCaptcha(None, wx.ID_ANY, "")
        self.SetTopWindow(self.rbx_captcha)
        self.rbx_captcha.Show()
        return True


async def authenticate_prompt(client):
    """
    Prompts a login screen.
    Returns True if the user has sucessfully been authenticated and False if they have not.

    Login prompts look like this:
    .. image:: https://raw.githubusercontent.com/rbx-libdev/ro.py/main/resources/login_prompt.png
    They also display a captcha, which looks very similar to captcha_prompt():
    .. image:: https://raw.githubusercontent.com/rbx-libdev/ro.py/main/resources/login_captcha_prompt.png

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
    await app.MainLoop()
    return app.rbx_login.status


async def captcha_prompt(unsolved_captcha):
    """
    Prompts a captcha solve screen.
    First item in tuple is True if the solve was sucessful, and the second item is the token.

    Image will be placed here soon.

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
    await app.MainLoop()
    return app.rbx_captcha.status, app.rbx_captcha.token
