import streamlit as st
from supabase_client import supabase
import pandas as pd
from datetime import datetime

def bookmark_question(student_id, question_id, question_text):
    """Bookmark a question for later review"""
    try:
        response = supabase.table("bookmarks").insert({
            "student_id": student_id,
            "question_id": question_id,
            "question_text": question_text,
            "bookmarked_at": datetime.now().isoformat()
        }).execute()
        return True
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            st.error("❌ Database table 'bookmarks' not found. Please create the table in your Supabase dashboard using the SQL from database/init_schema.sql")
        else:
            st.error(f"Failed to bookmark question: {error_msg}")
        return False

def remove_bookmark(student_id, question_id):
    """Remove a bookmarked question"""
    try:
        supabase.table("bookmarks").delete().eq("student_id", student_id).eq("question_id", question_id).execute()
        return True
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            st.error("❌ Database table 'bookmarks' not found. Please create the table in your Supabase dashboard using the SQL from database/init_schema.sql")
        else:
            st.error(f"Failed to remove bookmark: {error_msg}")
        return False

def get_bookmarks(student_id):
    """Get all bookmarked questions for a student"""
    try:
        response = supabase.table("bookmarks").select("*").eq("student_id", student_id).execute()
        return response.data if response.data else []
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            st.error("❌ Database table 'bookmarks' not found. Please create the table in your Supabase dashboard using the SQL from database/init_schema.sql")
        else:
            st.error(f"Failed to fetch bookmarks: {error_msg}")
        return []

def is_question_bookmarked(student_id, question_id):
    """Check if a specific question is bookmarked by the student"""
    try:
        response = supabase.table("bookmarks").select("*").eq("student_id", student_id).eq("question_id", question_id).execute()
        return len(response.data) > 0 if response.data else False
    except Exception as e:
        # If there's an error, we'll assume the question is not bookmarked
        return False

def add_discussion_post(question_id, student_id, student_name, content):
    """Add a discussion post for a question"""
    try:
        supabase.table("discussion_posts").insert({
            "question_id": question_id,
            "student_id": student_id,
            "student_name": student_name,
            "content": content,
            "posted_at": datetime.now().isoformat()
        }).execute()
        return True
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            st.error("❌ Database table 'discussion_posts' not found. Please create the table in your Supabase dashboard using the SQL from database/init_schema.sql")
        else:
            st.error(f"Failed to add discussion post: {error_msg}")
        return False

def get_discussion_posts(question_id):
    """Get all discussion posts for a question"""
    try:
        response = supabase.table("discussion_posts").select("*").eq("question_id", question_id).order("posted_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            st.error("❌ Database table 'discussion_posts' not found. Please create the table in your Supabase dashboard using the SQL from database/init_schema.sql")
        else:
            st.error(f"Failed to fetch discussion posts: {error_msg}")
        return []

def get_leaderboard():
    """Get class leaderboard based on accuracy and speed"""
    try:
        # This is a simplified version - in practice, you'd want to calculate
        # accuracy and average time from quiz_attempts table
        response = supabase.table("users").select("id, full_name, role").eq("role", "student").execute()
        students = response.data if response.data else []
        
        leaderboard_data = []
        for student in students:
            # Get student's quiz attempts
            attempts_resp = supabase.table("quiz_attempts").select("is_correct, time_taken_seconds").eq("student_id", student["id"]).execute()
            attempts = attempts_resp.data if attempts_resp.data else []
            
            if attempts:
                total_questions = len(attempts)
                correct_answers = sum(1 for attempt in attempts if attempt["is_correct"])
                accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
                avg_time = sum(attempt["time_taken_seconds"] for attempt in attempts) / total_questions if total_questions > 0 else 0
                
                leaderboard_data.append({
                    "student_name": student["full_name"],
                    "accuracy": round(accuracy, 1),
                    "avg_time": round(avg_time, 1),
                    "total_questions": total_questions
                })
        
        # Sort by accuracy (descending) and then by average time (ascending)
        leaderboard_data.sort(key=lambda x: (-x["accuracy"], x["avg_time"]))
        return leaderboard_data
    except Exception as e:
        st.error(f"Failed to fetch leaderboard: {str(e)}")
        return []

def award_badge(student_id, badge_name, description):
    """Award a badge to a student"""
    try:
        supabase.table("badges").insert({
            "student_id": student_id,
            "badge_name": badge_name,
            "description": description,
            "awarded_at": datetime.now().isoformat()
        }).execute()
        return True
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            st.error("❌ Database table 'badges' not found. Please create the table in your Supabase dashboard using the SQL from database/init_schema.sql")
        else:
            st.error(f"Failed to award badge: {error_msg}")
        return False

def get_student_badges(student_id):
    """Get all badges for a student"""
    try:
        response = supabase.table("badges").select("*").eq("student_id", student_id).execute()
        return response.data if response.data else []
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            st.error("❌ Database table 'badges' not found. Please create the table in your Supabase dashboard using the SQL from database/init_schema.sql")
        else:
            st.error(f"Failed to fetch badges: {error_msg}")
        return []
