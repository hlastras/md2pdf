#!/bin/bash

# Check if required arguments are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_markdown_file> <output_pdf_file>"
    exit 1
fi

INPUT_MD="$1"
OUTPUT_PDF="$2"

# Check if input file exists
if [ ! -f "$INPUT_MD" ]; then
    echo "Error: Input file '$INPUT_MD' not found."
    exit 1
fi

# Create temporary file names
TEMP_MD="preprocessed_$(basename "$INPUT_MD")"
TEMP_BIB="bibliography.bib"

# Determine Python command (use venv if it exists)
PYTHON_CMD="python3"
if [ -f "/app/venv/bin/python" ]; then
    PYTHON_CMD="/app/venv/bin/python"
fi

# Run the Python processing script
echo "Processing markdown file..."
$PYTHON_CMD process.py "$INPUT_MD" "$TEMP_MD" "$TEMP_BIB"

if [ ! -f "$TEMP_MD" ]; then
    echo "Error: Failed to create preprocessed markdown file."
    exit 1
fi

if [ ! -f "$TEMP_BIB" ]; then
    echo "Error: Failed to create bibliography file."
    exit 1
fi

# Run pandoc to create PDF
echo "Creating PDF..."
pandoc --citeproc --bibliography="$TEMP_BIB" --csl=cites.csl "$TEMP_MD" -o "$OUTPUT_PDF" --pdf-engine=xelatex --include-in-header=preamble.tex

# Check if the previous command failed or if the PDF was created successfully
if [ $? -ne 0 ] || [ ! -f "$OUTPUT_PDF" ]; then
    echo "Error: Failed to create PDF file."
    exit 1
fi

# Delete intermediate files
echo "Cleaning up temporary files..."
rm -f "$TEMP_MD" "$TEMP_BIB"

echo "Conversion complete: $OUTPUT_PDF" 