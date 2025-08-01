import streamlit as st
from supabase_client import supabase
import json
import random
import time
import json
import plotly.express as px
import base64
import os
# =============================
# Page Setup
# =============================
st.set_page_config(page_title="Olympiad Prep", page_icon="🧠")
st.title("🧠 Olympiad Preparation Platform")

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.role = None

# =============================
# LOGOUT (if logged in)
# =============================
if st.session_state.user:
    try:
        user_email = st.session_state.user.user.email
    except AttributeError:
        user_email = "User"

    st.sidebar.success(f"Logged in as {user_email}")
    if st.sidebar.button("Logout"):
        supabase.auth.sign_out()
        st.session_state.clear()
        st.rerun()
    st.sidebar.divider()

# =============================
# AUTHENTICATION: Login / Sign Up
# =============================
if not st.session_state.user:
    menu = st.sidebar.radio("🔐 Menu", [
        "Student Login", 
        "Student Sign Up", 
        "Teacher Login",
        "Teacher Sign Up"
    ])
else:
    # Quick Access Dashboard for logged-in users
    st.sidebar.markdown("### 🚀 Quick Access")
    if st.session_state.role == "student":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("📝 Take Quiz", use_container_width=True):
                st.session_state.page = "quiz"
                st.rerun()
        with col2:
            if st.button("📊 Analytics", use_container_width=True):
                st.session_state.page = "analytics"
                st.rerun()
        
        if st.sidebar.button("📺 Video Learning", use_container_width=True):
            st.session_state.page = "video_learning"
            st.rerun()
        
        if st.sidebar.button("❓ Ask Doubt", use_container_width=True):
            st.session_state.page = "doubt_box_student"
            st.rerun()
        
        st.sidebar.markdown("### 🤝 Social Learning")
        if st.sidebar.button("🔖 My Bookmarks", use_container_width=True):
            st.session_state.page = "bookmarks"
            st.rerun()
        
        if st.sidebar.button("🏆 Leaderboard", use_container_width=True):
            st.session_state.page = "leaderboard"
            st.rerun()
        
        if st.sidebar.button("🏅 Achievements", use_container_width=True):
            st.session_state.page = "badges"
            st.rerun()
        
        if st.sidebar.button("👥 Study Groups", use_container_width=True):
            st.session_state.page = "study_groups"
            st.rerun()
        
        if st.sidebar.button("🔍 Debug Bookmarks", use_container_width=True):
            st.session_state.page = "debug_bookmarks"
            st.rerun()
    
    elif st.session_state.role == "teacher":
        if st.sidebar.button("👩‍🏫 Dashboard", use_container_width=True):
            st.session_state.page = "teacher_dashboard"
            st.rerun()
        if st.sidebar.button("📬 View Doubts", use_container_width=True):
            st.session_state.page = "doubt_box_teacher"
            st.rerun()
        if st.sidebar.button("📺 Video Resources", use_container_width=True):
            st.session_state.page = "video_resources"
            st.rerun()
    
    st.sidebar.divider()
    menu = None  # Skip menu for logged-in users

# 0. TEACHER SIGN UP (Admin-Controlled)
if menu == "Teacher Sign Up":
    st.subheader("🔐 Register as Teacher")
    with st.form("teacher_signup_form"):
        email = st.text_input("Institution Email (e.g., @school.edu)")
        password = st.text_input("Password", type="password")
        full_name = st.text_input("Full Name")
        secret_code = st.text_input("Registration Code", type="password")
        submitted = st.form_submit_button("Register as Teacher")

        if submitted:
            if not email or not password or not full_name or not secret_code:
                st.error("Please fill all fields")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            elif secret_code != "MATH2025":  # ← Change this to your preferred code
                st.error("Invalid registration code")
            elif not email.endswith((".edu", ".ac.in", "school", "k12")) and "teacher" not in email.lower():
                st.warning("Please use an institutional email")
            else:
                try:
                    # Sign up via Supabase Auth
                    response = supabase.auth.sign_up({
                        "email": email,
                        "password": password,
                        "options": {
                            "data": {
                                "full_name": full_name
                            }
                        }
                    })
                    if response.user:
                        # Update role to 'teacher' in public.users
                        supabase.table("users").update({"role": "teacher"}).eq("id", response.user.id).execute()
                        st.success("✅ Teacher registration successful! You can now login.")
                    else:
                        st.info("Check your email (optional)")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
