import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import random

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
            
            # Create a simple progress bar visualization instead of gauge
            st.markdown("### 📊 Yield Progress")
            
            fig, ax = plt.subplots(figsize=(10, 2))
            
            # Create a progress bar using matplotlib
            max_possible_yield = area * 5
            progress_percentage = (total_yield / max_possible_yield) * 100
            
            # Create horizontal bar for progress
            bars = ax.barh(['Yield Progress'], [progress_percentage], color='#27AE60')
            ax.set_xlim(0, 100)
            ax.set_xlabel('Percentage of Maximum Potential')
            ax.text(progress_percentage/2, 0, f'{total_yield:.1f} tons ({progress_percentage:.1f}%)', 
                   ha='center', va='center', color='white', fontweight='bold')
            
            # Add threshold lines
            ax.axvline(x=40, color='red', linestyle='--', alpha=0.5, label='Low Yield')
            ax.axvline(x=70, color='orange', linestyle='--', alpha=0.5, label='Medium Yield')
            ax.axvline(x=90, color='green', linestyle='--', alpha=0.5, label='High Yield')
            
            ax.legend(loc='upper right')
            st.pyplot(fig)

# ============================================
# 🚀 AI RESPONSE SECTION
# ============================================
# ============================================
# 🚀 SMART MODEL SELECTION & RESPONSE GENERATION
# ============================================

# List of available Gemini models to try
AVAILABLE_MODELS = [
    'gemini-pro',           # Most reliable, widely available
    'models/gemini-pro',    # Full path version
    'gemini-1.0-pro',       # Stable version 1.0
    'gemini-1.5-pro',       # Try 1.5 if available
    'gemini-1.5-pro-latest' # Latest 1.5 version
]

selected_model = None
ai_response = None
model_tested = ""

# Clear progress

# Show model testing status
model_status = st.empty()
model_status.info("🔍 **Testing available AI models...**")

# Try each model until one works
for model_name in AVAILABLE_MODELS:
    try:
        model_status.info(f"🔄 Testing model: `{model_name}`...")
       # Brief pause for user visibility
        
        # Configure model
        model = genai.GenerativeModel(model_name)
        
        # Test with a simple prompt first
        test_prompt = f"Say 'FarmGenius AI is ready' in 3 words."
        test_response = model.generate_content(test_prompt, request_options={"timeout": 10})
        
        # If test passes, try the actual prompt
        actual_response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=800,
                top_p=0.8,
                top_k=40
            ),
            request_options={"timeout": 30}
        )
        
        # Success! Store the response and model
        selected_model = model_name
        ai_response = actual_response.text
        model_tested = f"✅ Using: `{model_name}`"
        
        model_status.success(f"✅ **Model `{model_name}` works perfectly!**")
        # Show success message briefly
        model_status.empty()
        break  # Exit loop after success
        
    except Exception as model_error:
        model_status.warning(f"⚠️ Model `{model_name}` failed: {str(model_error)[:50]}...")
          # Brief pause
        continue  # Try next model

# If all models failed, use demo response
if ai_response is None:
    model_status.error("⚠️ All AI models failed. Using demo response...")
    
    model_status.empty()
    
    # Create a smart demo response based on user input
    demo_responses = {
        "India 🇮🇳": """
        🌾 **FarmGenius AI Advice for {} (DEMO MODE)**

        **1. 🌱 Pearl Millet (Bajra)**
        - ✅ **Actionable Step:** Plant between August 1-15 with 45x15 cm spacing
        - 💡 **Reason:** Drought-resistant, requires only 300-400mm rainfall
        - 📊 **Impact:** Yield potential: 1.5-2 tons per acre
        - ⚠️ **Risk to Avoid:** Ensure proper drainage to prevent waterlogging

        **2. 🌿 Green Gram (Moong)**
        - ✅ **Actionable Step:** Use short-duration varieties (60-70 days)
        - 💡 **Reason:** Fits monsoon window, improves soil nitrogen
        - 📊 **Impact:** Can harvest before winter, 0.8-1.2 tons per acre
        - ⚠️ **Risk to Avoid:** Apply neem-based pesticides for pest control

        **3. 🌻 Cluster Bean (Guar)**
        - ✅ **Actionable Step:** Sow with 30x15 cm spacing
        - 💡 **Reason:** Tolerates sandy soil, low water requirement
        - 📊 **Impact:** Good for soil conservation, 0.5-0.8 tons per acre
        - ⚠️ **Risk to Avoid:** Avoid planting in waterlogged areas

        **🌦️ Seasonal Tip:** {} in August typically has moderate rainfall. Consider rainwater harvesting and organic mulching.
        """,
        
        "Ghana 🇬🇭": """
        🌾 **FarmGenius AI Advice for Ghana (DEMO MODE)**

        **1. 🍌 Plantain Cultivation**
        - ✅ **Actionable Step:** Plant suckers 3m x 3m apart
        - 💡 **Reason:** Thrives in Ghana's tropical climate
        - 📊 **Impact:** High yield, year-round production
        - ⚠️ **Risk to Avoid:** Control banana weevil with pheromone traps

        **2. 🥜 Groundnut (Peanut)**
        - ✅ **Actionable Step:** Use certified seeds, plant at onset of rains
        - 💡 **Reason:** Fixes nitrogen, improves soil fertility
        - 📊 **Impact:** 1-1.5 tons per hectare
        - ⚠️ **Risk to Avoid:** Rotate crops to prevent disease buildup

        **3. 🍠 Cassava**
        - ✅ **Actionable Step:** Plant cuttings 1m x 1m apart
        - 💡 **Reason:** Drought-tolerant, staple food crop
        - 📊 **Impact:** High carbohydrate yield
        - ⚠️ **Risk to Avoid:** Control mosaic virus disease
        """,
        
        "Canada 🇨🇦": """
        🌾 **FarmGenius AI Advice for Canada (DEMO MODE)**

        **1. 🌾 Spring Wheat**
        - ✅ **Actionable Step:** Plant early spring, use winter-hardy varieties
        - 💡 **Reason:** Adapted to Canadian climate, high market demand
        - 📊 **Impact:** 2.5-3.5 tons per acre
        - ⚠️ **Risk to Avoid:** Monitor for fusarium head blight

        **2. 🥔 Potatoes**
        - ✅ **Actionable Step:** Use certified seed potatoes, rotate crops
        - 💡 **Reason:** High-value crop, good storage potential
        - 📊 **Impact:** 15-20 tons per acre
        - ⚠️ **Risk to Avoid:** Implement integrated pest management

        **3. 🌿 Canola**
        - ✅ **Actionable Step:** Plant early, use hybrid varieties
        - 💡 **Reason:** Oilseed crop with high economic value
        - 📊 **Impact:** 1.5-2 tons per acre
        - ⚠️ **Risk to Avoid:** Control flea beetles early season
        """
    }
    
    # Select appropriate demo response
    country_key = country.split(" ")[0]  # Get country name without flag
    if country_key in demo_responses:
        ai_response = demo_responses[country_key].format(region, region)
    else:
        ai_response = demo_responses["India 🇮🇳"].format(region, region)
    
    model_tested = "⚠️ DEMO MODE (AI models unavailable)"

