import os
import csv
import requests
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# === Load credentials ===
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = os.getenv("LOCAL_API_URL")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# === PDF Reading ===
def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

# === Chunking ===
def chunk_text(text, max_chars=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
    return chunks

# === LLM Extraction ===
def extract_csv_from_chunk(text_chunk):
    prompt = f"""
From the following research article text, extract all synthesis conditions of the material discussed.
Return results ONLY as valid CSV with columns:
Step, Temperature (°C), Time (h), Solvent, Other Conditions.

No commentary, no explanation — CSV only.

Article text:
{text_chunk}
"""
    data = {
        "messages": [
            {"role": "system", "content": "You are a precise scientific data extractor."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": 800
    }

    response = requests.post(API_URL, headers=HEADERS, json=data, verify=False)
    if response.status_code != 200:
        raise RuntimeError(f"API error {response.status_code}: {response.text}")
    return response.json()["choices"][0]["message"]["content"].strip()

# === CSV Merging ===
def merge_csv_outputs(csv_texts):
    merged_rows = []
    for csv_text in csv_texts:
        reader = csv.reader(csv_text.splitlines())
        for row in reader:
            if not row:
                continue
            # Skip duplicate headers
            if merged_rows and row[0].strip().lower() == "step":
                continue
            merged_rows.append(row)
    return merged_rows

# === Main Workflow ===
if __name__ == "__main__":
    pdf_path = "article.pdf"
    pdf_text = read_pdf(pdf_path)
    chunks = chunk_text(pdf_text, max_chars=4000, overlap=200)

    print(f"PDF loaded. Total chunks: {len(chunks)}")

    all_csv_parts = []
    for i, chunk in enumerate(chunks, 1):
        print(f"Processing chunk {i}/{len(chunks)}...")
        csv_chunk = extract_csv_from_chunk(chunk)
        all_csv_parts.append(csv_chunk)

    merged_rows = merge_csv_outputs(all_csv_parts)

    output_path = "synthesis_conditions.csv"
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(merged_rows)

    print(f"CSV saved to {output_path}")
