#!/usr/bin/env python3
"""
Script to convert hex color codes in a markdown table to color swatches
"""

import re
import sys

def convert_hex_to_swatch(hex_color):
    """Convert a hex color code to a color swatch with HTML"""
    if not hex_color.strip():
        return ""
    
    # Clean up the hex color (remove extra spaces)
    hex_color = hex_color.strip()
    
    swatch_html = f'<span style="display:inline-block;width:60px;height:20px;background-color:{hex_color};border:1px solid #ccc;"></span><br>`{hex_color}`'
    return swatch_html

def convert_table_row(line):
    """Convert a table row with hex codes to swatches"""
    if not line.startswith('|') or '-----' in line or 'Column' in line:
        return line
    
    # Split the line by pipes and process each cell
    cells = line.split('|')
    converted_cells = []
    
    for i, cell in enumerate(cells):
        cell = cell.strip()
        if i == 0 or i == len(cells) - 1:  # First and last are empty due to split
            converted_cells.append(cell)
        elif cell.startswith('#') or cell.upper().startswith('#'):
            # This is a hex color code
            converted_cells.append(' ' + convert_hex_to_swatch(cell) + ' ')
        else:
            converted_cells.append(' ' + cell + ' ')
    
    return '|'.join(converted_cells)

def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_to_swatches.py input_file.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = input_file.replace('.md', '_swatches.md')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        converted_lines = []
        for line in lines:
            converted_line = convert_table_row(line.rstrip())
            converted_lines.append(converted_line)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(converted_lines))
        
        print(f"Converted file saved as: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
