import streamlit as st
import os
from src.input_handler import identify_input_type, extract_from_url, extract_from_pdf
from src.language_services import detect_language, translate_text
from src.audio_generator import generate_audio

# Page Config
st.set_page_config(page_title="Leitor Inteligente", page_icon="🎧", layout="wide")

# Sidebar
with st.sidebar:
    st.header("Configurações")
    user_name = st.text_input("Seu Nome", value="Usuário")
    api_key = st.text_input("OpenAI API Key", type="password", help="Insira sua chave da OpenAI aqui.")
    
    st.markdown("---")
    st.subheader("Voz e Idioma")
    voice_option = st.selectbox("Voz", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"])
    
    st.markdown("---")
    st.subheader("Tradução")
    translating = st.checkbox("Traduzir texto antes de ler?")
    target_lang = "Português" # Default
    if translating:
        target_lang = st.selectbox("Traduzir para:", ["Português", "Inglês", "Espanhol", "Francês", "Alemão", "Italiano"])
    
if not api_key:
    st.warning("⚠️ Por favor, insira sua API Key da OpenAI na barra lateral para começar.")
    st.stop()

st.title(f"🎧 Olá, {user_name}! O que vamos ler hoje?")

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
                    
                st.success("Texto extraído com sucesso!")
                
                # Show text preview
                with st.expander("Ver texto extraído", expanded=True):
                    st.write(raw_text)
                    
                # 2. Language Detection
                lang = detect_language(raw_text)
                st.caption(f"Idioma detectado original: {lang}")
                
                # 3. Translation (Optional - uses settings from Sidebar)
                final_text = raw_text
                if translating:
                    with st.spinner(f"Traduzindo para {target_lang}..."):
                        final_text = translate_text(raw_text, target_lang, api_key)
                        st.subheader("Texto Traduzido")
                        st.write(final_text)
                
                # 4. Audio Generation
                st.markdown("---")
                st.subheader("🎧 Áudio Gerado")
                with st.spinner("Gerando áudio (isso pode levar alguns segundos)..."):
                    audio_path = generate_audio(final_text, api_key, voice=voice_option)
                    
                    # Audio Player
                    st.audio(audio_path, format='audio/wav')
                    
                    # Download Button   
                    with open(audio_path, "rb") as file:
                        st.download_button(
                            label="📥 Baixar Áudio",
                            data=file,
                            file_name="leitura_inteligente.wav",
                            mime="audio/wav"
                        )
                        
            except Exception as e:
                st.error(f"Ocorreu um erro: {str(e)}")
