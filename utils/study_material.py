import streamlit as st

def show_data_handling_material():
    """Display study material for Data Handling - Class 8"""
    st.title("📚 Data Handling - Class 8 Study Material")
    
    st.markdown("""
    ## 1. What is Data?
    Data is a collection of facts or information. Examples include marks of students, daily temperatures, or number of people in different age groups.
    
    ## 2. Organizing Data
    Instead of writing random numbers, we organize them using:
    - Tables
    - Tally Marks
    - Pictographs
    - Bar Graphs
    
    ## 3. Tally Marks
    Tally marks help quickly count data in groups of 5.
    
    **Example:**
    
    | Fruit | Tally | Frequency |
    |-------|-------|-----------|
    | Apple | |||| | 4 |
    | Banana | |||| || | 7 |
    | Orange | |||| |||| | 9 |
    
    ## 4. Pictograph
    A pictograph uses pictures to show data. 
    
    **Example:** 🍎 = 2 apples. So 🍎🍎🍎 = 6 apples.
    
    ## 5. Bar Graph
    A bar graph uses bars (rectangles) to show data. Each bar's height represents the value.
    
    ## 6. Histogram (Advanced)
    A histogram is like a bar graph but used for continuous data such as marks or heights.
    
    ## 7. Circle Graph (Pie Chart)
    A circle graph is divided into sectors. Each sector represents a part of the whole.
    
    ## 8. Measures of Central Tendency
    These are used to find the average or middle value.
    
    - **Mean (Average):** Sum of values ÷ Number of values
      *Example: 10, 15, 20 → Mean = (10+15+20)/3 = 15*
      
    - **Median:** Middle value when data is arranged in order.
      *Example: 10, 15, 20 → Median = 15*
      *If even number of values: 10, 20, 30, 40 → Median = (20+30)/2 = 25*
      
    - **Mode:** Value that appears most often.
      *Example: 10, 15, 15, 20 → Mode = 15*
    
    ## 9. Probability (Introduction)
    Probability tells how likely something is to happen.
    
    *Example: Tossing a coin → Chance of Heads = 1/2*
    
    **Formula:** Probability = Favourable Outcomes / Total Outcomes
    
    *Example: Dice roll → Probability of 3 = 1/6*
    
    ## 10. Summary Table
    
    | Concept | Meaning |
    |---------|---------|
    | Data | Information in numbers |
    | Tally Marks | Counting in 5s |
    | Pictograph | Data using pictures |
    | Bar Graph | Bars for comparison |
    | Mean | Average |
    | Median | Middle value |
    | Mode | Most frequent number |
    | Probability | Likelihood of an event |
    
    ## 11. Example Questions
    
    1. Find the mean of 12, 15, 10, 13 → (12+15+10+13)/4 = 12.5
    2. Find the mode of 5, 7, 7, 8, 9 → Mode = 7
    3. Median of 2, 4, 6, 8 → (4+6)/2 = 5
    4. Probability of red ball from 3 red, 2 blue → 3/5
    """)

def show_mensuration_material():
    """Display study material for Mensuration - Class 8"""
    st.title("📐 Mensuration - Class 8 Study Material")
    
    st.markdown("""
    ## Chapter 11: Mensuration
    Based on NCERT Curriculum
    
    🔷 1. Introduction
    Mensuration is the branch of mathematics that deals with measurement of shapes and objects, including their lengths, areas, and volumes. It is used in real life for tasks such as finding the area of land, volume of containers, and surface area of objects.
    
    This chapter focuses on:
    
    - Area of trapezium, general quadrilateral, and polygons
    
    - Surface area and volume of cuboid and cube
    
    - Unit conversions for area and volume
    
    🔷 2. Area of Plane Figures
    📌 2.1 Trapezium
    A trapezium has one pair of parallel sides.
    
    Formula:
    Area = 1/2 × (a + b) × h
    where:
    a and b = lengths of the parallel sides
    h = height (distance between them)
    
    📌 2.2 General Quadrilateral
    Any quadrilateral can be divided into two triangles.
    
    Formula:
    Area = 1/2 × diagonal × (height1 + height2)
    
    📌 2.3 Polygons
    Polygons like pentagons and hexagons can be broken into triangles or trapeziums. Find the area of each part and add them to get total area.
    
    🔷 3. Surface Area of Solids
    🧱 3.1 Cuboid
    Lateral Surface Area = 2 × (length + breadth) × height
    
    Total Surface Area = 2 × (length × breadth + breadth × height + height × length)
    
    🧊 3.2 Cube
    Lateral Surface Area = 4 × side²
    
    Total Surface Area = 6 × side²
    
    🔷 4. Volume of Solids
    🧱 4.1 Cuboid
    Volume = length × breadth × height
    
    🧊 4.2 Cube
    Volume = side × side × side (side³)
    
    🔷 5. Units and Conversions
    
    | Quantity | Units | Conversion |
    |----------|-------|------------|
    | Length | cm, m | 1 m = 100 cm |
    | Area | cm², m² | 1 m² = 10,000 cm² |
    | Volume | cm³, m³ | 1 m³ = 1,000,000 cm³ |
    
    🔷 6. Real-Life Applications
    - Estimating floor area of rooms
    
    - Finding volume of water tanks
    
    - Measuring paint needed for walls
    
    - Designing tiles or garden plots
    
    🔷 7. Solved Example
    Q: Find the area of a trapezium with parallel sides 10 cm and 6 cm, and height 5 cm.
    
    Solution:
    Area = 1/2 × (10 + 6) × 5 = 1/2 × 16 × 5 = 40 cm²
    
    🔷 8. Tips for Practice
    - Learn and revise all formulas regularly
    
    - Convert units to the same system before solving
    
    - Understand the difference between area and volume
    
    - Solve all NCERT examples and exercises
    
    📌 Conclusion
    Mensuration helps in solving many practical problems in daily life. With a good understanding of formulas and practice, students can master this topic easily.
    """)
