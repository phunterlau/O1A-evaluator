# CV Processor for O1A Visa Evaluation

## Purpose

This system processes CVs (Curriculum Vitae) and evaluates them for O1A visa eligibility. The O1A visa is for individuals with extraordinary ability in sciences, education, business, or athletics. Our system automates the initial evaluation process, providing insights into a candidate's qualifications across various categories.

## Workflow

1. **PDF Parsing**: Extract text from the uploaded CV.
2. **Data Enrichment**: Enhance CV data using external sources (e.g., Semantic Scholar API).
3. **CV Analysis**: Analyze the enriched data to identify extraordinary achievements.
4. **O1A Evaluation**: Assess the candidate's qualifications across 8 O1A visa categories.
5. **Report Generation**: Produce a detailed evaluation report and summary.

## Key Steps

### 1. PDF Parsing
- Use PyPDF2 to extract text from the uploaded PDF CV.
- Parse the extracted text to identify key information (education, publications, etc.).

### 2. Data Enrichment
- Utilize the Semantic Scholar API to gather additional details about publications.
- Enrich the CV data with citation counts, venue information, and other relevant metrics.

### 3. CV Analysis
- Label extraordinary achievements in education, awards, and employment history.
- Calculate impact metrics (e.g., publication rate vs. field median).
- Generate insights about the researcher's contributions and capabilities.

### 4. O1A Evaluation
Assess the candidate across 8 categories:
1. Awards
2. Membership
3. Press
4. Judging
5. Original contribution
6. Scholarly articles
7. Critical employment
8. High remuneration

For each category, provide a rating (low, medium, high) and justification.

### 5. Report Generation
- Create a JSON file with detailed evaluation results.
- Generate a markdown summary highlighting key findings and category ratings.

## API Usage

The system exposes a FastAPI endpoint for CV processing:

- **Endpoint**: `/process_cv/`
- **Method**: POST
- **Input**: PDF file (multipart/form-data)
- **Output**: JSON containing O1A evaluation results

## Conclusion

This CV Processor automates the initial screening for O1A visa applications, providing a standardized evaluation across key categories. It combines data extraction, enrichment, and analysis to offer insights into a candidate's extraordinary abilities and achievements.
