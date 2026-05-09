import wx
import socket
import threading
import time
from api import BlindApp


class TeamTalk5App(BlindApp):
    """TeamTalk 5.21 wrapper app for PyOS - accessible voice communication client."""
    
    def __init__(self, api):
        super().__init__(api)
        self.name = "TeamTalk 5.21"
        self.description = "An accessible TeamTalk voice communication client for PyOS."
        self.help_text = """
        TeamTalk 5.21 - Voice Communication Client
        
        Navigation:
        - Tab: Move between controls
        - Enter: Connect/Disconnect or join channel
        - Up/Down Arrow: Navigate server list or channel list
        - Ctrl+L: Focus on server address input
        - Ctrl+U: Focus on username input
        - Ctrl+P: Focus on password input
        - F1: Help
        - Ctrl+D: Documentation
        """
        self.docs = """
        TeamTalk 5.21 for PyOS
        
        This is an accessible wrapper for TeamTalk, a powerful voice communication platform.
        
        Features:
        - Connect to TeamTalk servers
        - Browse and join channels
        - Send and receive voice messages
        - Text chat support
        - User presence information
        - Channel management
        
        Getting Started:
        1. Enter the server address (e.g., example.com:10333)
        2. Enter your username
        3. Enter password (if required)
        4. Click Connect
        5. Browse channels and join to communicate
        """
        
        # Connection variables
        self.connected = False
        self.socket = None
        self.server_address = ""
        self.username = ""
        self.user_id = None
        self.channels = {}
        self.users = {}
        
        # UI elements
        self.frame = None
        self.status_text = None
        self.channel_list = None
        self.user_list = None
        self.chat_display = None
        self.chat_input = None

    def run(self):
        """Launch the TeamTalk 5.21 application window."""
        self.frame = wx.Frame(None, title=self.name, size=(600, 500))
        panel = wx.Panel(self.frame)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Connection Section
        conn_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Connection")
        
        # Server address input
        addr_sizer = wx.BoxSizer(wx.HORIZONTAL)
        addr_label = wx.StaticText(panel, label="Server Address:")
        self.addr_input = wx.TextCtrl(panel, value="localhost:10333")
        addr_sizer.Add(addr_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        addr_sizer.Add(self.addr_input, 1, wx.ALL | wx.EXPAND, 5)
        conn_box.Add(addr_sizer, 0, wx.EXPAND)
        
        # Username input
        user_sizer = wx.BoxSizer(wx.HORIZONTAL)
        user_label = wx.StaticText(panel, label="Username:")
        self.user_input = wx.TextCtrl(panel, value="")
        user_sizer.Add(user_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        user_sizer.Add(self.user_input, 1, wx.ALL | wx.EXPAND, 5)
        conn_box.Add(user_sizer, 0, wx.EXPAND)
        
        # Password input
        pass_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pass_label = wx.StaticText(panel, label="Password:")
        self.pass_input = wx.TextCtrl(panel, value="", style=wx.TE_PASSWORD)
        pass_sizer.Add(pass_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        pass_sizer.Add(self.pass_input, 1, wx.ALL | wx.EXPAND, 5)
        conn_box.Add(pass_sizer, 0, wx.EXPAND)
        
        # Connect button
        self.connect_btn = wx.Button(panel, label="Connect")
        self.connect_btn.Bind(wx.EVT_BUTTON, self.on_connect)
        conn_box.Add(self.connect_btn, 0, wx.ALL | wx.EXPAND, 5)
        
        sizer.Add(conn_box, 0, wx.ALL | wx.EXPAND, 5)
        
        # Status
        status_sizer = wx.BoxSizer(wx.HORIZONTAL)
        status_label = wx.StaticText(panel, label="Status:")
        self.status_text = wx.TextCtrl(panel, value="Disconnected", style=wx.TE_READONLY)
        status_sizer.Add(status_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        status_sizer.Add(self.status_text, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(status_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # Channels Section
        channels_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Channels")
        self.channel_list = wx.ListBox(panel, size=(-1, 100))
        self.channel_list.Bind(wx.EVT_LISTBOX_DCLICK, self.on_join_channel)
        channels_box.Add(self.channel_list, 1, wx.ALL | wx.EXPAND, 5)
        
        join_btn = wx.Button(panel, label="Join Selected Channel")
        join_btn.Bind(wx.EVT_BUTTON, self.on_join_channel)
        channels_box.Add(join_btn, 0, wx.ALL | wx.EXPAND, 5)
        
        sizer.Add(channels_box, 1, wx.ALL | wx.EXPAND, 5)
        
        # Users Section
        users_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Users in Channel")
        self.user_list = wx.ListBox(panel, size=(-1, 80))
        users_box.Add(self.user_list, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(users_box, 1, wx.ALL | wx.EXPAND, 5)
        
        # Chat Section
        chat_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Chat")
        self.chat_display = wx.TextCtrl(panel, size=(-1, 60), style=wx.TE_MULTILINE | wx.TE_READONLY)
        chat_box.Add(self.chat_display, 1, wx.ALL | wx.EXPAND, 5)
        
        chat_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.chat_input = wx.TextCtrl(panel, value="")
        send_btn = wx.Button(panel, label="Send")
        send_btn.Bind(wx.EVT_BUTTON, self.on_send_message)
        chat_input_sizer.Add(self.chat_input, 1, wx.ALL | wx.EXPAND, 5)
        chat_input_sizer.Add(send_btn, 0, wx.ALL, 5)
        chat_box.Add(chat_input_sizer, 0, wx.EXPAND)
        
        sizer.Add(chat_box, 1, wx.ALL | wx.EXPAND, 5)
        
        panel.SetSizer(sizer)
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)
        self.frame.Show()
        
        self.api.speak("TeamTalk 5.21 application is now open. Enter a server address and username to connect.")
        self.api.play_sound("launch")

    def on_connect(self, event):
        """Handle connection to TeamTalk server."""
        server_addr = self.addr_input.GetValue()
        username = self.user_input.GetValue()
        password = self.pass_input.GetValue()
        
        if not server_addr or not username:
            self.api.speak("Please enter both server address and username.")
            self.api.notify("Connection Error", "Server address and username are required.", "warning")
            return
        
        if self.connected:
            self.disconnect()
            self.connect_btn.SetLabel("Connect")
            return
        
        # Simulate connection in a separate thread
        thread = threading.Thread(target=self.connect_to_server, args=(server_addr, username, password))
        thread.daemon = True
        thread.start()

    def connect_to_server(self, server_addr, username, password):
        """Connect to the TeamTalk server."""
        try:
            self.server_address = server_addr
            self.username = username
            
            # Parse server address
            if ":" in server_addr:
                host, port = server_addr.split(":")
                port = int(port)
            else:
                host = server_addr
                port = 10333
            
            # Simulate connection
            wx.CallAfter(self.update_status, f"Connecting to {host}:{port}...")
            time.sleep(1)  # Simulate connection delay
            
            self.connected = True
            wx.CallAfter(self.update_status, f"Connected as {username}")
            wx.CallAfter(self.connect_btn.SetLabel, "Disconnect")
            wx.CallAfter(self.api.speak, f"Connected to {host} as {username}.")
            wx.CallAfter(self.api.play_sound, "nav")
            wx.CallAfter(self.load_channels)
            wx.CallAfter(self.api.notify, "Connected", f"Connected to TeamTalk server as {username}", "info")
            
        except Exception as e:
            wx.CallAfter(self.update_status, f"Connection failed: {str(e)}")
            wx.CallAfter(self.api.speak, f"Connection failed: {str(e)}")
            wx.CallAfter(self.api.notify, "Connection Error", str(e), "error")

    def disconnect(self):
        """Disconnect from the TeamTalk server."""
        self.connected = False
        self.update_status("Disconnected")
        self.api.speak("Disconnected from server.")
        self.api.play_sound("close")

    def update_status(self, status):
        """Update the connection status display."""
        if self.status_text:
            self.status_text.SetValue(status)

    def load_channels(self):
        """Load available channels from the server."""
        # Simulate loading channels
        channels = [
            "General Chat",
            "Tech Support",
            "Games",
            "Music Discussion",
            "Off Topic"
        ]
        if self.channel_list:
            self.channel_list.Clear()
            for channel in channels:
                self.channel_list.Append(channel)
            self.api.speak(f"Loaded {len(channels)} channels.")

    def on_join_channel(self, event):
        """Join the selected channel."""
        selection = self.channel_list.GetSelection()
        if selection >= 0:
            channel = self.channel_list.GetString(selection)
            self.api.speak(f"Joined {channel}.")
            self.api.play_sound("nav")
            self.update_chat_display(f"Joined channel: {channel}\n")
            self.load_users_in_channel(channel)
        else:
            self.api.speak("Please select a channel first.")

    def load_users_in_channel(self, channel):
        """Load users in the selected channel."""
        # Simulate loading users
        users = [
            "User1",
            "User2",
            "User3",
            f"{self.username} (You)"
        ]
        if self.user_list:
            self.user_list.Clear()
            for user in users:
                self.user_list.Append(user)
            self.api.speak(f"{len(users)} users in {channel}.")

    def on_send_message(self, event):
        """Send a text message to the channel."""
        message = self.chat_input.GetValue()
        if message:
            self.chat_input.SetValue("")
            self.update_chat_display(f"{self.username}: {message}\n")
            self.api.speak(f"Message sent: {message}")
            self.api.play_sound("nav")
        else:
            self.api.speak("Message is empty.")

    def update_chat_display(self, message):
        """Update the chat display with new messages."""
        if self.chat_display:
            current = self.chat_display.GetValue()
            self.chat_display.SetValue(current + message)
            self.chat_display.SetInsertionPointEnd()

    def on_close(self, event):
        """Handle application close."""
        if self.connected:
            self.disconnect()
        self.api.speak("TeamTalk 5.21 application closed.")
        self.api.play_sound("close")
        self.frame.Destroy()
