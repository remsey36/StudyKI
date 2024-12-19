import os 
import tiktoken
import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openai import OpenAI
from dotenv import load_dotenv


MODEL = "gpt-4o-mini"  # Update to later to gpt-4 or gpt-4o

encoding = tiktoken.encoding_for_model(MODEL)

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENAI_API_KEY")  # Get API key from environment variable

def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def save_to_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 100, text)
    c.save()

def get_tokens(pdf_path):
    text = read_pdf(pdf_path)
    tokens = encoding.encode(text)
    return tokens

def pdf_price(pdf_path, output_text, input_token_price=0.0000025, output_token_price=0.00001):
    input_tokens = get_tokens(pdf_path)
    output_tokens = encoding.encode(output_text)
    
    input_cost = len(input_tokens) * input_token_price
    output_cost = len(output_tokens) * output_token_price
    total_cost = input_cost + output_cost
    
    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost
    }

def send_to_chatgpt(text):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=MODEL,
        store=True,
        messages=[
            {"role": "user", "content": text}
        ]
    )
    return completion['choices'][0]['message']['content']

