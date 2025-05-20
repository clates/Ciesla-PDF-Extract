import os
import sys
import argparse
from convert_to_csv import convert_out_to_csv
from pdftotext import extract_all_pdfs
from combine_csv import combine_csv_files

def process_all_out_files(debug=False):
    # Create output directory if it doesn't exist
    input_dir = os.path.join('out', 'text')
    output_dir = os.path.join('out', 'csv')
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.")
        return False
    
    # Process each .out file
    processed_count = 0
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.out'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace('.out', '.csv'))
            
            try:
                print(f"Processing {input_path} -> {output_path}")
                convert_out_to_csv(input_path, output_path, debug=debug)
                processed_count += 1
                print(f"Converted to CSV: {output_path}")
            except Exception as e:
                print(f"Error processing {input_path}: {str(e)}")
    
    print(f"\nProcessing complete. Converted {processed_count} .out files to CSV.")
    return processed_count > 0

def process_workflow(extract_pdfs=True, convert_to_csv=True, combine_csvs=True, debug=False):
    """Run the complete workflow: PDF -> Text -> CSV -> Combined CSV"""
    success = True
    
    if extract_pdfs:
        print("=== STEP 1: Converting PDFs to text files ===")
        pdf_success = extract_all_pdfs()
        if not pdf_success:
            print("Warning: PDF extraction encountered issues.")
            success = False
    
    if convert_to_csv:
        print("\n=== STEP 2: Converting text files to CSV ===")
        csv_success = process_all_out_files(debug=debug)
        if not csv_success:
            print("Warning: CSV conversion encountered issues.")
            success = False
    
    if combine_csvs:
        print("\n=== STEP 3: Combining all CSVs into a single file ===")
        input_dir = os.path.join('out', 'csv')
        output_file = os.path.join('out', 'combined_invoices.csv')
        combine_success = combine_csv_files(input_dir, output_file)
        if not combine_success:
            print("Warning: CSV combination encountered issues.")
            success = False
    
    if success:
        print("\n✓ Complete workflow processed successfully!")
    else:
        print("\n⚠ Workflow completed with warnings or errors.")
    
    return success

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process PDFs to CSV via text extraction')
    parser.add_argument('--pdf-only', action='store_true', help='Only extract text from PDFs')
    parser.add_argument('--csv-only', action='store_true', help='Only convert text files to CSV')
    parser.add_argument('--combine-only', action='store_true', help='Only combine existing CSV files')
    parser.add_argument('--skip-combine', action='store_true', help='Skip the CSV combination step')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    # Determine which steps to run
    run_pdf = not (args.csv_only or args.combine_only)
    run_csv = not (args.pdf_only or args.combine_only)
    run_combine = not (args.pdf_only or args.csv_only or args.skip_combine)
    
    # Run the workflow
    process_workflow(
        extract_pdfs=run_pdf, 
        convert_to_csv=run_csv,
        combine_csvs=run_combine,
        debug=args.debug
    )
