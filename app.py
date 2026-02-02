import streamlit as st
import google.generativeai as genai
import time
from streamlit_lottie import st_lottie
import requests
import json
import random
from datetime import datetime

# --- 1. APP CONFIGURATION with enhanced theme ---
st.set_page_config(
    page_title="BiharKrishi AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom fonts and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@800;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Welcome Animation */
    .welcome-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        background: linear-gradient(135deg, #1a472a 0%, #2e7d32 50%, #66bb6a 100%);
        z-index: 9999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: fadeOut 1.5s ease-out 3s forwards;
    }
    
    @keyframes fadeOut {
        to { opacity: 0; visibility: hidden; }
    }
    
    .welcome-text {
        font-family: 'Montserrat', sans-serif;
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(45deg, #fff, #c8e6c9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: textGlow 2s infinite alternate;
    }
    
    @keyframes textGlow {
        from { text-shadow: 0 0 10px rgba(255,255,255,0.5); }
        to { text-shadow: 0 0 30px rgba(255,255,255,0.9); }
    }
    
    .loading-bar {
        width: 300px;
        height: 4px;
        background: rgba(255,255,255,0.2);
        border-radius: 2px;
        margin-top: 30px;
        overflow: hidden;
    }
    
    .loading-progress {
        width: 0%;
        height: 100%;
        background: linear-gradient(90deg, #fff, #c8e6c9);
        animation: loading 3s ease-out forwards;
    }
    
    @keyframes loading {
        to { width: 100%; }
    }
    
    /* Main Content Animation */
    .main-content {
        animation: slideUp 1s ease-out 3.5s both;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Header Styles */
    .animated-header {
        background: linear-gradient(135deg, #1a472a 0%, #2e7d32 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .animated-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255,255,255,0.1) 50%,
            transparent 70%
        );
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Floating Cards */
    .floating-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(46, 125, 50, 0.15);
        border: 1px solid rgba(76, 175, 80, 0.1);
        animation: float 6s ease-in-out infinite;
        transition: all 0.3s ease;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(46, 125, 50, 0.25);
    }
    
    /* Animated Button */
    .animated-button {
        background: linear-gradient(135deg, #1a472a 0%, #2e7d32 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 16px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .animated-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }
    
    .animated-button:hover::before {
        left: 100%;
    }
    
    .animated-button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(26, 71, 42, 0.3);
    }
    
    /* Particle Effect */
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(255,255,255,0.5);
        border-radius: 50%;
        pointer-events: none;
        opacity: 0;
    }
    
    /* Input Animation */
    .stTextInput > div > div > input {
        animation: inputFocus 0.5s ease-out;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 12px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2e7d32;
        box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1); }
        50% { box-shadow: 0 0 0 6px rgba(46, 125, 50, 0.2); }
    }
    
    /* Sidebar Animation */
    .sidebar-animation {
        animation: slideInLeft 1s ease-out;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Progress Bar */
    .progress-container {
        width: 100%;
        height: 6px;
        background: #e0e0e0;
        border-radius: 3px;
        overflow: hidden;
        margin: 20px 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #2e7d32, #4caf50);
        width: 0%;
        animation: progress 2s ease-in-out infinite;
    }
    
    @keyframes progress {
        0% { width: 0%; }
        50% { width: 100%; }
        100% { width: 0%; }
    }
    
    /* Result Card Animation */
    .result-card {
        animation: popIn 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    @keyframes popIn {
        0% {
            opacity: 0;
            transform: scale(0.8);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 2. WELCOME ANIMATION ---
st.markdown("""
<div class="welcome-container">
    <div class="welcome-text">🌾 BiharKrishi AI</div>
    <div>Empowering Farmers with Intelligence</div>
    <div class="loading-bar">
        <div class="loading-progress"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 3. SECURE API CONNECTION ---
if "api_key" in st.secrets:
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
    st.error("⚠️ API Key missing!")
    st.stop()

# --- 4. SIDEBAR WITH ANIMATIONS ---
with st.sidebar:
    st.markdown('<div class="sidebar-animation">', unsafe_allow_html=True)
    
    # Profile section with animation
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="width: 100px; height: 100px; margin: 0 auto 1rem; 
                    background: linear-gradient(135deg, #2e7d32, #4caf50); 
                    border-radius: 50%; display: flex; align-items: center; 
                    justify-content: center; font-size: 40px; color: white;
                    animation: bounce 2s infinite;">
            👨‍🌾
        </div>
        <h3>Farmer Profile</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Animated profile inputs
    farmer_name = st.text_input("**👤 Name**", value="Ram Kumar Baitha", 
                               help="Enter your full name")
    
    farmer_location = st.text_input("**📍 Location**", value="Kishanganj, Bihar",
                                   help="Your village/town")
    
    land_size = st.text_input("**🌱 Land Size**", value="0.25 Hectares",
                             help="Size of your farmland")
    
    # Animated stats
    st.markdown("---")
    st.markdown("### 📊 Live Stats")
    
    cols = st.columns(3)
    with cols[0]:
        st.metric("🌡️ Soil Temp", "28°C", "↑2°")
    with cols[1]:
        st.metric("💧 Moisture", "65%", "→")
    with cols[2]:
        st.metric("🌤️ Forecast", "Sunny", "")
    
    # Progress animation
    st.markdown("""
    <style>
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. MAIN CONTENT ---
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Animated Header
st.markdown("""
<div class="animated-header">
    <h1 style="margin: 0; font-size: 2.8rem; animation: fadeIn 2s ease-out;">🌾 BiharKrishi AI</h1>
    <p style="font-size: 1.2rem; opacity: 0.9; animation: fadeIn 2s ease-out 0.5s both;">
        Smart Farming Assistant for Bihar • Turning Challenges into Opportunities
    </p>
</div>
""", unsafe_allow_html=True)

# Floating Input Cards
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="floating-card">', unsafe_allow_html=True)
    st.markdown("### 📍 District")
    location = st.selectbox(
        "Select your district",
        ["Samastipur", "Patna", "Muzaffarpur", "Gaya", "Bhagalpur", 
         "Purnia", "Darbhanga", "Munger", "Araria", "Kishanganj"],
        index=0,
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="floating-card" style="animation-delay: 0.2s">', unsafe_allow_html=True)
    st.markdown("### 🌱 Crop Stage")
    crop_stage = st.select_slider(
        "",
        options=["Germination", "Vegetative", "Flowering", "Fruiting", "Harvest"],
        value="Vegetative",
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="floating-card" style="animation-delay: 0.4s">', unsafe_allow_html=True)
    st.markdown("### 🎯 Category")
    category = st.selectbox(
        "What do you need help with?",
        ["Cost Saving", "Pest Control", "Water Management", 
         "Fertilizer Use", "Crop Rotation", "Weather Impact"],
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="floating-card" style="animation-delay: 0.6s">', unsafe_allow_html=True)
    st.markdown("### 💭 Your Question")
    user_query = st.text_area(
        "",
        placeholder="Type your farming question here...\nExample: How can I save on diesel costs for irrigation?",
        height=100,
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Center button with animation
col_btn = st.columns([1, 2, 1])[1]
with col_btn:
    st.markdown("""
    <style>
    @keyframes buttonPulse {
        0% { box-shadow: 0 0 0 0 rgba(46, 125, 50, 0.4); }
        70% { box-shadow: 0 0 0 20px rgba(46, 125, 50, 0); }
        100% { box-shadow: 0 0 0 0 rgba(46, 125, 50, 0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    button_clicked = st.button(
        "🚀 Get AI Farming Advice",
        use_container_width=True,
        key="main_button"
    )

# Progress bar animation
if button_clicked:
    st.markdown("""
    <div class="progress-container">
        <div class="progress-bar"></div>
    </div>
    """, unsafe_allow_html=True)

# Process query when button is clicked
if button_clicked and user_query:
    with st.spinner("🌱 Analyzing soil patterns & weather data..."):
        time.sleep(1)  # Simulate processing
        
        # Create a placeholder for results
        result_placeholder = st.empty()
        
        # Show loading animation
        with result_placeholder.container():
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; animation: spin 2s linear infinite;">
                    🌾
                </div>
                <h3>Consulting Agricultural Database...</h3>
            </div>
            <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            </style>
            """, unsafe_allow_html=True)
        
        time.sleep(1.5)
        
        # Get AI response
        full_prompt = f"""
        You are an expert Bihar agricultural consultant. 
        User Profile: {farmer_name} from {farmer_location} with {land_size} hectares.
        Current Query Context: District {location}, Crop Stage {crop_stage}, Category: {category}.
        Question: {user_query}
        
        Provide a formatted response:
        1. Use bullet points for actionable steps
        2. Include brief justifications
        3. Use simple language
        """
        
        try:
            response = model.generate_content(full_prompt)
            
            # Clear loading and show results with animation
            result_placeholder.empty()
            
            # Animated result card
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e8f5e9, #c8e6c9); 
                        padding: 2rem; border-radius: 20px; margin: 2rem 0;">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="background: #2e7d32; color: white; width: 40px; height: 40px; 
                                border-radius: 50%; display: flex; align-items: center; 
                                justify-content: center; margin-right: 1rem; font-size: 1.5rem;">
                        💡
                    </div>
                    <h2 style="margin: 0; color: #1a472a;">AI Recommendations</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Display response
            st.markdown(response.text)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Additional animated tips
            st.markdown("---")
            st.markdown("### 🌟 Pro Tips for You")
            
            tips = [
                {"icon": "⏰", "title": "Best Timing", "desc": "Water plants early morning"},
                {"icon": "💰", "title": "Cost Saver", "desc": "Use organic compost from farm waste"},
                {"icon": "🌧️", "title": "Weather Watch", "desc": "Check forecast before spraying"},
                {"icon": "🐝", "title": "Natural Pest", "desc": "Attract beneficial insects with marigolds"},
            ]
            
            cols = st.columns(4)
            for idx, tip in enumerate(tips):
                with cols[idx]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; border-radius: 15px; 
                                background: white; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
                                animation: fadeIn 1s ease-out {0.2*idx}s both;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{tip['icon']}</div>
                        <h4 style="margin: 0; color: #2e7d32;">{tip['title']}</h4>
                        <p style="font-size: 0.9rem; color: #666;">{tip['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)[:100]}...")

# Footer with animations
st.markdown("---")
footer_cols = st.columns(3)

with footer_cols[0]:
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 2s ease-out 1s both;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌦️</div>
        <h4>Weather Advisory</h4>
        <p>Partly Cloudy • 28°C</p>
        <small>Perfect for fertilizer application</small>
    </div>
    """, unsafe_allow_html=True)

with footer_cols[1]:
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 2s ease-out 1.2s both;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📞</div>
        <h4>Support</h4>
        <p>1800-XXX-XXXX</p>
        <small>Available 24/7</small>
    </div>
    """, unsafe_allow_html=True)

with footer_cols[2]:
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 2s ease-out 1.4s both;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
        <h4>Success Rate</h4>
        <p>85% Better Yield</p>
        <small>Based on user feedback</small>
    </div>
    """, unsafe_allow_html=True)

# Floating particles effect (simulated with emojis)
st.markdown("""
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            pointer-events: none; z-index: -1; opacity: 0.1;">
    <div style="position: absolute; top: 10%; left: 5%; animation: float 8s ease-in-out infinite;">🌱</div>
    <div style="position: absolute; top: 20%; right: 10%; animation: float 10s ease-in-out infinite 1s;">💧</div>
    <div style="position: absolute; bottom: 30%; left: 15%; animation: float 12s ease-in-out infinite 2s;">☀️</div>
    <div style="position: absolute; bottom: 20%; right: 20%; animation: float 9s ease-in-out infinite 0.5s;">🌾</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Add JavaScript for particle effect
st.components.v1.html("""
<script>
// Create floating particles
document.addEventListener('DOMContentLoaded', function() {
    const container = document.createElement('div');
    container.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    `;
    
    document.body.appendChild(container);
    
    // Create particles
    for(let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: linear-gradient(45deg, #2e7d32, #4caf50);
            border-radius: 50%;
            opacity: 0.3;
        `;
        
        // Random position
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        
        // Animation
        const duration = 3 + Math.random() * 4;
        particle.style.animation = `
            floatParticle ${duration}s ease-in-out infinite
        `;
        particle.style.animationDelay = Math.random() * 2 + 's';
        
        container.appendChild(particle);
    }
    
    // Add CSS for particle animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatParticle {
            0%, 100% {
                transform: translate(0, 0) rotate(0deg);
                opacity: 0.2;
            }
            25% {
                transform: translate(20px, -20px) rotate(90deg);
                opacity: 0.4;
            }
            50% {
                transform: translate(0, -40px) rotate(180deg);
                opacity: 0.2;
            }
            75% {
                transform: translate(-20px, -20px) rotate(270deg);
                opacity: 0.4;
            }
        }
    `;
    document.head.appendChild(style);
});
</script>
""")
