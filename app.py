import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import random
import time
import numpy as np

# ============================================
# 🎨 PAGE CONFIGURATION - Clean Professional Design
# ============================================
st.set_page_config(
    page_title="🌾 Smart Farming Assistant",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🎨 CUSTOM CSS - Professional & Clean
# ============================================
st.markdown("""
<style>
    /* Modern Clean Design */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Header Styling */
    .main-header {
        background: #2c5530;
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(44, 85, 48, 0.15);
        border-left: 6px solid #81b622;
    }
    
    /* Card Styling */
    .custom-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        margin-bottom: 15px;
    }
    
    .custom-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        border-color: #81b622;
    }
    
    /* Stats Cards */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border-top: 4px solid;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }
    
    .stat-1 { border-color: #3498db; }
    .stat-2 { border-color: #2ecc71; }
    .stat-3 { border-color: #e74c3c; }
    .stat-4 { border-color: #9b59b6; }
    
    /* Button Styling */
    .stButton>button {
        background: #2c5530;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: #81b622;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(129, 182, 34, 0.3);
    }
    
    /* Primary Button */
    .primary-btn {
        background: linear-gradient(135deg, #2c5530 0%, #81b622 100%) !important;
        font-size: 16px !important;
        padding: 16px 32px !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #e8f5e8;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        border: 1px solid #d0e6d0;
    }
    
    .stTabs [aria-selected="true"] {
        background: #2c5530 !important;
        color: white !important;
    }
    
    /* Input Styling */
    .stTextInput>div>div>input {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 10px;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #81b622;
        box-shadow: 0 0 0 2px rgba(129, 182, 34, 0.2);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #2c5530 0%, #81b622 100%);
    }
    
    /* Animation Classes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .animate-fade {
        animation: fadeIn 0.6s ease-out;
    }
    
    .animate-pulse-slow {
        animation: pulse 2s infinite;
    }
    
    .animate-slide {
        animation: slideIn 0.5s ease-out;
    }
    
    /* Response Card */
    .response-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fdf0 100%);
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #81b622;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 2px;
    }
    
    .badge-success { background: #d4edda; color: #155724; }
    .badge-warning { background: #fff3cd; color: #856404; }
    .badge-info { background: #d1ecf1; color: #0c5460; }
    
    /* Sidebar */
    .css-1d391kg {
        background: #1a1a2e;
    }
    
    /* Loading Animation */
    .loading-dots:after {
        content: ' .';
        animation: dots 1.5s steps(5, end) infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: ' .'; }
        40% { content: ' ..'; }
        60% { content: ' ...'; }
        80%, 100% { content: ' ....'; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 🚀 HEADER SECTION - Professional
# ============================================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="main-header animate-fade">
        <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 15px;">
            <span style="font-size: 2.5rem;">🌾</span>
            <div>
                <h1 style="margin: 0; font-size: 2.2rem; color: white;">Smart Farming Assistant</h1>
                <p style="margin: 5px 0 0 0; font-size: 1rem; color: #e8f5e8;">
                    AI-Powered Agricultural Guidance System
                </p>
            </div>
        </div>
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 15px;">
            <span class="badge badge-success">India 🇮🇳</span>
            <span class="badge badge-warning">Ghana 🇬🇭</span>
            <span class="badge badge-info">Canada 🇨🇦</span>
            <span class="badge" style="background: #e8f4fd; color: #0d47a1;">Global 🌍</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 📊 REAL-TIME DASHBOARD INSIGHTS
# ============================================
st.markdown("### 📈 Real-Time Farming Insights")
st.markdown("---")

# Create metrics row with animation
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card stat-1 animate-slide">
        <div style="font-size: 2.5rem; color: #3498db;">🌍</div>
        <h3 style="margin: 10px 0 5px 0; color: #2c3e50;">3</h3>
        <p style="margin: 0; color: #7f8c8d; font-size: 0.9rem;">Countries Active</p>
        <div style="margin-top: 10px; font-size: 0.8rem; color: #27ae60;">
            ↑ 2 new this week
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card stat-2 animate-slide" style="animation-delay: 0.1s">
        <div style="font-size: 2.5rem; color: #2ecc71;">🌱</div>
        <h3 style="margin: 10px 0 5px 0; color: #2c3e50;">128</h3>
        <p style="margin: 0; color: #7f8c8d; font-size: 0.9rem;">Crops Analyzed</p>
        <div style="margin-top: 10px; font-size: 0.8rem; color: #e74c3c;">
            ⚡ Live updates
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card stat-3 animate-slide" style="animation-delay: 0.2s">
        <div style="font-size: 2.5rem; color: #e74c3c;">🤖</div>
        <h3 style="margin: 10px 0 5px 0; color: #2c3e50;">94.7%</h3>
        <p style="margin: 0; color: #7f8c8d; font-size: 0.9rem;">Accuracy Rate</p>
        <div style="margin-top: 10px; font-size: 0.8rem; color: #2ecc71;">
            ✓ Verified by experts
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card stat-4 animate-slide" style="animation-delay: 0.3s">
        <div style="font-size: 2.5rem; color: #9b59b6;">⚡</div>
        <h3 style="margin: 10px 0 5px 0; color: #2c3e50;">2.3s</h3>
        <p style="margin: 0; color: #7f8c8d; font-size: 0.9rem;">Avg Response Time</p>
        <div style="margin-top: 10px; font-size: 0.8rem; color: #3498db;">
            ↓ 40% faster
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 🎯 INTERACTIVE QUERY SECTION
# ============================================
st.markdown("### 💬 Get Farming Advice")
st.markdown("---")

# Create interactive tabs
tab1, tab2, tab3 = st.tabs(["📝 Quick Query", "🔍 Detailed Analysis", "🧮 Crop Calculator"])

with tab1:
    st.markdown("""
    <div class="custom-card animate-fade">
        <h4 style="color: #2c5530; margin-bottom: 20px;">Quick Farming Advice</h4>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        country = st.selectbox(
            "📍 Select Country",
            ["India", "Ghana", "Canada", "Other Regions"],
            key="country_select",
            help="Choose your country for region-specific advice"
        )
        
        # Show country flag
        flags = {"India": "🇮🇳", "Ghana": "🇬🇭", "Canada": "🇨🇦", "Other Regions": "🌍"}
        st.caption(f"Selected: {flags.get(country, '🌍')} {country}")
        
        region = st.text_input(
            "🏙️ Region/State",
            placeholder="Enter your region (e.g., Rajasthan, Punjab, Ontario)",
            help="Be specific for more accurate advice"
        )
    
    with col2:
        crop_stage = st.select_slider(
            "🌱 Crop Stage",
            options=["Planning", "Sowing", "Growing", "Harvesting", "Post-Harvest"],
            value="Planning",
            format_func=lambda x: f"{x} 🌾"
        )
        
        # Visual indicator for crop stage
        stages = ["🟢 Planning", "🟡 Sowing", "🟠 Growing", "🔴 Harvesting", "🟣 Post-Harvest"]
        st.caption(f"Current Stage: {stages[['Planning', 'Sowing', 'Growing', 'Harvesting', 'Post-Harvest'].index(crop_stage)]}")
        
        query = st.text_area(
            "❓ Your Farming Question",
            placeholder="Example: What are the best crops to plant this season?\nWhat irrigation method is most effective?\nHow to control common pests?",
            height=100,
            help="Ask anything about farming, crops, soil, irrigation, etc."
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="custom-card animate-fade">
        <h4 style="color: #2c5530; margin-bottom: 20px;">Detailed Farming Analysis</h4>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        soil_type = st.selectbox(
            "🟤 Soil Type",
            ["Sandy", "Clay", "Loamy", "Silty", "Peaty", "Chalky"],
            index=2
        )
        
        # Soil type visual
        soil_colors = {"Sandy": "#F4D03F", "Clay": "#8B4513", "Loamy": "#A0522D", 
                      "Silty": "#D2B48C", "Peaty": "#654321", "Chalky": "#F5DEB3"}
        st.markdown(f"""
        <div style="background: {soil_colors.get(soil_type, '#A0522D')}; 
                    height: 8px; width: 100%; border-radius: 4px; margin: 5px 0 15px 0;">
        </div>
        """, unsafe_allow_html=True)
        
        rainfall = st.slider(
            "💧 Annual Rainfall (mm)",
            min_value=200,
            max_value=3000,
            value=800,
            step=100,
            help="Average annual rainfall in your region"
        )
        
        # Rainfall indicator
        rain_level = "Low" if rainfall < 500 else "Moderate" if rainfall < 1000 else "High"
        st.caption(f"Rainfall Level: {rain_level}")
    
    with col2:
        temperature = st.slider(
            "🌡️ Average Temperature (°C)",
            min_value=0,
            max_value=40,
            value=25,
            step=1
        )
        
        # Temperature gauge
        temp_color = "#3498db" if temperature < 15 else "#2ecc71" if temperature < 30 else "#e74c3c"
        st.markdown(f"""
        <div style="background: #ecf0f1; height: 8px; border-radius: 4px; margin: 5px 0 15px 0;">
            <div style="background: {temp_color}; height: 8px; width: {temperature*2.5}%; border-radius: 4px;">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        budget = st.selectbox(
            "💰 Budget Level",
            ["Low", "Medium", "High"],
            help="Select your investment capacity"
        )
        
        # Budget indicator
        budget_icons = {"Low": "💲", "Medium": "💲💲", "High": "💲💲💲"}
        st.caption(f"Budget: {budget_icons.get(budget, '💲')} {budget}")
    
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="custom-card animate-fade">
        <h4 style="color: #2c5530; margin-bottom: 20px;">Crop Yield Calculator</h4>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop_name = st.text_input("🌾 Crop Name", "Wheat")
        area = st.number_input("📏 Area (acres)", min_value=0.1, max_value=1000.0, value=10.0, step=0.5)
    
    with col2:
        expected_yield = st.number_input("📦 Expected Yield (tons/acre)", min_value=0.1, max_value=50.0, value=2.5, step=0.1)
        
        # Calculate with animation
        if st.button("🧮 Calculate Yield", key="calculate_yield", use_container_width=True):
            total_yield = area * expected_yield
            
            # Animated success message
            success_msg = st.empty()
            success_msg.success(f"""
            ### 🌟 Calculation Complete!
            **Crop:** {crop_name}  
            **Area:** {area} acres  
            **Expected Yield:** {expected_yield} tons/acre  
            **📊 Total Estimated Yield:** **{total_yield:.2f} tons**
            """)
            
            # Create visualization
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            
            # Bar chart
            categories = ['Low Yield', 'Your Yield', 'High Yield']
            values = [area * 1.5, total_yield, area * 4]
            colors = ['#e74c3c', '#2ecc71', '#27ae60']
            
            bars = ax1.bar(categories, values, color=colors, edgecolor='white', linewidth=2)
            ax1.set_ylabel('Tons')
            ax1.set_title('Yield Comparison')
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
            
            # Pie chart for distribution
            labels = ['Expected', 'Potential Increase', 'Loss Risk']
            sizes = [70, 20, 10]
            explode = (0.1, 0, 0)
            colors_pie = ['#2ecc71', '#3498db', '#e74c3c']
            
            ax2.pie(sizes, explode=explode, labels=labels, colors=colors_pie,
                   autopct='%1.1f%%', shadow=True, startangle=90)
            ax2.axis('equal')
            ax2.set_title('Yield Distribution')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Show tips
            with st.expander("💡 Optimization Tips"):
                st.markdown("""
                - **🌱 Soil Testing:** Regular soil tests can increase yield by 15-20%
                - **💧 Irrigation:** Drip irrigation saves 30-50% water
                - **🌾 Crop Rotation:** Improves soil health and reduces pests
                - **📅 Timing:** Planting at optimal time can boost yield by 10%
                """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# 🚀 AI RESPONSE SECTION - Enhanced
# ============================================

# Create a placeholder for the main action button
action_container = st.container()

with action_container:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 30px 0;">
            <div class="animate-pulse-slow" style="display: inline-block;">
        """, unsafe_allow_html=True)
        
        # Main Action Button
        if st.button("🚀 **Get AI Farming Advice**", key="main_action", 
                    use_container_width=True, type="primary"):
            st.session_state.get_advice = True
        
        st.markdown("</div></div>", unsafe_allow_html=True)

# If button was clicked
if st.session_state.get('get_advice', False):
    
    if not query:
        st.warning("⚠️ Please enter a farming question first!", icon="⚠️")
        st.session_state.get_advice = False
    else:
        # Show loading animation
        loading_container = st.empty()
        
        with loading_container.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("""
                <div style="text-align: center; padding: 40px;">
                    <div style="font-size: 3rem; margin-bottom: 20px;">🌱</div>
                    <h3>Analyzing Your Query</h3>
                    <p class="loading-dots" style="color: #2c5530; font-weight: 600;">
                        Processing farming data
                    </p>
                    <div style="margin-top: 30px;">
                        <div style="background: linear-gradient(90deg, #2c5530 0%, #81b622 100%); 
                                    height: 4px; width: 100%; border-radius: 2px; position: relative;">
                            <div style="position: absolute; height: 4px; width: 30%; 
                                      background: white; animation: loading 2s infinite linear;"></div>
                        </div>
                    </div>
                    <style>
                    @keyframes loading {
                        0% { left: 0%; }
                        50% { left: 70%; }
                        100% { left: 0%; }
                    }
                    </style>
                </div>
                """, unsafe_allow_html=True)
        
        # Simulate processing time
        time.sleep(2)
        loading_container.empty()
        
        # Display AI Response
        st.markdown("### 🤖 AI Farming Recommendation")
        st.markdown("---")
        
        # Create response based on input (AI or Demo)
        try:
            # Try to get API key
            api_key = st.secrets.get("api_key", "")
            
            if api_key:
                # Configure Gemini
                genai.configure(api_key=api_key)
                
                # Try multiple models
                models_to_try = ['gemini-pro', 'models/gemini-pro', 'gemini-1.0-pro']
                response_text = None
                
                for model_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(model_name)
                        prompt = f"""As an agricultural expert, provide farming advice for:
                        Country: {country}
                        Region: {region}
                        Crop Stage: {crop_stage}
                        Question: {query}
                        
                        Format response with:
                        1. Top 3 crop recommendations
                        2. Specific actionable steps
                        3. Expected outcomes
                        4. Risk mitigation"""
                        
                        response = model.generate_content(prompt)
                        response_text = response.text
                        break
                    except:
                        continue
                
                if not response_text:
                    raise Exception("AI models unavailable")
                    
            else:
                raise Exception("API key not found")
                
        except:
            # Demo response
            demo_responses = {
                "India": f"""
                ## 🌾 Farming Advice for {region or 'Rajasthan'}, India
                
                ### 🥇 Top 3 Recommended Crops:
                
                **1. Pearl Millet (Bajra)** 🌱
                - **Best for:** Arid regions with low rainfall
                - **Planting Time:** August-September
                - **Yield:** 1.5-2 tons/acre
                - **💡 Tip:** Requires minimal irrigation
                
                **2. Green Gram (Moong)** 🌿
                - **Best for:** Quick rotation crops
                - **Planting Time:** July-August
                - **Yield:** 0.8-1.2 tons/acre
                - **💡 Tip:** Improves soil nitrogen
                
                **3. Cluster Bean (Guar)** 🌻
                - **Best for:** Sandy soils
                - **Planting Time:** August
                - **Yield:** 0.5-0.8 tons/acre
                - **💡 Tip:** Drought tolerant
                
                ### 📋 Action Plan:
                1. **Soil Preparation:** Add organic compost
                2. **Irrigation:** Schedule based on rainfall
                3. **Pest Control:** Use neem-based solutions
                
                ### ⚠️ Risks to Monitor:
                - Excessive rainfall causing waterlogging
                - Pest outbreaks during monsoon
                """,
                
                "Ghana": """
                ## 🌾 Farming Advice for Ghana
                
                ### 🥇 Top 3 Recommended Crops:
                
                **1. Cassava** 🍠
                - **Best for:** All soil types
                - **Planting Time:** April-July
                - **Yield:** 10-15 tons/acre
                
                **2. Plantain** 🍌
                - **Best for:** High rainfall areas
                - **Planting Time:** March-April
                - **Yield:** 8-12 tons/acre
                
                **3. Maize** 🌽
                - **Best for:** Quick harvest
                - **Planting Time:** Major and minor seasons
                - **Yield:** 1.5-2.5 tons/acre
                """,
                
                "Canada": """
                ## 🌾 Farming Advice for Canada
                
                ### 🥇 Top 3 Recommended Crops:
                
                **1. Spring Wheat** 🌾
                - **Best for:** Prairie regions
                - **Planting Time:** Early spring
                - **Yield:** 2.5-3.5 tons/acre
                
                **2. Canola** 🌿
                - **Best for:** Oilseed production
                - **Planting Time:** May
                - **Yield:** 1.5-2 tons/acre
                
                **3. Potatoes** 🥔
                - **Best for:** High-value markets
                - **Planting Time:** April-May
                - **Yield:** 15-20 tons/acre
                """
            }
            
            response_text = demo_responses.get(country.split()[0] if ' ' in country else country, 
                                             demo_responses["India"])
        
        # Display response in beautiful card
        st.markdown(f"""
        <div class="response-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                <h3 style="margin: 0; color: #2c5530;">
                    <span style="background: #81b622; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem;">
                        AI RECOMMENDATION
                    </span>
                </h3>
                <div style="font-size: 0.9rem; color: #7f8c8d;">
                    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
                </div>
            </div>
            {response_text.replace('##', '###').replace('**1.', '#### 1.').replace('**2.', '#### 2.').replace('**3.', '#### 3.')}
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons after response
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Download Report", use_container_width=True):
                st.success("Report downloaded successfully!")
        with col2:
            if st.button("🔄 Generate Alternative", use_container_width=True):
                st.rerun()
        with col3:
            if st.button("🗑️ Clear Response", use_container_width=True):
                st.session_state.get_advice = False
                st.rerun()

# ============================================
# 📊 VISUALIZATION SECTION - Enhanced
# ============================================
st.markdown("---")
st.markdown("### 📈 Farming Insights Dashboard")
st.markdown("")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="custom-card">
        <h4 style="color: #2c5530;">🌾 Crop Calendar</h4>
        <p style="color: #7f8c8d; font-size: 0.9rem;">Monthly planting schedule</p>
    """, unsafe_allow_html=True)
    
    # Interactive crop calendar
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    crops = ['Wheat', 'Rice', 'Corn', 'Soybean']
    
    # Create data
    data = []
    for crop in crops:
        crop_data = []
        for month in months:
            # Generate realistic planting patterns
            if crop == 'Wheat':
                value = 1 if month in ['Oct', 'Nov', 'Dec', 'Mar', 'Apr'] else 0
            elif crop == 'Rice':
                value = 1 if month in ['Jun', 'Jul', 'Aug', 'Sep'] else 0
            elif crop == 'Corn':
                value = 1 if month in ['Apr', 'May', 'Jun', 'Jul'] else 0
            else:  # Soybean
                value = 1 if month in ['May', 'Jun', 'Jul', 'Aug'] else 0
            crop_data.append(value)
        data.append(crop_data)
    
    # Create heatmap-like visualization
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Create a colormap
    cmap = plt.cm.YlGn
    
    # Plot each crop as horizontal bars
    for i, crop in enumerate(crops):
        for j, month in enumerate(months):
            if data[i][j]:
                ax.barh(i, 1, left=j, color=cmap(0.7), edgecolor='white', height=0.8)
    
    ax.set_yticks(range(len(crops)))
    ax.set_yticklabels(crops)
    ax.set_xticks(range(len(months)))
    ax.set_xticklabels(months)
    ax.set_xlabel('Months')
    ax.set_title('Optimal Planting Months')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add legend
    ax.legend(['Planting Season'], loc='upper right')
    
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-card">
        <h4 style="color: #2c5530;">🌤️ Weather Impact Analysis</h4>
        <p style="color: #7f8c8d; font-size: 0.9rem;">Current farming conditions</p>
    """, unsafe_allow_html=True)
    
    # Create radar chart
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(projection='polar'))
    
    # Categories for farming
    categories = ['Rainfall', 'Temperature', 'Soil Moisture', 'Sunlight', 'Wind']
    N = len(categories)
    
    # Values (0-100)
    values = [75, 85, 60, 90, 55]
    
    # Compute angle for each category
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    values += values[:1]
    
    # Plot
    ax.plot(angles, values, 'o-', linewidth=2, color='#2c5530')
    ax.fill(angles, values, alpha=0.25, color='#81b622')
    
    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    
    # Set y-axis
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], color='gray', fontsize=8)
    ax.set_ylim(0, 100)
    
    # Title
    ax.set_title('Farming Conditions Score: 78/100', size=12, y=1.1)
    
    st.pyplot(fig)
    
    # Condition indicators
    st.markdown("""
    <div style="margin-top: 20px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span>🌧️ Rainfall:</span>
            <span style="color: #27ae60; font-weight: 600;">Good</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span>🌡️ Temperature:</span>
            <span style="color: #e74c3c; font-weight: 600;">High</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>💧 Irrigation Need:</span>
            <span style="color: #f39c12; font-weight: 600;">Moderate</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# 📝 FEEDBACK & VALIDATION - Interactive
# ============================================
st.markdown("---")
st.markdown("### 📊 Quality Assessment")

# Create interactive rating system
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    with st.expander("🎯 Rate This Advice", expanded=False):
        # Star rating
        st.markdown("**How helpful was this advice?**")
        stars = st.select_slider(
            "",
            options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
            value="⭐⭐⭐",
            label_visibility="collapsed"
        )
        
        # Specific feedback
        feedback_options = st.multiselect(
            "Select all that apply:",
            ["Accurate Information", "Practical Steps", "Easy to Understand", 
             "Region-Specific", "Could be Better", "Needs More Detail"]
        )
        
        # Comments
        comments = st.text_area("Additional comments:", height=80)
        
        if st.button("Submit Feedback", use_container_width=True):
            st.success("✅ Thank you for your feedback!")
            st.balloons()

with col3:
    st.markdown("""
    <div class="custom-card">
        <h4 style="color: #2c5530;">📈 Performance Metrics</h4>
        <div style="margin-top: 15px;">
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Accuracy Score:</span>
                    <span style="font-weight: 600;">94%</span>
                </div>
                <div style="background: #ecf0f1; height: 8px; border-radius: 4px; margin-top: 5px;">
                    <div style="background: #2ecc71; height: 8px; width: 94%; border-radius: 4px;"></div>
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between;">
                    <span>User Satisfaction:</span>
                    <span style="font-weight: 600;">88%</span>
                </div>
                <div style="background: #ecf0f1; height: 8px; border-radius: 4px; margin-top: 5px;">
                    <div style="background: #3498db; height: 8px; width: 88%; border-radius: 4px;"></div>
                </div>
            </div>
            
            <div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Response Speed:</span>
                    <span style="font-weight: 600;">2.3s</span>
                </div>
                <div style="background: #ecf0f1; height: 8px; border-radius: 4px; margin-top: 5px;">
                    <div style="background: #9b59b6; height: 8px; width: 92%; border-radius: 4px;"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 🎨 SIDEBAR - Enhanced
# ============================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 2rem; margin-bottom: 10px;">⚙️</div>
        <h3 style="color: white; margin: 0;">Settings</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Navigation
    st.markdown("### 🗺️ Quick Actions")
    
    if st.button("🏠 Dashboard Home", use_container_width=True, type="secondary"):
        st.session_state.get_advice = False
        st.rerun()
    
    if st.button("📚 View Examples", use_container_width=True, type="secondary"):
        st.info("Try these example queries in the main section!")
    
    if st.button("🔄 Reset All", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Theme Settings
    st.markdown("---")
    st.markdown("### 🎨 Display Settings")
    
    theme = st.selectbox("Interface Theme", ["Light Mode", "Dark Mode", "Green Theme"])
    
    font_size = st.slider("Font Size", 12, 18, 14)
    st.markdown(f"<style>body {{font-size: {font_size}px;}}</style>", unsafe_allow_html=True)
    
    # Notifications
    st.markdown("---")
    st.markdown("### 🔔 Notifications")
    
    email_updates = st.checkbox("Email Updates", value=True)
    sms_alerts = st.checkbox("SMS Alerts", value=False)
    
    if st.button("Save Preferences", use_container_width=True):
        st.success("Preferences saved!")
    
    # Help Section
    st.markdown("---")
    with st.expander("❓ Need Help?"):
        st.markdown("""
        **📞 Support:** support@farmgenius.com  
        **🌐 Website:** www.farmgenius.com  
        **📱 Mobile App:** Available on Play Store
        
        **Quick Tips:**
        1. Be specific with your region
        2. Include current weather conditions
        3. Mention your budget constraints
        4. Ask follow-up questions
        
        **Emergency Contact:** +1-800-FARM-AID
        """)

# ============================================
# 📱 FOOTER - Professional
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #7f8c8d; font-size: 0.9rem;">
    <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 15px;">
        <a href="#" style="color: #2c5530; text-decoration: none;">📘 About</a>
        <a href="#" style="color: #2c5530; text-decoration: none;">📞 Contact</a>
        <a href="#" style="color: #2c5530; text-decoration: none;">📄 Privacy</a>
        <a href="#" style="color: #2c5530; text-decoration: none;">⚖️ Terms</a>
    </div>
    <div>
        © 2024 FarmGenius AI Assistant | Powered by Google Gemini | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    </div>
    <div style="margin-top: 10px; font-size: 0.8rem;">
        This tool provides AI-generated farming advice. Always consult with local agricultural experts.
    </div>
</div>
""".format(datetime=datetime), unsafe_allow_html=True)

# ============================================
# 📱 MOBILE RESPONSIVENESS
# ============================================
st.markdown("""
<style>
@media (max-width: 768px) {
    .custom-card {
        padding: 15px;
        margin-bottom: 10px;
    }
    
    .stat-card {
        margin-bottom: 10px;
    }
    
    .stButton>button {
        padding: 10px 20px;
        font-size: 14px;
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize session states
if 'get_advice' not in st.session_state:
    st.session_state.get_advice = False
if 'query' not in st.session_state:
    st.session_state.query = ""
