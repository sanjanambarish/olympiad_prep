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
      "Full Chapter Lecture": "https://www.youtube.com/watch?v=IMnSIaPcqiE",
      "Rational, Irrational & Real Numbers": "https://www.youtube.com/watch?v=4IQZ83iUBjI",
      "Rational and Irrational Numbers – Detailed Explanation": "https://www.youtube.com/watch?v=3KnwD1dolBo",
      "Plotting Irrational Numbers on the Number Line": "https://www.youtube.com/watch?v=aDKek9X4jC4",
      "Irrational Numbers – NCERT Chapter 1 Topic": "https://www.youtube.com/watch?v=vEhfXjVc3zE"
    },
    "Polynomials": {
      "Full Chapter Lecture": "https://www.youtube.com/watch?v=4VHrvMutJQw",
      "Introduction and Definitions": "https://www.youtube.com/watch?v=-nzUVj4zbIU",
      "Basic Concepts Explained in Detail": "https://www.youtube.com/watch?v=YnFHxA4aJAs",
      "Exercise 2.1 Solved Examples": "https://www.youtube.com/watch?v=BGLHDudXCdE"
    },
    "Coordinate Geometry": {
      "Full Chapter Playlist": "https://www.youtube.com/playlist?list=PLoHhdH7lwiIFYn_zP1_sTYhvWv3lc3Gmi",
      "Introduction to Coordinate Geometry": "https://www.youtube.com/watch?v=P-Wkq5QjBMs",
      "Plotting Points in a Plane (NCERT)": "https://www.youtube.com/watch?v=fkh6kJcZOMg"
    },
    "Linear Equations in Two Variables": {
      "Full Chapter Video": "https://www.youtube.com/watch?v=rnudiJxVXxM",
      "Concept Introduction": "https://www.youtube.com/watch?v=EtHj_WhP-NA",
      "Chapter Explained in Full Detail (NCERT Solutions)": "https://www.youtube.com/watch?v=azj5FA3w0xU",
      "Exercise 4.1 Solution Walkthrough": "https://www.youtube.com/watch?v=kEsalPdruDE"
    },
    "Introduction to Euclid’s Geometry": {
      "Full Chapter Video (One-Shot)": "https://www.youtube.com/watch?v=obHLST63Nrs"
    },
    "Lines and Angles": {
      "Full Chapter Lecture": "https://www.youtube.com/watch?v=pIEt9y3wXp8",
      "Types of Angle Pairs": "https://www.youtube.com/watch?v=hMYV-Pp3Li0"
    },
    "Triangles": {
      "Full Chapter Video": "https://www.youtube.com/watch?v=wIeiqvdVCJI",
      "Comprehensive One‑Shot Chapter": "https://www.youtube.com/watch?v=vc_AR7guu8E",
      "Detailed Explanation with NCERT Solutions and MCQs": "https://www.youtube.com/watch?v=ddQODZ28pjM"
    },
    "Quadrilaterals": {
      "Full Chapter Video (One-Shot)": "https://www.youtube.com/watch?v=Y8mfN42SJ6k"
    }
  },
  10: {
    "Real Numbers": {
      "Full Chapter": "https://www.youtube.com/watch?v=-UdHmSTmQtw"
    },
    "Polynomials": {
      "Full Chapter": "https://www.youtube.com/watch?v=Us2I1wAfs7g"
    },
    "Triangles": {
      "Full Chapter": "https://www.youtube.com/watch?v=4zsA9r2euAc"
    },
    "Quadratic Equations": {
      "Full Chapter": "https://www.youtube.com/watch?v=GtKXeWrZeuk"
    },
    "Arithmetic Progressions": {
      "Full Chapter": "https://www.youtube.com/watch?v=NUsxSiOpW54"
    },
    "Pair of Linear Equations in Two Variables": {
      "Full Chapter": "https://www.youtube.com/watch?v=p_yr53bhesU"
    },
    "Probability": {
      "Chapter 14 – Probability": "https://www.youtube.com/watch?v=OE9TXeMCqKs",
      "Alternate for Probability": "https://www.youtube.com/watch?v=NX2qmFZwb4I"
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
