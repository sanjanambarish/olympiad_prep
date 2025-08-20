import os
import socket
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_internet_connection():
    """Check if there's an active internet connection"""
    try:
        # Try to connect to a reliable server (Google's DNS)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

# Supabase configuration
SUPABASE_URL = "https://udnldwyzdeswoljxange.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVkbmxkd3l6ZGVzd29sanhhbmdlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM4NTQzNjIsImV4cCI6MjA2OTQzMDM2Mn0.RJttMLbRPrlIWVdlp0yXxoLR0dX0zDweLjNgot2q2xA"

# Initialize Supabase client with error handling
supabase = None
try:
    if not check_internet_connection():
        raise ConnectionError("No internet connection. Please check your network settings.")
    
    # Initialize with custom options for better error handling
    supabase: Client = create_client(
        SUPABASE_URL,
        SUPABASE_KEY,
        options=ClientOptions(
            postgrest_client_timeout=10,  # 10 seconds timeout
            storage_client_timeout=10,
            realtime_timeout=10,
            verify=True  # SSL verification
        )
    )
    
    # Test the connection
    test = supabase.table('users').select('*').limit(1).execute()
    
except Exception as e:
    error_msg = f"❌ Failed to initialize Supabase client: {str(e)}"
    if "getaddrinfo failed" in str(e).lower() or "name or service not known" in str(e).lower():
        error_msg = "❌ Could not connect to the authentication server. Please check your internet connection and try again."
    elif "SSL" in str(e):
        error_msg = "❌ SSL certificate verification failed. Please check your system's date and time settings."
    
    class ErrorClient:
        def __getattr__(self, name):
            def method(*args, **kwargs):
                raise Exception(error_msg)
            return method
    
    supabase = ErrorClient()
    print(error_msg)  # Also print to console for debugging