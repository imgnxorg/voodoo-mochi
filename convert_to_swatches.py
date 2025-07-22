#!/usr/bin/env python3
"""
Script to convert hex color codes from a text file to color swatches in markdown
"""

import sys

def convert_hex_to_swatch(hex_color):
    """Convert a hex color code to a color swatch with HTML"""
    if not hex_color.strip():
        return ""
    
    # Clean up the hex color (remove extra spaces)
    hex_color = hex_color.strip()
    
    swatch_html = f'<span style="display:inline-block;width:60px;height:20px;background-color:{hex_color};border:1px solid #ccc;"></span><br>`{hex_color}`'
    return swatch_html

def main():
    # if len(sys.argv) != 2:
        # print("Usage: python convert_to_swatches.py path/to/_COLORS.txt")
        # sys.exit(1)
    
    input_file = "./taku/box/_COLORS"  # Ensure the file has the correct extension
    output_file = input_file.lower().replace('colors', 'swatches').replace('color', 'swatch')

    if 'swatches' not in output_file:
        output_file += f"_{uuid.uuid4().hex}.md"
        else:
        output_file += ".md"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            colors = f.readlines()
        
        converted_lines = []
        for color in colors:
            color = color.strip()
            if color:  # Skip empty lines
                converted_lines.append(convert_hex_to_swatch(color))
        
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
