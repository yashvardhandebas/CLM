# used to extract text from a pdf file and return it as a string
import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

    return extracted_text.strip()
