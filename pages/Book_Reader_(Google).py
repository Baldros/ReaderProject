
import streamlit as st
import os
from src.input_handler import extract_from_url, extract_from_pdf
from src.language_services_google import detect_language
from src.audio_generator_google import generate_audio
from dotenv import load_dotenv

load_dotenv()

# Page Config
st.set_page_config(page_title="Leitor Inteligente (Google)", page_icon="🎧", layout="wide")

# Sidebar
with st.sidebar:
    st.header("Configurações (Google Edition)")
    user_name = st.text_input("Seu Nome", value="Usuário")
    api_key = os.getenv("GOOGLE_API_KEY")
    
    st.markdown("---")
    st.subheader("Idioma da Leitura")
    
    # Language Selection for Audio
    lang_options = ["Português", "Inglês", "Espanhol", "Francês", "Alemão", "Italiano"]
    target_lang = st.selectbox("Selecione o idioma para leitura:", lang_options)


st.title(f"🎧 Olá, {user_name}! O que vamos ler hoje? (Google)")

# Tabs for Input
# Input Selection
input_option = st.radio("Escolha o método de entrada:", ["🔗 Link (URL)", "📄 Arquivo PDF", "📝 Texto Direto"], horizontal=True)

input_data = None
input_type = None

if input_option == "🔗 Link (URL)":
    url_input = st.text_input("Cole o link do artigo aqui:")
    if url_input:
        input_data = url_input
        input_type = "URL"

elif input_option == "📄 Arquivo PDF":
    uploaded_file = st.file_uploader("Arraste seu PDF aqui", type=["pdf"])
    if uploaded_file:
        input_data = uploaded_file # Streamlit returns a BytesIO object
        input_type = "PDF_STREAM"

elif input_option == "📝 Texto Direto":
    text_input = st.text_area("Cole ou digite seu texto aqui:")
    if text_input:
        input_data = text_input
        input_type = "TEXT"

# Main Processing
if st.button("🚀 Processar e Ler"):
    if not input_data:
        st.warning("⚠️ Por favor, forneça um link, arquivo ou texto antes de processar.")
    else:
        with st.spinner("Extraindo texto..."):
            try:
                # 1. Extraction
                if input_type == "URL":
                    raw_text = extract_from_url(input_data)
                elif input_type == "PDF_STREAM":
                    raw_text = extract_from_pdf(input_data)
                else:
                    raw_text = input_data
                
                if len(raw_text) < 5:
                    st.error("O texto extraído é muito curto ou vazio.")
                    st.stop()

                if len(raw_text) > 1000:
                    st.error(f"O texto extraído é muito longo, {len(raw_text)} caracteres. O limite são 1000 caracteres.")
                    st.stop()
                    
                st.success("Texto extraído com sucesso!")
                
                # Show text preview
                with st.expander("Ver texto extraído", expanded=True):
                    st.write(raw_text)
                    
                # 2. Language Detection
                lang = detect_language(raw_text)
                st.caption(f"Idioma detectado original: {lang}")
                
                # 3. Translation (Removed)
                final_text = raw_text
                
                # 4. Audio Generation
                st.markdown("---")
                st.subheader("🎧 Áudio Gerado (gTTS)")
                with st.spinner("Gerando áudio..."):
                    audio_path = generate_audio(final_text, api_key=None, lang=target_lang)
                    
                    # Audio Player
                    st.audio(audio_path, format='audio/mp3')
                    
                    # Download Button   
                    with open(audio_path, "rb") as file:
                        st.download_button(
                            label="📥 Baixar Áudio",
                            data=file,
                            file_name="leitura_inteligente_google.wav",
                            mime="audio/wav"
                        )
                        
            except Exception as e:
                st.error(f"Ocorreu um erro: {str(e)}")
