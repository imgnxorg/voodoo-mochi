#!/usr/bin/env python3
"""
Script to convert the 6-column color swatch table to a square format.
This will adjust the table to have an equal number of columns and rows.
"""

import re
import math

def convert_table_to_square(input_file, output_file):
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
    
    # Extract data rows
    data_rows = []
    for line in table_lines[1:]:  # Skip header
        if line.strip() and line.startswith('| <span'):
            # Extract each cell including the color code
            cells = re.findall(r'<span[^<]+</span><br>`[^`]+`', line)
            if cells:
                data_rows.extend(cells)
    
    # Determine the size of the square table
    total_cells = len(data_rows)
    square_size = math.ceil(math.sqrt(total_cells))
    
    # Pad the data to make it a perfect square
    data_rows += [''] * (square_size**2 - total_cells)
    
    # Create new square table header
    header_line = '| ' + ' | '.join(['---'] * square_size) + ' |'
    
    # Format rows for the square table
    square_rows = []
    for i in range(0, len(data_rows), square_size):
        row_text = '| ' + ' | '.join(data_rows[i:i + square_size]) + ' |'
        square_rows.append(row_text)
    
    # Reconstruct the full content
    new_lines = before_table + [header_line] + square_rows + after_table
    new_content = '\n'.join(new_lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Converted table to square format.")
    print(f"Square size: {square_size}x{square_size}")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    input_file = "_PRESS.md"
    output_file = "_PRESS_square.md"
    convert_table_to_square(input_file, output_file)
