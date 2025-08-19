
import os
from openai import OpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# Load API key and URL
load_dotenv()
# Load API key and URL
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("LOCAL_API_URL")

# Create OpenAI-compatible client
client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

# Step 1: Read PDF
pdf_path = "article.pdf"
reader = PdfReader(pdf_path)
pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)

# Optional: Truncate or chunk text to avoid token limits
max_chars = 500  # adjust to fit your model's context
text_chunk = pdf_text[:max_chars]

# Step 2: Send request to LLM
prompt = f"""
You are an expert materials scientist.
From the following research article text, extract all synthesis conditions of the material discussed.
Return results as CSV with columns: Concentration, Hydrolysis ratio, Rate of base addition, Cation ratio, Other Conditions.

Article text:
{text_chunk}
"""

response = client.chat.completions.create(
    model="deepseek-ai--DeepSeek-R1-Distill-Llama-70B",
    messages=[
        {"role": "system", "content": "You are a concise scientific data extractor."},
        {"role": "user", "content": prompt}
    ],
    temperature=0,
    max_tokens=800
)

# Step 3: Save CSV output
csv_output = response.choices[0].message.content.strip()
with open("synthesis_conditions.csv", "w") as f:
    f.write(csv_output)

print("CSV saved to synthesis_conditions.csv")
