import streamlit as st

# NCERT Video Resources Database
# Format: {class: {chapter: {topic: youtube_url}}}
NCERT_VIDEO_RESOURCES = {
    8: {
        
       
        "Data Handling": {
            "Organizing Data": "https://www.youtube.com/watch?v=JmkL6HdAr0Y",
            "Grouping Data": "https://youtu.be/rK8eNsnF8H8?si=WjRD7vx551VYjxvG",
            "Circle Graph or Pie Chart": "https://youtu.be/icqiqHpt7AA?si=jgDNa2o3U2LprWmi",
            "Chance and Probability": "https://youtu.be/7aD6cVhUMfo?si=JZn-BnOsEw4nB7Nn"
        },
        "Mensuration": {
    "Area of Trapezium": "https://youtu.be/r6PGhrEleU8?si=6_78EIw7HYvcMPco",
    "Volume of Cube, Cuboid & Cylinder": "https://www.youtube.com/watch?v=XQntiGZydvE"
  },
        "Direct and Inverse Proportion": {
            "Direct Proportion & Inverse Proportion": "https://www.youtube.com/watch?v=4jZpJAiNBj4&t=2s",
            
        },
        "Exponents and Powers": {
            "Laws of Exponents": "https://youtu.be/1sQQJJ0PW7M?si=TWDna6J6D0tX8O6I",
            "Powers with Negative Exponents": "https://youtu.be/LhtqURYB1vU?si=AgKkyrGlG6RmIyIW"
        },
       "Playing with Numbers": {
    "Numbers in General Form": "https://youtu.be/ktrKsGnKHnc?si=QuWKyEpoZ8uqusC4",
    "Letters for Digits": "https://youtu.be/KUf1Yqhlmqw?si=Ir8iS7rVKYLbq1Tx"
  }
    },
    9: {
        "Number Systems": {
            "Irrational Numbers": "https://www.youtube.com/watch?v=3X7gcB7dR7U",
            "Real Numbers and their Decimal Expansions": "https://www.youtube.com/watch?v=5P9719u7NIM"
        },
        "Polynomials": {
            "Polynomials in One Variable": "https://www.youtube.com/watch?v=7rK3VgI7F8w",
            "Zeroes of a Polynomial": "https://www.youtube.com/watch?v=3X7gcB7dR7U"
        },
        "Coordinate Geometry": {
            "Cartesian System": "https://www.youtube.com/watch?v=5P9719u7NIM"
        }
    },
    10: {
        "Real Numbers": {
            "Euclid's Division Lemma": "https://www.youtube.com/watch?v=3X7gcB7dR7U",
            "The Fundamental Theorem of Arithmetic": "https://www.youtube.com/watch?v=7rK3VgI7F8w"
        },
        "Polynomials": {
            "Geometrical Meaning of Zeroes": "https://www.youtube.com/watch?v=5P9719u7NIM",
            "Relationship between Zeroes and Coefficients": "https://www.youtube.com/watch?v=3X7gcB7dR7U"
        }
    }
}

def get_video_resources(class_level, chapter):
    """Get available video resources for a specific class and chapter"""
    if class_level in NCERT_VIDEO_RESOURCES and chapter in NCERT_VIDEO_RESOURCES[class_level]:
        return NCERT_VIDEO_RESOURCES[class_level][chapter]
    return {}

def show_video_resources(class_level, chapter):
    """Display video resources in the Streamlit app"""
    videos = get_video_resources(class_level, chapter)
    
    if videos:
        st.subheader("📺 Learning Videos")
        st.info("Watch these NCERT videos to strengthen your understanding of this chapter")
        
        for topic, url in videos.items():
            st.markdown(f"**{topic}**")
            st.video(url)
            st.markdown("---")
    else:
        st.info("No video resources available for this chapter yet. More videos coming soon!")

def show_video_dashboard():
    """Show a dashboard of all available videos by class and chapter"""
    st.title("📺 Video Learning Resources")
    st.info("Browse NCERT Maths videos organized by class and chapter")
    
    # Class selection
    selected_class = st.selectbox("Select Class", [8, 9, 10], key="video_class_selector")
    
    if selected_class in NCERT_VIDEO_RESOURCES:
        chapters = list(NCERT_VIDEO_RESOURCES[selected_class].keys())
        selected_chapter = st.selectbox("Select Chapter", chapters, key="video_chapter_selector")
        
        if selected_chapter:
            show_video_resources(selected_class, selected_chapter)
    else:
        st.info("No video resources available for this class yet.")
