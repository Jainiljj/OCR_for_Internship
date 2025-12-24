import cv2
import pytesseract
import re
import json
import os

# CONFIGURATION
# Uncomment and update the path if Tesseract is not in your PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """
    Converts image to grayscale and applies thresholding to improve OCR accuracy.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")
        
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Binary thresholding to separate dark text from light background
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_text(processed_img):
    """
    Uses Tesseract OCR to extract raw text string from the processed image.
    """
    # --oem 3: Default OCR Engine Mode
    # --psm 6: Assume a single uniform block of text (good for invoices)
    custom_config = r'--oem 3 --psm 6'
    return pytesseract.image_to_string(processed_img, config=custom_config)

def parse_invoice_data(text):
    """
    Parses raw text using Regex to extract structured JSON data.
    """
    data = {}
    
    # 1. Extract Basic Fields using Regex
    
    # Date (Looking for YYYY-MM-DD format)
    date_match = re.search(r'Date:\s*(\d{4}-\d{2}-\d{2})', text)
    data['date'] = date_match.group(1) if date_match else None
    
    # Invoice Number (Alphanumeric characters after 'Invoice #')
    inv_match = re.search(r'Invoice\s*#:\s*([A-Za-z0-9-]+)', text)
    data['invoice_number'] = inv_match.group(1) if inv_match else None
    
    # Total Amount (Extracts number after 'Total Due' and $)
    total_match = re.search(r'Total Due:\s*\$([\d,.]+)', text)
    data['total_amount'] = float(total_match.group(1).replace(',', '')) if total_match else 0.0
    
    # Vendor Name (Heuristic: First non-empty line is usually the vendor)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    data['vendor_name'] = lines[0] if lines else None
    
    # 2. Extract Line Items
    data['line_items'] = []
    
    # Pattern: Description ... $Price ... $Total
    # Group 1 (Description): Non-greedy match until the first price
    # Group 2 & 3: Numeric values formatted as currency
    item_pattern = re.compile(r'(.*?)\s+\$([\d,.]+)\s+\$([\d,.]+)')
    
    for line in lines:
        match = item_pattern.search(line)
        # Filter out summary lines (Subtotal, Tax, Total) to avoid duplicates
        if match and not any(x in line for x in ["Subtotal", "Tax", "Total Due"]):
            item = {
                "description": match.group(1).strip(),
                "unit_price": float(match.group(2).replace(',', '')),
                "line_total": float(match.group(3).replace(',', ''))
            }
            data['line_items'].append(item)

    return data

if __name__ == "__main__":
    # Ensure you have an image named 'invoice.jpg' in the same directory
    image_path = 'invoice.jpg' 
    
    try:
        print(f"Processing {image_path}...")
        
        # 1. Preprocessing
        clean_img = preprocess_image(image_path)
        
        # 2. OCR Extraction
        raw_text = extract_text(clean_img)
        
        # 3. Parsing
        structured_data = parse_invoice_data(raw_text)
        
        # 4. Output
        json_output = json.dumps(structured_data, indent=4)
        print("\n--- Extracted JSON Data ---")
        print(json_output)
        
        # Optional: Save to file
        with open('output.json', 'w') as f:
            f.write(json_output)
            print("\nSuccessfully saved to output.json")
            
    except Exception as e:
        print(f"Error: {e}")
