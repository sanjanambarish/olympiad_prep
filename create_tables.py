from supabase_client import supabase

def check_tables():
    """Check if required tables exist"""
    print("Checking if required tables exist...")
    
    # Check bookmarks table
    try:
        supabase.table("bookmarks").select("*").limit(1).execute()
        print("[OK] Bookmarks table exists")
    except Exception as e:
        error_msg = str(e)
        if "not found" in error_msg.lower() or "404" in error_msg or "does not exist" in error_msg.lower():
            print("[ERROR] Bookmarks table does not exist. Please create it in your Supabase dashboard using the SQL from database/init_schema.sql")
        else:
            print("[OK] Bookmarks table exists (different error)")
    
    # Check discussion_posts table
    try:
        supabase.table("discussion_posts").select("*").limit(1).execute()
        print("[OK] Discussion posts table exists")
    except Exception as e:
        error_msg = str(e)
        if "not found" in error_msg.lower() or "404" in error_msg or "does not exist" in error_msg.lower():
            print("[ERROR] Discussion posts table does not exist. Please create it in your Supabase dashboard using the SQL from database/init_schema.sql")
        else:
            print("[OK] Discussion posts table exists (different error)")
    
    # Check badges table
    try:
        supabase.table("badges").select("*").limit(1).execute()
        print("[OK] Badges table exists")
    except Exception as e:
        error_msg = str(e)
        if "not found" in error_msg.lower() or "404" in error_msg or "does not exist" in error_msg.lower():
            print("[ERROR] Badges table does not exist. Please create it in your Supabase dashboard using the SQL from database/init_schema.sql")
        else:
            print("[OK] Badges table exists (different error)")
    
    print("\nInstructions to create tables:")
    print("1. Go to your Supabase dashboard")
    print("2. Navigate to the SQL editor")
    print("3. Copy and run the SQL code from database/init_schema.sql")

if __name__ == "__main__":
    check_tables()