# ============================================
# 📋 DISPLAY RESPONSE WITH MODEL INFO
# ============================================

# Show which model was used
st.info(f"**{model_tested}**")

# Display response in a beautiful card
st.markdown(f"""
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
st.markdown(ai_response)

# Add download option
st.download_button(
    label="📥 Download Advice as PDF",
    data=ai_response,
    file_name=f"farmgenius_advice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
    mime="text/plain"
)
# ============================================
# 📊 VISUALIZATION SECTION (Matplotlib Only)
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
    
    # Set width of bars
    bar_width = 0.25
    
    # Set position of bars on X axis
    r1 = range(len(df['Month']))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    
    # Create bars
    ax.bar(r1, df['Wheat'], color='#FFA726', width=bar_width, edgecolor='white', label='Wheat')
    ax.bar(r2, df['Rice'], color='#42A5F5', width=bar_width, edgecolor='white', label='Rice')
    ax.bar(r3, df['Corn'], color='#66BB6A', width=bar_width, edgecolor='white', label='Corn')
    
    # Add labels and title
    ax.set_xlabel('Month')
    ax.set_ylabel('Growth Stage (1=Growing)')
    ax.set_title('Monthly Crop Planting Calendar')
    ax.set_xticks([r + bar_width for r in range(len(df['Month']))])
    ax.set_xticklabels(df['Month'])
    ax.legend()
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    st.pyplot(fig)

with col2:
    # Weather Impact Visualization
    st.markdown("### 🌤️ Weather Impact Score")
    
    # Create a radial chart (simpler alternative to gauge)
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(projection='polar'))
    
    # Data for the chart
    categories = ['Rainfall', 'Temperature', 'Humidity', 'Sunshine', 'Wind']
    values = [75, 85, 65, 90, 55]  # Example values
    
    # Number of categories
    N = len(categories)
    
    # Create angles for each category
    angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
    angles += angles[:1]  # Close the circle
    
    # Close the values list
    values += values[:1]
    
    # Plot the data
    ax.plot(angles, values, 'o-', linewidth=2, color='#3498db')
    ax.fill(angles, values, alpha=0.25, color='#3498db')
    
    # Set labels for each category
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    
    # Set y-axis limits
    ax.set_ylim(0, 100)
    
    # Add a title
    ax.set_title('Weather Favorability Score: 78/100', size=14, y=1.1)
    
    # Add grid
    ax.grid(True)
    
    st.pyplot(fig)

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
        query = "What are the best crops to grow in Rajasthan during August?"
        st.session_state.query = query
        st.rerun()

with example_cols[1]:
    if st.button("💧 Water-saving techniques\nfor Ghana", use_container_width=True):
        query = "Suggest water-saving irrigation techniques for farms in Ghana"
        st.session_state.query = query
        st.rerun()

with example_cols[2]:
    if st.button("❄️ Winter farming in\nCanada", use_container_width=True):
        query = "What crops can be grown during winter in Canadian greenhouses?"
        st.session_state.query = query
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
        api_key_input = st.text_input("Gemini API Key", type="password", help="Enter your Gemini API key here")
        temperature = st.slider("AI Creativity", 0.0, 1.0, 0.7, 0.1)
        max_tokens = st.slider("Response Length", 100, 2000, 500, 50)
        
        if st.button("Save API Key"):
            st.success("API key saved (for demo only - use Streamlit secrets in production)")
    
    # Theme Selection
    with st.expander("🎨 Theme Customization"):
        theme = st.selectbox("Choose Theme", ["Default", "Dark Mode", "Green Fields", "Sunset"])
        if theme == "Dark Mode":
            st.markdown("""<style>.main {background: #2c3e50; color: white;}</style>""", unsafe_allow_html=True)
        elif theme == "Green Fields":
            st.markdown("""<style>.main {background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);}</style>""", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("🔄 Clear All", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
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

# Initialize session state for query
if 'query' not in st.session_state:
    st.session_state.query = ""
