import requests
import tiktoken
import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

MODEL = "gpt-4o"
encoding = tiktoken.encoding_for_model(MODEL)

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

def pdf_price(pdf_path, output_text, input_token_price=0.0001, output_token_price=0.0002):
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

def send_to_chatgpt(api_key, text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": text}
        ],
        "max_tokens": 1500
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    
    if 'choices' not in response_json:
        raise ValueError(f"Unexpected response format: {response_json}")
    
    return response_json['choices'][0]['message']['content']