# 1. STUDENT SIGN UP
if menu == "Student Sign Up":
    st.subheader("📝 Register as Student")
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        full_name = st.text_input("Full Name")
        student_class = st.selectbox("Class", [8, 9, 10])
        submitted = st.form_submit_button("Register")

        if submitted:
            if not email or not password or not full_name:
                st.error("Please fill all fields")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                try:
                    response = supabase.auth.sign_up({
                        "email": email,
                        "password": password,
                        "options": {
                            "data": {
                                "full_name": full_name,
                                "class": student_class
                            }
                        }
                    })
                    st.success("✅ Registration successful! Please login.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# 2. STUDENT LOGIN
elif menu == "Student Login":
    st.subheader("🎓 Student Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state.user = user
            st.session_state.role = "student"
            st.success("Logged in as Student!")
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {str(e)}")

# 3. TEACHER LOGIN
elif menu == "Teacher Login":
    st.subheader("👩‍🏫 Teacher Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            result = supabase.table("users").select("role").eq("id", user.user.id).execute()
            if result.data and result.data[0]["role"] == "teacher":
                st.session_state.user = user
                st.session_state.role = "teacher"
                st.success("Teacher logged in!")
                st.rerun()
            else:
                st.error("You are not authorized as a teacher.")
        except Exception as e:
            st.error(f"Login failed: {str(e)}")

# =============================
# PAGE ROUTING SYSTEM
# =============================
def show_main_dashboard():
    """Show the main dashboard based on user role"""
    current_page = st.session_state.get("page", "main")
    
    if st.session_state.role == "student":
        if current_page == "main":
            show_student_dashboard()
        elif current_page == "quiz":
            show_student_dashboard()
        elif current_page == "video_learning":
            from utils.video_resources import show_video_dashboard
            show_video_dashboard()
        else:
            show_student_dashboard()
    elif st.session_state.role == "teacher":
        if current_page == "video_resources":
            from utils.video_resources import show_video_dashboard
            show_video_dashboard()
        else:
            show_teacher_main()

def show_student_dashboard():
    """Student dashboard with quiz options and video resources"""
    st.title("📚 Your Learning Dashboard")
    st.info("💡 For detailed analytics, click 'Detailed Analytics' in the sidebar")

def show_teacher_main():
    """Teacher main page with overview"""
    st.title("👩‍🏫 Teacher Dashboard")
    st.info("Welcome! Use the sidebar to navigate to different sections.")
    
    # Quick overview
    try:
        students_response = supabase.table("users").select("*").eq("role", "student").execute()
        total_students = len(students_response.data) if students_response.data else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Students", total_students)
        with col2:
            # Count total quiz attempts across all students
            attempts_response = supabase.table("quiz_attempts").select("*").execute()
            total_attempts = len(attempts_response.data) if attempts_response.data else 0
            st.metric("Total Quiz Attempts", total_attempts)
    except Exception:
        st.warning("Could not load overview stats")

# =============================
# STUDENT DASHBOARD (After Login)
# =============================
if st.session_state.user and st.session_state.role == "student":
    # Handle page routing
    current_page = st.session_state.get("page", "main")
    
    if current_page == "main":
        show_student_dashboard()
    elif current_page == "quiz":
        show_student_dashboard()
    elif current_page == "video_learning":
        from utils.video_resources import show_video_dashboard
        show_video_dashboard()

    # Fetch student info
    try:
        user_email = st.session_state.user.user.email
        user_data = supabase.table("users").select("full_name, class").eq("email", user_email).execute()

        if not user_data.data:
            st.error("User data not found!")
            st.stop()

        student_name = user_data.data[0]["full_name"]
        student_class = user_data.data[0]["class"]
        st.success(f"Hello, {student_name}! 👋 Welcome to Class {student_class}")
        st.markdown("---")

        # Quiz Selection
        st.subheader("🎯 Start a Quiz")
        selected_class = st.selectbox("Select Class", [8, 9, 10], index=student_class - 8, key="class_selector")

        # Load chapters dynamically from dataset
        try:
            with open("data/ncert_maths_dataset.json", "r", encoding="utf-8") as f:
                all_questions = json.load(f)
            mcq_questions = [q for q in all_questions if q.get("question_type", "MCQ") == "MCQ"]
            all_chapters = sorted(list(set(
                q["chapter"] for q in mcq_questions if q["class_level"] == selected_class
            )))
        except Exception:
            all_chapters = [
                "Linear Equations in One Variable",
                "Mensuration", "Data Handling", "Exponents and Powers",  "Playing with numbers"
            ]

        selected_chapter = st.selectbox("Select Chapter", all_chapters, key="chapter_selector")

        # Difficulty filter
        difficulty = st.selectbox("Select Difficulty", ["Any", "Easy", "Medium", "Hard"], key="difficulty_selector")

        st.info(f"Class: {selected_class} | Chapter: {selected_chapter} | Difficulty: {difficulty}")

        # Enhanced quiz options
        col1, col2 = st.columns(2)
        with col1:
            num_questions = st.selectbox("Number of Questions", [5, 10, 15, 20], index=0, key="num_questions_selector")
        with col2:
            # Check for saved progress
            user_id = st.session_state.user.user.id
            from utils.enhanced_quiz import load_quiz_progress
            saved_progress = load_quiz_progress(user_id)
            
            if saved_progress:
                if st.button("💾 Resume Saved Quiz"):
                    st.session_state.quiz_questions = saved_progress['quiz_data']
                    st.session_state.current_answers = saved_progress['current_answers']
                    st.session_state.current_question = saved_progress['current_question']
                    st.session_state.quiz_start_time = {}
                    st.session_state.quiz_info = {
                        "class": selected_class,
                        "chapter": "Resumed Quiz",
                        "difficulty": difficulty,
                        "count": len(saved_progress['quiz_data'])
                    }
                    st.success("Quiz resumed!")
                    st.rerun()
        
        # Add buttons for both starting quiz and studying material
        col1, col2 = st.columns(2)
        
        with col1:
            # Create download button for study material PDF
            if selected_chapter == "Mensuration":
                pdf_file = "data/mensuration_study_material.pdf"
                pdf_filename = "mensuration_study_material.pdf"
            else:
                pdf_file = "data/data_handling_study_material.pdf"
                pdf_filename = "data_handling_study_material.pdf"
            
            if os.path.exists(pdf_file):
                with open(pdf_file, "rb") as f:
                    pdf_data = f.read()
                st.download_button(
                    label="📚 Study Material (PDF)",
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
            else:
                if st.button("📚 Study Material"):
                    st.session_state.page = "study_material"
                    st.session_state.study_chapter = selected_chapter
                    st.rerun()
        
        with col2:
            if st.button("🚀 Start New Quiz"):
                from utils.enhanced_quiz import load_questions_with_filters, clear_quiz_progress
                
                # Clear any existing progress
                clear_quiz_progress(user_id)
                
                with st.spinner("Loading your quiz..."):
                    questions, error = load_questions_with_filters(selected_class, selected_chapter, difficulty, num_questions)
                    
                    if error:
                        st.error(error)
                    else:
                        st.session_state.quiz_questions = questions
                        st.session_state.quiz_start_time = {}
                        st.session_state.current_answers = {}
                        st.session_state.current_question = 0
                        st.session_state.quiz_info = {
                            "class": selected_class,
                            "chapter": selected_chapter,
                            "difficulty": difficulty,
                            "count": len(questions)
                        }
                        st.success(f"Quiz loaded with {len(questions)} questions!")
                        st.rerun()
        
        # Video Resources Section
        st.markdown("---")
        st.info("📺 For learning videos, click 'Video Learning' in the sidebar")

    except Exception as e:
        st.error(f"Failed to load student data: {str(e)}")

# =============================
# DISPLAY QUIZ (if loaded)
# =============================
# =============================
# STUDENT ANALYTICS
# =============================
if st.session_state.user and st.session_state.role == "student":
    if st.session_state.get("page") == "analytics":
        from utils.analytics import show_student_analytics
        show_student_analytics(st.session_state.user.user.id)

        if st.button("Back to Quiz"):
            st.session_state.pop("page")
            st.rerun()
    

if st.session_state.user and st.session_state.role == "student" and "quiz_questions" in st.session_state:
    questions = st.session_state.quiz_questions
    st.markdown(f"### 📝 Quiz: {st.session_state.quiz_info['chapter']}")
    st.markdown(f"**Class**: {st.session_state.quiz_info['class']} | "
                f"**Difficulty**: {st.session_state.quiz_info['difficulty']} | "
                f"**Questions**: {len(questions)}")
    st.info("Click 'Start Answering' for each question to reveal it and begin timing.")
    st.markdown("---")

    for i, q in enumerate(questions):
        # Check if student has started answering this question
        started_key = f"started_{i}"
        if started_key not in st.session_state:
            st.session_state[started_key] = False
            
        # Button to start answering
        if not st.session_state[started_key]:
            if st.button(f"Start Answering Q{i+1}", key=f"start_btn_{i}"):
                st.session_state[started_key] = True
                # Start timer when student clicks the button
                st.session_state.quiz_start_time[f"start_time_{i}"] = time.time()
                st.rerun()
        else:
            # Show question and options once started
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**Q{i+1}. {q['question_text']}**")
            with col2:
                # Bookmark button
                from utils.social_features import is_question_bookmarked
                question_id = q.get('id', i)
                student_id = st.session_state.user.user.id
                
                # Check if question is already bookmarked
                is_bookmarked = is_question_bookmarked(student_id, question_id)
                
                bookmark_key = f"bookmark_{question_id}"
                bookmark_label = "✅" if is_bookmarked else "🔖"
                bookmark_help = "Question already bookmarked" if is_bookmarked else "Bookmark this question for later review"
                
                if st.button(bookmark_label, key=bookmark_key, help=bookmark_help, disabled=is_bookmarked):
                    from utils.social_features import bookmark_question
                    if bookmark_question(student_id, question_id, q['question_text']):
                        st.success("Question bookmarked!")
                        time.sleep(1)  # Show success message for 1 second
                        st.rerun()
                    else:
                        st.error("Failed to bookmark question")

            # Show options
            options = q["options"]
            chosen = st.radio(
                f"Choose answer for Q{i+1}",
                options=list(options.keys()),
                format_func=lambda opt: f"**{opt}**: {options[opt]}",
                key=f"q_{i}",
                horizontal=False
            )
            st.session_state.current_answers[f"q_{i}"] = chosen
        st.markdown("---")

    # Submit Quiz
    if st.button("✅ Submit Quiz"):
        quiz_session_id = f"quiz_{int(time.time())}"
        correct_count = 0
        results_data = []

        for i, q in enumerate(questions):
            selected = st.session_state.current_answers.get(f"q_{i}")
            is_correct = selected == q["correct_answer"]
            if is_correct:
                correct_count += 1

            start_time = st.session_state.quiz_start_time.get(f"start_time_{i}", time.time())
            time_taken = int(time.time() - start_time)

            # Store result data for detailed display
            results_data.append({
                "question_num": i + 1,
                "question_text": q["question_text"],
                "selected_answer": selected,
                "correct_answer": q["correct_answer"],
                "is_correct": is_correct,
                "time_taken": time_taken
            })

            try:
                supabase.table("quiz_attempts").insert({
                    "student_id": st.session_state.user.user.id,
                    "question_id": q.get("id", i + 1),
                    "selected_answer": selected,
                    "is_correct": is_correct,
                    "time_taken_seconds": time_taken,
                    "quiz_session_id": quiz_session_id
                }).execute()
            except Exception as e:
                st.error(f"Failed to save answer {i+1}: {str(e)}")

        # Detailed Results
        st.markdown("---")
        st.subheader("📊 Quiz Results")
        total = len(questions)
        accuracy = int((correct_count / total) * 100)
        st.success(f"🎉 Quiz Submitted! **{correct_count}/{total} Correct**")
        st.info(f"🎯 Overall Accuracy: **{accuracy}%**")
        if accuracy >= 80:
            st.balloons()

        # Show detailed results for each question
        st.markdown("### Question-by-Question Analysis")
        for result in results_data:
            status_emoji = "✅" if result["is_correct"] else "❌"
            status_text = "Correct" if result["is_correct"] else "Incorrect"
            time_text = f"{result['time_taken']} seconds"
            
            st.markdown(f"**Q{result['question_num']}. {result['question_text']}**")
            st.markdown(f"- Your Answer: **{result['selected_answer']}**")
            st.markdown(f"- Correct Answer: **{result['correct_answer']}**")
            st.markdown(f"- Status: {status_emoji} {status_text}")
            st.markdown(f"- Time Taken: ⏱️ {time_text}")
            st.markdown("---")
    
    # Discussion Forum
    st.markdown("### 💬 Discuss This Quiz")
    st.info("Discuss questions with your classmates in the forum below!")
    from utils.social_ui import show_discussion_forum
    # Show discussion forum for the first question as an example
    if questions:
        first_question = questions[0]
        show_discussion_forum(
            first_question.get('id', 0), 
            first_question['question_text'], 
            st.session_state.user.user.id, 
            st.session_state.user.user.email.split('@')[0]
        )
# =============================
# DOUBT BOX - STUDENT
# =============================
if st.session_state.user and st.session_state.role == "student":
    if st.session_state.get("page") == "doubt_box_student":
        st.title("❓ Doubt Box")
        from utils.doubt_box import student_doubt_box
        student_doubt_box(st.session_state.user.user.id)

        if st.button("Back to Dashboard"):
            st.session_state.pop("page")
            st.rerun()

# =============================
# DOUBT BOX - TEACHER
# =============================
if st.session_state.user and st.session_state.role == "teacher":
    if st.session_state.get("page") == "doubt_box_teacher":
        st.title("📬 Teacher: Respond to Doubts")
        from utils.doubt_box import teacher_doubt_box
        teacher_doubt_box(st.session_state.user.user.id)

        if st.button("Back to Dashboard"):
            st.session_state.pop("page")
            st.rerun()
# =============================
# TEACHER DASHBOARD
# =============================
if st.session_state.user and st.session_state.role == "teacher":
    st.sidebar.divider()
    if st.sidebar.button("📊 Class Dashboard"):
        st.session_state.page = "teacher_dashboard"
        st.rerun()

    if st.session_state.get("page") == "teacher_dashboard":
        st.title("👩‍🏫 Teacher Dashboard")
        from utils.teacher_dashboard import teacher_dashboard
        teacher_dashboard(st.session_state.user.user.id)

        if st.button("Back to Login"):
            st.session_state.clear()
            st.rerun()

        # Clear session
        keys_to_remove = ["quiz_questions", "quiz_start_time", "current_answers", "quiz_info"]
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        st.button("Back to Dashboard", on_click=lambda: st.rerun())
        
    # Handle video resources page for teachers
    if st.session_state.get("page") == "video_resources":
        st.title("📺 Video Learning Resources")
        from utils.video_resources import show_video_dashboard
        show_video_dashboard()

        if st.button("Back to Dashboard"):
            st.session_state.pop("page")
            st.rerun()
    
    # Handle social learning pages for students
    if st.session_state.get("page") == "bookmarks":
        st.title("🔖 My Bookmarks")
        from utils.social_ui import show_bookmarks_page
        show_bookmarks_page(st.session_state.user.user.id)

        if st.button("Back to Dashboard"):
            st.session_state.pop("page")
            st.rerun()
    
    # Handle study material page
    if st.session_state.get("page") == "study_material":
        st.title("📚 Study Material")
        from utils.study_material import show_data_handling_material, show_mensuration_material
        
        chapter = st.session_state.get("study_chapter", "Data Handling")
        
        # Debug information
        st.caption(f"Debug: Selected chapter is '{chapter}'")
        st.caption(f"Debug: Chapter type is {type(chapter)}")
        st.caption(f"Debug: Chapter.strip() == 'Mensuration' is {chapter.strip() == 'Mensuration'}")
        
        # Handle chapter selection (with case insensitive and strip for robustness)
        if isinstance(chapter, str) and chapter.strip().lower() == "mensuration":
            show_mensuration_material()
        else:
            show_data_handling_material()

        if st.button("Back to Dashboard"):
            st.session_state.pop("page")
            st.session_state.pop("study_chapter", None)
            st.rerun()
    
    if st.session_state.get("page") == "leaderboard":
        st.title("🏆 Class Leaderboard")
        from utils.social_ui import show_leaderboard_page
        show_leaderboard_page()

        if st.button("Back to Dashboard"):
            st.session_state.pop("page")
            st.rerun()
    
    if st.session_state.get("page") == "badges":
        st.title("🏅 My Achievements")
        from utils.social_ui import show_badges_page
        show_badges_page(st.session_state.user.user.id)

        if st.button("Back to Dashboard"):
            st.session_state.pop("page")
            st.rerun()
    
    if st.session_state.get("page") == "study_groups":
        st.title("👥 Study Groups")
        from utils.social_ui import show_study_groups_page
        show_study_groups_page(st.session_state.user.user.id)

        if st.button("Back to Dashboard"):
            st.session_state.pop("page")
            st.rerun()
    
    if st.session_state.get("page") == "debug_bookmarks":
        import debug_bookmarks_simple

        if st.button("Back to Dashboard"):
            st.session_state.pop("page")
            st.rerun()
    