import PyPDF2
import trafilatura

def extract_from_url(url):
    """
    Extracts main text content from a given URL using Trafilatura.
    Trafilatura is excellent at ignoring boilerplate (menus, ads, footers) and detecting the main article.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
             raise Exception("Falha ao baixar o conteúdo da URL (bloqueio ou site fora do ar).")
             
        text = trafilatura.extract(downloaded)
        
        if not text:
             raise Exception("Nenhum texto relevante encontrado na página.")
            
        return text.strip()
    except Exception as e:
        raise Exception(f"Erro ao extrair texto da URL: {str(e)}")

def extract_from_pdf(file_stream):
    """
    Extracts text from a PDF file stream (bytes).
    """
    try:
        reader = PyPDF2.PdfReader(file_stream)
        text = []
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
                
        return "\n".join(text)
    except Exception as e:
        raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")
