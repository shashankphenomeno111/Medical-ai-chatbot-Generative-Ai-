# Medical AI Chatbot - Streamlit V8 Ultimate
# Enhanced: Creative Sidebar, Browser Voice, Clear Cache, Bullet Points

import streamlit as st
from chatbot import get_chatbot, MedicalInfo, SYMPTOM_DATABASE
from config import DISCLAIMER
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="🏥 Medical AI V8",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultimate CSS with Creative Sidebar Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background: linear-gradient(135deg, #0d1117 0%, #1a1f2e 100%); color: #c9d1d9; }
    
    .mega-title {
        font-size: 3.5rem; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, #00ff88, #00d4ff, #a855f7, #ff6b6b);
        background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: flow 5s ease infinite; margin-top: -20px;
    }
    @keyframes flow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    
    .subtitle { text-align: center; color: #8b949e; letter-spacing: 1px; margin-bottom: 2rem; }
    
    .glass-card {
        background: rgba(22, 27, 34, 0.9); 
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    .glass-card:hover { 
        border-color: #00ff88; 
        box-shadow: 0 0 25px rgba(0, 255, 136, 0.3);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    .section-title { font-weight: 700; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 10px; font-size: 1.1rem; }
    .title-sym { color: #f97316; } .title-cau { color: #a855f7; } .title-tre { color: #22c55e; } 
    .title-pre { color: #06b6d4; } .title-ove { color: #3b82f6; }
    
    .section-content { line-height: 1.8; white-space: pre-line; }
    
    .disease-header {
        font-size: 2.5rem; font-weight: 800; 
        background: linear-gradient(90deg, #00ff88, #00d4ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0,255,136,0.3);
    }
    
    /* Creative Sidebar */
    section[data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #0a0f1a 0%, #1a1f35 50%, #0f1420 100%) !important; 
        border-right: 1px solid rgba(0,255,136,0.2);
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,212,255,0.1)) !important;
        border: 1px solid rgba(0,255,136,0.3) !important;
        color: #00ff88 !important;
        transition: all 0.3s ease !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #00ff88, #00d4ff) !important;
        color: #000 !important;
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0,255,136,0.4);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(168,85,247,0.15));
        border: 1px solid rgba(0,255,136,0.3);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sidebar-section {
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-left: 3px solid #00ff88;
    }
    
    /* Voice Button */
    .voice-btn {
        background: linear-gradient(135deg, #8b5cf6, #ec4899) !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 25px !important;
        color: white !important;
        font-weight: 600 !important;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .voice-btn:hover { transform: scale(1.05); box-shadow: 0 0 20px rgba(139,92,246,0.5); }
    
    /* Emergency Pulse */
    .emergency-pulse {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.1));
        border: 2px solid #ef4444; border-radius: 12px;
        padding: 1rem; animation: pulse 2s infinite; margin-bottom: 1rem;
    }
    @keyframes pulse { 0%, 100% { opacity: 1; box-shadow: 0 0 20px rgba(239,68,68,0.3); } 50% { opacity: 0.7; box-shadow: 0 0 40px rgba(239,68,68,0.6); } }
    
    /* Clear Cache Button */
    .clear-btn {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        border: none !important;
        color: white !important;
    }
    
    /* Related Diseases Buttons - Colorful Hover */
    .stMainBlockContainer .stButton > button {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
        color: #94a3b8 !important;
        transition: all 0.3s ease !important;
        border-radius: 10px !important;
    }
    
    .stMainBlockContainer .stButton > button:hover {
        background: linear-gradient(135deg, #8b5cf6, #ec4899, #f97316) !important;
        background-size: 200% 200% !important;
        animation: gradient-shift 2s ease infinite !important;
        border: 1px solid transparent !important;
        color: #fff !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
</style>
""", unsafe_allow_html=True)

# Browser Voice Input Component - Auto-triggers search via URL
VOICE_INPUT_HTML = """
<div style="text-align: center; padding: 10px;">
    <button id="voiceBtn" onclick="startVoice()" style="
        background: linear-gradient(135deg, #8b5cf6, #ec4899);
        border: none; padding: 15px 30px; border-radius: 30px;
        color: white; font-weight: 600; font-size: 16px;
        cursor: pointer; transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(139,92,246,0.4);
    ">
        🎤 Click to Speak
    </button>
    <p id="voiceStatus" style="color: #8b949e; margin-top: 10px; font-size: 14px;"></p>
</div>

<script>
function startVoice() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        document.getElementById('voiceStatus').innerHTML = '❌ Use Chrome/Edge for voice';
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    
    document.getElementById('voiceBtn').innerHTML = '🔴 Listening...';
    document.getElementById('voiceBtn').style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
    document.getElementById('voiceStatus').innerHTML = '🎙️ Speak now...';
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('voiceStatus').innerHTML = '✅ Searching: <strong>' + transcript + '</strong>';
        
        // Redirect to trigger search with query parameter
        const currentUrl = window.parent.location.href.split('?')[0];
        window.parent.location.href = currentUrl + '?voice_query=' + encodeURIComponent(transcript);
    };
    
    recognition.onerror = function(event) {
        document.getElementById('voiceStatus').innerHTML = '❌ Error: ' + event.error;
        document.getElementById('voiceBtn').innerHTML = '🎤 Click to Speak';
        document.getElementById('voiceBtn').style.background = 'linear-gradient(135deg, #8b5cf6, #ec4899)';
    };
    
    recognition.onend = function() {
        document.getElementById('voiceBtn').innerHTML = '🎤 Click to Speak';
        document.getElementById('voiceBtn').style.background = 'linear-gradient(135deg, #8b5cf6, #ec4899)';
    };
    
    recognition.start();
}
</script>
"""


def init_session():
    if 'history' not in st.session_state: st.session_state.history = []
    if 'chatbot' not in st.session_state: st.session_state.chatbot = None
    if 'pending' not in st.session_state: st.session_state.pending = None


def get_bot():
    if st.session_state.chatbot is None: st.session_state.chatbot = get_chatbot()
    return st.session_state.chatbot


def display_medical_card(info: MedicalInfo):
    """V8 Professional Medical Information Card with Bullet Points"""
    
    if info.is_emergency:
        st.markdown('<div class="emergency-pulse">🚨 <strong>EMERGENCY WARNING</strong>: Seek immediate professional help!</div>', unsafe_allow_html=True)
    
    head_col, pdf_col = st.columns([5, 1])
    with head_col: st.markdown(f'<div class="disease-header">{info.title}</div>', unsafe_allow_html=True)
    with pdf_col:
        pdf_data = get_bot().generate_pdf(info)
        st.download_button("📥 PDF", pdf_data, f"{info.title}_Report.pdf", "application/pdf", key=f"pdf_{info.title}")
    
    # Image & Overview
    c1, c2 = st.columns([1, 2.5])
    with c1:
        if info.image_url:
            st.image(info.image_url, caption="Medical Illustration", use_container_width=True)
        else:
            st.info("🖼️ Image loading...")
    with c2:
        st.markdown(f'<div class="glass-card"><div class="section-title title-ove">📄 Overview</div><div class="section-content">{info.summary}</div></div>', unsafe_allow_html=True)
    
    # Grid with Bullet Points
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f'<div class="glass-card"><div class="section-title title-sym">🤒 Symptoms</div><div class="section-content">{info.symptoms}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="glass-card"><div class="section-title title-tre">💊 Treatment & Remedies</div><div class="section-content">{info.treatment}</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="glass-card"><div class="section-title title-cau">🔬 Causes</div><div class="section-content">{info.causes}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="glass-card"><div class="section-title title-pre">🛡️ Prevention Tips</div><div class="section-content">{info.prevention}</div></div>', unsafe_allow_html=True)
    
    # Related
    if info.related_conditions:
        st.markdown("**🔗 Related Conditions:**")
        cols = st.columns(min(len(info.related_conditions), 5))
        for i, cond in enumerate(info.related_conditions[:5]):
            with cols[i]:
                if st.button(cond, key=f"rel_{info.title}_{i}", use_container_width=True):
                    st.session_state.pending = cond
                    st.rerun()


def main():
    init_session()
    bot = get_bot()
    
    # Handle voice query from URL parameter
    query_params = st.query_params
    voice_query = query_params.get('voice_query') or query_params.get('voice')
    if voice_query:
        st.query_params.clear()  # Clear the param
        st.session_state.pending = voice_query
    
    # Creative Sidebar
    with st.sidebar:
        # Header
        st.markdown("""
        <div class="sidebar-header">
            <div style="font-size: 1.8rem; font-weight: 800; background: linear-gradient(90deg, #00ff88, #00d4ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🏥 MediBot V8
            </div>
            <div style="color: #8b949e; font-size: 0.9rem;">Ultimate Medical Encyclopedia</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice Search Section - Reliable Solution
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("#### 🎤 Voice Search")
        
        # HTML Voice Component that actually works
        voice_html = """
        <div style="text-align: center;">
            <button id="voiceBtn" onclick="startVoice()" style="
                background: linear-gradient(135deg, #8b5cf6, #ec4899);
                border: none; padding: 12px 20px; border-radius: 25px;
                color: white; font-weight: 600; font-size: 14px;
                cursor: pointer; width: 100%; margin-bottom: 8px;
            ">🎤 Click to Speak</button>
            <div id="voiceResult" style="color: #00ff88; font-size: 14px; min-height: 20px; font-weight: bold;"></div>
        </div>
        <script>
        function startVoice() {
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                document.getElementById('voiceResult').innerHTML = '❌ Use Chrome/Edge';
                return;
            }
            const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
            const r = new SR();
            r.lang = 'en-US';
            document.getElementById('voiceBtn').innerHTML = '🔴 Listening...';
            document.getElementById('voiceResult').innerHTML = '🎙️ Speak now...';
            r.onresult = (e) => {
                const text = e.results[0][0].transcript;
                document.getElementById('voiceResult').innerHTML = '✅ ' + text;
                document.getElementById('voiceBtn').innerHTML = '🎤 Click to Speak';
                navigator.clipboard.writeText(text);
            };
            r.onerror = () => { document.getElementById('voiceBtn').innerHTML = '🎤 Click to Speak'; };
            r.onend = () => { document.getElementById('voiceBtn').innerHTML = '🎤 Click to Speak'; };
            r.start();
        }
        </script>
        """
        components.html(voice_html, height=80)
        
        # Text input + Search button (user pastes with Ctrl+V or types)
        voice_text = st.text_input("Type or paste (Ctrl+V):", key="voice_input", placeholder="Paste voice result here...")
        if st.button("🚀 Search Now", key="voice_search_btn", use_container_width=True):
            if voice_text.strip():
                st.session_state.pending = voice_text.strip()
                st.rerun()
        
        st.caption("💡 Voice copies to clipboard. Paste with Ctrl+V")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Search History
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("#### 📜 Recent Searches")
        hist = bot.get_search_history()
        if hist:
            for h in reversed(hist[-5:]):
                if st.button(f"🔍 {h}", key=f"hist_{h}", use_container_width=True):
                    st.session_state.pending = h
                    st.rerun()
        else:
            st.caption("No searches yet")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Access - Categorized
        st.markdown("#### 🚀 Quick Access")
        
        with st.expander("🦠 Infectious Diseases", expanded=True):
            diseases = ["COVID-19", "Ebola", "Malaria", "Dengue", "Typhoid", "Influenza", "Tuberculosis", "HIV/AIDS"]
            c1, c2 = st.columns(2)
            for i, d in enumerate(diseases):
                with (c1 if i % 2 == 0 else c2):
                    if st.button(d, key=f"inf_{d}", use_container_width=True): st.session_state.pending = d; st.rerun()
        
        with st.expander("❤️ Heart & Blood", expanded=False):
            diseases = ["Heart Attack", "Stroke", "Hypertension", "Anemia", "Leukemia", "Angina"]
            c1, c2 = st.columns(2)
            for i, d in enumerate(diseases):
                with (c1 if i % 2 == 0 else c2):
                    if st.button(d, key=f"hrt_{d}", use_container_width=True): st.session_state.pending = d; st.rerun()
        
        with st.expander("🧠 Brain & Mental", expanded=False):
            diseases = ["Migraine", "Depression", "Alzheimer's", "Epilepsy", "Parkinson's", "Anxiety"]
            c1, c2 = st.columns(2)
            for i, d in enumerate(diseases):
                with (c1 if i % 2 == 0 else c2):
                    if st.button(d, key=f"brn_{d}", use_container_width=True): st.session_state.pending = d; st.rerun()
        
        with st.expander("🫁 Respiratory", expanded=False):
            diseases = ["Asthma", "Pneumonia", "Bronchitis", "COPD", "Lung Cancer"]
            c1, c2 = st.columns(2)
            for i, d in enumerate(diseases):
                with (c1 if i % 2 == 0 else c2):
                    if st.button(d, key=f"rsp_{d}", use_container_width=True): st.session_state.pending = d; st.rerun()
        
        with st.expander("🦴 Bones & Joints", expanded=False):
            diseases = ["Arthritis", "Osteoporosis", "Gout", "Lupus", "Fibromyalgia"]
            c1, c2 = st.columns(2)
            for i, d in enumerate(diseases):
                with (c1 if i % 2 == 0 else c2):
                    if st.button(d, key=f"bone_{d}", use_container_width=True): st.session_state.pending = d; st.rerun()
        
        st.markdown("---")
        
        # Clear Options
        st.markdown("#### 🧹 Clear Options")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🗑️ History", use_container_width=True, help="Clear search history"):
                bot.clear_history()
                st.session_state.history = []
                st.rerun()
        with c2:
            if st.button("🔄 Cache", use_container_width=True, help="Clear app cache"):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.session_state.chatbot = None
                st.rerun()

    # Main UI - More Attractive Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div class="mega-title">Medical AI Encyclopedia</div>
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 10px;">
            <span style="background: linear-gradient(135deg, #22c55e, #16a34a); padding: 6px 16px; border-radius: 20px; font-size: 0.9rem;">🌍 Global Knowledge</span>
            <span style="background: linear-gradient(135deg, #8b5cf6, #7c3aed); padding: 6px 16px; border-radius: 20px; font-size: 0.9rem;">🩺 Symptom Checker</span>
            <span style="background: linear-gradient(135deg, #ec4899, #db2777); padding: 6px 16px; border-radius: 20px; font-size: 0.9rem;">🎤 Voice Search</span>
            <span style="background: linear-gradient(135deg, #f97316, #ea580c); padding: 6px 16px; border-radius: 20px; font-size: 0.9rem;">📥 PDF Reports</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab_search, tab_symptoms = st.tabs(["🔍 Search Engine", "🩺 Global Symptom Checker"])
    
    with tab_search:
        # Styled Disclaimer
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.15), rgba(245, 158, 11, 0.1)); 
                    border: 1px solid rgba(251, 191, 36, 0.4); border-radius: 12px; padding: 12px 16px; margin-bottom: 1rem;">
            <span style="color: #fbbf24; font-weight: 600;">⚠️ Medical Disclaimer:</span>
            <span style="color: #d4d4d4;"> {DISCLAIMER}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Message Container
        msg_container = st.container()
        
        with msg_container:
            for msg in st.session_state.history:
                if msg["role"] == "user":
                    st.chat_message("user").write(msg["content"])
                else:
                    with st.chat_message("assistant", avatar="🩺"):
                        display_medical_card(msg["info"])
        
        # Pending queries from sidebar
        if st.session_state.pending:
            query = st.session_state.pending
            st.session_state.pending = None
            st.session_state.history.append({"role": "user", "content": query})
            with st.spinner("🔬 Researching..."):
                data = bot.chat(query)
            st.session_state.history.append({"role": "assistant", "info": data})
            st.rerun()

        # Main Input
        user_input = st.chat_input("🔍 Search any disease, condition, or medical topic...")
        if user_input:
            st.session_state.history.append({"role": "user", "content": user_input})
            with st.spinner("🔬 Researching..."):
                data = bot.chat(user_input)
            st.session_state.history.append({"role": "assistant", "info": data})
            st.rerun()

    with tab_symptoms:
        st.markdown("### 🩺 Dynamic Symptom Intelligence")
        st.write("Enter your symptoms and our AI will analyze possible conditions.")
        
        sym_input = st.text_input("Describe your symptoms (e.g., 'fever, headache, cough')", key="sym_in")
        
        if sym_input:
            with st.spinner("🤖 Analyzing symptoms..."):
                results = bot.check_symptoms(sym_input.split(','))
                if results:
                    st.markdown("#### 📊 Possible Conditions")
                    for res in results:
                        c1, c2 = st.columns([4, 1])
                        with c1:
                            st.markdown(f"""
                            <div style="background:rgba(34,197,94,0.1); border:1px solid #22c55e; border-radius:12px; padding:12px; margin-bottom:8px;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <strong style="font-size:1.1rem;">{res['condition']}</strong>
                                    <span style="color:#22c55e; font-weight:600;">{res['match']}% Match</span>
                                </div>
                                <div style="background:linear-gradient(90deg,#22c55e,#10b981); height:6px; width:{res['match']}%; border-radius:3px; margin-top:8px;"></div>
                            </div>
                            """, unsafe_allow_html=True)
                        with c2:
                            if st.button("Learn More", key=f"sym_{res['condition']}", use_container_width=True):
                                st.session_state.pending = res['condition']
                                st.rerun()
                else:
                    st.info("No matches found. Try adding more symptoms.")
        
        st.markdown("---")
        st.caption("🚨 **Disclaimer**: This tool is for educational purposes only. Always consult a healthcare professional.")

if __name__ == "__main__":
    main()
