from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from an uploaded PDF file.

    Parameters:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        str: Extracted text
    """

    try:

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as error:

        print(f"PDF extraction error: {error}")

        return ""