import streamlit as st
from supabase_client import supabase
import pandas as pd
from datetime import datetime
import mimetypes

def student_doubt_box(student_id):
    st.subheader("❓ Ask a Doubt")
    
    with st.form("doubt_form"):
        doubt_text = st.text_area("Describe your doubt", height=150)
        # File upload (optional) - supports images and documents
        uploaded_file = st.file_uploader("Attach a file (optional) - Images, PDFs, Docs supported", type=["png", "jpg", "jpeg", "pdf", "doc", "docx"])
        submitted = st.form_submit_button("Submit Doubt")
        
        if submitted:
            if not doubt_text.strip():
                st.error("Please enter your doubt.")
            else:
                try:
                    # Upload file if provided
                    file_url = None
                    if uploaded_file:
                        try:
                            file_extension = uploaded_file.name.split('.')[-1]
                            file_name = f"doubt_{student_id}_{int(datetime.now().timestamp())}.{file_extension}"
                            content_type = mimetypes.guess_type(uploaded_file.name)[0] or "application/octet-stream"
                            
                            # Read file content into bytes to avoid stream issues
                            file_content = uploaded_file.read()
                            
                            # Upload to Supabase Storage
                            # Check if 'doubts' bucket exists
                            try:
                                buckets = supabase.storage.list_buckets()
                                doubt_bucket = next((b for b in buckets if b.name == "doubts"), None)
                                if not doubt_bucket:
                                    st.warning("Storage bucket 'doubts' not found.")
                                    st.info("Please follow these steps to create the bucket in your Supabase dashboard:")
                                    st.markdown("""
                                    1. Go to Storage → Buckets in your Supabase dashboard
                                    2. Click "New Bucket" and name it `doubts`
                                    3. Enable public access for the bucket
                                    4. Set up appropriate policies for authenticated users to insert files
                                    """)
                                    st.info("The doubt will be submitted without the file.")
                                else:
                                    # Try to upload the file
                                    try:
                                        supabase.storage.from_("doubts").upload(file_name, file_content, {"content-type": content_type})
                                        # Get public URL
                                        file_url_resp = supabase.storage.from_("doubts").get_public_url(file_name)
                                        file_url = file_url_resp.get('publicUrl') or file_url_resp.get('public_url') or file_url_resp  # fallback
                                    except Exception as upload_error:
                                        st.warning(f"File upload failed: {str(upload_error)}")
                                        st.info("Please check the following in your Supabase dashboard:")
                                        st.markdown("""
                                        1. Go to Storage → Configuration → Policies
                                        2. Ensure authenticated users can insert files
                                        3. Check that the 'doubts' bucket has public read access
                                        4. Verify that your Supabase key has sufficient permissions (service role key recommended)
                                        """)
                                        # Add more detailed error information
                                        st.info(f"Debug info: file_name={file_name}, content_type={content_type}, content_length={len(file_content) if 'file_content' in locals() else 'unknown'}")
                                        st.info("The doubt will be submitted without the file.")
                            except Exception as bucket_check_error:
                                # Fallback method if list_buckets is not available
                                try:
                                    supabase.storage.from_("doubts").list()
                                    # If we get here, bucket exists, try upload
                                    try:
                                        supabase.storage.from_("doubts").upload(file_name, file_content, {"content-type": content_type})
                                        file_url_resp = supabase.storage.from_("doubts").get_public_url(file_name)
                                        file_url = file_url_resp.get('publicUrl') or file_url_resp.get('public_url') or file_url_resp
                                    except Exception as fallback_upload_error:
                                        st.warning(f"File upload failed: {str(fallback_upload_error)}")
                                        st.info("Please check the following in your Supabase dashboard:")
                                        st.markdown("""
                                        1. Go to Storage → Configuration → Policies
                                        2. Ensure authenticated users can insert files
                                        3. Check that the 'doubts' bucket has public read access
                                        4. Verify that your Supabase key has sufficient permissions (service role key recommended)
                                        """)
                                        # Add more detailed error information
                                        st.info(f"Debug info: file_name={file_name}, content_type={content_type}, content_length={len(file_content) if 'file_content' in locals() else 'unknown'}")
                                        st.info("The doubt will be submitted without the file.")
                                except Exception:
                                    st.warning("Could not verify storage bucket. The doubt will be submitted without the file.")
                        except Exception as e:
                            st.warning(f"File processing failed: {str(e)}")
                            st.info("The doubt will be submitted without the file.")
                    
                    # Insert doubt into database
                    doubt_data = {
                        "student_id": str(student_id),
                        "question_text": doubt_text,
                        "image_url": file_url,  # Using the same field for both images and documents
                        "status": "pending"
                    }
                    
                    result = supabase.table("doubts").insert(doubt_data).execute()
                    st.success("✅ Doubt submitted successfully!")
                    st.rerun()
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
                    # Check if it's an image or document
                    if row['image_url'].lower().endswith(('.png', '.jpg', '.jpeg')):
                        st.image(row['image_url'], caption="Attached Image")
                    else:
                        st.markdown(f"[📎 Download Attachment]({row['image_url']})")
                
                # Fetch response
                resp = supabase.table("doubt_responses").select("*").eq("doubt_id", row['id']).execute()
                if resp.data and len(resp.data) > 0:
                    response_row = resp.data[0]
                    st.markdown(f"**Teacher Response:** {response_row['response_text']}")
                    if response_row.get('response_image_url'):
                        # Check if it's an image or document
                        if response_row['response_image_url'].lower().endswith(('.png', '.jpg', '.jpeg')):
                            st.image(response_row['response_image_url'], caption="Teacher's Diagram/Attachment")
                        else:
                            st.markdown(f"[📎 Download Teacher's Attachment]({response_row['response_image_url']})")
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
                    # Check if it's an image or document
                    if row['image_url'].lower().endswith(('.png', '.jpg', '.jpeg')):
                        st.image(row['image_url'], caption="Student's Diagram/Attachment")
                    else:
                        st.markdown(f"[📎 Download Student's Attachment]({row['image_url']})")
                
                # Reply form
                with st.form(f"reply_form_{row['id']}"):
                    reply_text = st.text_area("Your Response", key=f"reply_text_{row['id']}")
                    reply_file = st.file_uploader("Attach explanation file (optional) - Images, PDFs, Docs supported", type=["png", "jpg", "jpeg", "pdf", "doc", "docx"], key=f"img_{row['id']}")
                    submitted = st.form_submit_button("Send Response")
                    
                    if submitted:
                        if not reply_text.strip() and not reply_file:
                            st.error("Please provide a text response or file.")
                        else:
                            try:
                                # Upload file
                                file_url = None
                                if reply_file:
                                    try:
                                        file_extension = reply_file.name.split('.')[-1]
                                        file_name = f"reply_{row['id']}_{int(datetime.now().timestamp())}.{file_extension}"
                                        content_type = mimetypes.guess_type(reply_file.name)[0] or "application/octet-stream"
                                        
                                        # Read file content into bytes to avoid stream issues
                                        file_content = reply_file.read()
                                        
                                        # Check if 'doubts' bucket exists
                                        try:
                                            buckets = supabase.storage.list_buckets()
                                            doubt_bucket = next((b for b in buckets if b.name == "doubts"), None)
                                            if not doubt_bucket:
                                                st.warning("Storage bucket 'doubts' not found.")
                                                st.info("Please follow these steps to create the bucket in your Supabase dashboard:")
                                                st.markdown("""
                                                1. Go to Storage → Buckets in your Supabase dashboard
                                                2. Click "New Bucket" and name it `doubts`
                                                3. Enable public access for the bucket
                                                4. Set up appropriate policies for authenticated users to insert files
                                                """)
                                            else:
                                                # Try to upload the file
                                                try:
                                                    supabase.storage.from_("doubts").upload(file_name, file_content, {"content-type": content_type})
                                                    file_url_resp = supabase.storage.from_("doubts").get_public_url(file_name)
                                                    file_url = file_url_resp.get('publicUrl') or file_url_resp.get('public_url') or file_url_resp
                                                except Exception as upload_error:
                                                    st.warning(f"File upload failed: {str(upload_error)}")
                                                    st.info("Please check the following in your Supabase dashboard:")
                                                    st.markdown("""
                                                    1. Go to Storage → Configuration → Policies
                                                    2. Ensure authenticated users can insert files
                                                    3. Check that the 'doubts' bucket has public read access
                                                    4. Verify that your Supabase key has sufficient permissions (service role key recommended)
                                                    """)
                                                    # Add more detailed error information
                                                    st.info(f"Debug info: file_name={file_name}, content_type={content_type}, content_length={len(file_content) if 'file_content' in locals() else 'unknown'}")
                                                    st.info("The response will be submitted without the file.")
                                        except Exception as bucket_check_error:
                                            # Fallback method if list_buckets is not available
                                            try:
                                                supabase.storage.from_("doubts").list()
                                                # If we get here, bucket exists, try upload
                                                try:
                                                    supabase.storage.from_("doubts").upload(file_name, file_content, {"content-type": content_type})
                                                    file_url_resp = supabase.storage.from_("doubts").get_public_url(file_name)
                                                    file_url = file_url_resp.get('publicUrl') or file_url_resp.get('public_url') or file_url_resp
                                                except Exception as fallback_upload_error:
                                                    st.warning(f"File upload failed: {str(fallback_upload_error)}")
                                                    st.info("Please check the following in your Supabase dashboard:")
                                                    st.markdown("""
                                                    1. Go to Storage → Configuration → Policies
                                                    2. Ensure authenticated users can insert files
                                                    3. Check that the 'doubts' bucket has public read access
                                                    4. Verify that your Supabase key has sufficient permissions (service role key recommended)
                                                    """)
                                                    # Add more detailed error information
                                                    st.info(f"Debug info: file_name={file_name}, content_type={content_type}, content_length={len(file_content) if 'file_content' in locals() else 'unknown'}")
                                                    st.info(f"Error details: {fallback_upload_error.__class__.__name__}, {fallback_upload_error.__traceback__}")
                                                    st.info("The response will be submitted without the file.")
                                            except Exception:
                                                st.warning("Could not verify storage bucket. The response will be submitted without the file.")
                                    except Exception as e:
                                        st.warning(f"File processing failed: {str(e)}")
                                        st.info("The response will be submitted without the file.")
                                
                                # Insert response
                                supabase.table("doubt_responses").insert({
                                    "doubt_id": row['id'],
                                    "teacher_id": str(teacher_id),
                                    "response_text": reply_text,
                                    "response_image_url": file_url
                                }).execute()
                                
                                # Update doubt status
                                supabase.table("doubts").update({"status": "answered"}).eq("id", row['id']).execute()
                                
                                st.success("✅ Response sent!")
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"Failed to send response: {str(e)}")
    except Exception as e:
        st.error(f"Error fetching doubts: {str(e)}")
