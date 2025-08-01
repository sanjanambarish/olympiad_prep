import streamlit as st
from supabase_client import supabase
import pandas as pd
from datetime import datetime
import mimetypes

def student_doubt_box(student_id):
    st.subheader("❓ Ask a Doubt")
    
    with st.form("doubt_form"):
        doubt_text = st.text_area("Describe your doubt", height=150)
        # Image upload (optional)
        uploaded_image = st.file_uploader("Attach a screenshot (optional)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Submit Doubt")
        
        if submitted:
            if not doubt_text.strip():
                st.error("Please enter your doubt.")
            else:
                try:
                    # Upload image if provided
                    image_url = None
                    if uploaded_image:
                        file_extension = uploaded_image.name.split('.')[-1]
                        file_name = f"doubt_{student_id}_{int(datetime.now().timestamp())}.{file_extension}"
                        content_type = mimetypes.guess_type(uploaded_image.name)[0] or "image/jpeg"
                        # Upload to Supabase Storage (you need to create 'doubts' bucket)
                        try:
                            supabase.storage.from_("doubts").upload(file_name, uploaded_image, {"content-type": content_type})
                            # supabase.storage.from_().get_public_url returns dict with 'publicUrl' key (depending on SDK)
                            image_url_resp = supabase.storage.from_("doubts").get_public_url(file_name)
                            image_url = image_url_resp.get('publicUrl') or image_url_resp.get('public_url') or image_url_resp  # fallback
                        except Exception as e:
                            st.warning("Image upload failed, but doubt was submitted.")
                    
                    # Insert doubt
                    supabase.table("doubts").insert({
                        "student_id": str(student_id),
                        "question_text": doubt_text,
                        "image_url": image_url,
                        "status": "pending"
                    }).execute()
                    
                    st.success("✅ Your doubt has been submitted! A teacher will respond soon.")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Failed to submit doubt: {str(e)}")

    # Show past doubts
    st.markdown("---")
    st.subheader("📬 Your Doubt History")
    
    try:
        # Fetch doubts
        response = supabase.table("doubts").select("*").eq("student_id", student_id).order("created_at", desc=True).execute()
        if not response.data or len(response.data) == 0:
            st.info("No doubts posted yet.")
            return
        
        doubts_df = pd.DataFrame(response.data)
        doubts_df['created_at'] = pd.to_datetime(doubts_df['created_at']).dt.strftime('%b %d, %H:%M')
        
        for _, row in doubts_df.iterrows():
            with st.expander(f"🗨️ {row['question_text'][:50]}... ({row['status'].title()})"):
                st.markdown(f"**Asked on:** {row['created_at']}")
                st.markdown(f"**Your doubt:** {row['question_text']}")
                
                if row['image_url']:
                    st.image(row['image_url'], caption="Attached Image")
                
                # Fetch response
                resp = supabase.table("doubt_responses").select("*").eq("doubt_id", row['id']).execute()
                if resp.data and len(resp.data) > 0:
                    response_row = resp.data[0]
                    st.markdown(f"**Teacher Response:** {response_row['response_text']}")
                    if response_row.get('response_image_url'):
                        st.image(response_row['response_image_url'], caption="Teacher's Diagram")
                else:
                    st.info("Waiting for teacher response...")
    except Exception as e:
        st.error(f"Error loading doubts: {str(e)}")


def teacher_doubt_box(teacher_id):
    st.subheader("📬 Doubt Box: Student Queries")

    # Fetch all pending doubts
    try:
        doubts_resp = supabase.table("doubts") \
            .select("*, student:student_id(full_name, email)") \
            .eq("status", "pending") \
            .order("created_at", desc=True) \
            .execute()
        
        if not doubts_resp.data or len(doubts_resp.data) == 0:
            st.info("No pending doubts.")
            return
        
        doubts_df = pd.DataFrame(doubts_resp.data)
        
        for _, row in doubts_df.iterrows():
            with st.expander(f"🧑‍🎓 {row['student']['full_name']}: {row['question_text'][:40]}..."):
                st.markdown(f"**From:** {row['student']['full_name']} (Class {row.get('class', 'N/A')})")
                st.markdown(f"**Question:** {row['question_text']}")
                if row['image_url']:
                    st.image(row['image_url'], caption="Student's Diagram")
                
                # Reply form
                with st.form(f"reply_form_{row['id']}"):
                    reply_text = st.text_area("Your Response", key=f"reply_text_{row['id']}")
                    reply_image = st.file_uploader("Attach explanation image (optional)", type=["png", "jpg", "jpeg"], key=f"img_{row['id']}")
                    submitted = st.form_submit_button("Send Response")
                    
                    if submitted:
                        if not reply_text.strip() and not reply_image:
                            st.error("Please provide a text response or image.")
                        else:
                            try:
                                # Upload image
                                image_url = None
                                if reply_image:
                                    file_extension = reply_image.name.split('.')[-1]
                                    file_name = f"reply_{row['id']}_{int(datetime.now().timestamp())}.{file_extension}"
                                    content_type = mimetypes.guess_type(reply_image.name)[0] or "image/jpeg"
                                    supabase.storage.from_("doubts").upload(file_name, reply_image, {"content-type": content_type})
                                    image_url_resp = supabase.storage.from_("doubts").get_public_url(file_name)
                                    image_url = image_url_resp.get('publicUrl') or image_url_resp.get('public_url') or image_url_resp
                                
                                # Insert response
                                supabase.table("doubt_responses").insert({
                                    "doubt_id": row['id'],
                                    "teacher_id": str(teacher_id),
                                    "response_text": reply_text,
                                    "response_image_url": image_url
                                }).execute()
                                
                                # Update doubt status
                                supabase.table("doubts").update({"status": "answered"}).eq("id", row['id']).execute()
                                
                                st.success("✅ Response sent!")
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"Failed to send response: {str(e)}")
    except Exception as e:
        st.error(f"Error fetching doubts: {str(e)}")
