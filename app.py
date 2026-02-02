import streamlit as st
import google.generativeai as genai
import time
from streamlit_lottie import st_lottie
import requests
import json

# --- 1. APP CONFIGURATION with custom theme ---
st.set_page_config(
    page_title="BiharKrishi AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(46, 125, 50, 0.2);
        animation: fadeInDown 1s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 5px solid #4CAF50;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(46, 125, 50, 0.3);
    }
    
    .input-field {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 10px;
        transition: all 0.3s ease;
    }
    
    .input-field:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
        color: white;
    }
    
    .profile-badge {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .success-animation {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        animation: slideInRight 0.8s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SECURE API CONNECTION ---
if "api_keyY" in st.secrets:
    api_key = st.secrets["api_key"]
    genai.configure(api_key=api_key)
    
    generation_config = {
        "temperature": 0.2, 
        "max_output_tokens": 400,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        generation_config=generation_config
    )
else:
    st.error("⚠️ API Key missing! Please add your key to Streamlit Secrets.")
    st.stop()

# --- 3. LOAD ANIMATIONS ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie animations
farm_animation = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_w51pcehl.json")
farmer_animation = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_tll8jxlx.json")

# --- 4. SIDEBAR: MODERN USER PROFILE ---
with st.sidebar:
    st.markdown("<div class='profile-badge'>", unsafe_allow_html=True)
    
    # Animation in sidebar
    if farmer_animation:
        st_lottie(farmer_animation, height=150, key="farmer")
    
    st.markdown("### 👤 Farmer Profile")
    
    # Profile inputs with icons
    farmer_name = st.text_input("**Farmer Name**", value="Ram Kumar Baitha")
    farmer_location = st.text_input("**📍 Location**", value="Kishanganj, Bihar")
    land_size = st.text_input("**🌱 Land Size**", value="0.25 Hectares")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick stats
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Soil Health", "Good", "↑")
    with col2:
        st.metric("Water Level", "Adequate", "→")
    with col3:
        st.metric("Yield", "85%", "↑")

# --- 5. MAIN INTERFACE ---
# Header with animation
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.markdown("""
    <div class='main-header'>
        <h1>🌾 BiharKrishi AI</h1>
        <h3>Smart Farming Assistant for Bihar</h3>
        <p>Turning challenges into opportunities with AI-powered agriculture</p>
    </div>
    """, unsafe_allow_html=True)

with col_header2:
    if farm_animation:
        st_lottie(farm_animation, height=150, key="header")

# Input Cards in Grid Layout
st.markdown("### 📝 Ask Your Farming Question")

# Create two columns for inputs
col_input1, col_input2 = st.columns(2)

with col_input1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**📍 District**")
    location = st.text_input("", value="Samastipur", label_visibility="collapsed")
    
    st.markdown("**🌱 Crop Stage**")
    crop_stage = st.selectbox(
        "",
        ["Germination", "Vegetative", "Flowering", "Fruiting", "Harvest"],
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_input2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**🎯 Category**")
    category = st.selectbox(
        "",
        ["Cost Saving", "Pest Control", "Water Management", "Fertilizer Use", "Crop Rotation"],
        label_visibility="collapsed"
    )
    
    st.markdown("**💭 Your Question**")
    user_query = st.text_input(
        "",
        placeholder="Type your farming question here...",
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Action Button with animation
col_btn, col_space, col_info = st.columns([1, 2, 1])
with col_btn:
    if st.button("🚀 Get AI Advice", use_container_width=True):
        if user_query and location:
            with st.spinner("🌱 Analyzing soil patterns..."):
                time.sleep(1)  # Simulate processing for animation
                
                # Full prompt
                full_prompt = f"""
                You are an expert Bihar agricultural consultant. 
                User Profile: {farmer_name} from {farmer_location} with {land_size} hectares.
                Current Query Context: District {location}, Crop Stage {crop_stage}.
                Question: {user_query}
                
                Instructions: Provide a formatted response as per FA-2 standards:
                1. Use a bulleted list for actionable steps.
                2. Include a brief 'Why' (justification) for each suggestion.
                3. Use simple, non-technical language.
                """
                
                try:
                    # Create placeholder for animation
                    result_placeholder = st.empty()
                    
                    # Show loading animation
                    with result_placeholder.container():
                        st.markdown("<div class='success-animation'>", unsafe_allow_html=True)
                        st_lottie(load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_yr6zz3wv.json"), height=100)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    time.sleep(1.5)  # Show loading animation
                    
                    # Get AI response
                    response = model.generate_content(full_prompt)
                    
                    # Clear loading and show results
                    result_placeholder.empty()
                    
                    # Display results with animation
                    st.markdown("### 💡 AI Recommendations")
                    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
                    
                    # Parse and display response
                    lines = response.text.split('\n')
                    for line in lines:
                        if line.strip():
                            if line.strip().startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')):
                                st.markdown(f"✅ {line.strip()}")
                            else:
                                st.markdown(line.strip())
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Additional Tips Section
                    st.markdown("### 🌟 Pro Tips")
                    tips_col1, tips_col2 = st.columns(2)
                    
                    with tips_col1:
                        st.markdown("""
                        <div class='card'>
                        <b>📅 Best Time</b><br>
                        Morning hours for pesticide application
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("""
                        <div class='card'>
                        <b>💧 Water Wisdom</b><br>
                        Check soil moisture before irrigation
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with tips_col2:
                        st.markdown("""
                        <div class='card'>
                        <b>💰 Cost Saver</b><br>
                        Use organic manure from farm waste
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("""
                        <div class='card'>
                        <b>🐛 Pest Alert</b><br>
                        Monitor crops weekly for early signs
                        </div>
                        """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}...")
        else:
            st.warning("⚠️ Please enter both district and question")

with col_info:
    st.markdown("""
    <div class='card'>
    <b>ℹ️ Quick Tips</b><br>
    • Be specific with your question<br>
    • Mention exact crop name<br>
    • Include current weather conditions
    </div>
    """, unsafe_allow_html=True)

# Footer Section
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**🌦️ Weather Advisory**")
    st.metric("Today", "Partly Cloudy", "28°C")

with footer_col2:
    st.markdown("**📱 Contact Support**")
    st.markdown("📧 support@biharkrishi.ai")
    st.markdown("📞 1800-XXX-XXXX")

with footer_col3:
    st.markdown("**🏆 Success Rate**")
    st.progress(85)
    st.caption("85% of farmers reported better yield")

# Bottom animation
st.markdown("---")
if load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_x1gjdldd.json"):
    st_lottie(load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_x1gjdldd.json"), height=100)
