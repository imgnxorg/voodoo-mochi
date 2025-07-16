#!/usr/bin/env python3
"""
Script to convert a 6-column markdown table to 12-column format
"""

import re

def convert_to_12_columns(input_file, output_file):
    """Convert 6-column table to 12-column format"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    output_lines = []
    
    # Process header and CSS first
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Update CSS for 12-column layout
        if 'width: 60px' in line:
            line = line.replace('width: 60px', 'width: 50px')
        if 'height: 50px' in line:
            line = line.replace('height: 50px', 'height: 40px')
        if 'border-radius: 5px' in line:
            line = line.replace('border-radius: 5px', 'border-radius: 3px')
            
        # Handle table header
        if line.startswith('| ---') and '---' in line:
            # Create 12-column header
            output_lines.append('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |')
            i += 1
            continue
            
        # Handle table rows - combine pairs of rows into single 12-column rows
        if line.startswith('| <span') and i + 1 < len(lines) and lines[i + 1].startswith('| <span'):
            # Get current row and next row
            row1 = lines[i]
            row2 = lines[i + 1]
            
            # Extract cells from both rows
            cells1 = [cell.strip() for cell in row1.split('|')[1:-1]]  # Remove first and last empty cells
            cells2 = [cell.strip() for cell in row2.split('|')[1:-1]]
            
            # Update span dimensions to 50px width
            def update_span_dimensions(cell):
                cell = cell.replace('width:60px;height:20px', 'width:50px;height:20px')
                return cell
            
            cells1 = [update_span_dimensions(cell) for cell in cells1]
            cells2 = [update_span_dimensions(cell) for cell in cells2]
            
            # Combine into 12-column row
            all_cells = cells1 + cells2
            combined_row = '| ' + ' | '.join(all_cells) + ' |'
            output_lines.append(combined_row)
            
            i += 2  # Skip the next row since we processed it
            continue
            
        # Handle single remaining row (if odd number of rows)
        elif line.startswith('| <span'):
            # Extract cells and pad to 12 columns
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            
            # Update span dimensions
            def update_span_dimensions(cell):
                cell = cell.replace('width:60px;height:20px', 'width:50px;height:20px')
                return cell
            
            cells = [update_span_dimensions(cell) for cell in cells]
            
            # Pad with empty cells to make 12 columns
            while len(cells) < 12:
                cells.append('')
            
            combined_row = '| ' + ' | '.join(cells) + ' |'
            output_lines.append(combined_row)
            i += 1
            continue
        
        # For all other lines, just copy them
        output_lines.append(line)
        i += 1
    
    # Write the output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"12-column version saved as: {output_file}")

if __name__ == "__main__":
    convert_to_12_columns('_PRESS.md', '_PRESS_12col.md')
