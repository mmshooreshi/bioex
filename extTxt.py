import os
import fitz  # This is PyMuPDF

def extract_text_from_pdfs(input_dir="./inputs", output_dir="./outputs"):
    # Ensure directories exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if not os.path.exists(input_dir):
        print(f"Error: The directory {input_dir} does not exist.")
        return

    # List all files in the input directory
    files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not files:
        print("No PDF files found in the inputs directory.")
        return

    print(f"Found {len(files)} PDF files. Starting extraction...\n")

    for filename in files:
        pdf_path = os.path.join(input_dir, filename)
        txt_filename = f"{os.path.splitext(filename)[0]}.txt"
        output_path = os.path.join(output_dir, txt_filename)
        
        print(f"Processing: {filename}...")
        
        try:
            # Open the PDF file
            with fitz.open(pdf_path) as doc:
                full_text = []
                
                # Iterate over each page
                for page_num, page in enumerate(doc, start=1):
                    # extract_text("text") grabs plain text. 
                    # flags=fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE helps precision
                    # sort=True attempts to order text logically (good for columns)
                    page_text = page.get_text("text", sort=True)
                    
                    # Add a marker for page breaks (optional, but helpful for context)
                    full_text.append(f"--- Page {page_num} ---\n{page_text}")
                
                # Join all pages and write to file
                final_content = "\n".join(full_text)
                
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(final_content)
                    
            print(f"   -> Saved to: {output_path}")

        except Exception as e:
            print(f"   -> FAILED to process {filename}: {e}")

    print("\nExtraction complete.")

if __name__ == "__main__":
    extract_text_from_pdfs()