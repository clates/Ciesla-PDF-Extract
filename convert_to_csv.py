import csv
import re
import os

def convert_out_to_csv(input_file, output_file, debug=False):
    # Get just the filename without path
    input_filename = os.path.basename(input_file)
    
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        
        # Write the CSV header - replace Validation with Filename
        csv_writer.writerow(["ORLN", "Cust Part ID / GWS Part ID", "Rev", "Description", "Ship Qty", "Unit Price", "Amount", "Filename"])
        
        # Initialize variables
        current_item = {}
        buffer_lines = []
        data_started = False
        last_orln = 0  # Track the last ORLN number to verify sequence
        processed_items = 0
        header_found = False  # Flag to indicate if we've found the "Amount" header
        
        for line in infile:
            line = line.strip()
            
            if debug:
                print(f"Processing line: '{line}'")
            
            # Skip everything until we find the "Amount" header
            if not header_found:
                if "Amount" in line:
                    header_found = True
                    if debug:
                        print(f"Found 'Amount' header, starting to process data")
                continue
            
            # Stop processing if we hit the Total line
            if line.startswith("Total"):
                if debug:
                    print(f"Found Total line: {line} - stopping processing")
                # Process any remaining buffered item
                if current_item:
                    process_and_write_item(current_item, csv_writer, input_filename, debug)
                break
            
            # Check if line is a new ORLN (sequential number)
            if re.match(r'^\d+$', line) and (int(line) == last_orln + 1 or last_orln == 0):
                # This is the start of a new item
                
                # If we have an existing item, process it first
                if current_item and 'Ship Qty' in current_item and 'Unit Price' in current_item and 'Amount' in current_item:
                    if debug:
                        print(f"Processing complete item before new ORLN: {current_item}")
                    process_and_write_item(current_item, csv_writer, input_filename, debug)
                    processed_items += 1
                
                # Start a new item
                current_item = {'ORLN': line, 'notes': []}
                last_orln = int(line)
                buffer_lines = []
                data_started = True
                
                if debug:
                    print(f"Started new item with sequential ORLN: {line}")
            
            # If we've started collecting data items
            elif data_started:
                # Check for BACKORDER or shipping notes
                if "BACKORDER" in line or "SHIP" in line:
                    current_item['notes'].append(line)
                    if debug:
                        print(f"Added note to ORLN {current_item.get('ORLN')}: {line}")
                else:
                    # Add to buffer for current item
                    buffer_lines.append(line)
                    
                    # Try to extract part ID (format like "123-456789")
                    if 'Part ID' not in current_item:
                        part_id_match = re.search(r'\d+-\d+', line)
                        if part_id_match:
                            current_item['Part ID'] = part_id_match.group(0)
                            if debug:
                                print(f"Found Part ID: {current_item['Part ID']}")
                    
                    # Extract ship quantity - standalone number that's not a part ID
                    if 'Ship Qty' not in current_item:
                        # If line is just a number, it's likely the ship quantity
                        if re.match(r'^\d+$', line):
                            current_item['Ship Qty'] = line
                            if debug:
                                print(f"Found Ship Qty: {line}")
                    
                    # Extract unit price and amount
                    if '$' in line:
                        # Find all currency values in the line
                        currency_pattern = r'\$[\d,]+\.\d{2}'
                        currency_matches = re.findall(currency_pattern, line)
                        
                        if len(currency_matches) >= 2:
                            current_item['Unit Price'] = currency_matches[0]
                            current_item['Amount'] = currency_matches[1]
                            if debug:
                                print(f"Found Unit Price: {current_item['Unit Price']} and Amount: {current_item['Amount']}")
                        elif len(currency_matches) == 1 and 'Unit Price' not in current_item:
                            current_item['Unit Price'] = currency_matches[0]
                            if debug:
                                print(f"Found Unit Price: {current_item['Unit Price']}")
                        elif len(currency_matches) == 1 and 'Unit Price' in current_item:
                            current_item['Amount'] = currency_matches[0]
                            if debug:
                                print(f"Found Amount: {current_item['Amount']}")
                    
                    # After adding the line, try to extract description
                    if 'Part ID' in current_item and 'Description' not in current_item and len(buffer_lines) > 1:
                        # Description is typically the line after part ID that's not a quantity or price
                        for bl in buffer_lines:
                            if bl != current_item.get('Part ID') and not re.match(r'^\d+$', bl) and '$' not in bl:
                                current_item['Description'] = bl
                                if debug:
                                    print(f"Found Description: {current_item['Description']}")
                                break
        
        
        if debug:
            print(f"Processing complete. Processed {processed_items} items.")

def process_and_write_item(item, csv_writer, filename, debug=False):
    """Process the item data and write it to the CSV."""
    orln = item.get('ORLN', '')
    part_id = item.get('Part ID', '')
    description = item.get('Description', '')
    ship_qty = item.get('Ship Qty', '')
    unit_price = item.get('Unit Price', '')
    amount = item.get('Amount', '')
    
    # Perform the validation check, but only for debugging
    if debug:
        try:
            # Convert to numeric values (remove currency symbols and commas)
            qty = int(ship_qty)
            price = float(unit_price.replace('$', '').replace(',', ''))
            total = float(amount.replace('$', '').replace(',', ''))
            
            # Calculate expected total
            calculated_total = qty * price
            
            # Compare with a small tolerance for floating point errors
            if abs(calculated_total - total) > 0.01:
                print(f"VALIDATION FAILED: {qty} × {price} = {calculated_total}, not {total}")
            else:
                print("VALIDATION PASSED")
        except (ValueError, TypeError) as e:
            print(f"VALIDATION ERROR: {e}")
    
    # Write to CSV with filename instead of validation
    csv_writer.writerow([orln, part_id, "", description, ship_qty, unit_price, amount, filename])
    
    # Write any notes for this item
    for note in item.get('notes', []):
        csv_writer.writerow(["", "", "", note, "", "", "", filename])  # Also include filename in note rows

# Only run on example.out if this file is executed directly
if __name__ == "__main__":
    convert_out_to_csv('example.out', 'output.csv', debug=True)
