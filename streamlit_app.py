import streamlit as st
from supabase_client import supabase
import json
import random
import time
import json
import plotly.express as px
import base64
import os
import google.generativeai as genai

# Configure Gemini API (add your API key to environment variables)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAlRm3mbpE7O43u7Ohm2pw6wtzLDbrIR4Y")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None
# =============================
# Gemini API Integration
# =============================

def get_gemini_explanation(question_text, options, correct_answer, student_answer):
    """Generate explanation for wrong answers using Gemini API"""
    if not model:
        return "💡 To get AI-powered explanations, please configure your Gemini API key."
    
    try:
        prompt = f"""
        A student answered a math question incorrectly. Please provide a clear, step-by-step explanation 
        of how to solve this problem correctly.
        
        Question: {question_text}
        Options: {options}
        Correct Answer: {correct_answer}
        Student's Answer: {student_answer}
        
        Please explain:
        1. Why the correct answer is right
        2. Why the student's answer is wrong
        3. Step-by-step solution to reach the correct answer
        4. Key concepts to remember
        
        Keep the explanation clear and educational, appropriate for a student.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"💡 AI explanation temporarily unavailable. Please try again later. Error: {str(e)}"

# =============================
# Page Setup
# =============================
st.set_page_config(page_title="Olympiad Prep", page_icon="🧠")
st.title("🧠 Olympiad Preparation Platform")

# =============================
# About Us Section
# =============================
# Adding custom CSS for hover effects
st.markdown("""
<style>
.about-container {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #e6e6e6;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
}

.about-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    border-color: #4CAF50;
}

.about-title {
    transition: color 0.3s ease;
}

