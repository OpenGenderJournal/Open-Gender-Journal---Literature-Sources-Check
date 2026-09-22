pip install python-docx
pip install regex
pip install citeproc-py

import re
from docx import Document

doc = Document(r"C:\Users\pfist\Desktop\+215-Artikeltext-1830-1-15-20230202+tc_finale_Überarbeitung_TH+tc+SSch.docx")

full_text = "\n".join([p.text for p in doc.paragraphs])

def extract_bibliography(text):
    match = re.search(r"(Literaturverzeichnis.*)", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return text  # fallback

bibliography_text = extract_bibliography(full_text)

entries = [e.strip() for e in bibliography_text.split("\n\n") if e.strip()]

def extract_author_year(entry):
    match = re.match(r"([A-Za-zÄÖÜäöüß\-]+).*?\((\d{4})\)", entry)
    if match:
        author = match.group(1)
        year = match.group(2)
        return f"{author} {year}"
    return None

bib_keys = set()
for e in entries:
    key = extract_author_year(e)
    if key:
        bib_keys.add(key)

citations = re.findall(r"\(([A-Za-zÄÖÜäöüß\-]+)\s*(\d{4})\)", full_text)

text_keys = set([f"{a} {y}" for a, y in citations])

missing_in_text = bib_keys - text_keys
missing_in_bib = text_keys - bib_keys

print("\n--- NICHT im Text zitiert ---")
for m in missing_in_text:
    print(m)

print("\n--- NICHT im Literaturverzeichnis ---")
for m in missing_in_bib:
    print(m)