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
    
    /* Enhanced Response Styling */
    .response-section {
        background: linear-gradient(135deg, #f8fff8 0%, #e8f5e9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #2e7d32;
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
    
    .response-bullet {
        display: flex;
        align-items: flex-start;
        margin: 0.8rem 0;
        padding-left: 0.5rem;
    }
    
    .response-bullet::before {
        content: "🌱";
        margin-right: 10px;
        font-size: 1.2rem;
    }
    
    .why-note {
        background: rgba(46, 125, 50, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.3rem 0 0.3rem 1.5rem;
        font-size: 0.9rem;
        color: #1a472a;
        border-left: 3px solid #4caf50;
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
        "max_output_tokens": 800,  # Increased for detailed responses
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        generation_config=generation_config
    )
else:
    st.error("⚠️ API Key missing! Please add GOOGLE_API_KEY to Streamlit Secrets.")
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

# --- ENHANCED PROMPT ENGINEERING FUNCTION ---
def get_enhanced_prompt(farmer_name, farmer_location, land_size, location, crop_stage, category, user_query):
    """Generate enhanced prompt with Bihar-specific context"""
    
    return f"""
# BIHAR AGRICULTURAL EXPERT ASSISTANT PROMPT
## ROLE & CONTEXT:
You are a certified agricultural consultant specializing in Bihar's unique farming conditions. You have 20+ years of experience helping small-scale farmers in Bihar improve yields while reducing costs and environmental impact.

## USER PROFILE:
- 👤 Farmer: {farmer_name}
- 📍 Location: {farmer_location}
- 🌱 Land Size: {land_size} hectares
- 🏛️ District: {location}
- 🌾 Crop Stage: {crop_stage}
- 🎯 Concern Category: {category}

## USER QUERY:
"{user_query}"

## RESPONSE REQUIREMENTS:
### STRUCTURE (Follow exactly):
1. **📍 Situation Analysis** (2-3 sentences summarizing the specific Bihar context)
2. **🎯 Immediate Actions** (Next 24-48 hours, max 3 bullet points)
3. **📅 Short-term Plan** (This week, max 3 bullet points)
4. **🌱 Long-term Strategy** (This season, max 2 bullet points)
5. **⚠️ Bihar-Specific Warnings** (What to avoid in {location} district)
6. **💪 Motivational Tip** (Include a farming-related quote or encouragement)

### FORMATTING RULES:
- Use **bold** for section headers
- Use • for bullet points (not dashes or numbers)
- Each bullet: Action + "Why?" explanation in parentheses
- Use simple Hindi-English mix if technical terms needed
- Keep each bullet max 2 lines

### CONTENT GUIDELINES:
1. **LOCALIZE**: Reference specific conditions in {location} district
2. **COST-EFFECTIVE**: Prioritize low-cost solutions under ₹500
3. **PRACTICAL**: Recommend only tools/materials available in local markets
4. **SCALABLE**: Solutions should work for {land_size} hectare farms
5. **SUSTAINABLE**: Promote organic/local resources

### SPECIAL CONSIDERATIONS FOR BIHAR:
- Account for frequent power cuts
- Consider flood-prone areas in {location} if applicable
- Account for small land holdings (like {land_size} hectares)
- Consider local labor availability
- Remember common crops in {location}: rice, wheat, maize, pulses

### CURRENT CONDITIONS (Assume unless specified):
- Season: {'Kharif' if datetime.now().month in [6,7,8,9,10] else 'Rabi'}
- Weather: {'Monsoon season' if datetime.now().month in [6,7,8,9] else 'Dry season'}

## FINAL INSTRUCTION:
Provide actionable, localized advice that {farmer_name} can implement immediately. Focus on practical solutions available in {location} district for a {land_size} hectare farm.
"""

# --- ENHANCED RESPONSE DISPLAY FUNCTION ---
def display_enhanced_response(response_text):
    """Display AI response with enhanced formatting"""
    
    # Animated result card
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e8f5e9, #c8e6c9); 
                padding: 2rem; border-radius: 20px; margin: 2rem 0;">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: #2e7d32; color: white; width: 50px; height: 50px; 
                        border-radius: 50%; display: flex; align-items: center; 
                        justify-content: center; margin-right: 1rem; font-size: 1.8rem;
                        animation: bounce 2s infinite;">
                💡
            </div>
            <h2 style="margin: 0; color: #1a472a; font-size: 1.8rem;">🌾 AI Farming Recommendations</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display response with enhanced formatting
    st.markdown('<div class="response-section">', unsafe_allow_html=True)
    
    # Process and display the response
    lines = response_text.split('\n')
    current_section = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for section headers
        if line.startswith('**📍') or line.startswith('**🎯') or line.startswith('**📅') or line.startswith('**🌱') or line.startswith('**⚠️') or line.startswith('**💪'):
            st.markdown(f"### {line.replace('**', '')}")
            current_section = line
        elif line.startswith('•'):
            # Display bullet points with enhanced styling
            bullet_content = line[1:].strip()
            if '(' in bullet_content and ')' in bullet_content:
                # Split action and why
                parts = bullet_content.split('(')
                if len(parts) > 1:
                    action = parts[0].strip()
                    why = '(' + parts[1].strip()
                    st.markdown(f'<div class="response-bullet"><strong>{action}</strong></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="why-note">{why}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="response-bullet">{bullet_content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="response-bullet">{bullet_content}</div>', unsafe_allow_html=True)
        elif any(line.startswith(num) for num in ['1.', '2.', '3.', '4.', '5.']):
            # Convert numbered lists to bullet points
            bullet_content = line[2:].strip()
            st.markdown(f'<div class="response-bullet">{bullet_content}</div>', unsafe_allow_html=True)
        else:
            # Regular text
            st.markdown(line)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

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
                <p>Analyzing conditions in {location} district</p>
            </div>
            <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            </style>
            """.format(location=location), unsafe_allow_html=True)
        
        time.sleep(1.5)
        
        try:
            # Get enhanced prompt
            enhanced_prompt = get_enhanced_prompt(
                farmer_name, farmer_location, land_size, 
                location, crop_stage, category, user_query
            )
            
            # Get AI response
            response = model.generate_content(enhanced_prompt)
            
            # Clear loading and show results with animation
            result_placeholder.empty()
            
            # Display enhanced response
            display_enhanced_response(response.text)
            
            # Additional animated tips
            st.markdown("---")
            st.markdown("### 🌟 Additional Pro Tips")
            
            tips = [
                {"icon": "⏰", "title": "Best Timing", "desc": "Water plants early morning", "color": "#2e7d32"},
                {"icon": "💰", "title": "Cost Saver", "desc": "Use organic compost from farm waste", "color": "#4caf50"},
                {"icon": "🌧️", "title": "Weather Watch", "desc": "Check forecast before spraying", "color": "#2196f3"},
                {"icon": "🐝", "title": "Natural Pest", "desc": "Attract beneficial insects with marigolds", "color": "#ff9800"},
            ]
            
            cols = st.columns(4)
            for idx, tip in enumerate(tips):
                with cols[idx]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; border-radius: 15px; 
                                background: white; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
                                animation: fadeIn 1s ease-out {0.2*idx}s both;
                                border-top: 4px solid {tip['color']};">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{tip['icon']}</div>
                        <h4 style="margin: 0; color: {tip['color']};">{tip['title']}</h4>
                        <p style="font-size: 0.9rem; color: #666;">{tip['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Success message
            st.success("✅ AI analysis completed! Implement these steps for better results.")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)[:100]}...")
            st.info("Please try again with a different question or check your internet connection.")

# Footer with animations
st.markdown("---")
footer_cols = st.columns(3)

with footer_cols[0]:
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 2s ease-out 1s both;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem; animation: bounce 2s infinite;">🌦️</div>
        <h4>Weather Advisory</h4>
        <p>Partly Cloudy • 28°C</p>
        <small>Perfect for fertilizer application</small>
    </div>
    """, unsafe_allow_html=True)

with footer_cols[1]:
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 2s ease-out 1.2s both;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem; animation: bounce 2s infinite 0.5s;">📞</div>
        <h4>Support</h4>
        <p>1800-XXX-XXXX</p>
        <small>Available 24/7</small>
    </div>
    """, unsafe_allow_html=True)

with footer_cols[2]:
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 2s ease-out 1.4s both;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem; animation: bounce 2s infinite 1s;">📊</div>
        <h4>Success Rate</h4>
        <p>85% Better Yield</p>
        <small>Based on user feedback</small>
    </div>
    """, unsafe_allow_html=True)

# Floating particles effect
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

# Add JavaScript for enhanced particle effect
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
    const colors = ['#2e7d32', '#4caf50', '#66bb6a', '#81c784'];
    for(let i = 0; i < 25; i++) {
        const particle = document.createElement('div');
        const size = 2 + Math.random() * 4;
        const color = colors[Math.floor(Math.random() * colors.length)];
        
        particle.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: ${color};
            border-radius: 50%;
            opacity: 0.2;
            filter: blur(0.5px);
        `;
        
        // Random position
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        
        // Animation
        const duration = 4 + Math.random() * 6;
        const delay = Math.random() * 3;
        particle.style.animation = `
            floatParticle ${duration}s ease-in-out infinite ${delay}s
        `;
        
        container.appendChild(particle);
    }
    
    // Add CSS for particle animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatParticle {
            0%, 100% {
                transform: translate(0, 0) rotate(0deg);
                opacity: 0.1;
            }
            25% {
                transform: translate(30px, -30px) rotate(90deg);
                opacity: 0.3;
            }
            50% {
                transform: translate(0, -60px) rotate(180deg);
                opacity: 0.1;
            }
            75% {
                transform: translate(-30px, -30px) rotate(270deg);
                opacity: 0.3;
            }
        }
    `;
    document.head.appendChild(style);
});
</script>
""", height=0)
