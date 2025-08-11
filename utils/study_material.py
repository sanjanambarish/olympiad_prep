import streamlit as st
import os
from supabase_client import supabase

# Class 10 Study Materials Mapping
# Format: {chapter_name: pdf_filename}
CLASS_10_STUDY_MATERIALS = {
    "Real Numbers": "real numbers 10th.pdf",
    "Polynomials": "Polynomials 10th.pdf",
    "Pair Of Linear Equations In Two Variables": "Pair Of Linear Equations In Two Variables 10th.pdf",
    "Quadratic Equations": "Quadratic Equations 10th.pdf",
    "Arithmetic Progressions": "Arithmetic Progressions 10th.pdf",
    "Introduction to Trigonometry": "Introduction to Trigonometry 10th.pdf",
    "Statistics": "Statistics 10th.pdf",
    "Probability": "Probability 10th.pdf"
}

# Class 9 Study Materials Mapping
CLASS_9_STUDY_MATERIALS = {
    "Number Systems": "Number Systems 9th.pdf",
    "Polynomials": "Polynomials 9th.pdf",
    "Coordinate Geometry": "Coordinate Geometry 9th.pdf",
    "Linear Equations in Two Variables": "Linear Equations in Two Variables 9th.pdf",
    "Introduction to Euclids Geometry": "Introduction to Euclids Geometry 9th.pdf",
    "Lines and Angles": "Lines and Angles 9th.pdf",
    "Triangles": "Triangles 9th.pdf",
    "Quadrilaterals": "Quadrilaterals 9th.pdf"
}

# Class 8 Study Materials Mapping
CLASS_8_STUDY_MATERIALS = {
    "Rational Numbers": "rational numbers 8th.pdf",
    "Linear Equations in One Variable": "Linear Equations in One Variable 8th.pdf",
    "Understanding Quadrilaterals": "Understanding Quadrilaterals 8th.pdf",
    "Practical Geometry": "Practical Geometry 8th.pdf",
    "Data Handling": "Data Handling 8th.pdf",
    "Squares and Square Roots": "Squares and Square Roots 8th.pdf",
    "Cube and Cube Roots": "Cube and Cube Roots 8th.pdf",
    "Comparing Quantities": "Comparing Quantities 8th.pdf",
    "Algebraic Expressions and Identities": "Algebraic Expressions and Identities 8th.pdf",
    "Visualizing Solid Shapes": "Visualizing Solid Shapes 8th.pdf",
    "Mensuration": "Mensuration 8th.pdf",
    "Exponents and Powers": "Exponents and Powers 8th.pdf",
    "Direct and Inverse Proportions": "Direct and Inverse Proportions 8th.pdf",
    "Factorisation": "Factorisation 8th.pdf",
    "Playing with Numbers": "Playing with Numbers 8th.pdf"
}

def get_study_materials_for_class(class_level):
    """Get study materials mapping for a specific class"""
    if class_level == 10:
        return CLASS_10_STUDY_MATERIALS
    elif class_level == 9:
        return CLASS_9_STUDY_MATERIALS
    elif class_level == 8:
        return CLASS_8_STUDY_MATERIALS
    else:
        return {}

def show_study_material(class_level, chapter):
    """Display study material PDF for a specific class and chapter"""
    materials = get_study_materials_for_class(class_level)
    
    if chapter in materials:
        pdf_filename = materials[chapter]
        pdf_path = os.path.join("data", pdf_filename)
        
        # Check if file exists
        if os.path.exists(pdf_path):
            # Display PDF using Streamlit's built-in PDF viewer
            with open(pdf_path, "rb") as file:
                st.subheader(f"📚 {chapter} - Study Material")
                st.caption(f"Class {class_level}")
                st.download_button(
                    label="📥 Download PDF",
                    data=file,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
                
                # Show PDF in Streamlit
                st.markdown("---")
                st.markdown("### Study Material Preview")
                st.caption("Note: Scroll down to see the full document")
                st.markdown("---")
                
                # Display PDF using Streamlit's PDF viewer
                st.markdown("---")
                st.markdown("### Full Document Viewer")
                st.caption("Use the download button above to save this material for offline study")
                st.markdown("---")
                
                # Reset file pointer to beginning
                file.seek(0)
                pdf_bytes = file.read()
                st.download_button(
                    label="📥 Download PDF (Alternative)",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    key="download_pdf_alt"
                )
                
                # Try to display PDF inline
                try:
                    import base64
                    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                except Exception as e:
                    st.warning("Unable to display PDF inline. Please use the download button to view the material.")
                    st.error(f"Error details: {str(e)}")
        else:
            st.error(f"Study material file not found: {pdf_filename}")
    else:
        st.info(f"No study material available for {chapter} yet. More materials coming soon!")

def show_study_material_dashboard():
    """Show a dashboard of all available study materials by class and chapter"""
    st.title("📚 Study Materials")
    st.info("Browse comprehensive study materials organized by class and chapter")
    
    # Class selection
    selected_class = st.selectbox("Select Class", [8, 9, 10], key="study_class_selector")
    
    materials = get_study_materials_for_class(selected_class)
    
    if materials:
        chapters = list(materials.keys())
        selected_chapter = st.selectbox("Select Chapter", chapters, key="study_chapter_selector")
        
        if selected_chapter:
            show_study_material(selected_class, selected_chapter)
    else:
        st.info("No study materials available for this class yet.")
