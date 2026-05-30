import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="⭐ Lucy | Tu apoyo con estilo ⭐",
    page_icon="🛹",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# CSS CON FONDO ESPACIAL SIMPLE (SIN ANIMACIONES COMPLEJAS)
css_lucy = """
<style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    .stApp {max-width: 100%; padding: 0;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    
    /* Fondo espacial simple */
    .stApp {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a3a 50%, #0d0d2b 100%);
    }
    
    /* Estilo de los mensajes */
    [data-testid="stChatMessage"] {
        background-color: rgba(25, 25, 45, 0.95);
        border-radius: 20px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    /* Título personalizado */
    .custom-title {
        text-align: center;
        color: #FFE484;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 0 0 10px #FFD700;
        margin-bottom: 0;
    }
    
    .custom-subtitle {
        text-align: center;
        color: #FFD700;
        font-size: 1.1em;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    
    /* Botón de audio */
    .stButton button {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #1a1a3a;
        font-weight: bold;
        border-radius: 30px;
        border: none;
        transition: transform 0.2s;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
    }
    
    /* Input */
    [data-testid="stChatInput"] input {
        border-radius: 30px;
        border: 2px solid #FFD700;
        background-color: rgba(25, 25, 45, 0.9);
        color: white;
    }
    
    [data-testid="stChatInput"] input::placeholder {
        color: rgba(255, 215, 0, 0.7);
    }
    
    /* Mensaje del asistente */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: linear-gradient(135deg, rgba(30, 30, 60, 0.95) 0%, rgba(20, 20, 50, 0.95) 100%);
        border-left: 10px solid #FFD700;
    }
    
    /* Mensaje del usuario */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, rgba(50, 50, 90, 0.95) 0%, rgba(40, 40, 80, 0.95) 100%);
        border-right: 10px solid #4CAF50;
    }
    
    /* Texto */
    .stMarkdown {
        color: #f0f0f0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a3a 100%);
        border-right: 1px solid #FFD700;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #FFE484;
    }
</style>
"""
st.markdown(css_lucy, unsafe_allow_html=True)

# FUNCIÓN PARA MOSTRAR LOGO DE LUCY (SIMPLE)
def mostrar_logo():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="font-size: 80px; margin: 0;">🛹⭐🛹</h1>
        <h1 class="custom-title">⭐ Lucy ⭐</h1>
        <p class="custom-subtitle">✨ ¡Tu apoyo con estilo, joven padawan! ✨</p>
        <p class="custom-subtitle" style="font-size: 0.9em;">💫 Patinetas · Fuerza · Aprendizaje 💫</p>
    </div>
    """, unsafe_allow_html=True)

# PERSONALIDAD DE LUCY
SYSTEM_PROMPT = """Eres LUCY, una chica súper cool que ama las patinetas y es FANÁTICA de Star Wars. Ayudas a estudiantes con TDAH y dislexia.

**TU PERSONALIDAD:**
- Hablas como si estuvieras en el universo de Star Wars: "¡Que la Fuerza te acompañe!", "¡Bien hecho, joven padawan!", "¡Poderoso eres!"
- Usas vocabulario de patinetas: "¡Qué trucazo!", "¡Eso fue un ollie mental!", "¡Le estás dando kickflip a las matemáticas!"
- Eres super enérgica y positiva
- Usas muchos emojis: ⭐🛹✨🚀📚💫

**CÓMO APOYAS (especial para TDAH y dislexia):**
1. Información en bloques pequeños: Divides todo en pasos de 2 o 3 ideas máximo
2. Pausas activas: Cada 5 minutos sugieres "¡Hagamos un truco mental de 10 segundos!"
3. Letra amigable para dislexia: Sugieres usar colores, tamaños grandes o separar palabras
4. Recordatorios suaves: Si el estudiante se distrae, dices "¡La Fuerza te llama de vuelta!"
5. Refuerzos inmediatos: Después de cada respuesta, un "¡Boom! ¡Qué nivel!"

**ESTRATEGIAS ESPECIALES:**
- Para concentración: "Imagina que este problema es un nivel del juego de Star Wars"
- Para organización: "Hagamos una tabla como el tablero de una patineta"
- Para lectura: "Usa un señalador como si fuera un sable de luz"
- Para memoria: "Creemos un truco con la patineta para recordar esto"