.about-container:hover .about-title {
    color: #4CAF50;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown('<div class="about-container"><h3 class="about-title">🎯 Our Mission</h3><p>We aim to provide comprehensive Olympiad preparation resources for students, helping them excel in competitive mathematics examinations.</p></div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="about-container"><h3 class="about-title">👥 Our Approach</h3><p>Our platform combines interactive quizzes, video resources, and collaborative learning tools to create an engaging educational experience.</p></div>', unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown('<div class="about-container"><h3 class="about-title">🌟 Why Choose Us</h3><p>Personalized learning paths, real-time progress tracking, and expert-curated content designed specifically for Olympiad success.</p></div>', unsafe_allow_html=True)

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
    st.sidebar.markdown("### 👤 User Authentication")
    
    # Create tabs for better organization
    auth_option = st.sidebar.selectbox("Choose an option:", ["Login", "Sign Up"])
    
    if auth_option == "Login":
        login_type = st.sidebar.radio("Login as:", ["Student", "Teacher"])
        
        if login_type == "Student":
            st.sidebar.markdown("#### 🎓 Student Login")
            with st.sidebar.form("student_login_form"):
                st.markdown("🔐 Secure login for students")
                email = st.text_input("Email", placeholder="student@example.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                login_submitted = st.form_submit_button("Login as Student", use_container_width=True)
                
                if login_submitted:
                    if not email or not password:
                        st.error("⚠️ Please enter both email and password")
                    else:
                        try:
                            with st.spinner("Logging in..."):
                                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                                st.session_state.user = user
                                st.session_state.role = "student"
                                st.success("✅ Successfully logged in as Student!")
                                time.sleep(1)
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ Login failed: {str(e)}")
        
        elif login_type == "Teacher":
            st.sidebar.markdown("#### 👩‍🏫 Teacher Login")
            with st.sidebar.form("teacher_login_form"):
                st.markdown("🔐 Secure login for teachers")
                email = st.text_input("Email ", placeholder="teacher@school.edu")
                password = st.text_input("Password ", type="password", placeholder="••••••••")
                login_submitted = st.form_submit_button("Login as Teacher", use_container_width=True)
                
                if login_submitted:
                    if not email or not password:
                        st.error("⚠️ Please enter both email and password")
                    else:
                        try:
                            with st.spinner("Verifying credentials..."):
                                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                                result = supabase.table("users").select("role").eq("id", user.user.id).execute()
                                if result.data and result.data[0]["role"] == "teacher":
                                    st.session_state.user = user
                                    st.session_state.role = "teacher"
                                    st.success("✅ Teacher successfully logged in!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("⚠️ You are not authorized as a teacher. Please contact admin.")
                        except Exception as e:
                            st.error(f"❌ Login failed: {str(e)}")
    
    elif auth_option == "Sign Up":
        signup_type = st.sidebar.radio("Sign up as:", ["Student", "Teacher"])
        
        if signup_type == "Student":
            st.sidebar.markdown("#### 📝 Student Registration")
            with st.sidebar.form("student_signup_form"):
                st.markdown("🎓 Join our learning platform")
                email = st.text_input("Email", placeholder="student@example.com")
                password = st.text_input("Password", type="password", placeholder="At least 6 characters")
                full_name = st.text_input("Full Name", placeholder="Your full name")
                student_class = st.selectbox("Class", [8, 9, 10], help="Select your current class")
                signup_submitted = st.form_submit_button("Register as Student", use_container_width=True)
                
                if signup_submitted:
                    if not email or not password or not full_name:
                        st.error("⚠️ Please fill all required fields")
                    elif len(password) < 6:
                        st.error("⚠️ Password must be at least 6 characters long")
                    elif "@" not in email or "." not in email:
                        st.error("⚠️ Please enter a valid email address")
                    else:
                        try:
                            with st.spinner("Creating your account..."):
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
                                st.success("✅ Registration successful! Please check your email for verification link.")
                                st.info("💡 Tip: Check your spam folder if you don't see the email")
                        except Exception as e:
                            st.error(f"❌ Registration failed: {str(e)}")
        
        elif signup_type == "Teacher":
            st.sidebar.markdown("#### 🔐 Teacher Registration")
            with st.sidebar.form("teacher_signup_form"):
                st.markdown("👩‍🏫 Join our teaching community")
                email = st.text_input("Institution Email", placeholder="teacher@school.edu")
                password = st.text_input("Password", type="password", placeholder="At least 6 characters")
                full_name = st.text_input("Full Name", placeholder="Your full name")
                secret_code = st.text_input("Registration Code", type="password", placeholder="Enter teacher registration code")
                signup_submitted = st.form_submit_button("Register as Teacher", use_container_width=True)
                
                if signup_submitted:
                    if not email or not password or not full_name or not secret_code:
                        st.error("⚠️ Please fill all required fields")
                    elif len(password) < 6:
                        st.error("⚠️ Password must be at least 6 characters long")
                    elif secret_code != "MATH2025":
                        st.error("⚠️ Invalid registration code. Please contact admin for the correct code.")
                    elif not email.endswith((".edu", ".ac.in", "school", "k12")) and "teacher" not in email.lower():
                        st.warning("⚠️ Please use an institutional email address (e.g., @school.edu)")
                    elif "@" not in email or "." not in email:
                        st.error("⚠️ Please enter a valid email address")
                    else:
                        try:
                            with st.spinner("Creating your teacher account..."):
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
                                    st.success("✅ Teacher registration successful! Please check your email for verification link.")
                                    st.info("💡 Tip: Check your spam folder if you don't see the email")
                                else:
                                    st.info("Check your email for verification (optional)")
                        except Exception as e:
                            st.error(f"❌ Registration failed: {str(e)}")
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
        
        # Study Groups feature removed as per user request
    
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
            ,"Number Systems"]

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
        
        # Add buttons for starting quiz, sample papers, and studying material
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Create download button for study material PDF based on selected chapter
            chapter_to_pdf = {
                "Mensuration": "data/Mensuration 8th.pdf",
                "Data Handling": "data/Data Handling 8th.pdf",
                "Algebraic Expressions and Identities": "data/Algebraic Expressions and Identities 8th.pdf",
                "Comparing Quantities": "data/Comparing Quantities 8th.pdf",
                "Direct and Inverse Proportions": "data/Direct and Inverse Proportions 8th.pdf",
                "Exponents and Powers": "data/Exponents and Powers 8th.pdf",
                "Factorisation": "data/Factorisation 8th.pdf",
                "Linear Equations in One Variable": "data/Linear Equations in One Variable 8th.pdf",
                "Playing with Numbers": "data/Playing with Numbers 8th.pdf",
                "Squares and Square Roots": "data/Squares and Square Roots 8th.pdf",
                "Rational Numbers": "data/rational numbers 8th.pdf"
            }
            
            # Default fallback PDFs
            pdf_file = chapter_to_pdf.get(selected_chapter, "data/mensuration_study_material.pdf")
            pdf_filename = os.path.basename(pdf_file)
            
            if os.path.exists(pdf_file):
                with open(pdf_file, "rb") as f:
                    pdf_data = f.read()
                st.download_button(
                    label=f"📚 {selected_chapter} Study Material (PDF)",
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
            # Sample Paper buttons for each class
            sample_paper_file = f"data/CMO-Sample-Paper-for-Class-{selected_class}.pdf"
            sample_paper_filename = f"CMO-Sample-Paper-for-Class-{selected_class}.pdf"
            
            if os.path.exists(sample_paper_file):
                with open(sample_paper_file, "rb") as f:
                    sample_paper_data = f.read()
                st.download_button(
                    label=f"📝 Class {selected_class} Sample Paper (PDF)",
                    data=sample_paper_data,
                    file_name=sample_paper_filename,
                    mime="application/pdf",
                    key=f"sample_paper_{selected_class}"
                )
            else:
                st.warning(f"Sample paper for Class {selected_class} not found.")
        
        with col3:
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
                        
                        # Initialize question-specific session state
                        for i in range(len(questions)):
                            st.session_state[f"started_{i}"] = False
                            st.session_state[f"answered_{i}"] = False
                            st.session_state[f"feedback_{i}"] = None
                            st.session_state[f"timer_{i}"] = None
                            st.session_state.question_times[f"time_{i}"] = {"start": None, "end": None, "duration": 0}
                        
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
    st.info("Click 'Start Question' to reveal each question and begin timing.")
    st.markdown("---")

    # Initialize session state for answer feedback
    if "answer_feedback" not in st.session_state:
        st.session_state.answer_feedback = {}
    
    # Initialize session state for time tracking per question
    if "question_times" not in st.session_state:
        st.session_state.question_times = {}

    for i, q in enumerate(questions):
        # Initialize timer for this question if not already started
        timer_key = f"timer_{i}"
        if timer_key not in st.session_state:
            st.session_state[timer_key] = None
            
        # Initialize answer feedback for this question
        feedback_key = f"feedback_{i}"
        if feedback_key not in st.session_state:
            st.session_state[feedback_key] = None
            
        # Initialize time tracking for this question
        time_key = f"time_{i}"
        if time_key not in st.session_state.question_times:
            st.session_state.question_times[time_key] = {"start": None, "end": None, "duration": 0}

        # Track if answer has been submitted for this question
        answered_key = f"answered_{i}"
        if answered_key not in st.session_state:
            st.session_state[answered_key] = False

        # Track if question has been started
        started_key = f"started_{i}"
        if started_key not in st.session_state:
            st.session_state[started_key] = False

        # Button to start the question
        if not st.session_state[started_key]:
            if st.button(f"Start Question {i+1}", key=f"start_btn_{i}"):
                st.session_state[started_key] = True
                # Start timer when student clicks the button
                st.session_state.question_times[time_key]["start"] = time.time()
                st.rerun()
        else:
            # Show question and options once started
            st.markdown(f"**Q{i+1}. {q['question_text']}**")
            
            # Show options
            options = q["options"]
            chosen = st.radio(
                f"Choose answer for Q{i+1}",
                options=list(options.keys()),
                format_func=lambda opt: f"**{opt}**: {options[opt]}",
                key=f"q_{i}",
                horizontal=False,
                index=None  # No default selection
            )
            
            # If an answer is selected and not yet processed, stop timer and provide immediate feedback
            if chosen and not st.session_state[answered_key]:
                # Update current answer
                st.session_state.current_answers[f"q_{i}"] = chosen
                
                # Mark as answered
                st.session_state[answered_key] = True
                
                # Stop timer
                if st.session_state.question_times[time_key]["end"] is None:
                    st.session_state.question_times[time_key]["end"] = time.time()
                    st.session_state.question_times[time_key]["duration"] = \
                        st.session_state.question_times[time_key]["end"] - st.session_state.question_times[time_key]["start"]
                
                # Provide immediate feedback
                is_correct = chosen == q["correct_answer"]
                if is_correct:
                    st.session_state[feedback_key] = ("✅ Correct!", "green")
                else:
                    st.session_state[feedback_key] = (f"❌ Incorrect. The correct answer is {q['correct_answer']}", "red")
                
                # Save to database immediately
                try:
                    supabase.table("quiz_attempts").insert({
                        "student_id": st.session_state.user.user.id,
                        "question_id": q.get("id", i + 1),
                        "selected_answer": chosen,
                        "is_correct": is_correct,
                        "time_taken_seconds": int(st.session_state.question_times[time_key]["duration"]),
                        "quiz_session_id": f"quiz_{st.session_state.user.user.id}_{int(time.time())}"
                    }).execute()
                except Exception as e:
                    st.error(f"Failed to save answer {i+1}: {str(e)}")
                
                st.rerun()
            
            # Show feedback if available and question has been answered
            if st.session_state[feedback_key] and st.session_state[answered_key]:
                feedback_text, feedback_color = st.session_state[feedback_key]
                time_taken = st.session_state.question_times[time_key]["duration"]
                st.markdown(f"<span style='color:{feedback_color}'>{feedback_text}</span>", unsafe_allow_html=True)
                st.markdown(f"⏱️ Time taken: {int(time_taken)} seconds")
        
        st.markdown("---")

    # Submit Quiz button (for completion tracking)
    if st.button("✅ Finish Quiz"):
        # Calculate and show final results
        correct_count = 0
        total_questions = len(questions)
        
        # Count correct answers
        for i in range(total_questions):
            answered_key = f"answered_{i}"
            feedback_key = f"feedback_{i}"
            if st.session_state.get(answered_key, False) and st.session_state.get(feedback_key):
                feedback_text, _ = st.session_state[feedback_key]
                if "✅ Correct!" in feedback_text:
                    correct_count += 1
        
        # Show results
        st.markdown("---")
        st.subheader("📊 Final Quiz Results")
        st.success(f"🎉 Quiz Completed! **{correct_count}/{total_questions} Correct**")
        
        if total_questions > 0:
            accuracy = int((correct_count / total_questions) * 100)
            st.info(f"🎯 Overall Accuracy: **{accuracy}%**")
            if accuracy >= 80:
                st.balloons()
        
        # Show question-by-question analysis with AI explanations for wrong answers
        st.markdown("### Question-by-Question Analysis")
        for i in range(total_questions):
            answered_key = f"answered_{i}"
            feedback_key = f"feedback_{i}"
            time_key = f"time_{i}"
            
            if st.session_state.get(answered_key, False) and st.session_state.get(feedback_key):
                feedback_text, _ = st.session_state[feedback_key]
                time_taken = st.session_state.question_times.get(time_key, {}).get("duration", 0)
                
                status_emoji = "✅" if "✅ Correct!" in feedback_text else "❌"
                status_text = "Correct" if "✅ Correct!" in feedback_text else "Incorrect"
                
                st.markdown(f"**Q{i+1}.** Status: {status_emoji} {status_text}")
                st.markdown(f"⏱️ Time taken: {int(time_taken)} seconds")
                
                # For incorrect answers, show AI explanation
                if "❌" in feedback_text and i < len(questions):
                    question = questions[i]
                    student_answer = st.session_state.current_answers.get(f"q_{i}", "Not answered")
                    
                    with st.expander("💡 AI-Powered Explanation", expanded=False):
                        with st.spinner("Generating explanation..."):
                            explanation = get_gemini_explanation(
                                question["question_text"],
                                question["options"],
                                question["correct_answer"],
                                student_answer
                            )
                            st.markdown(explanation)
                
                st.markdown("---")
        
        # Clear quiz session state after showing results
        if st.button("Close Results"):
            keys_to_remove = ["quiz_questions", "quiz_start_time", "current_answers", "quiz_info", "answer_feedback", "question_times"]
            for i in range(len(questions)):
                keys_to_remove.extend([f"timer_{i}", f"feedback_{i}", f"time_{i}", f"started_{i}", f"start_btn_{i}", f"q_{i}", f"answered_{i}"])
            for key in keys_to_remove:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
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
    
    if st.session_state.get("page") == "study_groups":
        st.title("👥 Study Groups")
        from utils.social_ui import show_study_groups_page
        show_study_groups_page(st.session_state.user.user.id)

        if st.button("Back to Dashboard"):
            st.session_state.pop("page")
            st.rerun()
    