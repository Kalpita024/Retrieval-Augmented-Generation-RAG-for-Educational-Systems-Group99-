from langchain_community.document_loaders import PyPDFLoader
import logging

logger = logging.getLogger(__name__)

def load_pdf(pdf_path):
    """
    Load a single PDF and return LangChain documents.
    """

    try:
        logger.info(f"Loading PDF: {pdf_path}")

        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        logger.info(f"Successfully loaded {pdf_path}")
        logger.info(f"Pages loaded: {len(documents)}")

        return documents

    except Exception as e:
        logger.error(f"Error loading PDF {pdf_path}: {e}")
        return []


def load_multiple_pdfs(pdf_paths):
    """
    Load multiple PDFs and combine all documents.
    """

    all_documents = []

    for pdf_path in pdf_paths:
        docs = load_pdf(pdf_path)
        all_documents.extend(docs)

    logger.info(f"Total pages loaded: {len(all_documents)}")

    return all_documents


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    pdf_files = [
        "sample.pdf"
    ]

    documents = load_multiple_pdfs(pdf_files)

    if documents:
        print("\nFirst page preview:\n")
        print(documents[0].page_content[:1000])
