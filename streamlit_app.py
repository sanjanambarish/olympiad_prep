import streamlit as st
from supabase_client import supabase
import json
import random
import time
import json
import plotly.express as px
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
menu = st.sidebar.radio("🔐 Menu", [
    "Student Login", 
    "Student Sign Up", 
    "Teacher Login",
    "Teacher Sign Up"  # ← Add this
])
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
# STUDENT DASHBOARD (After Login)
# =============================
if st.session_state.user and st.session_state.role == "student":
    st.title("📚 Your Learning Dashboard")

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
        selected_class = st.selectbox("Select Class", [8, 9, 10], index=student_class - 8)

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

        selected_chapter = st.selectbox("Select Chapter", all_chapters)

        # Difficulty filter
        difficulty = st.selectbox("Select Difficulty", ["Any", "Easy", "Medium", "Hard"], key="diff_select")

        st.info(f"Class: {selected_class} | Chapter: {selected_chapter} | Difficulty: {difficulty}")

        if st.button("Load Questions"):
            try:
                with open("data/ncert_maths_dataset.json", "r", encoding="utf-8") as f:
                    all_questions = json.load(f)

                mcq_questions = [q for q in all_questions if q.get("question_type", "MCQ") == "MCQ"]
                filtered = [
                    q for q in mcq_questions
                    if q["class_level"] == selected_class and q["chapter"] == selected_chapter
                ]

                if difficulty != "Any":
                    filtered = [q for q in filtered if q["difficulty"] == difficulty]

                if len(filtered) == 0:
                    st.warning("No MCQs found for this filter.")
                    st.stop()

                with st.spinner("Loading your quiz..."):
                    random.shuffle(filtered)
                    num = min(5, len(filtered))
                    st.session_state.quiz_questions = filtered[:num]
                    st.session_state.quiz_start_time = {}
                    st.session_state.current_answers = {}
                    st.session_state.quiz_info = {
                        "class": selected_class,
                        "chapter": selected_chapter,
                        "difficulty": difficulty,
                        "count": num
                    }
                    st.rerun()

            except FileNotFoundError:
                st.error("❌ Dataset not found! Place 'ncert_maths_dataset.json' in 'data/' folder.")
            except Exception as e:
                st.error(f"Error loading dataset: {str(e)}")

    except Exception as e:
        st.error(f"Failed to load student data: {str(e)}")

# =============================
# DISPLAY QUIZ (if loaded)
# =============================
# =============================
# STUDENT ANALYTICS
# =============================
if st.session_state.user and st.session_state.role == "student":
    st.sidebar.divider()
    if st.sidebar.button("📊 My Performance"):
        st.session_state.page = "analytics"
        st.rerun()

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
    st.markdown("---")

    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['question_text']}**")

        # Start timer
        if f"start_time_{i}" not in st.session_state.quiz_start_time:
            st.session_state.quiz_start_time[f"start_time_{i}"] = time.time()

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

        for i, q in enumerate(questions):
            selected = st.session_state.current_answers.get(f"q_{i}")
            is_correct = selected == q["correct_answer"]
            if is_correct:
                correct_count += 1

            start_time = st.session_state.quiz_start_time.get(f"start_time_{i}", time.time())
            time_taken = int(time.time() - start_time)

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

        # Final Result
        total = len(questions)
        accuracy = int((correct_count / total) * 100)
        st.success(f"🎉 Quiz Submitted! **{correct_count}/{total} Correct**")
        st.info(f"🎯 Accuracy: **{accuracy}%**")
        if accuracy >= 80:
            st.balloons()
# =============================
# DOUBT BOX - STUDENT
# =============================
if st.session_state.user and st.session_state.role == "student":
    st.sidebar.divider()
    if st.sidebar.button("❓ Ask a Doubt"):
        st.session_state.page = "doubt_box_student"
        st.rerun()

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
    st.sidebar.divider()
    if st.sidebar.button("📬 View Doubts"):
        st.session_state.page = "doubt_box_teacher"
        st.rerun()

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