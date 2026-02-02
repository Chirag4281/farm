import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================
# 🎨 PAGE CONFIGURATION - Premium Design
# ============================================
st.set_page_config(
    page_title="🌱 FarmGenius AI Assistant",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🎨 CUSTOM CSS FOR ENHANCED UI
# ============================================
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 20px;
    }
    
    /* Header styling */
    .header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #00b09b 0%, #96c93d 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(0,176,155,0.4);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ff7e5f 0%, #feb47b 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    
    /* Animated text */
    .animated-text {
        background: linear-gradient(45deg, #FF512F, #DD2476, #FF512F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
        background-size: 400% 400%;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 🚀 HEADER SECTION
# ============================================
st.markdown("""
<div class="header">
    <h1 style="font-size: 3.5rem; margin: 0;">🌱 FarmGenius AI</h1>
    <h2 style="font-size: 1.5rem; margin: 10px 0 20px 0;">Smart Farming Assistant Powered by Gemini 1.5</h2>
    <p style="font-size: 1.1rem;">Get personalized, region-specific farming advice for India 🇮🇳, Ghana 🇬🇭, and Canada 🇨🇦</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# 📊 DASHBOARD STATS (Top Metrics)
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card" style="text-align: center;">
        <h3 style="color: #2E86C1;">🌍</h3>
        <h2 style="color: #2E86C1;">3</h2>
        <p style="color: #7F8C8D;">Countries Supported</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card" style="text-align: center;">
        <h3 style="color: #27AE60;">🌾</h3>
        <h2 style="color: #27AE60;">50+</h2>
        <p style="color: #7F8C8D;">Crops Analyzed</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card" style="text-align: center;">
        <h3 style="color: #E74C3C;">🤖</h3>
        <h2 style="color: #E74C3C;">AI-Powered</h2>
        <p style="color: #7F8C8D;">Gemini 1.5 Pro</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card" style="text-align: center;">
        <h3 style="color: #8E44AD;">⚡</h3>
        <h2 style="color: #8E44AD;">Real-time</h2>
        <p style="color: #7F8C8D;">Instant Advice</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 🎯 MAIN INPUT SECTION
# ============================================
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px; margin: 30px 0;">
    <h2 style="color: white; text-align: center; margin-bottom: 25px;">📝 Enter Your Farming Query</h2>
""", unsafe_allow_html=True)

# Create tabs for different input methods
tab1, tab2, tab3 = st.tabs(["🎯 Quick Query", "🌍 Detailed Analysis", "📊 Crop Calculator"])

with tab1:
    st.markdown("### Quick Farming Advice")
    col1, col2 = st.columns(2)
    
    with col1:
        country = st.selectbox(
            "Select Country",
            ["India 🇮🇳", "Ghana 🇬🇭", "Canada 🇨🇦", "Other 🌍"],
            key="country_select"
        )
        
        region = st.text_input(
            "Region/State",
            placeholder="e.g., Rajasthan, Punjab, Ontario...",
            help="Enter your specific region for precise advice"
        )
    
    with col2:
        crop_stage = st.select_slider(
            "Crop Stage",
            options=["Planning 🌱", "Sowing 🌾", "Growing 🌿", "Harvesting 🎯", "Post-Harvest 📦"],
            value="Planning 🌱"
        )
        
        query = st.text_area(
            "Your Farming Question",
            placeholder="e.g., What to grow in August? How to handle pests? Best irrigation methods?",
            height=100
        )

with tab2:
    st.markdown("### Detailed Farming Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        soil_type = st.selectbox(
            "Soil Type",
            ["Sandy", "Clay", "Loamy", "Silty", "Peaty", "Chalky"]
        )
        
        rainfall = st.slider(
            "Annual Rainfall (mm)",
            min_value=200,
            max_value=3000,
            value=800,
            step=100
        )
    
    with col2:
        temperature = st.slider(
            "Average Temperature (°C)",
            min_value=0,
            max_value=40,
            value=25,
            step=1
        )
        
        budget = st.selectbox(
            "Budget Level",
            ["Low", "Medium", "High"]
        )

with tab3:
    st.markdown("### Crop Yield Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop_name = st.text_input("Crop Name", "Wheat")
        area = st.number_input("Area (acres)", min_value=0.1, max_value=1000.0, value=10.0)
    
    with col2:
        expected_yield = st.number_input("Expected Yield (tons/acre)", min_value=0.1, max_value=50.0, value=2.5)
        
        # Calculate button
        if st.button("Calculate Yield", key="calculate_yield"):
            total_yield = area * expected_yield
            st.success(f"🌾 Estimated Total Yield: **{total_yield:.2f} tons**")
            
            # Create a gauge chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_yield,
                title = {'text': "Estimated Yield"},
                gauge = {
                    'axis': {'range': [None, area * 5]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, area * 2], 'color': "lightgray"},
                        {'range': [area * 2, area * 4], 'color': "gray"},
                        {'range': [area * 4, area * 5], 'color': "darkgray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': area * 4
                    }
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# 🚀 AI RESPONSE SECTION
# ============================================
st.markdown("</div>", unsafe_allow_html=True)

# Generate Advice Button with Animation
if st.button("🚀 Generate Smart Farming Advice", use_container_width=True):
    
    if not query:
        st.warning("⚠️ Please enter a farming query first!")
        st.stop()
    
    # Show loading animation
    with st.spinner("🧠 **FarmGenius AI is analyzing...**"):
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"Analyzing... {i+1}%")
        
        # Configure Gemini API (replace with your actual API key)
        genai.configure(api_key=st.secrets["api_key"])
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Create comprehensive prompt
        prompt = f"""
        You are FarmGenius AI - a world-class agricultural expert specializing in {country}.
        
        **USER QUERY:**
        Region: {region}
        Crop Stage: {crop_stage}
        Question: {query}
        
        **ADDITIONAL CONTEXT:**
        Soil Type: {soil_type if 'soil_type' in locals() else 'Not specified'}
        Rainfall: {rainfall if 'rainfall' in locals() else 'Not specified'} mm
        Temperature: {temperature if 'temperature' in locals() else 'Not specified'}°C
        
        **REQUIREMENTS:**
        1. Provide 3-5 specific recommendations
        2. Each recommendation MUST include:
           - ✅ Actionable step
           - 💡 Reason/Benefit (explain "why")
           - 📊 Estimated impact
           - ⚠️ Potential risks to avoid
        3. Format with clear headings and emojis
        4. Include local best practices for {country}
        5. Add seasonal considerations
        6. Provide alternatives if applicable
        
        Make it practical, encouraging, and easy to understand!
        """
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Clear progress
        progress_bar.empty()
        status_text.empty()
        
        # Display response in a beautiful card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%); 
                    padding: 30px; 
                    border-radius: 20px; 
                    border-left: 8px solid #27AE60;
                    margin: 30px 0;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
            <h2 style="color: #2C3E50; border-bottom: 3px solid #3498db; padding-bottom: 10px;">🤖 FarmGenius AI Advice</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Display formatted response
        st.markdown(response.text)
        
        # Add download option
        st.download_button(
            label="📥 Download Advice as PDF",
            data=response.text,
            file_name=f"farmgenius_advice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

# ============================================
# 📊 VISUALIZATION SECTION
# ============================================
st.markdown("---")
st.markdown("## 📊 Farming Insights Dashboard")

col1, col2 = st.columns(2)

with col1:
    # Crop Cycle Visualization
    st.markdown("### 🌱 Typical Crop Cycle")
    
    # Sample crop data
    crops_data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Wheat': [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
        'Rice': [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        'Corn': [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0]
    }
    
    df = pd.DataFrame(crops_data)
    fig, ax = plt.subplots(figsize=(10, 6))
    df.set_index('Month').plot(kind='bar', stacked=True, ax=ax, colormap='viridis')
    ax.set_ylabel('Growth Stage')
    ax.set_title('Crop Planting Calendar')
    ax.legend(title='Crops', bbox_to_anchor=(1.05, 1))
    st.pyplot(fig)

with col2:
    # Weather Impact Gauge
    st.markdown("### 🌤️ Weather Impact Score")
    
    # Create interactive gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = 78,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Favorability Index", 'font': {'size': 24}},
        delta = {'reference': 50, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkgreen"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': 'red'},
                {'range': [40, 70], 'color': 'yellow'},
                {'range': [70, 100], 'color': 'green'}],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 90}}))
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# 📝 FEEDBACK & VALIDATION SECTION
# ============================================
st.markdown("---")
st.markdown("## 📋 AI Response Quality Checklist")

