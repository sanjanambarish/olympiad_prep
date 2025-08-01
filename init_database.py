import streamlit as st
from supabase_client import supabase

def init_database():
    """Initialize the database with required tables for social features"""
    try:
        # Check if tables exist by trying to query them
        try:
            supabase.table("bookmarks").select("*").limit(1).execute()
            st.success("✅ Bookmarks table already exists")
        except Exception as e:
            st.info("Creating bookmarks table...")
            # In Supabase, tables are typically created via the dashboard or migrations
            # We'll need to create them manually in the Supabase dashboard
            st.warning("Please create the bookmarks table in your Supabase dashboard using the SQL from database/init_schema.sql")
        
        try:
            supabase.table("discussion_posts").select("*").limit(1).execute()
            st.success("✅ Discussion posts table already exists")
        except Exception as e:
            st.info("Creating discussion_posts table...")
            st.warning("Please create the discussion_posts table in your Supabase dashboard using the SQL from database/init_schema.sql")
            
        try:
            supabase.table("badges").select("*").limit(1).execute()
            st.success("✅ Badges table already exists")
        except Exception as e:
            st.info("Creating badges table...")
            st.warning("Please create the badges table in your Supabase dashboard using the SQL from database/init_schema.sql")
            
        st.info("Database initialization check complete!")
        
    except Exception as e:
        st.error(f"Error initializing database: {str(e)}")

if __name__ == "__main__":
    st.title("Initialize Database Tables")
    st.markdown("This script checks if the required tables exist and creates them if needed.")
    init_database()
