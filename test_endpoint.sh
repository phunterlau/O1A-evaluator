#!/bin/bash

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

# Send the request to the API and capture both stdout and stderr
response=$(curl -s -S -X POST \
    -H "Content-Type: multipart/form-data" \
    -F "file=@$pdf_file" \
    "$api_url" 2>&1)

# Check if the curl command was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to connect to the API"
    echo "Response:"
    echo "$response"
    exit 1
fi

# Check if the response is an error message
if [[ "$response" == *"detail"* ]]; then
    echo "API returned an error:"
    echo "$response" | jq '.'
    exit 1
fi

# Clean the response: remove control characters
cleaned_response=$(echo "$response" | tr -d '[:cntrl:]' | sed 's/\\n/ /g')

# Print the cleaned response
echo "API Response:"
echo "$cleaned_response" | jq '.'

# Save the cleaned response to a file
echo "$cleaned_response" > cv_evaluation_result.json
echo "Result saved to cv_evaluation_result.json"