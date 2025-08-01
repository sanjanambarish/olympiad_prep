from supabase_client import supabase
import streamlit as st

def debug_bookmarks(student_id):
    """Debug function to check bookmarks"""
    st.title("Debug Bookmarks")

    # Get all bookmarks from the database
    try:
        response = supabase.table("bookmarks").select("*").execute()
        bookmarks = response.data if response.data else []
        
        st.write(f"Total bookmarks in database: {len(bookmarks)}")
        
        if bookmarks:
            st.write("All bookmarks:")
            for bookmark in bookmarks:
                st.write(bookmark)
        else:
            st.write("No bookmarks found in database")
            
    except Exception as e:
        st.error(f"Error fetching bookmarks: {str(e)}")

    # Check if user is logged in
    if 'user' in st.session_state and st.session_state.user:
        st.write(f"Current user ID: {st.session_state.user.user.id}")
        
        # Get bookmarks for current user
        try:
            response = supabase.table("bookmarks").select("*").eq("student_id", st.session_state.user.user.id).execute()
            user_bookmarks = response.data if response.data else []
            
            st.write(f"Bookmarks for current user: {len(user_bookmarks)}")
            
            if user_bookmarks:
                st.write("User bookmarks:")
                for bookmark in user_bookmarks:
                    st.write(bookmark)
            else:
                st.write("No bookmarks found for current user")
                
        except Exception as e:
            st.error(f"Error fetching user bookmarks: {str(e)}")
    else:
        st.write("No user logged in")

if __name__ == "__main__":
    # Use a placeholder student ID
    student_id = "00000000-0000-0000-0000-000000000000"  # Placeholder
    
    debug_bookmarks(student_id)
