import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ============================================
# 🎨 PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="🌱 FarmGenius AI Assistant",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🎨 CUSTOM CSS
# ============================================
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; border-radius: 20px; }
    .header { background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    .card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin: 10px 0; text-align: center; }
    .stButton>button { background: linear-gradient(90deg, #00b09b 0%, #96c93d 100%); color: white; border: none; padding: 15px 30px; border-radius: 50px; font-weight: bold; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 20px rgba(0,176,155,0.4); }
</style>
""", unsafe_allow_html=True)

# ============================================
# 🚀 HEADER SECTION
# ============================================
st.markdown("""
<div class="header">
    <h1 style="font-size: 3rem; margin: 0;">🌱 FarmGenius AI</h1>
    <h2 style="font-size: 1.2rem; margin: 10px 0;">Live Precision Agriculture Assistant</h2>
</div>
""", unsafe_allow_html=True)

# ============================================
# 📊 TOP METRICS
# ============================================
col1, col2, col3, col4 = st.columns(4)
metrics = [("🌍", "Global", "Support"), ("🌾", "50+", "Crops"), ("🤖", "2.0 Flash", "Model"), ("⚡", "Live", "Status")]
for col, (icon, val, txt) in zip([col1, col2, col3, col4], metrics):
    col.markdown(f'<div class="card"><h3>{icon}</h3><h2>{val}</h2><p>{txt}</p></div>', unsafe_allow_html=True)

# ============================================
# 🎯 MAIN INPUT SECTION
# ============================================
st.markdown('<div style="background: #667eea; padding: 20px; border-radius: 20px; color: white; margin-top: 20px;">', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["🎯 Quick Query", "🌍 Detailed Analysis", "📊 Crop Calculator"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Country", ["India 🇮🇳", "Ghana 🇬🇭", "Canada 🇨🇦", "Other 🌍"])
        region = st.text_input("Region/State", placeholder="e.g. Punjab, Ontario...")
    with col2:
        crop_stage = st.select_slider("Crop Stage", options=["Planning 🌱", "Sowing 🌾", "Growing 🌿", "Harvesting 🎯"])
        query = st.text_area("Question", placeholder="How do I optimize yield for this season?", height=100)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        soil_type = st.selectbox("Soil Type", ["Sandy", "Clay", "Loamy", "Silty"])
        rainfall = st.slider("Rainfall (mm)", 200, 3000, 800)
    with col2:
        temperature = st.slider("Temp (°C)", 0, 50, 25)
        budget = st.selectbox("Budget", ["Low", "Medium", "High"])

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input("Area (acres)", 0.1, 1000.0, 10.0)
    with col2:
        expected_yield = st.number_input("Yield (tons/acre)", 0.1, 50.0, 2.5)
    if st.button("Calculate Total Potential"):
        st.success(f"🌾 Estimated Yield: {area * expected_yield:.2f} tons")

# ============================================
# 🚀 LIVE AI LOGIC (NO DEMO)
# ============================================
st.markdown("---")
if st.button("🚀 GENERATE AI ADVICE"):
    api_key = st.sidebar.get('api_key_input') # Logic to get from sidebar
    
    # Check if API Key is present in sidebar or session state
    current_key = st.session_state.get('api_key', "")
    
    if not current_key:
        st.error("❌ API Key Missing! Please enter your Gemini API Key in the sidebar settings.")
    else:
        genai.configure(api_key=current_key)
        # Prioritizing the latest models
        models_to_try = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-pro']
        
        success = False
        with st.spinner("🧠 Analyzing soil and climate data..."):
            for m_name in models_to_try:
                try:
                    model = genai.GenerativeModel(m_name)
                    full_prompt = f"""
                    Act as a senior Agronomist.
                    Location: {country}, {region}. 
                    Context: Stage={crop_stage}, Soil={soil_type if 'soil_type' in locals() else 'Standard'}, 
                    Temp={temperature if 'temperature' in locals() else '25'}C.
                    User Inquiry: {query}
                    Provide: 1. Actionable Steps 2. Scientific Reasoning 3. Risk Mitigation.
                    """
                    response = model.generate_content(full_prompt)
                    
                    st.markdown(f"### 🤖 AI Advice ({m_name})")
                    st.info(response.text)
                    
                    st.download_button("📥 Save Advice", response.text, file_name="farm_advice.txt")
                    success = True
                    break
                except Exception as e:
                    continue
            
            if not success:
                st.error("❌ Connection Error: Unable to reach AI models. Please check your API key and internet connection.")

# ============================================
# 📊 VISUALIZATION
# ============================================
st.markdown("---")
st.markdown("## 📊 Field Analytics")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("### 🌱 Growth Projection")
    fig, ax = plt.subplots()
    sns.lineplot(x=['Sowing', 'Vegetative', 'Flowering', 'Harvest'], y=[10, 40, 80, 100], marker='o', ax=ax)
    st.pyplot(fig)
with col_b:
    st.markdown("### 🌤️ Parameter Balance")
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    ax.fill([0, 1, 2, 3, 4, 0], [80, 70, 90, 60, 85, 80], alpha=0.3)
    st.pyplot(fig)

# ============================================
# ⚙️ SIDEBAR
# ============================================
with st.sidebar:
    st.title("⚙️ Configuration")
    api_input = st.text_input("Gemini API Key", type="password")
    if st.button("🔑 Save Key"):
        st.session_state['api_key'] = api_input
        st.success("Key updated!")
    
    st.markdown("---")
    st.info("💡 **Pro Tip**: Provide specific soil details for better pest-control advice.")

# Footer
st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')} | System Online")
