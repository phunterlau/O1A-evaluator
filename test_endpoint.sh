#!/bin/bash

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq to run this script."
    exit 1
fi

# Check if a file name was provided
if [ $# -eq 0 ]; then
    echo "Error: No PDF file specified"
    echo "Usage: $0 <path_to_pdf_file>"
    exit 1
fi

# Get the PDF file path
pdf_file="$1"

# Check if the file exists
if [ ! -f "$pdf_file" ]; then
    echo "Error: File '$pdf_file' not found"
    exit 1
fi

# Check if the file is a PDF
if [[ $(file -b --mime-type "$pdf_file") != "application/pdf" ]]; then
    echo "Error: '$pdf_file' is not a PDF file"
    exit 1
fi

# API endpoint URL
api_url="http://localhost:8000/process_cv/"

echo "Sending $pdf_file to CV Processor API..."

# Send the request to the API, format the JSON with jq, and save the response to a file
curl -s -S -X POST \
    -H "Content-Type: multipart/form-data" \
    -F "file=@$pdf_file" \
    "$api_url" | jq '.' > cv_evaluation_result.json

# Check if the curl command was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to connect to the API or process the response"
    exit 1
fi

# Check if the file was created and has content
if [ -s cv_evaluation_result.json ]; then
    echo "API response saved to cv_evaluation_result.json with proper indentation"
else
    echo "Error: No data received from the API or JSON formatting failed"
    exit 1
fi