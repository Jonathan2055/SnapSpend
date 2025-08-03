import requests
import json
import os
import logging

def process_invoice(image_path):
   
    try:
        
        text = extract_text_from_image(image_path)
        invoice_data = extract_invoice_data(text)
        invoice_data['raw_text'] = text
        return invoice_data
        
    except Exception as e:
        logging.error(f"Invoice processing error: {e}")
        raise Exception(f"Failed to process invoice: {str(e)}")

def extract_text_from_image(image_path):
    ocr_url = "https://ocr-extract-text.p.rapidapi.com/ocr"
    
    ocr_headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "ocr-extract-text.p.rapidapi.com"
    }
    
    try:
        with open(image_path, "rb") as image_file:
            files = {"image": image_file}
            ocr_response = requests.post(ocr_url, files=files, headers=ocr_headers)
            print(ocr_response.raise_for_status())
            ocr_data = ocr_response.json()
            text = ocr_data['text'] if isinstance(ocr_data, dict) and 'text' in ocr_data else ocr_response.text
            
            if not text or text.strip() == '':
                raise Exception("No text extracted from image")
                
            return text
            
    except requests.exceptions.RequestException as e:
        logging.error(f"OCR API error: {e}")
        raise Exception("OCR service unavailable")
    except Exception as e:
        logging.error(f"OCR processing error: {e}")
        raise Exception("Failed to extract text from image")

def extract_invoice_data(text):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    prompt = f"""
    Extract the following information from the invoice text and return it in valid JSON format:
    - invoice_date (format: YYYY-MM-DD, or null if not found)
    - due_date (format: YYYY-MM-DD, or null if not found)
    - items (array of objects with: name, quantity, price, total)
    - total_amount (numeric value only, no currency symbols)

    Return only valid JSON in this exact format:
    {{
      "invoice_date": "YYYY-MM-DD or null",
      "due_date": "YYYY-MM-DD or null", 
      "items": [
        {{"name": "item name", "quantity": 1, "price": 10.00, "total": 10.00}}
      ],
      "total_amount": 100.00
    }}

    Invoice text:
    {text}
    
    """
    print(text)
    try:
        gemini_payload = {
            "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                     ]
                 }
                ]
            }

        gemini_headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY
            }

        gemini_response = requests.post(GEMINI_URL, json=gemini_payload, headers=gemini_headers)
        gemini_response.raise_for_status()
        Result = gemini_response.json()
        response=Result['candidates'][0]['content']['parts'][0]['text']

        
        if not response:
            raise Exception("Empty response from AI service")
        
        # Removing Unnecesary details so that I can use my response as I need
        result_text = response.strip()
        print(result_text)
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
        
        result_text = result_text.strip()

        try:
            invoice_data = json.loads(result_text)
            
            
            if not isinstance(invoice_data, dict):
                raise ValueError("Response is not a JSON object")
            
            invoice_data.setdefault('invoice_date', None)
            invoice_data.setdefault('due_date', None)
            invoice_data.setdefault('items', [])
            invoice_data.setdefault('total_amount', 0.0)
            
            # Turning total amount into a float character
            if isinstance(invoice_data['total_amount'], str):
                try:
                    invoice_data['total_amount'] = float(invoice_data['total_amount'].replace('$', '').replace(',', ''))
                except ValueError:
                    invoice_data['total_amount'] = 0.0
            
            return invoice_data
            
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing error: {e}, Raw text: {result_text}")
            
            return {
                'invoice_date': None,
                'due_date': None,
                'items': [],
                'total_amount': 0.0
            }
            
    except Exception as e:
        logging.error(f"Gemini AI error: {e}")
        raise Exception("AI service unavailable")
