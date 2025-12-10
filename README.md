# 📖 **ReaderProject** – Inteligente Leitor de Texto com IA

---

## Visão Geral

**ReaderProject** é uma aplicação web interativa construída com **Streamlit** que permite ao usuário:
- **Inserir texto** a partir de um **link (URL)**, **arquivo PDF** ou **texto direto**;
- **Detectar automaticamente o idioma** do conteúdo;
- **Gerar áudio** de alta qualidade usando **OpenAI TTS** (para a versão OpenAI) ou **Google TTS** (para a versão Google);
- **Selecionar o idioma da leitura** para adequar a voz ao idioma desejado.

A interface foi projetada com **design premium** – cores vibrantes, tipografia moderna (Google Fonts *Inter*), efeitos de glassmorphism e micro‑animações – para proporcionar uma experiência visual e interativa de alto nível.

---

## Principais Funcionalidades

- **Entrada flexível** – escolha entre URL, PDF ou texto direto via um seletor de rádio exclusivo (evita conflitos de estado).
- **Detecção de idioma** automática usando os serviços de linguagem da OpenAI/Google.
- **Geração de áudio** em poucos segundos, com opção de download.
- **Botão “Processar e Ler” sempre visível** e com validação de entrada para evitar cliques sem conteúdo.
- **Modo OpenAI** (usando `src.language_services` e `src.audio_generator`) e **modo Google** (usando `src.language_services_google` e `src.audio_generator_google`).
- **Configurações de usuário** – nome, chave de API (quando necessária) e seleção de idioma da voz.

---

## Capturas de Tela

![App Mockup](../.gemini/antigravity/brain/f1e75cc6-fa5f-4e7f-93b3-5ddea55c2710/app_mockup_1765404106416.png)

> *A imagem acima mostra a interface principal com barra lateral, seleção de método de entrada e botão “Processar e Ler”.*

---

## Instalação

```bash
# Clone o repositório
git clone git@github.com:Baldros/ReaderProject.git
cd ReaderProject

# Crie e ative um ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt
```

> **Obs.:**  Para a versão Google, configure a variável de ambiente `GOOGLE_API_KEY` no arquivo `.env`.

---

## Uso

```bash
# Inicie a aplicação Streamlit
streamlit run Book_Reader_OpenAI.py   # versão OpenAI
# ou
streamlit run pages/Book_Reader_(Google).py   # versão Google (sem tradução)
```

1. Preencha seu **nome** e, se necessário, a **API Key**.
2. Selecione o **idioma da leitura** (necessário para a voz correta).
3. Escolha o **método de entrada** (Link, PDF ou Texto Direto) via rádio.
4. Clique em **🚀 Processar e Ler** – o texto será extraído, o idioma detectado e o áudio gerado.
5. Ouça o áudio na própria página ou faça download usando o botão de download.

---

## Estrutura do Projeto

```
ReaderProject/
├─ pages/
│   ├─ Book_Reader_(Google).py   # versão Google (sem tradução)
├─ Book_Reader_OpenAI.py          # versão OpenAI (com TTS da OpenAI)
├─ src/
│   ├─ input_handler.py          # extração de URL e PDF
│   ├─ language_services.py      # detecção de idioma (OpenAI)
│   ├─ language_services_google.py # detecção de idioma (Google)
│   ├─ audio_generator.py        # geração de áudio (OpenAI)
│   ├─ audio_generator_google.py # geração de áudio (Google TTS)
│   └─ ...
├─ .env                           # variáveis de ambiente (API keys)
├─ requirements.txt               # dependências Python
└─ README.md                      # este documento
```

---

## Contribuição

Contribuições são bem‑vindas! Para colaborar:
1. Fork o repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/minha-feature`).
3. Commit suas alterações e abra um Pull Request.
4. Certifique‑se de que os testes (se houver) passem e que o código siga o padrão de estilo PEP 8.

---

## Licença

Este projeto está licenciado sob a **MIT License** – sinta‑se livre para usar, modificar e distribuir.

---

**Happy reading!** 🎧
