import streamlit as st
from supabase_client import supabase

st.title("📚 Bookmark Debug Tool")

if st.button("Check All Bookmarks"):
    try:
        response = supabase.table("bookmarks").select("*").execute()
        bookmarks = response.data if response.data else []
        
        st.write(f"Total bookmarks in database: {len(bookmarks)}")
        
        if bookmarks:
            for i, bookmark in enumerate(bookmarks):
                st.write(f"{i+1}. Student: {bookmark['student_id']}")
                st.write(f"   Question ID: {bookmark['question_id']}")
                st.write(f"   Text: {bookmark['question_text']}")
                st.write(f"   Date: {bookmark['bookmarked_at']}")
                st.write("---")
        else:
            st.write("No bookmarks found in database")
    except Exception as e:
        st.error(f"Error: {str(e)}")

if st.session_state.user:
    st.write(f"Current user ID: {st.session_state.user.user.id}")
    
    if st.button("Check My Bookmarks"):
        try:
            response = supabase.table("bookmarks").select("*").eq("student_id", st.session_state.user.user.id).execute()
            user_bookmarks = response.data if response.data else []
            
            st.write(f"Your bookmarks: {len(user_bookmarks)}")
            
            if user_bookmarks:
                for i, bookmark in enumerate(user_bookmarks):
                    st.write(f"{i+1}. Question: {bookmark['question_text']}")
                    st.write(f"   Bookmarked: {bookmark['bookmarked_at']}")
                    st.write("---")
            else:
                st.write("You have no bookmarks")
        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    st.write("Please log in to check your bookmarks")