feedback_cols = st.columns(5)

with feedback_cols[0]:
    region_specific = st.checkbox("🌍 Region-Specific", value=True)
with feedback_cols[1]:
    clear_reasoning = st.checkbox("💡 Clear Reasoning", value=True)
with feedback_cols[2]:
    simple_language = st.checkbox("📝 Simple Language", value=True)
with feedback_cols[3]:
    practical = st.checkbox("⚙️ Practical Advice", value=True)
with feedback_cols[4]:
    safe_accurate = st.checkbox("✅ Safe & Accurate", value=True)

# Feedback form
with st.expander("📊 Submit Detailed Feedback"):
    feedback_text = st.text_area("Your feedback helps us improve:")
    rating = st.slider("Rate this advice (1-5 stars)", 1, 5, 4)
    
    if st.button("Submit Feedback"):
        st.success("🎉 Thank you for your valuable feedback!")
        st.balloons()

# ============================================
# 🌟 EXAMPLE PROMPTS SECTION
# ============================================
st.markdown("---")
st.markdown("## 💡 Try These Example Prompts")

example_cols = st.columns(3)

with example_cols[0]:
    if st.button("🌾 Best crops for Rajasthan\nin August", use_container_width=True):
        st.session_state.query = "What are the best crops to grow in Rajasthan during August?"
        st.rerun()

