import fitz  # PyMuPDF
import os
import json

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# Folder containing all PDFs
pdf_folder = "Resources"
all_text = ""

# Iterate through all PDFs
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        all_text += extract_text_from_pdf(pdf_path) + "\n"

# Save extracted text
with open("medical_text.json", "w", encoding="utf-8") as f:
    json.dump({"content": all_text}, f, indent=4)

print("✅ Extracted text saved as 'medical_text.json'!")
