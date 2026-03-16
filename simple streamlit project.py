import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Set page configuration for a premium look
st.set_page_config(
    page_title="ZenFit | Wellness Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a premium, glassmorphic feel
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1e1e2f 0%, #121212 100%);
        color: #ffffff;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease;
    }
    .stMetric:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
    }
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        color: #00d4ff;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff 0%, #0083fe 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/bubbles/200/natural-food.png", width=150)
    st.title("Settings")
    name = st.text_input("Profile Name", value="Alex")
    goal_steps = st.slider("Daily Step Goal", 1000, 20000, 10000)
    st.divider()
    st.markdown("### Quick Actions")
    if st.button("Log Workout"):
        st.toast("Workout Logged Successfully!", icon="🔥")
    if st.button("Drink Water"):
        st.toast("Stay Hydrated! +250ml", icon="💧")

# --- Main Dashboard ---
st.title(f"Welcome back, {name}! 🧘‍♂️")
st.markdown("Your wellness journey at a glance.")

# Top Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Steps Today", value="8,432", delta="1,200", delta_color="normal")
with col2:
    st.metric(label="Calories Burned", value="452 kcal", delta="15%", delta_color="normal")
with col3:
    st.metric(label="Water Intake", value="1.5 L", delta="-0.5L", delta_color="inverse")
with col4:
    st.metric(label="Sleep Quality", value="82%", delta="4%", delta_color="normal")

st.divider()

# Charts Section
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Activity Trend (Last 7 Days)")
    # Generate dummy data
    chart_data = pd.DataFrame(
        np.random.randn(7, 3) * [500, 100, 50] + [8000, 500, 250],
        columns=['Steps', 'Calories', 'Activity Min']
    )
    st.line_chart(chart_data, color=["#00d4ff", "#ff4b4b", "#00ff00"], use_container_width=True)

with col_right:
    st.subheader("Goal Progress")
    progress = 8432 / goal_steps
    st.write(f"Steps: {8432} / {goal_steps}")
    st.progress(min(progress, 1.0), text=f"{int(progress*100)}% reached")
    
    st.subheader("Health Byte 💡")
    tips = [
        "Walking after dinner improves digestion.",
        "Blue light from screens can disrupt sleep.",
        "Stretching for 5 mins reduces stress levels.",
        "Green tea is packed with antioxidants."
    ]
    st.info(np.random.choice(tips))

# Bottom Section: Meal Log
st.divider()
st.subheader("Log Your Today's Meals")
with st.expander("Add New Entry"):
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
    meal_name = st.text_input("Meal Description")
    col_a, col_b = st.columns(2)
    with col_a:
        meal_cal = st.number_input("Est. Calories", 0, 2000, 300)
    with col_b:
        meal_time = st.time_input("Time", datetime.now().time())
    
    if st.button("Save Meal Record"):
        with st.status("Saving to Database...", expanded=True) as status:
            st.write("Verifying data...")
            time.sleep(1)
            st.write("Syncing with Cloud...")
            time.sleep(1)
            status.update(label="Sync Complete!", state="complete", expanded=False)
        st.success(f"Logged: {meal_name} ({meal_cal} kcal)")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>Made with ❤️ using Streamlit by Antigravity</div>", 
    unsafe_allow_html=True
)
