import os

from utils import get_tokens, pdf_price, read_pdf, save_to_pdf, send_to_chatgpt

# Set the OPENAI_API_KEY environment variable
api_key = os.getenv("OPENAI_API_KEY")  # Get API key from environment variable

def task_gen(input_pdf, output_path=None):
    if not api_key:
        raise ValueError("No API key found. Please set the OPENAI_API_KEY environment variable.")

    if output_path is None:
        output_path = input_pdf.replace(".pdf", "_output.pdf")

    # Read the PDF and send it to ChatGPT
    text = read_pdf(input_pdf)
    response = send_to_chatgpt(text)
    
    # Save the response to a PDF file
    save_to_pdf(response, output_path)

    # Calculate the production price
    price_info = pdf_price(input_pdf, response)
    print(price_info)

task_gen("Test_PDFs/Geschichte.pdf")