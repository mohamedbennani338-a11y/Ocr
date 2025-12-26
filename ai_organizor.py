import os
import json
from cerebras.cloud.sdk import Cerebras

#

def extract_fields_as_json(ocr_text, api_key):
    """
    Extracts fields from OCR text and returns them in JSON format
    """

    client = Cerebras(api_key=api_key)

    prompt = f"""
    Extract all key-value pairs from the following OCR text.
    Identify the fields dynamically based on the content.
    
    OCR TEXT:
    \"\"\"
    {ocr_text}
    \"\"\"

    Return ONLY a valid JSON object.
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a data extraction assistant. Your response must be a single, valid JSON object."
                },
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b",
            response_format={"type": "json_object"}
        )

        # Convert the raw string response into JSON format
        json_output = json.loads(response.choices[0].message.content)
        
        return json_output

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__" : 
    # Example Usage
    raw_ocr_input = """
    Printable Receipt
    Receipt #12345
    March 15, 2050
    Bill To:
    Tom Waiter
    tom@you.mail
    Wireless Bluetooth Headphones 2 $50.00 $100.00
    Premium Software Subscription 1 $150.00 $150.00
    Portable Power Bank 3 $20.00 $60.00
    Express Shipping Fee 1 $15.00 $15.00
    Total Amount: $325.00
    Payment Method: Crecit Card
    Thank you for your purchase! If you have any questions, feel free to contact us at [YOUR
    COMPANY EMAIL].
    For further assistance or inguiries, please vist (YOUR COMPANY NAME] at [YOUR
    COMPANY ADDRESS]. Have a great day!
    """

    data = extract_fields_as_json(raw_ocr_input, "api ...")

    
    print(json.dumps(data, indent=4))