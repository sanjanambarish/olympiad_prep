import streamlit as st
import pandas as pd
from utils.social_features import *

def show_bookmarks_page(student_id):
    """Display the bookmarks page"""
    st.title("🔖 My Bookmarks")
    
    # Debug information
    st.caption(f"Debug: Student ID: {student_id}")
    
    bookmarks = get_bookmarks(student_id)
    
    # Debug information
    st.caption(f"Debug: Found {len(bookmarks)} bookmarks")
    
    if not bookmarks:
        st.info("You haven't bookmarked any questions yet. Bookmark questions during quizzes to review them later!")
        return
    
    st.markdown(f"**{len(bookmarks)}** bookmarked questions")
    
    for i, bookmark in enumerate(bookmarks):
        with st.expander(f"Q{i+1}: {bookmark['question_text'][:50]}...", expanded=False):
            st.markdown(f"**Question:** {bookmark['question_text']}")
            st.markdown(f"Bookmarked on: {bookmark['bookmarked_at']}")
            
            # Option to remove bookmark
            if st.button("Remove Bookmark", key=f"remove_{bookmark['question_id']}"):
                if remove_bookmark(student_id, bookmark['question_id']):
                    st.success("Bookmark removed!")
                    st.rerun()

def show_leaderboard_page():
    """Display the class leaderboard"""
    st.title("🏆 Class Leaderboard")
    st.info("Rankings based on accuracy and average time per question")
    
    leaderboard = get_leaderboard()
    
    if not leaderboard:
        st.info("No data available for leaderboard yet. Complete some quizzes to see rankings!")
        return
    
    # Display leaderboard as a table
    df = pd.DataFrame(leaderboard)
    df.index = range(1, len(df) + 1)
    df.index.name = "Rank"
    
    # Style the dataframe
    styled_df = df.style.set_properties(**{'text-align': 'center'})
    styled_df = styled_df.set_table_styles([
        dict(selector="th", props=[("text-align", "center")]),
        dict(selector="td", props=[("text-align", "center")])
    ])
    
    st.dataframe(styled_df, use_container_width=True)

def show_badges_page(student_id):
    """Display the student's badges"""
    st.title("🏅 My Achievements")
    badges = get_student_badges(student_id)
    
    if not badges:
        st.info("You haven't earned any badges yet. Complete quizzes and activities to earn achievements!")
        return
    
    st.markdown(f"**{len(badges)}** badges earned")
    
    # Display badges in a grid
    cols = st.columns(3)
    for i, badge in enumerate(badges):
        with cols[i % 3]:
            st.markdown(f"### {badge['badge_name']}")
            st.markdown(f"_{badge['description']}_")
            st.markdown(f"Awarded: {badge['awarded_at'][:10]}")
            st.markdown("---")

def show_discussion_forum(question_id, question_text, student_id, student_name):
    """Display discussion forum for a question"""
    st.markdown(f"### 💬 Discussion: {question_text[:50]}...")
    
    # Show existing posts
    posts = get_discussion_posts(question_id)
    
    if posts:
        for post in posts:
            st.markdown(f"**{post['student_name']}** - {post['posted_at'][:16]}")
            st.markdown(f"> {post['content']}")
            st.markdown("---")
    else:
        st.info("No discussions yet. Be the first to start a conversation!")
    
    # Add new post form
    st.markdown("### Add Your Comment")
    with st.form(key=f"discussion_form_{question_id}"):
        new_post = st.text_area("Your thoughts or questions:", key=f"post_content_{question_id}")
        submit_button = st.form_submit_button("Post Comment")
        
        if submit_button and new_post:
            if add_discussion_post(question_id, student_id, student_name, new_post):
                st.success("Comment posted successfully!")
                st.rerun()
            else:
                st.error("Failed to post comment. Please try again.")

def show_study_groups_page(student_id):
    """Display study groups page"""
    st.title("👥 Study Groups")
    st.info("Coming soon: Collaborate with classmates in study groups!")
    
    # Placeholder for study groups functionality
    st.markdown("""
    ### Features Coming Soon:
    - Create and join study groups
    - Schedule group study sessions
    - Share resources with group members
    - Group progress tracking
    - Peer tutoring sessions
    """)
