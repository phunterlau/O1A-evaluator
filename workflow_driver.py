import os
import json
from pdf_parser import extract_text_from_pdf, parse_cv, predict_research_field
from cv_data_enrichment import enrich_cv_data
from cv_analyst import analyze_cv, generate_insights
from evaluator import O1AEvaluation, CategoryRating, evaluate_category

def process_cv(pdf_path: str) -> dict:
    # Step 1: Parse PDF
    cv_text = extract_text_from_pdf(pdf_path)
    parsed_cv = parse_cv(cv_text)
    research_fields = predict_research_field(cv_text)
    
    # Combine parsed CV and research fields
    cv_data = {**parsed_cv, "predicted_research_fields": research_fields["fields"]}
    
    # Save initial CV data
    with open("cv_data.json", "w") as f:
        json.dump(cv_data, f, indent=2)
    
    # Step 2: Enrich CV data using Semantic Scholar API
    enriched_cv_data = enrich_cv_data(cv_data)
    
    # Save enriched CV data
    with open("enriched_cv_data.json", "w") as f:
        json.dump(enriched_cv_data, f, indent=2)
    
    # Step 3: Analyze CV
    further_enriched_cv = analyze_cv(enriched_cv_data)
    insights = generate_insights(further_enriched_cv)
    
    # Save further enriched CV data
    with open("further_enriched_cv_data.json", "w") as f:
        json.dump(further_enriched_cv, f, indent=2)
    
    # Step 4: Evaluate O1A visa categories
    categories = [
        "Awards", "Membership", "Press", "Judging", "Original contribution",
        "Scholarly articles", "Critical employment", "High remuneration"
    ]
    
    category_ratings = []
    for category in categories:
        evaluation = evaluate_category(category, further_enriched_cv)
        category_ratings.append(CategoryRating(
            category=category,
            rating=evaluation["rating"],
            justification=evaluation["justification"],
            information_used=evaluation["information_used"],
            information_unused=evaluation["information_unused"]
        ))
    
    o1a_evaluation = O1AEvaluation(
        name=further_enriched_cv["name"],
        email=further_enriched_cv["email"],
        education=further_enriched_cv["education"],
        category_ratings=category_ratings
    )
    
    # Save O1A evaluation
    with open("o1a_evaluation.json", "w") as f:
        json.dump(o1a_evaluation.model_dump(), f, indent=2)
    
    # Generate markdown summary
    markdown_summary = generate_markdown_summary(o1a_evaluation, insights)
    
    with open("summary.md", "w") as f:
        f.write(markdown_summary)
    
    return {
        "o1a_evaluation": o1a_evaluation.model_dump(),
        "further_enriched_cv": further_enriched_cv,
        "markdown_summary": markdown_summary
    }

def generate_markdown_summary(o1a_evaluation: O1AEvaluation, insights: str) -> str:
    summary = f"# O1A Visa Evaluation Summary for {o1a_evaluation.name}\n\n"
    summary += f"## Applicant Information\n"
    summary += f"- Name: {o1a_evaluation.name}\n"
    summary += f"- Email: {o1a_evaluation.email}\n\n"
    summary += f"## Education\n"
    for edu in o1a_evaluation.education:
        summary += f"- {edu['degree']} from {edu['school']} ({edu['year']})\n"
    summary += f"\n## Category Evaluations\n"
    for rating in o1a_evaluation.category_ratings:
        summary += f"### {rating.category}\n"
        summary += f"- Rating: {rating.rating}\n"
        summary += f"- Justification: {rating.justification}\n\n"
    summary += f"## Insights\n{insights}\n"
    return summary

if __name__ == "__main__":
    pdf_path = "yann_cv.pdf"  # Replace with actual path
    result = process_cv(pdf_path)
    print("Processing complete. Check the output files for results.")