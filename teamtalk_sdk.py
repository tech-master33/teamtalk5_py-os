# TeamTalk 5.21 SDK Python Bindings
# This file provides ctypes bindings for the TeamTalk 5.21 SDK

import ctypes
import platform
import os
from ctypes import *

# Determine the platform and load the appropriate library
def load_teamtalk_library():
    """Load TeamTalk SDK library based on platform."""
    system = platform.system()
    possible_paths = []
    
    if system == "Windows":
        possible_names = [
            "TeamTalk5.dll",
            "TeamTalk5Client.dll",
            os.path.join(os.path.dirname(__file__), "lib", "TeamTalk5.dll"),
            os.path.join(os.path.dirname(__file__), "TeamTalk5.dll"),
            "C:\\Program Files\\TeamTalk\\TeamTalk5.dll",
            "C:\\Program Files (x86)\\TeamTalk\\TeamTalk5.dll",
        ]
    elif system == "Linux":
        possible_names = [
            "libTeamTalk5.so",
            os.path.join(os.path.dirname(__file__), "lib", "libTeamTalk5.so"),
            "/usr/lib/libTeamTalk5.so",
            "/usr/local/lib/libTeamTalk5.so",
        ]
    elif system == "Darwin":  # macOS
        possible_names = [
            "libTeamTalk5.dylib",
            os.path.join(os.path.dirname(__file__), "lib", "libTeamTalk5.dylib"),
            "/usr/local/lib/libTeamTalk5.dylib",
        ]
    else:
        possible_names = []
    
    for name in possible_names:
        try:
            return ctypes.CDLL(name)
        except OSError:
            continue
    
    return None


# Load the library
TEAMTALK_LIB = load_teamtalk_library()


# ============================================================================
# CONSTANTS
# ============================================================================

# User types
USERTYPE_DEFAULT = 0
USERTYPE_ADMIN = 1

# Channel types
CHANNEL_DEFAULT = 0
CHANNEL_HIDDEN = 1
CHANNEL_MODERATED = 2

# Message types
MSGTYPE_USER = 1
MSGTYPE_CHANNEL = 2
MSGTYPE_BROADCAST = 3

# Connection states
CONNECTED = 1
DISCONNECTED = 0

# Audio codec types
AUDIO_CODEC_NONE = 0
AUDIO_CODEC_SPEEX = 1
AUDIO_CODEC_OPUS = 2

# Max values
MAX_USERNAME = 512
MAX_CHANNELS = 1000
MAX_USERS = 10000
MAX_MESSAGES = 1000
MAX_MESSAGE_SIZE = 4096

TEAMTALK_ROOT_CHANNEL = 0


# ============================================================================
# STRUCTURES
# ============================================================================

class TTUser(Structure):
    """TeamTalk User structure."""
    _fields_ = [
        ("nUserID", c_int),
        ("nChannelID", c_int),
        ("szUsername", c_char * MAX_USERNAME),
        ("nUserType", c_int),
        ("szStatusMsg", c_char * 1024),
        ("bMute", c_bool),
        ("bDeaf", c_bool),
        ("nLastActivity", c_int),
    ]


class TTChannel(Structure):
    """TeamTalk Channel structure."""
    _fields_ = [
        ("nChannelID", c_int),
        ("nParentID", c_int),
        ("szChannelName", c_char * 512),
        ("szTopic", c_char * 512),
        ("nMaxUsers", c_int),
        ("nUsers", c_int),
        ("nChannelType", c_int),
        ("bPassword", c_bool),
    ]


class TTMessage(Structure):
    """TeamTalk Text Message structure."""
    _fields_ = [
        ("nFromUserID", c_int),
        ("nToUserID", c_int),
        ("nChannelID", c_int),
        ("nMsgType", c_int),
        ("szMessage", c_char * MAX_MESSAGE_SIZE),
        ("nTimestamp", c_int),
    ]


class TTAudioFormat(Structure):
    """TeamTalk Audio Format structure."""
    _fields_ = [
        ("nSampleRate", c_int),
        ("nChannels", c_int),
        ("nCodec", c_int),
        ("nBitrate", c_int),
    ]


class TTServerInfo(Structure):
    """TeamTalk Server Information structure."""
    _fields_ = [
        ("szServerName", c_char * 512),
        ("szMotd", c_char * 1024),
        ("nMaxUsers", c_int),
        ("nUserCount", c_int),
        ("nChannelCount", c_int),
    ]


class TTClientEvent(Structure):
    """TeamTalk Client Event structure."""
    _fields_ = [
        ("nEventType", c_int),
        ("nErrorNumber", c_int),
        ("user", POINTER(TTUser)),
        ("channel", POINTER(TTChannel)),
        ("message", POINTER(TTMessage)),
    ]


# ============================================================================
# FUNCTION PROTOTYPES (if SDK available)
# ============================================================================

