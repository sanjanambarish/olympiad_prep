import streamlit as st
from utils.social_features import get_bookmarks

def debug_bookmarks_ui(student_id):
    """Simulate the bookmarks UI to check if there's an issue"""
    print(f"Simulating bookmarks UI for student_id: {student_id}")
    
    # This is what happens in show_bookmarks_page
    bookmarks = get_bookmarks(student_id)
    print(f"Bookmarks retrieved: {len(bookmarks)}")
    
    if not bookmarks:
        print("No bookmarks found - would show info message")
    else:
        print(f"Would show {len(bookmarks)} bookmarked questions")
        for i, bookmark in enumerate(bookmarks):
            print(f"  {i+1}. {bookmark['question_text'][:50]}...")
    
    return bookmarks

if __name__ == "__main__":
    # Use the student ID from our previous debug output
    student_id = "366424d6-50e1-452a-a8a8-6e8989373d9c"
    debug_bookmarks_ui(student_id)
