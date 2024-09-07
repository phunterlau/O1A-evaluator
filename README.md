# CV Processor for O1A Visa Evaluation

## Purpose

This system processes CVs (Curriculum Vitae) and evaluates them for O1A visa eligibility, focusing on individuals with extraordinary ability in sciences, education, business, or athletics. Our system automates the initial evaluation process, providing data-driven insights into a candidate's qualifications across various categories.

## Target Audience

The primary users of this system are scientific researchers and engineers applying for O1A visas. The evaluation focuses on their publications, media coverage, peer review contributions, and other relevant accomplishments that demonstrate extraordinary ability.

## Workflow

1. **PDF Parsing**: Extract text from the uploaded CV.
2. **Data Enrichment**: Enhance CV data using external sources (e.g., Semantic Scholar API, media searches).
3. **CV Analysis**: Analyze the enriched data to identify and label extraordinary achievements.
4. **O1A Evaluation**: Assess the candidate's qualifications across 8 O1A visa categories.
5. **Report Generation**: Produce a detailed evaluation report and summary with supporting evidence.

## Key Features and Design Considerations

### Data Extraction and Enrichment
- Parse CVs for key information (education, publications, awards, etc.).
- Enrich publication data using Semantic Scholar API for citation counts and venue information.
- Predict research field to establish baselines for citation impact.
- Search major US media outlets for coverage of the candidate's work.

### Metrics and Evaluation
- Focus on metrics that demonstrate being "much better than peers in the same category."
- Compare citation counts to field medians to establish significance.
- Count patents and other non-traditional publications.
- Label extraordinary achievements in each category for final evaluation.

### O1A Category Assessment
- Evaluate across 8 categories: Awards, Membership, Press, Judging, Original contribution, Scholarly articles, Critical employment, High remuneration.
- Provide a rating (low, medium, high) with supporting data and justification for each category.
- Emphasize the need for strong evidence in at least 3 categories.

### LLM Integration
- Use LLM knowledge to assess the extraordinariness of awards, memberships, and education.
- Employ LLM for final category evaluations, ensuring use of only provided data to avoid bias or hallucination.

### Report Generation
- Create detailed JSON output with evaluation results and supporting data.
- Generate a markdown summary highlighting key findings and category ratings.

## API Usage

The system exposes a FastAPI endpoint for CV processing:

- **Endpoint**: `/process_cv/`
- **Method**: POST
- **Input**: PDF file (multipart/form-data) and optional Google Scholar profile URL
- **Output**: JSON containing O1A evaluation results with supporting evidence

## Future Improvements

1. Enhance data enrichment with more accurate citation count searches and validation.
2. Incorporate actual median citation count data for research fields instead of LLM estimates.
3. Improve handling of non-traditional publications (e.g., textbooks, patents).
4. Expand media coverage search to include more major US outlets.
5. Implement additional metrics like recent citations (within X years) and citations by high-impact papers.

## Evaluation Criteria

- Align assessments with typical profiles of researchers and engineers in the target audience.
- Compare key metrics (e.g., citation count, publication count) to field medians to identify significant achievements.
- Validate media coverage to ensure explicit mention of the candidate's major contributions.
- Provide clear, evidence-based justifications for each category rating to support the O1A application process.

## Conclusion

This CV Processor offers a data-driven, unbiased initial screening for O1A visa applications. By combining thorough data extraction, enrichment, and analysis, it provides valuable insights into a candidate's extraordinary abilities and achievements, streamlining the evaluation process for both applicants and reviewers.