with example_cols[1]:
    if st.button("💧 Water-saving techniques\nfor Ghana", use_container_width=True):
        st.session_state.query = "Suggest water-saving irrigation techniques for farms in Ghana"
        st.rerun()

with example_cols[2]:
    if st.button("❄️ Winter farming in\nCanada", use_container_width=True):
        st.session_state.query = "What crops can be grown during winter in Canadian greenhouses?"
        st.rerun()

# ============================================
# 📱 RESPONSIVE DESIGN & FOOTER
# ============================================
st.markdown("---")
footer_cols = st.columns(4)

with footer_cols[0]:
    st.markdown("### 🌍 Global Coverage")
    st.write("India • Ghana • Canada")

with footer_cols[1]:
    st.markdown("### 🛠️ Technologies")
    st.write("Streamlit • Gemini AI • Python")

with footer_cols[2]:
    st.markdown("### 📞 Support")
    st.write("farmgenius@agronova.com")

with footer_cols[3]:
    st.markdown("### 🔄 Live Status")
    st.success("✅ System Online")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================
# 🎨 SIDEBAR FOR ADDITIONAL FEATURES
# ============================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: white;">⚙️ Settings</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # API Settings
    with st.expander("🔧 API Configuration"):
        api_key = st.text_input("Gemini API Key", type="password")
        temperature = st.slider("AI Creativity", 0.0, 1.0, 0.7, 0.1)
        max_tokens = st.slider("Response Length", 100, 2000, 500, 50)
    
    # Theme Selection
    with st.expander("🎨 Theme Customization"):
        theme = st.selectbox("Choose Theme", ["Default", "Dark Mode", "Green Fields", "Sunset"])
        if theme == "Dark Mode":
            st.markdown("""<style>.main {background: #2c3e50; color: white;}</style>""", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("🔄 Clear All", use_container_width=True):
        st.rerun()
    
    if st.button("📚 View Examples", use_container_width=True):
        st.info("Check the example prompts section below!")
    
    if st.button("📈 View Analytics", use_container_width=True):
        st.info("Detailed analytics coming soon!")
    
    # Tips Section
    st.markdown("---")
    st.markdown("### 💡 Pro Tips")
    st.info("""
    1. Be specific about your region
    2. Mention current weather conditions
    3. Include your budget if possible
    4. Ask follow-up questions for clarity
    """)

# ============================================
# 📱 MOBILE RESPONSIVENESS CHECK
# ============================================
st.markdown("""
<style>
    @media (max-width: 768px) {
        .card {
            margin: 10px 0;
        }
        .stButton>button {
            padding: 12px 20px;
            font-size: 14px;
        }
    }
</style>
""", unsafe_allow_html=True)
