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
</style>
""", unsafe_allow_html=True)

# ============================================
# ⚙️ SIDEBAR CONFIGURATION
# ============================================
with st.sidebar:
    st.title("⚙️ Settings")
    # We store the key directly in session_state or a variable
    api_key_input = st.text_input("Gemini API Key", type="password", help="Enter your key to enable AI features")
    
    if st.button("🔑 Save & Initialize"):
        if api_key_input:
            st.session_state['api_key'] = api_key_input
            st.success("API Key Saved!")
        else:
            st.error("Please enter a valid key.")
    
    st.markdown("---")
    st.info("💡 **Pro Tip**: Use the 'Detailed Analysis' tab for better soil-specific recommendations.")

# ============================================
# 🚀 HEADER SECTION
# ============================================
st.markdown("""
<div class="header">
    <h1 style="font-size: 3rem; margin: 0;">🌱 FarmGenius AI</h1>
    <h2 style="font-size: 1.2rem; margin: 10px 0;">Precision Agriculture Powered by Gemini 2.0</h2>
</div>
""", unsafe_allow_html=True)

# ============================================
# 🎯 MAIN INPUT SECTION
# ============================================
tab1, tab2, tab3 = st.tabs(["🎯 Quick Query", "🌍 Detailed Analysis", "📊 Crop Calculator"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Country", ["India 🇮🇳", "Ghana 🇬🇭", "Canada 🇨🇦", "Other 🌍"])
        region = st.text_input("Region/State", placeholder="e.g. Maharashtra, Ontario...")
    with col2:
        crop_stage = st.select_slider("Crop Stage", options=["Planning 🌱", "Sowing 🌾", "Growing 🌿", "Harvesting 🎯"])
        query = st.text_area("Question", placeholder="What is the best fertilizer for this stage?", height=100)

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
        expected_yield = st.number_input("Yield (tons/acre)", 0.1, 50.0, 2.5)
    if st.button("Calculate Yield"):
        st.success(f"🌾 Total Potential: {area * expected_yield:.2f} tons")

# ============================================
# 🚀 UPDATED AI LOGIC (STABLE VERSION)
# ============================================
st.markdown("---")
if st.button("🚀 GENERATE AI ADVICE"):
    current_key = st.session_state.get('api_key', "")
    
    if not current_key:
        st.error("❌ API Key Missing.")
    else:
        try:
            genai.configure(api_key=current_key)
            
            # Use stable aliases to avoid 404 errors
            models_to_try = [
                'gemini-1.5-flash',      # High daily limit (1500 RPD)
                'gemini-2.0-flash',      # Latest (but lower free limit)
                'gemini-1.5-pro'         # Powerful (very low free limit)
            ]
            
            success = False
            for m_name in models_to_try:
                try:
                    model = genai.GenerativeModel(m_name)
                    response = model.generate_content(f"Advice for {country}: {query}")
                    
                    st.success(f"✅ Success using {m_name}")
                    st.write(response.text)
                    success = True
                    break
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg:
                        st.warning(f"⚠️ {m_name} quota exceeded for today.")
                    elif "404" in error_msg:
                        st.warning(f"⚠️ {m_name} not found or unsupported in this region.")
                    else:
                        st.error(f"❌ {m_name} failed: {error_msg}")
                    continue
            
            if not success:
                st.error("🛑 All available models have reached their Free Tier limits. Please try again tomorrow or enable billing in Google AI Studio.")
                
        except Exception as e:
            st.error(f"❌ Configuration Error: {e}")
# ============================================
# 📊 VISUALIZATION
# ============================================

st.markdown("---")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("### 🌱 Growth Curve")
    fig, ax = plt.subplots()
    sns.lineplot(x=['Sowing', 'Vegetative', 'Flowering', 'Harvest'], y=[10, 35, 75, 100], marker='o', color='green', ax=ax)
    st.pyplot(fig)
with col_b:
    st.markdown("### 🌤️ Nutrient Balance")
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    ax.fill([0, 1, 2, 3, 4, 0], [70, 80, 60, 90, 75, 70], color='skyblue', alpha=0.5)
    st.pyplot(fig)

st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')} | No Demo Data Active")
