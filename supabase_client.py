
from supabase import create_client

# 🔥 Replace these with your Supabase project values
SUPABASE_URL = "https://udnldwyzdeswoljxange.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVkbmxkd3l6ZGVzd29sanhhbmdlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM4NTQzNjIsImV4cCI6MjA2OTQzMDM2Mn0.RJttMLbRPrlIWVdlp0yXxoLR0dX0zDweLjNgot2q2xA"  # Starts with "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)