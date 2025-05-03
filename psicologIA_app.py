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

    - Explorar tu **bloqueos mentales**.
    - Entender patrones de **comportamiento que te molestan**.
    - Descubrir tus **distorsiones cognitivas**.
    - Trazar un plan de transformación personal.

    💡 Escribe con la mayor sinceridad posible. Nadie más leerá esto.
    """)

st.info("Escribe lo que te está afectando o lo que quieres trabajar. Puede ser una emoción, un hábito, una situación, etc.")

user_input = st.text_area("✍️ ¿Qué te gustaría explorar hoy?", height=250)

if st.button("🧩 Iniciar Análisis Profundo"):
    if user_input.strip() == "":
        st.warning("Por favor escribe algo para poder iniciar la sesión.")
    else:
        with st.spinner("Analizando profundamente tu caso..."):
            full_prompt = base_prompt + f"\n\nContexto personal proporcionado por el usuario:\n{user_input}"
            response = model.generate_content(full_prompt)
            st.success("✅ Análisis completado")
            st.markdown("### 🧾 Resultado de tu sesión:")
            st.markdown(response.text)
