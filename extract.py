import fitz

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

pdf_path = "Corpus.pdf"
corpus_text = extract_text_from_pdf(pdf_path)

with open("corpus.txt", "w") as file:
    file.write(corpus_text)