# ROBLOSECURITY

When you log in on the Roblox website, you create a new session with a special identifier linked to it, and that token is stored on your computer as a cookie.
Every single time your computer asks Roblox to do anything - for example, "give me the name of this user" - your computer also gives this token to Roblox, and it can look and see if that token is valid.  

Let's say you're asking Roblox to give you a list of your friends. It'll look at that token and know who you are, and can use that to give you your friends list.
When you log out, that token is invalidated. Even if the client holds on to the token, it won't be valid after logging out.

This token is called the `.ROBLOSECURITY` token and you will need one to do anything that you need to be logged in to do
on Roblox, including:  
- getting information about yourself (name, description, ID, etc)  
- changing avatar  
- getting friends list  
- playing games  

!!! danger
    You may have heard of this token before and have been told that you should never, under any circumstances, share 
    this token with anyone - and this is true! This token does give an attacker access to your Roblox account. However,
    this doesn't mean they gain access to *everything* - over time, more and more things are being locked behind other
    verification methods, like 2-step verification. 
    We recommend using an alternate account with only the permissions it needs to limit the destruction an attacker can 
    do. [Always enable 2-step verification!](https://en.help.roblox.com/hc/articles/212459863)

The best way to authenticate your ro.py application is to log in to Roblox on the website and then taking the
.ROBLOSECURITY token from there.

!!! warning
    Pressing the "Log out" button on the Roblox website invalidates your token, so you should not press this button
    after grabbing your token. Instead, consider using a private or incognito window and closing it when you are done.

To grab your .ROBLOSECURITY cookie, log into your account on the Roblox website and follow the instructions below.

=== "Chrome/Chromium-based"
    You can access the cookie by going to https://www.roblox.com/, pressing the padlock icon next to the URL in your
    browser, clicking the arrow next to `roblox.com`, opening up the "Cookies" folder, clicking ".ROBLOSECURITY",
    clicking on the "Content" text once, pressing ++control+a++, and then pressing ++control+c++
    (make sure **not** to double-click this field as you won't select the entire value!)  

    ![](../assets/screenshots/ChromeCookie.png){: style="width: 400px"}
    
    Alternatively, you can access the cookie by going to https://www.roblox.com/, pressing ++control+shift+i++ to access
    the Developer Tools, navigating to the "Application" tab, opening up the arrow next to "Cookies" on the sidebar on
    the left, clicking the `https://www.roblox.com` item underneath the Cookies button, and then copying the
    .ROBLOSECURITY token by double-clicking on the value and then hitting ++control+c++.
    
    ![](../assets/screenshots/ChromeDevTools.png){: style="height: 436px"}
=== "Firefox"
    You can access the cookie by going to https://www.roblox.com/ and pressing ++shift+f9++,
    pressing the "Storage" tab button on the top, opening up the "Cookies" section in the sidebar on the left, 
    clicking the `https://www.roblox.com` item underneath it,
    and then copying the .ROBLOSECURITY token by double-clicking on the value and then hitting ++control+c++.
    ![](../assets/screenshots/FirefoxCookie.jpeg)
