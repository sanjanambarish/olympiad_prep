import streamlit as st
import pandas as pd
from supabase_client import supabase
import json
from datetime import datetime
import xlsxwriter
from io import BytesIO


def generate_student_report(student_id, student_name):
    """Generate XLSX report for a single student"""
    try:
        response = supabase.table("quiz_attempts") \
            .select("*") \
            .eq("student_id", student_id) \
            .execute()

        if not response.data or len(response.data) == 0:
            st.warning("No quiz data to export.")
            return None

        df = pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

    try:
        with open("data/ncert_maths_dataset.json", "r", encoding="utf-8") as f:
            questions = pd.DataFrame(json.load(f))
        questions = questions[['id', 'chapter', 'topic', 'difficulty', 'question_text']]
        df = df.merge(questions, left_on='question_id', right_on='id', how='left')
    except Exception:
        df['chapter'] = "Unknown"
        df['topic'] = "Unknown"
        df['difficulty'] = "Unknown"
        df['question_text'] = "Question text not available"

    df['attempted_at'] = pd.to_datetime(df['attempted_at'])
    df['is_correct'] = df['is_correct'].map({True: '✅ Correct', False: '❌ Incorrect'})

    report_df = df[[
        'attempted_at', 'chapter', 'topic', 'difficulty',
        'question_text', 'selected_answer', 'is_correct', 'time_taken_seconds'
    ]].copy()

    report_df.columns = [
        'Attempted At', 'Chapter', 'Topic', 'Difficulty',
        'Question', 'Your Answer', 'Correctness', 'Time (s)'
    ]

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book

        header_format = workbook.add_format({
            'bold': True, 'bg_color': '#D7E4BC', 'border': 1, 'align': 'center'
        })
        correct_format = workbook.add_format({'bg_color': '#C6EFCE', 'border': 1})
        incorrect_format = workbook.add_format({'bg_color': '#FFC7CE', 'border': 1})
        text_wrap = workbook.add_format({'text_wrap': True})

        report_df.to_excel(writer, sheet_name='Quiz History', index=False)
        worksheet = writer.sheets['Quiz History']

        for col_num, value in enumerate(report_df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 18)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 12)
        worksheet.set_column('E:E', 50, text_wrap)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 15)
        worksheet.set_column('H:H', 10)

        worksheet.conditional_format('G2:G1000', {
            'type': 'text', 'criteria': 'containing',
            'value': 'Correct', 'format': correct_format
        })
        worksheet.conditional_format('G2:G1000', {
            'type': 'text', 'criteria': 'containing',
            'value': 'Incorrect', 'format': incorrect_format
        })

    output.seek(0)
    return output


def generate_class_report():
    """Generate class-wide XLSX report"""
    try:
        users_resp = supabase.table("users").select("*").eq("role", "student").execute()
        if not users_resp.data or len(users_resp.data) == 0:
            st.warning("No students found.")
            return None

        students_df = pd.DataFrame(users_resp.data)
        attempts_list = []

        for _, row in students_df.iterrows():
            resp = supabase.table("quiz_attempts").select("*").eq("student_id", row['id']).execute()
            if resp.data and len(resp.data) > 0:
                df_temp = pd.DataFrame(resp.data)
                df_temp['student_name'] = row['full_name']
                df_temp['class'] = row.get('class', 'N/A')
                attempts_list.append(df_temp)

        if not attempts_list:
            st.warning("No quiz attempts yet.")
            return None

        all_attempts = pd.concat(attempts_list, ignore_index=True)

        try:
            with open("data/ncert_maths_dataset.json", "r", encoding="utf-8") as f:
                questions = pd.DataFrame(json.load(f))
            questions = questions[['id', 'chapter']]
            all_attempts = all_attempts.merge(questions, left_on='question_id', right_on='id', how='left')
        except Exception:
            all_attempts['chapter'] = "Unknown"

        # Ensure 'is_correct' is boolean
        all_attempts['is_correct'] = all_attempts['is_correct'].astype(bool)

        student_summary = all_attempts.groupby(['student_name', 'class']).agg(
            total_questions=('is_correct', 'count'),
            correct=('is_correct', 'sum')
        ).reset_index()
        student_summary['accuracy'] = ((student_summary['correct'] / student_summary['total_questions']) * 100).round(1)
        student_summary = student_summary.sort_values('accuracy', ascending=False)

        chapter_summary = all_attempts.groupby('chapter').agg(
            avg_accuracy=('is_correct', 'mean'),
            total_questions=('is_correct', 'count')
        ).reset_index()
        chapter_summary['avg_accuracy'] = (chapter_summary['avg_accuracy'] * 100).round(1)
        chapter_summary = chapter_summary.sort_values('avg_accuracy')

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            header_format = workbook.add_format({'bold': True, 'bg_color': '#4472C4', 'font_color': 'white', 'border': 1})

            student_summary.to_excel(writer, sheet_name='Student Summary', index=False)
            worksheet1 = writer.sheets['Student Summary']
            for col_num, value in enumerate(student_summary.columns.values):
                worksheet1.write(0, col_num, value, header_format)
            worksheet1.set_column('A:B', 18)
            worksheet1.set_column('C:E', 15)

            chapter_summary.to_excel(writer, sheet_name='Chapter Insights', index=False)
            worksheet2 = writer.sheets['Chapter Insights']
            for col_num, value in enumerate(chapter_summary.columns.values):
                worksheet2.write(0, col_num, value, header_format)
            worksheet2.set_column('A:A', 25)
            worksheet2.set_column('B:C', 15)

        output.seek(0)
        return output

    except Exception as e:
        st.error(f"Error generating class report: {str(e)}")
        return None
