import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# ================= CONFIGURATION =================
# IF YOU ARE ON WINDOWS, UNCOMMENT THE LINE BELOW AND CHECK THE PATH:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

INPUT_DIR = "./inputs"
OUTPUT_DIR = "./outputs"
# =================================================

def exhaustive_extraction():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    if not os.path.exists(INPUT_DIR):
        print(f"Directory '{INPUT_DIR}' not found.")
        return

    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
    print(f"Found {len(files)} PDFs. Starting exhaustive extraction (Digital + OCR)...\n")

    for filename in files:
        pdf_path = os.path.join(INPUT_DIR, filename)
        txt_filename = f"{os.path.splitext(filename)[0]}_full.txt"
        output_path = os.path.join(OUTPUT_DIR, txt_filename)
        
        print(f"Processing: {filename}...")
        
        try:
            with fitz.open(pdf_path) as doc:
                full_content = []
                
                for page_num, page in enumerate(doc, start=1):
                    print(f"  -> Page {page_num}/{len(doc)}")
                    
                    # 1. Extract Digital Text (Best for standard documents)
                    digital_text = page.get_text("text", sort=True)
                    
                    # 2. Extract OCR Text (Best for scans/images)
                    # Render page to an image (zoom=2 for higher res/better OCR)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) 
                    img_data = pix.tobytes("png")
                    image = Image.open(io.BytesIO(img_data))
                    
                    # Run Tesseract
                    ocr_text = pytesseract.image_to_string(image)
                    
                    # 3. Format the Output
                    page_content = (
                        f"\n{'='*20} PAGE {page_num} {'='*20}\n"
                        f"--- [LAYER 1: DIGITAL TEXT EXTRACT] ---\n"
                        f"{digital_text.strip()}\n\n"
                        f"--- [LAYER 2: OCR IMAGE EXTRACT] ---\n"
                        f"{ocr_text.strip()}\n"
                    )
                    full_content.append(page_content)

                # Save to file
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(full_content))
                    
            print(f"✅ Completed: {output_path}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    print("\nAll done.")

if __name__ == "__main__":
    exhaustive_extraction()