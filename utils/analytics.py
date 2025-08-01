import pandas as pd
import plotly.express as px
import streamlit as st
from supabase_client import supabase
import json
def get_student_attempts(student_id):
    """Fetch all quiz attempts from Supabase"""
    try:
        response = supabase.table("quiz_attempts").select("*").eq("student_id", student_id).execute()
        if response.data:
            return pd.DataFrame(response.data)
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching attempts: {str(e)}")
        return pd.DataFrame()

def show_student_analytics(student_id):
    """Display analytics dashboard for student"""
    st.title("📈 Your Performance Dashboard")

    df = get_student_attempts(student_id)

    if df.empty:
        st.info("No quiz attempts yet. Complete a quiz to see your progress!")
        return

    # Clean & Prepare
    df['attempted_at'] = pd.to_datetime(df['attempted_at'])
    df['date'] = df['attempted_at'].dt.date
    df['hour'] = df['attempted_at'].dt.hour

    # === 1. Overall Stats ===
    total = len(df)
    correct = df['is_correct'].sum()
    accuracy = int((correct / total) * 100)
    avg_time = int(df['time_taken_seconds'].mean())

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Questions", total)
    col2.metric("Accuracy", f"{accuracy}%")
    col3.metric("Avg Time per Q", f"{avg_time}s")
    col4.metric("Quizzes Completed", df['quiz_session_id'].nunique())

    st.markdown("---")

    # === 2. Accuracy Over Time ===
    st.subheader("🎯 Accuracy Over Time")
    # Ensure datetime
    df['attempted_at'] = pd.to_datetime(df['attempted_at'])
    # Group by HOUR (for same-day practice)
    df['hour'] = df['attempted_at'].dt.floor('H')  # Round to nearest hour
    hourly = df.groupby('hour')['is_correct'].agg(['mean', 'count']).reset_index()
    hourly['mean'] = (hourly['mean'] * 100).round(1)
    hourly.rename(columns={'mean': 'accuracy'}, inplace=True)
    if len(hourly) == 0:
      st.info("No quiz attempts yet.")
    elif len(hourly) == 1:
        # Only one session — show as dot
        st.info(f"🎯 One quiz completed: {hourly['accuracy'][0]}% accuracy")
        fig = px.scatter(hourly, x='hour', y='accuracy',title="Quiz Performance", 
                     labels={"accuracy": "Accuracy (%)"})
        st.plotly_chart(fig, use_container_width=True)
    else:
    # Multiple sessions — show line
        fig = px.line(hourly, x='hour', y='accuracy',
                  title="Accuracy Trend (By Hour)",
                  labels={"accuracy": "Accuracy (%)", "hour": "Time"},
                  markers=True)
        st.plotly_chart(fig, use_container_width=True)                  
    # === 3. Performance by Chapter ===
    st.subheader("📚 Performance by Chapter")

    # We need chapter info → merge with question dataset
    try:
        with open("data/ncert_maths_dataset.json", "r", encoding="utf-8") as f:
            questions = pd.DataFrame(json.load(f))
        questions = questions[['id', 'chapter', 'topic', 'difficulty']]
        df_merged = df.merge(questions, left_on='question_id', right_on='id', how='left')
    except Exception:
        st.warning("Chapter details not available")
        df_merged = df
        df_merged['chapter'] = "Unknown"

    chapter_perf = df_merged.groupby('chapter').agg(
        correct=('is_correct', 'sum'),
        total=('is_correct', 'count')
    ).reset_index()
    chapter_perf['accuracy'] = (chapter_perf['correct'] / chapter_perf['total'] * 100).round(1)

    fig2 = px.bar(chapter_perf, x='chapter', y='accuracy',
                  color='accuracy',
                  color_continuous_scale=['red', 'yellow', 'green'],
                  title="Accuracy by Chapter",
                  labels={"accuracy": "Accuracy (%)"})
    st.plotly_chart(fig2, use_container_width=True)

    # Show table
    st.dataframe(
        chapter_perf.style.format({"accuracy": "{}%"}).background_gradient(cmap='RdYlGn', subset=["accuracy"]),
        use_container_width=True
    )

    st.markdown("---")

    # === 4. Time vs Accuracy (Enhanced) ===
    st.subheader("⏱️ Time vs Accuracy")

    # 1. Bar Chart: Average Time per Question Type
    st.markdown("#### Average Time per Question Type")
    df_grouped = df_merged.groupby('is_correct').agg(
        avg_time=('time_taken_seconds', 'mean')
    ).reset_index()
    df_grouped['is_correct'] = df_grouped['is_correct'].map({True: "✅ Correct", False: "❌ Incorrect"})

    fig_bar = px.bar(df_grouped, x='is_correct', y='avg_time',
                     color='is_correct',
                     color_discrete_map={"✅ Correct": "green", "❌ Incorrect": "red"},
                     title="Average Time per Question Type",
                     labels={"is_correct": "Answer", "avg_time": "Average Time (s)"},
                     text='avg_time')
    fig_bar.update_traces(texttemplate='%{text:.1f}s', textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

    # 2. Pie Chart: Correct vs. Incorrect
    st.markdown("#### Correct vs. Incorrect Answers")
    pie_data = df['is_correct'].value_counts().reset_index()
    pie_data.columns = ['Correctness', 'Count']
    pie_data['Correctness'] = pie_data['Correctness'].map({True: "✅ Correct", False: "❌ Incorrect"})

    fig_pie = px.pie(pie_data, values='Count', names='Correctness',
                     title="Percentage of Correct vs. Incorrect Answers",
                     color='Correctness',
                     color_discrete_map={"✅ Correct": "green", "❌ Incorrect": "red"})
    st.plotly_chart(fig_pie, use_container_width=True)

    # 3. Histogram: Time Distribution
    st.markdown("#### Time Distribution per Question")
    fig_hist = px.histogram(df, x='time_taken_seconds',
                           nbins=15,
                           title="Distribution of Time Taken per Question",
                           labels={"time_taken_seconds": "Time (seconds)"},
                           color_discrete_sequence=["#636EFA"])
    fig_hist.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # === 5. Weak Areas ===
    st.subheader("🔍 Suggested Improvements")
    weak = chapter_perf[chapter_perf['accuracy'] < 70]
    if len(weak) == 0:
        st.success("🎉 Great job! You're strong in all areas.")
    else:
        st.warning("You may want to revise these chapters:")
        for _, row in weak.iterrows():
            st.markdown(f"- **{row['chapter']}**: {row['accuracy']}% accuracy")