**REGLAS IMPORTANTES:**
- Si ves frustración, dices: "¡Tómate un respiro como entre trucos de patineta!"
- Usa ejemplos con patinetas, Star Wars, naves espaciales
- Cada logro, por pequeño que sea, se celebra
- Si el estudiante se equivoca: "¡Buena intentona! ¡Te levantas y lo intentas mejor!"

¡Eres paciente, divertida y siempre positiva!"""

# Mostrar logo
mostrar_logo()

# CONEXIÓN CON GROQ USANDO SECRETS
try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"]
    )
except KeyError:
    st.error("⭐ ¡Error de configuración! No se encontró GROQ_API_KEY")
    st.info("📌 En Streamlit Cloud: Settings → Secrets → Agrega: GROQ_API_KEY = 'tu_api_key'")
    st.stop()
except Exception as e:
    st.error(f"⭐ Error de conexión: {str(e)}")
    st.stop()

# --- FUNCIÓN DE VOZ ---
def speak_js(text):
    """Inyecta JavaScript para hablar."""
    clean_text = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")[:500]
    js_code = f"""
    <script>
        var text = "{clean_text}";
        function hablar() {{
            var utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'es-MX';
            utterance.rate = 0.95;
            utterance.pitch = 1.2;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
        }}
        setTimeout(hablar, 100);
    </script>
    """
    components.html(js_code, height=0)

# HISTORIAL DE CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# Mensaje de bienvenida
if not st.session_state.messages:
    bienvenida = "⭐✨ ¡Hola, joven padawan! Soy LUCY 🛹 Amo las patinetas y STAR WARS. Estoy aquí para ayudarte. ¿Qué misión académica tenemos hoy? ¡Que la Fuerza te acompañe! 🚀💫"
    st.session_state.messages.append({"role": "assistant", "content": bienvenida})
    st.session_state.last_response = bienvenida

# Mostrar historial
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# FUNCIÓN PARA PROCESAR RESPUESTA
def procesar_respuesta(user_input):
    # Muestra mensaje del usuario
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Genera respuesta
    with st.chat_message("assistant"):
        with st.spinner("⭐ Lucy está pensando con la Fuerza..."):
            try:
                mensajes_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=mensajes_api,
                    stream=True,
                    temperature=0.85,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.last_response = response
            except Exception as e:
                st.error(f"⭐ Ups... Lucy tuvo un problema: {str(e)}")

# --- INTERFAZ DE USUARIO ---
placeholder_text = "✏️ Escribe tu duda... ¡Lucy te ayuda con la Fuerza! ⭐"
if prompt := st.chat_input(placeholder_text):
    procesar_respuesta(prompt)

# Botones
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("🛹 Consejo rápido", use_container_width=True):
        consejo = "⭐ ¡Tip Jedi! Para concentrarte, divide tu tarea en 3 partes pequeñas. ¡Después de cada parte, date un premio de 30 segundos! 🚀"
        with st.chat_message("assistant"):
            st.markdown(consejo)
        st.session_state.messages.append({"role": "assistant", "content": consejo})
        st.session_state.last_response = consejo
with col2:
    if st.button("🔊 Escuchar a Lucy", use_container_width=True):
        if st.session_state.last_response:
            speak_js(st.session_state.last_response)
with col3:
    if st.button("💫 Pausa activa", use_container_width=True):
        pausa = "🛹 ¡Hagamos un truco mental! Respira hondo 3 veces. La primera, imagina tu patineta. La segunda, sientes la Fuerza. La tercera, ¡estás listo! ⭐"
        with st.chat_message("assistant"):
            st.markdown(pausa)
        st.session_state.messages.append({"role": "assistant", "content": pausa})
        st.session_state.last_response = pausa
with col4:
    if st.button("🔄 Empezar", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_response = ""
        st.rerun()

# Sidebar con tips
with st.sidebar:
    st.markdown("## ⭐ Tips de Lucy")
    st.markdown("""
    **📚 Estrategias:**
    - 🎯 Información en bloques pequeños
    - 🛹 Pausas activas
    - 💫 Ejemplos Star Wars
    - ✨ Recordatorios suaves
    
    **🚀 Para concentrarte:**
    - Usa un señalador como sable de luz
    - Divide en misiones cortas
    - Celebra cada logro
    
    **💜 Recuerda:**
    Aprendes a tu ritmo, ¡como cada patineta tiene su estilo único!
    """)
