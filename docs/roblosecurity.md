# The .ROBLOSECURITY Token

When you log in on the Roblox website, you create a new session with a special identifier linked to it, and that token is stored on your computer as a cookie.
Every single time your computer asks Roblox to do anything - for example, "give me the name of this user" - your computer also gives this token to Roblox, and it can look and see if that token is valid.  

Let's say you're asking Roblox to give you a list of your friends. It'll look at that token and know who you are, and can use that to give you your friends list.

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: Hello, can I log in? Here's my username and password.
    Note left of Server: Server makes a token and stores it, and then gives it to the client.
    Server->>Client: Okay! Here's your token.
    Note right of Client: Token is stored in the cookies.
    Client->>Server: Hello! Can you give me a list of my friends? Here is my cookie.
    Note left of Server: Server sees token in cookies and uses it to get their friend list.
    Server->>Client: Okay! Here is your friends list.
```

When you log out, that token is invalidated. Even if the client holds on to the token, it won't be valid after logging out.

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: Hello, can I log out?
    Note left of Server: Server deletes the token from its storage.
    Server->>Client: Okay! Please delete your token.
    Note right of Client: Token is deleted from cookies.
    Client->>Server: Hello! Can you give me a list of my friends? Here is my cookie.
    Note left of Server: Client has no token, so server responds with an error.
    Server->>Client: Sorry, you aren't logged in.
```

This token is called the `.ROBLOSECURITY` token and you will need one to do anything that you need to be logged in to do on Roblox, including:  

- getting information about yourself (name, description, id, etc)  
- changing avatar  
- getting friends list  
- playing games  


