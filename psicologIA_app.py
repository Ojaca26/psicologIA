import streamlit as st
import google.generativeai as genai

# Cargar API KEY
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Configurar modelo Gemini
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# Prompt base cargado del archivo
with open("psicologIA.txt", "r", encoding="utf-8") as f:
    base_prompt = f.read()

# Interfaz Streamlit
st.set_page_config(page_title="Asesor PsicologIA", layout="wide")

st.title("🧠 PsicologIA - Tu asesor de transformación personal")
st.markdown("**Bienvenido(a) a tu sesión privada. Comparte tu estado emocional, preocupaciones o patrones actuales.**")

with st.expander("🧭 ¿Cómo funciona PsicologIA? Haz clic aquí"):
    st.markdown("""
    Esta aplicación está diseñada como tu espacio seguro de exploración emocional profunda. Aquí puedes:

    - Explorar tus **bloqueos mentales**.
    - Entender patrones de **comportamiento que te molestan**.
    - Descubrir tus **distorsiones cognitivas**.
    - Trazar un plan de transformación personal.

    💡 Escribe con la mayor sinceridad posible. Nadie más leerá esto.
    """)

# Formulario personalizado
nombre_usuario = st.text_input("👤 ¿Cómo te llamas?, ó dime ¿cómo quieres que te llame?.", max_chars=30)
user_input = st.text_area("✍️ ¿Qué te gustaría explorar hoy?", height=250)

if st.button("🧩 Iniciar Análisis Profundo"):
    if nombre_usuario.strip() == "" or user_input.strip() == "":
        st.warning("Por favor escribe tu nombre y lo que deseas trabajar.")
    else:
        with st.spinner("Analizando profundamente tu caso..."):
            full_prompt = f"""{base_prompt}

Instrucción adicional: Haz sentir al usuario comprendido, utiliza su nombre frecuentemente de forma empática.

👤 Nombre del usuario: {nombre_usuario}
📝 Contexto emocional: {user_input}
"""
            response = model.generate_content(full_prompt)
            st.session_state.analisis = response.text
            st.session_state.nombre = nombre_usuario
            st.success("✅ Análisis completado")

# Mostrar resultado previo y mantener análisis visible
if "analisis" in st.session_state and "nombre" in st.session_state:
    st.markdown(f"### 🧾 Resultado de tu sesión, {st.session_state.nombre}:")
    st.markdown(st.session_state.analisis)

    st.markdown("---")
    st.subheader("💬 Dime todas las dudas sobre el análisis")
    pregunta = st.text_area("Puedes hacer una pregunta al profesional aquí:", key="pregunta_usuario")

    if st.button("🧠 Responder pregunta"):
        if pregunta.strip() == "":
            st.warning("Por favor escribe tu duda o pregunta.")
        else:
            with st.spinner("Reflexionando sobre tu consulta..."):
                prompt_pregunta = f"""
A continuación verás un análisis psicológico generado previamente para un usuario llamado {st.session_state.nombre}.

Análisis previo:
{st.session_state.analisis}

Ahora, como psicólogo experto, responde la siguiente pregunta del paciente con empatía y precisión:
Pregunta: {pregunta}
"""
                respuesta_pregunta = model.generate_content(prompt_pregunta)
                st.success("🗣️ Respuesta del profesional:")
                st.markdown(respuesta_pregunta.text)
