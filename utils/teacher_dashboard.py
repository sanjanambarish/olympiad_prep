import streamlit as st
import pandas as pd
import plotly.express as px
from supabase_client import supabase
import json
from datetime import datetime

def teacher_dashboard(teacher_id):
    # Fetch all students
    try:
        users_response = supabase.table("users").select("*").eq("role", "student").execute()
        if not users_response.data:
            st.error("No students found.")
            return
        students_df = pd.DataFrame(users_response.data)
    except Exception as e:
        st.error(f"Error fetching students: {str(e)}")
        return

    st.subheader("🎓 All Students")
    st.dataframe(students_df[['full_name', 'email', 'class']], use_container_width=True)

    # Student selection
    student_names = students_df['full_name'].tolist()
    selected_student_name = st.selectbox("Select Student for Performance Review", [""] + student_names)

    if selected_student_name:
        student_row = students_df[students_df['full_name'] == selected_student_name].iloc[0]
        student_id = student_row['id']
        class_level = student_row['class']
        st.markdown(f"### 📌 Selected: **{selected_student_name}** (Class {class_level})")

        # Fetch quiz attempts
        try:
            attempts_response = supabase.table("quiz_attempts").select("*").eq("student_id", student_id).execute()
            if not attempts_response.data:
                st.info("No quiz attempts yet.")
                return
            attempts_df = pd.DataFrame(attempts_response.data)
            attempts_df['attempted_at'] = pd.to_datetime(attempts_df['attempted_at'])
        except Exception as e:
            st.error(f"Error fetching attempts: {str(e)}")
            return

        # Load question data and merge
        merged_df = attempts_df.copy()
        try:
            with open("data/ncert_maths_dataset.json", "r", encoding="utf-8") as f:
                questions = pd.DataFrame(json.load(f))
                question_cols = [col for col in ['id', 'chapter', 'topic', 'difficulty'] if col in questions.columns]
                questions = questions[question_cols]
                merged_df = attempts_df.merge(questions, left_on='question_id', right_on='id', how='left')
        except FileNotFoundError:
            st.warning("📚 Question dataset not found.")
        except Exception as e:
            st.warning(f"⚠️ Could not load chapter data: {str(e)}")

        if 'chapter' not in merged_df.columns:
            merged_df['chapter'] = "Unknown"

        # === Student Summary ===
        total = len(merged_df)
        correct = merged_df['is_correct'].sum()
        accuracy = int((correct / total) * 100) if total > 0 else 0
        avg_time = int(merged_df['time_taken_seconds'].mean()) if total > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Questions", total)
        col2.metric("Accuracy", f"{accuracy}%")
        col3.metric("Avg Time", f"{avg_time}s")

        # === Performance by Chapter ===
        st.markdown("#### 📚 Performance by Chapter")
        chapter_perf = merged_df.groupby('chapter').agg(
            correct=('is_correct', 'sum'),
            total=('is_correct', 'count')
        ).reset_index()
        chapter_perf['accuracy'] = (chapter_perf['correct'] / chapter_perf['total'] * 100).round(1)

        fig2 = px.bar(chapter_perf, x='chapter', y='accuracy',
                      color='accuracy', color_continuous_scale=['red', 'yellow', 'green'],
                      title="Chapter-wise Accuracy", labels={"accuracy": "Accuracy (%)"})
        st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(
            chapter_perf.style.format({"accuracy": "{}%"}).background_gradient(cmap='RdYlGn', subset=["accuracy"]),
            use_container_width=True
        )

        # === Weak Areas ===
        st.markdown("#### 🔍 Areas Needing Improvement")
        weak = chapter_perf[chapter_perf['accuracy'] < 70]
        if weak.empty:
            st.success("🎉 This student is doing well in all areas.")
        else:
            st.warning("Focus on these chapters:")
            for _, row in weak.iterrows():
                st.markdown(f"- **{row['chapter']}**: {row['accuracy']}% accuracy")

        # === Download Student Report ===
        st.markdown("#### 📥 Download Student Report")
        from utils.reports import generate_student_report
        if st.button("📥 Generate Excel Report"):
            xlsx_data = generate_student_report(student_id, selected_student_name)
            if xlsx_data:
                st.download_button(
                    label="⬇️ Download XLSX Report",
                    data=xlsx_data,
                    file_name=f"report_{selected_student_name}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    # === Class-Wide Summary (Always shown) ===
    st.markdown("---")
    st.markdown("### 🏫 Class-Wide Performance")

    try:
        students_response = supabase.table("users").select("id, full_name, class").eq("role", "student").execute()
        students_df = pd.DataFrame(students_response.data)

        all_attempts = []
        for _, row in students_df.iterrows():
            sid = row['id']
            resp = supabase.table("quiz_attempts").select("*").eq("student_id", sid).execute()
            if resp.data:
                df_temp = pd.DataFrame(resp.data)
                df_temp['student_name'] = row['full_name']
                df_temp['class'] = row['class']
                all_attempts.append(df_temp)

        if all_attempts:
            all_df = pd.concat(all_attempts, ignore_index=True)
            all_df['attempted_at'] = pd.to_datetime(all_df['attempted_at'])

            try:
                with open("data/ncert_maths_dataset.json", "r", encoding="utf-8") as f:
                    questions = pd.DataFrame(json.load(f))
                    all_df = all_df.merge(questions[['id', 'chapter']], left_on='question_id', right_on='id', how='left')
            except Exception:
                all_df['chapter'] = "Unknown"

            class_perf = all_df.groupby('chapter').agg(
                avg_accuracy=('is_correct', 'mean'),
                total_questions=('is_correct', 'count')
            ).reset_index()
            class_perf['avg_accuracy'] = (class_perf['avg_accuracy'] * 100).round(1)

            fig3 = px.bar(class_perf, x='chapter', y='avg_accuracy',
                          color='avg_accuracy', color_continuous_scale=['red', 'yellow', 'green'],
                          title="Class Average Accuracy by Chapter",
                          labels={"avg_accuracy": "Avg Accuracy (%)"})
            st.plotly_chart(fig3, use_container_width=True)

            st.dataframe(
                class_perf.style.format({"avg_accuracy": "{}%"}).background_gradient(cmap='RdYlGn', subset=["avg_accuracy"]),
                use_container_width=True
            )

            # Download Class Report
            from utils.reports import generate_class_report
            st.markdown("#### 📥 Download Class Excel Report")
            if st.button("📥 Generate Class Excel Report"):
                class_xlsx = generate_class_report()
                if class_xlsx:
                    st.download_button(
                        label="⬇️ Download Class Report (XLSX)",
                        data=class_xlsx,
                        file_name=f"class_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        else:
            st.info("No class data available yet.")
    except Exception as e:
        st.error(f"Error fetching class data: {str(e)}")
