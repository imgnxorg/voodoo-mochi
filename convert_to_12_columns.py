#!/usr/bin/env python3
"""
Script to convert the 6-column color swatch table to a 12-column format.
This will merge every two consecutive rows into one 12-column row.
"""

import re

def convert_table_to_12_columns(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert each span from 60px to 50px width
    content = re.sub(r'width:60px', 'width:50px', content)
    
    # Split content into parts: before table, table, after table
    lines = content.split('\n')
    
    # Find table boundaries
    table_start_idx = -1
    table_end_idx = -1
    
    for i, line in enumerate(lines):
        if '| ---' in line and table_start_idx == -1:
            table_start_idx = i
        elif table_start_idx != -1 and line.strip() and not line.startswith('|'):
            table_end_idx = i
            break
    
    if table_end_idx == -1:
        table_end_idx = len(lines)
    
    before_table = lines[:table_start_idx]
    table_lines = lines[table_start_idx:table_end_idx]
    after_table = lines[table_end_idx:]
    
    # Create new 12-column header
    header_line = '| ' + ' | '.join(['---'] * 12) + ' |'
    
    # Process data rows
    data_rows = []
    
    # Collect all data rows (skip header)
    for line in table_lines[1:]:  # Skip header
        if line.strip() and line.startswith('| <span'):
            # Extract each cell including the color code
            cells = re.findall(r'<span[^<]+</span><br>`[^`]+`', line)
            if cells:
                data_rows.append(cells)
    
    # Combine pairs of rows into 12-column rows
    combined_rows = []
    for i in range(0, len(data_rows), 2):
        if i + 1 < len(data_rows):
            # Combine two 6-column rows into one 12-column row
            combined_row = data_rows[i] + data_rows[i + 1]
        else:
            # If odd number of rows, pad the last row with empty cells
            combined_row = data_rows[i] + [''] * 6
        
        # Format the combined row
        row_text = '| ' + ' | '.join(combined_row) + ' |'
        combined_rows.append(row_text)
    
    # Reconstruct the full content
    new_lines = before_table + [header_line] + combined_rows + after_table
    new_content = '\n'.join(new_lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Converted table from 6 columns to 12 columns.")
    print(f"Original rows: {len(data_rows)}")
    print(f"New rows: {len(combined_rows)}")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    input_file = "_PRESS.md"
    output_file = "_PRESS_12col.md"
    convert_table_to_12_columns(input_file, output_file)
