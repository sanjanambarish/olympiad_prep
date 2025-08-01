import streamlit as st
import json
import random
import time
from supabase_client import supabase

def save_quiz_progress(user_id, quiz_data, current_answers, current_question=0):
    """Save quiz progress to resume later"""
    try:
        progress_data = {
            "user_id": user_id,
            "quiz_data": quiz_data,
            "current_answers": current_answers,
            "current_question": current_question,
            "saved_at": time.time()
        }
        
        # Check if progress already exists
        existing = supabase.table("quiz_progress").select("*").eq("user_id", user_id).execute()
        
        if existing.data:
            # Update existing progress
            supabase.table("quiz_progress").update(progress_data).eq("user_id", user_id).execute()
        else:
            # Insert new progress
            supabase.table("quiz_progress").insert(progress_data).execute()
        
        return True
    except Exception as e:
        st.error(f"Could not save progress: {str(e)}")
        return False

def load_quiz_progress(user_id):
    """Load saved quiz progress"""
    try:
        response = supabase.table("quiz_progress").select("*").eq("user_id", user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception:
        return None

def clear_quiz_progress(user_id):
    """Clear saved quiz progress"""
    try:
        supabase.table("quiz_progress").delete().eq("user_id", user_id).execute()
    except Exception:
        pass

def enhanced_quiz_interface():
    """Enhanced quiz interface with progress saving and better UX"""
    if "quiz_questions" not in st.session_state:
        return
    
    questions = st.session_state.quiz_questions
    current_q_index = st.session_state.get("current_question", 0)
    
    # Progress bar
    progress = (current_q_index + 1) / len(questions)
    st.progress(progress)
    st.caption(f"Question {current_q_index + 1} of {len(questions)}")
    
    # Current question
    q = questions[current_q_index]
    
    st.markdown(f"### Question {current_q_index + 1}")
    st.markdown(f"**{q['question']}**")
    
    # Timer for current question
    if f"start_time_{current_q_index}" not in st.session_state.quiz_start_time:
        st.session_state.quiz_start_time[f"start_time_{current_q_index}"] = time.time()
    
    # Show options
    options = q["options"]
    chosen = st.radio(
        "Choose your answer:",
        options=list(options.keys()),
        format_func=lambda opt: f"**{opt}**: {options[opt]}",
        key=f"q_{current_q_index}",
        horizontal=False
    )
    st.session_state.current_answers[f"q_{current_q_index}"] = chosen
    
    # Navigation buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if current_q_index > 0:
            if st.button("⬅️ Previous"):
                st.session_state.current_question = current_q_index - 1
                st.rerun()
    
    with col2:
        if st.button("💾 Save Progress"):
            user_id = st.session_state.user.user.id
            if save_quiz_progress(user_id, st.session_state.quiz_questions, 
                                st.session_state.current_answers, current_q_index):
                st.success("Progress saved!")
                time.sleep(1)
                st.rerun()
    
    with col3:
        if current_q_index < len(questions) - 1:
            if st.button("Next ➡️"):
                st.session_state.current_question = current_q_index + 1
                st.rerun()
    
    with col4:
        if current_q_index == len(questions) - 1:
            if st.button("✅ Submit Quiz"):
                submit_quiz()
        else:
            if st.button("🏁 Finish Early"):
                if st.session_state.get("confirm_finish"):
                    submit_quiz()
                else:
                    st.session_state.confirm_finish = True
                    st.warning("Click again to confirm early submission")
                    st.rerun()

def submit_quiz():
    """Submit quiz and show results"""
    questions = st.session_state.quiz_questions
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
    
    # Clear progress after submission
    clear_quiz_progress(st.session_state.user.user.id)
    
    # Show results
    total = len(questions)
    accuracy = int((correct_count / total) * 100)
    
    st.success(f"🎉 Quiz Completed! **{correct_count}/{total} Correct**")
    st.info(f"🎯 Accuracy: **{accuracy}%**")
    
    if accuracy >= 80:
        st.balloons()
        st.success("🌟 Excellent performance!")
    elif accuracy >= 60:
        st.info("👍 Good job! Keep practicing!")
    else:
        st.warning("📚 Consider reviewing the material and trying again.")
    
    # Clear quiz session
    for key in ["quiz_questions", "quiz_start_time", "current_answers", "quiz_info", "current_question"]:
        if key in st.session_state:
            del st.session_state[key]
    
    if st.button("🔄 Take Another Quiz"):
        st.rerun()

def load_questions_with_filters(selected_class, selected_chapter, difficulty, num_questions=5):
    """Load questions with enhanced filtering"""
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
            return None, "No MCQs found for this filter."
        
        # Shuffle and select
        random.shuffle(filtered)
        num = min(num_questions, len(filtered))
        selected_questions = filtered[:num]
        
        return selected_questions, None
        
    except FileNotFoundError:
        return None, "❌ Dataset not found! Place 'ncert_maths_dataset.json' in 'data/' folder."
    except Exception as e:
        return None, f"Error loading dataset: {str(e)}"
