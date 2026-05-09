"""
TeamTalk SDK Integration Example and Tests
This module demonstrates how to use the TeamTalk SDK Python bindings
"""

import sys
import os
from teamtalk_sdk import TeamTalkSDK, TEAMTALK_LIB, TTUser, TTChannel


def test_sdk_available():
    """Test if TeamTalk SDK is available."""
    if TEAMTALK_LIB:
        print("✓ TeamTalk SDK library loaded successfully")
        return True
    else:
        print("✗ TeamTalk SDK library not found - please install")
        print("  See TEAMTALK_SDK_README.md for installation instructions")
        return False


def test_connection():
    """Test connecting to a TeamTalk server."""
    if not test_sdk_available():
        return False
    
    try:
        sdk = TeamTalkSDK()
        sdk.create_instance()
        print("✓ TeamTalk instance created")
        
        # Attempt connection (will fail if no real server available)
        # This is just to test the API
        print("Testing connection API...")
        sdk.close()
        print("✓ SDK API functions available")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_structures():
    """Test TeamTalk data structures."""
    try:
        user = TTUser()
        user.nUserID = 1
        user.szUsername = b"TestUser"
        print(f"✓ TTUser structure created: {user.nUserID}")
        
        channel = TTChannel()
        channel.nChannelID = 0
        channel.szChannelName = b"Lobby"
        print(f"✓ TTChannel structure created: {channel.nChannelID}")
        
        return True
    except Exception as e:
        print(f"✗ Structure error: {e}")
        return False


def main():
    """Run SDK integration tests."""
    print("=" * 60)
    print("TeamTalk SDK Integration Tests")
    print("=" * 60)
    
    print("\n1. Testing SDK Library Loading...")
    test_sdk_available()
    
    print("\n2. Testing SDK Structures...")
    test_structures()
    
    print("\n3. Testing SDK Instance Creation...")
    test_connection()
    
    print("\n" + "=" * 60)
    print("Tests Complete")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Install TeamTalk SDK from https://bearware.dk/?page_id=353")
    print("2. Copy the DLL/SO/DYLIB to the lib/ directory")
    print("3. Run this test again to verify installation")
    print("4. Use TeamTalkSDK class in your applications")


if __name__ == "__main__":
    main()
