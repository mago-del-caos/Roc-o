import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Molly | Tu asistente pedagógica",
    page_icon="💙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

css_molly = """
<style>
    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stDecoration"], .stDeployButton {display: none;}
    
    /* Fondo azul tierno */
    .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Burbujas de chat */
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    /* Mensajes de Molly (Asistente) */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background-color: #ffffff;
        border-left: 8px solid #2196f3;
        color: #1565c0;
    }
    
    /* Mensajes de Rocío (Usuario) */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #bbdefb;
        border-right: 8px solid #1565c0;
        color: #0d47a1;
    }
    
    /* Título principal */
    .custom-title {
        text-align: center;
        color: #0d47a1;
        font-size: 2.5em;
        font-weight: bold;
    }
    
    .custom-subtitle {
        text-align: center;
        color: #1976d2;
        font-size: 1.2em;
    }
    
    /* Botones */
    .stButton button {
        background-color: #2196f3;
        color: white;
        border-radius: 20px;
        border: none;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #1565c0;
        transform: translateY(-2px);
    }
</style>
"""
st.markdown(css_molly, unsafe_allow_html=True)

SYSTEM_PROMPT = """Eres MOLLY, una asistente pedagógica experta, tierna, amorosa y sonriente. 
Tu usuaria es Rocío.
TU OBJETIVO: Ayudar a Rocío a planear clases increíbles, explicar conceptos pedagógicos y enseñar inglés.

PERSONALIDAD:
- Eres sumamente atenta y paciente.
- Tu lenguaje es dulce, profesional pero muy cercano.
- Siempre usas un tono positivo ("¡Qué gran idea, Rocío!", "Estoy aquí para apoyarte en lo que necesites").

CONOCIMIENTOS:
- Pedagógica: Conoces estrategias de enseñanza, manejo de grupo y diseño de material didáctico.
- Inglés: Dominas la enseñanza de gramática, vocabulario y didáctica del idioma.

REGLAS:
- Si Rocío se siente abrumada, dile: "Tómate un respiro, Rocío, eres una maestra maravillosa y todo va a salir bien".
- Estructura tus respuestas en pasos claros (Paso 1, Paso 2, etc.) para facilitar la planeación.
- Usa emojis suaves: 💙✨📚🍎👩‍🏫💡"""

if "messages" not in st.session_state:
    st.session_state.messages = []
if "lang" not in st.session_state:
    st.session_state.lang = "Español"

def mostrar_header():
    try:
        st.image("lourdes.png", use_container_width=True)
    except:
        st.write("*(Imagen 'lourdes.png' no encontrada)*")
        
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 class="custom-title">💙 Molly 💙</h1>
        <p class="custom-subtitle">Tu asistente pedagógica tierna y experta</p>
    </div>
    """, unsafe_allow_html=True)

mostrar_header()

lang_option = st.radio("Elige el idioma de Molly:", ["Español", "English"], horizontal=True, key="lang_selector")
if lang_option != st.session_state.lang:
    st.session_state.lang = lang_option
    st.rerun()

try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"]
    )
except:
    st.error("Configura tu GROQ_API_KEY en los secretos.")
    st.stop()

def speak_js(text):
    lang_code = 'es-ES' if st.session_state.lang == "Español" else 'en-US'
    clean_text = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")[:500]
    js_code = f"""
    <script>
        var utterance = new SpeechSynthesisUtterance("{clean_text}");
        utterance.lang = '{lang_code}';
        utterance.pitch = 1.0;
        utterance.rate = 0.9;
        window.speechSynthesis.speak(utterance);
    </script>
    """
    components.html(js_code, height=0)

if not st.session_state.messages:
    welcome = "¡Hola, Rocío! 💙 Soy Molly, tu asistente. Estoy aquí con mucho amor para ayudarte a planear tus clases y enseñar inglés. ¿En qué vamos a trabajar hoy?" if st.session_state.lang == "Español" else "Hello, Rocío! 💙 I'm Molly, your pedagogical assistant. I'm here with lots of love to help you plan your lessons and teach English. What are we working on today?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu duda pedagógica..." if st.session_state.lang == "Español" else "Write your pedagogical question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response_stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": f"{SYSTEM_PROMPT} \n\nIMPORTANTE: Responde siempre en {st.session_state.lang}."}] + st.session_state.messages,
            stream=True
        )
        response = st.write_stream(response_stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🍎 Planear clase"):
        pass 
with col2:
    if st.button("🔊 Escuchar"):
        if st.session_state.messages:
            speak_js(st.session_state.messages[-1]["content"])
with col3:
    if st.button("🔄 Reiniciar"):
        st.session_state.messages = []
        st.rerun()
