import os
import csv
import glob

def combine_csv_files(input_dir, output_file):
    """Combine all CSV files in input_dir into a single output file"""
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.")
        return False
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Get all CSV files in the input directory
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in '{input_dir}'.")
        return False
    
    print(f"Found {len(csv_files)} CSV files to combine.")
    
    # Initialize counters
    total_rows = 0
    processed_files = 0
    
    # Open the output file for writing
    with open(output_file, 'w', newline='') as outfile:
        csv_writer = None  # Will be initialized with the first file's headers
        
        # Process each CSV file
        for i, file_path in enumerate(csv_files):
            try:
                with open(file_path, 'r', newline='') as infile:
                    csv_reader = csv.reader(infile)
                    
                    # Get headers from the first file
                    if i == 0:
                        headers = next(csv_reader)
                        csv_writer = csv.writer(outfile)
                        csv_writer.writerow(headers)
                        print(f"Using headers: {headers}")
                    else:
                        # Skip headers for subsequent files
                        next(csv_reader)
                    
                    # Write all rows from this file to the combined file
                    file_rows = 0
                    for row in csv_reader:
                        csv_writer.writerow(row)
                        file_rows += 1
                    
                    total_rows += file_rows
                    processed_files += 1
                    print(f"Added {file_rows} rows from {os.path.basename(file_path)}")
                    
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
    
    print(f"\nCombined CSV creation complete:")
    print(f"- Processed {processed_files} of {len(csv_files)} files")
    print(f"- Total rows written: {total_rows}")
    print(f"- Output file: {output_file}")
    
    return True

# Update process_all.py to include the CSV combination step
def update_process_workflow():
    input_dir = os.path.join('out', 'csv')
    output_file = os.path.join('out', 'combined_invoices.csv')
    
    result = combine_csv_files(input_dir, output_file)
    return result

if __name__ == "__main__":
    update_process_workflow()
