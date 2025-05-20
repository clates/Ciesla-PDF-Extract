# importing required modules
import os
from pypdf import PdfReader

def extract_all_pdfs():
    # Create output directory if it doesn't exist
    output_dir = os.path.join('out', 'text')
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all PDF files from the filesToExtract directory
    input_dir = 'filesToExtract'
    processed_count = 0
    
    # Check if directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' not found.")
        return False
    
    # Process each PDF file in the directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace('.pdf', '.out'))
            
            try:
                # Extract text from PDF
                print(f"Processing {input_path}")
                reader = PdfReader(input_path)
                
                # Open output file for writing
                with open(output_path, 'w', encoding='utf-8') as outfile:
                    # Process each page in the PDF
                    for i, page in enumerate(reader.pages):
                        text = page.extract_text()
                        outfile.write(text + '\n')
                
                processed_count += 1
                print(f"Extracted text saved to {output_path}")
                
            except Exception as e:
                print(f"Error processing {input_path}: {str(e)}")
    
    print(f"\nProcessing complete. Extracted text from {processed_count} PDF files.")
    return processed_count > 0

# Only run extraction if this file is executed directly
if __name__ == "__main__":
    extract_all_pdfs()