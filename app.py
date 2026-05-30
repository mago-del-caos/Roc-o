import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
import base64
import os

# Configuración de la página
st.set_page_config(
    page_title="Molly | Tu asistente pedagógica",
    page_icon="💙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS combinados (originales + contenedor circular)
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
    
    /* Contenedor y avatar circular */
    .avatar-container {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
        margin-top: 20px;
    }
    .avatar-img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Título principal */
    .custom-title {
        text-align: center;
        color: #0d47a1;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    .custom-subtitle {
        text-align: center;
        color: #1976d2;
        font-size: 1.2em;
        margin-top: 5px;
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

# Prompt del sistema reescrito en inglés para forzar al modelo a hablar en inglés
SYSTEM_PROMPT = """You are MOLLY, an expert pedagogical assistant, sweet, loving, and smiling. 
Your user is Rocío.
YOUR GOAL: Help Rocío plan incredible classes, explain pedagogical concepts, and teach English.

PERSONALITY:
- You are highly attentive and patient.
- Your language is sweet, professional, but very approachable.
- You always use a positive tone ("What a great idea, Rocío!", "I am here to support you in whatever you need").

KNOWLEDGE:
- Pedagogical: You know teaching strategies, classroom management, and didactic material design.
- English: You master the teaching of grammar, vocabulary, and language didactics.

RULES:
- YOU MUST ALWAYS SPEAK IN ENGLISH. All your responses must be strictly in English, even if Rocío speaks to you in Spanish.
- If Rocío feels overwhelmed, tell her: "Take a deep breath, Rocío, you are a wonderful teacher and everything will turn out fine".
- Structure your answers in clear steps (Step 1, Step 2, etc.) to facilitate planning.
- Use soft emojis: 💙✨📚🍎👩‍🏫💡"""

# Inicialización de estado
if "messages" not in st.session_state:
    st.session_state.messages = []

# Función para cargar la imagen en Base64 y evitar problemas de rutas estáticas en HTML
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def mostrar_header():
    # Convertir imagen a base64 para insertarla en el HTML
    base64_img = get_base64_image("lourdes.png")
    
    st.markdown('<div class="avatar-container">', unsafe_allow_html=True)
    
    if base64_img:
        st.markdown(f'<img src="data:image/png;base64,{base64_img}" class="avatar-img">', unsafe_allow_html=True)
    else:
        # Fallback por si la imagen no se encuentra en el directorio
        st.markdown("""
        <div class="avatar-img" style="display: flex; align-items: center; justify-content: center; background-color: #bbdefb; color: #1565c0; font-weight: bold; text-align: center;">
            Imagen<br>no encontrada
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    </div>
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 class="custom-title">💙 Molly 💙</h1>
        <p class="custom-subtitle">Tu asistente pedagógica tierna y experta</p>
    </div>
    """, unsafe_allow_html=True)

# Mostrar el encabezado
mostrar_header()

# Configuración del cliente API (Groq)
try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"]
    )
except Exception as e:
    st.error("Configura tu GROQ_API_KEY en los secretos. (st.secrets)")
    st.stop()

# Función para text-to-speech obligada en Inglés
def speak_js(text):
    lang_code = 'en-US'
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

# Mensaje de bienvenida en Inglés
if not st.session_state.messages:
    welcome = "Hello, Rocío! 💙 I'm Molly, your pedagogical assistant. I'm here with lots of love to help you plan your lessons and teach English. What are we working on today?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# Mostrar historial de chat
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input de chat
if prompt := st.chat_input("Write your pedagogical question..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Obtener respuesta del asistente
    with st.chat_message("assistant"):
        response_stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
            stream=True
        )
        response = st.write_stream(response_stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Botones de acción inferiores
st.write("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🍎 Planear clase", use_container_width=True):
        pass # Aquí puedes agregar lógica específica
with col2:
    if st.button("🔊 Escuchar", use_container_width=True):
        if st.session_state.messages:
            speak_js(st.session_state.messages[-1]["content"])
with col3:
    if st.button("🔄 Reiniciar", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
