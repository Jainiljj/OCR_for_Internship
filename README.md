# OCR_for_Internship

## Project Overview
This project is an automated document processing tool designed to extract structured data from semi-structured documents (specifically invoices). It uses **Optical Character Recognition (OCR)** to convert image data into text and **Regex-based Natural Language Processing (NLP)** to identify key entities like dates, invoice numbers, and line items.

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
* **Example:** Inputting the noisy OCR text `Description —SSSCS~S~S~S Sic]` into an LLM with the prompt *"Clean this table header"* would return the correct `Description | Qty | Unit Price | Total`.

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/fbc79977-9dd1-41ef-ab29-6fc10a37cb98" />


