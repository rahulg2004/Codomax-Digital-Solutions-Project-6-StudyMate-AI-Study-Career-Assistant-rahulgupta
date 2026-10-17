from pypdf import PdfReader

def extract_pdf_chunks(uploaded_file, chunk_size=1200, overlap=180):
    reader = PdfReader(uploaded_file)
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = " ".join(text.split())
        if text:
            pages.append(f"[Page {page_number}] {text}")

    full_text = "\n".join(pages)
    if not full_text.strip():
        return []

    chunks = []
    start = 0
    while start < len(full_text):
        end = min(start + chunk_size, len(full_text))
        chunk = full_text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(full_text):
            break
        start = end - overlap
    return chunks
