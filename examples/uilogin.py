import wx
import asyncio
import pytweening
from ro_py.client import Client
import wx.html2

roblox = Client()


async def user_login(username, password, key=None):
    if key:
        return await roblox.user_login(username, password, key)
    else:
        return await roblox.user_login(username, password)


class RbxLogin(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((512, 512))
        self.SetTitle("Login with Roblox")
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.username = None
        self.password = None

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
            """
            for i in range(0, 600):
                self.web_view.SetPosition((0, int(0 + pytweening.easeOutQuad(i / 600) * 600)))
            """
            lr = asyncio.get_event_loop().run_until_complete(user_login(self.username, self.password, token))
            if ".ROBLOSECURITY" in roblox.requests.session.cookies:
                self.Close()
            else:
                wx.MessageBox(f"Failed to log in.\n"
                              f"Detailed information from server: {lr.json()['errors'][0]['message']}", "Error", wx.OK | wx.ICON_ERROR)
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
        fd = asyncio.get_event_loop().run_until_complete(user_login(self.username, self.password))

        # Load the captcha URL.
        if fd:
            self.web_view.LoadURL(fd.url)
            self.web_view.Show()
        else:
            # No captcha needed.
            self.Close()


class MyApp(wx.App):
    def OnInit(self):
        self.rbx_login = RbxLogin(None, wx.ID_ANY, "")
        self.SetTopWindow(self.rbx_login)
        self.rbx_login.Show()
        return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
