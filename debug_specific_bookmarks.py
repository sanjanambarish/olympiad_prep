from supabase_client import supabase

def debug_specific_bookmarks():
    """Debug function to check bookmarks for the specific student from the debug output"""
    # Use the student ID from our previous debug output
    student_id = "366424d6-50e1-452a-a8a8-6e8989373d9c"
    
    print(f"Debugging bookmarks for student_id: {student_id}")
    
    try:
        # Check if bookmarks table exists
        response = supabase.table("bookmarks").select("*").limit(1).execute()
        print("[OK] Bookmarks table exists")
        
        # Get all bookmarks for this specific student
        bookmarks_response = supabase.table("bookmarks").select("*").eq("student_id", student_id).execute()
        bookmarks = bookmarks_response.data if bookmarks_response.data else []
        
        print(f"Found {len(bookmarks)} bookmarks for this student:")
        for i, bookmark in enumerate(bookmarks):
            print(f"  {i+1}. Question ID: {bookmark['question_id']}")
            print(f"      Text: {bookmark['question_text']}")
            print(f"      Bookmarked at: {bookmark['bookmarked_at']}")
            print()
        
        return bookmarks
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        return []

if __name__ == "__main__":
    debug_specific_bookmarks()
