# OCR_for_Internship

## Project Overview
This project is an automated document processing tool designed to extract structured data from semi-structured documents (specifically invoices). It uses **Optical Character Recognition (OCR)** to convert image data into text and **Regex-based Natural Language Processing (NLP)** to identify key entities like dates, invoice numbers, and line items.

<a href="https://colab.research.google.com/drive/138alu2u-ILo6TqokHQ2kxZk-8rPR5rLU?usp=sharing" target="_blank">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Features
* **Image Preprocessing:** Uses OpenCV to convert images to grayscale and apply thresholding for better OCR accuracy.
* **Text Extraction:** Utilizes Tesseract OCR (`pytesseract`) to generate raw text from images.
* **Structured Parsing:** extract key fields (Vendor, Date, Total Amount) and tabular data (Line Items) into a standardized JSON format.
* **Noise Handling:** Includes logic to filter out OCR artifacts (e.g., malformed table headers).

## Tech Stack
* **Language:** Python 3.x
* **OCR Engine:** Tesseract OCR
* **Libraries:** `opencv-python` (cv2), `pytesseract`, `pandas` (optional), `re` (Regex)

## How to Run
1.  **Install Dependencies:**
    ```bash
    pip install opencv-python pytesseract
    ```
    *(Note: Ensure Tesseract-OCR executable is installed on your system and added to PATH)*

2.  **Run the Parser:**
    ```bash
    python main.py
    ```

* **Example:** Inputting the noisy OCR text `Description —SSSCS~S~S~S Sic]` into an LLM with the prompt *"Clean this table header"* would return the correct `Description | Qty | Unit Price | Total`.

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/fbc79977-9dd1-41ef-ab29-6fc10a37cb98" />

### Output:
When running the script on the sample invoice, the system transforms the raw OCR text into structured JSON.

Raw Text:
TECHSOLUTIONS INC.
123 Innovation Drive
Tech City, TC 54321 , 2
INVOICE
Date: 2025-10-27
Invoice #: INV-2025-0001
Bill To:
Acme Corp
456 Corporate Blvd
Business Town, BT 98765
Description —SSSCS~S~S~S Sic]
IT Consulting Services $150.00 $1,500.00
Software License - Pro $300.00 $1,500.00
Software Securie System $300.00 $1,000.00
Software Machinest Back $150.00 $600.00
Subtotal: $3,000.00
Tax (10%): $300.00
Total Due: $3,300.00

<img width="524" height="454" alt="image" src="https://github.com/user-attachments/assets/ea7ef155-6c0f-46e7-a851-c4eb8ebea0c9" />



JSON Output:
{
    "date": "2025-10-27",
    "invoice_number": "INV-2025-0001",
    "total_amount": 3300.0,
    "vendor_name": "TECHSOLUTIONS INC.",
    "line_items": [
        {
            "description": "IT Consulting Services",
            "unit_price": 150.0,
            "line_total": 1500.0
        },
        {
            "description": "Software License - Pro",
            "unit_price": 300.0,
            "line_total": 1500.0
        },
        {
            "description": "Software Securie System",
            "unit_price": 300.0,
            "line_total": 1000.0
        },
        {
            "description": "Software Machinest Back",
            "unit_price": 150.0,
            "line_total": 600.0
        }
    ]
}

<img width="570" height="632" alt="image" src="https://github.com/user-attachments/assets/90d7f059-eef8-4ae0-a338-2f65c72ae70b" />



## 🧠 Future Improvements: Generative AI & LLM Integration
While the current Regex-based approach works well for standardized templates, it can be brittle when facing varying layouts. To improve accuracy and scalability, I propose the following Generative AI enhancements:

### 1. Vision-LLM Pipeline (GPT-4o / LayoutLM)
Instead of relying on rule-based parsing, we can utilize Multimodal LLMs that understand document layout (spatial awareness).
* **Approach:** Pass the invoice image directly to a model like **GPT-4o** or fine-tune a **LayoutLMv3** model.
* **Benefit:** These models can distinguish between a "Ship To" and "Bill To" address based on position, and correctly parse complex tables without explicit regex rules.

### 2. Retrieval-Augmented Generation (RAG) for Context
For processing valid vendor names or cross-referencing purchase orders:
* **Approach:** Store valid vendor data in a vector database.
* **Workflow:** When the OCR extracts a vendor name (e.g., "TechSol Inc"), the system queries the database to match it against the canonical name ("TechSolutions Inc.") before finalizing the JSON.

### 3. Post-Processing Correction
LLMs can be used to "clean" raw OCR text.
