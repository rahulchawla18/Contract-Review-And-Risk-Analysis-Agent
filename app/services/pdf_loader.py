from langchain_community.document_loaders import PyPDFLoader


def load_pdf(path: str):
    try:
        loader = PyPDFLoader(path)
        docs = loader.load()
        if not docs:
            raise ValueError("PDF file is empty or could not be read")
        return "\n".join([d.page_content for d in docs])
    except Exception as e:
        error_msg = str(e)
        if "cryptography" in error_msg.lower() or "AES" in error_msg:
            raise ValueError(
                "PDF is encrypted. Please provide an unencrypted PDF or install cryptography library. "
                "If the library is installed, the PDF may require a password."
            ) from e
        elif "password" in error_msg.lower():
            raise ValueError("PDF is password-protected. Please provide an unencrypted PDF.") from e
        else:
            raise ValueError(f"Error reading PDF: {error_msg}") from e