if TEAMTALK_LIB:
    # Session management
    TT_New = TEAMTALK_LIB.TT_New
    TT_New.argtypes = []
    TT_New.restype = c_void_p
    
    TT_Close = TEAMTALK_LIB.TT_Close
    TT_Close.argtypes = [c_void_p]
    TT_Close.restype = c_bool
    
    # Connection
    TT_Connect = TEAMTALK_LIB.TT_Connect
    TT_Connect.argtypes = [c_void_p, c_char_p, c_int, c_char_p, c_char_p]
    TT_Connect.restype = c_bool
    
    TT_Disconnect = TEAMTALK_LIB.TT_Disconnect
    TT_Disconnect.argtypes = [c_void_p]
    TT_Disconnect.restype = c_bool
    
    # Channel operations
    TT_JoinChannel = TEAMTALK_LIB.TT_JoinChannel
    TT_JoinChannel.argtypes = [c_void_p, c_int, c_char_p]
    TT_JoinChannel.restype = c_bool
    
    TT_LeaveChannel = TEAMTALK_LIB.TT_LeaveChannel
    TT_LeaveChannel.argtypes = [c_void_p]
    TT_LeaveChannel.restype = c_bool
    
    # Messaging
    TT_SendChannelMessage = TEAMTALK_LIB.TT_SendChannelMessage
    TT_SendChannelMessage.argtypes = [c_void_p, c_char_p]
    TT_SendChannelMessage.restype = c_bool
    
    TT_SendUserMessage = TEAMTALK_LIB.TT_SendUserMessage
    TT_SendUserMessage.argtypes = [c_void_p, c_int, c_char_p]
    TT_SendUserMessage.restype = c_bool
    
    # Query operations
    TT_GetUser = TEAMTALK_LIB.TT_GetUser
    TT_GetUser.argtypes = [c_void_p, c_int, POINTER(TTUser)]
    TT_GetUser.restype = c_bool
    
    TT_GetChannel = TEAMTALK_LIB.TT_GetChannel
    TT_GetChannel.argtypes = [c_void_p, c_int, POINTER(TTChannel)]
    TT_GetChannel.restype = c_bool
    
    # Event handling
    TT_GetMessage = TEAMTALK_LIB.TT_GetMessage
    TT_GetMessage.argtypes = [c_void_p, POINTER(TTClientEvent)]
    TT_GetMessage.restype = c_bool


# ============================================================================
# PYTHON WRAPPER CLASS
# ============================================================================

class TeamTalkSDK:
    """High-level Python wrapper for TeamTalk SDK."""
    
    def __init__(self):
        """Initialize TeamTalk SDK wrapper."""
        if TEAMTALK_LIB is None:
            raise RuntimeError("TeamTalk SDK library not found. Please install TeamTalk SDK.")
        
        self.instance = None
        self.connected = False
    
    def create_instance(self):
        """Create a new TeamTalk instance."""
        if TEAMTALK_LIB and TT_New:
            self.instance = TT_New()
            return self.instance is not None
        return False
    
    def connect(self, host, port, username, password):
        """Connect to a TeamTalk server."""
        if not self.instance:
            self.create_instance()
        
        if TEAMTALK_LIB and TT_Connect:
            host_bytes = host.encode('utf-8')
            user_bytes = username.encode('utf-8')
            pass_bytes = password.encode('utf-8')
            
            result = TT_Connect(self.instance, host_bytes, port, user_bytes, pass_bytes)
            self.connected = result
            return result
        return False
    
    def disconnect(self):
        """Disconnect from TeamTalk server."""
        if self.instance and TEAMTALK_LIB and TT_Disconnect:
            result = TT_Disconnect(self.instance)
            self.connected = False
            return result
        return False
    
    def join_channel(self, channel_id, password=""):
        """Join a channel."""
        if self.instance and TEAMTALK_LIB and TT_JoinChannel:
            pass_bytes = password.encode('utf-8') if password else b""
            return TT_JoinChannel(self.instance, channel_id, pass_bytes)
        return False
    
    def leave_channel(self):
        """Leave current channel."""
        if self.instance and TEAMTALK_LIB and TT_LeaveChannel:
            return TT_LeaveChannel(self.instance)
        return False
    
    def send_channel_message(self, message):
        """Send a message to current channel."""
        if self.instance and TEAMTALK_LIB and TT_SendChannelMessage:
            msg_bytes = message.encode('utf-8')
            return TT_SendChannelMessage(self.instance, msg_bytes)
        return False
    
    def send_user_message(self, user_id, message):
        """Send a private message to a user."""
        if self.instance and TEAMTALK_LIB and TT_SendUserMessage:
            msg_bytes = message.encode('utf-8')
            return TT_SendUserMessage(self.instance, user_id, msg_bytes)
        return False
    
    def get_user(self, user_id):
        """Get user information."""
        if self.instance and TEAMTALK_LIB and TT_GetUser:
            user = TTUser()
            if TT_GetUser(self.instance, user_id, byref(user)):
                return user
        return None
    
    def get_channel(self, channel_id):
        """Get channel information."""
        if self.instance and TEAMTALK_LIB and TT_GetChannel:
            channel = TTChannel()
            if TT_GetChannel(self.instance, channel_id, byref(channel)):
                return channel
        return None
    
    def get_message(self):
        """Get next event message from server."""
        if self.instance and TEAMTALK_LIB and TT_GetMessage:
            event = TTClientEvent()
            if TT_GetMessage(self.instance, byref(event)):
                return event
        return None
    
    def close(self):
        """Close TeamTalk instance."""
        if self.instance and TEAMTALK_LIB and TT_Close:
            TT_Close(self.instance)
            self.instance = None
            self.connected = False
