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
    
    # Step 2: Enrich CV data using Semantic Scholar API
    enriched_cv_data = enrich_cv_data(cv_data)
    
    # Step 3: Analyze CV
    further_enriched_cv = analyze_cv(enriched_cv_data)
    insights = generate_insights(further_enriched_cv)
    
    # Step 4: Evaluate O1A visa categories
    categories = [
        "Awards", "Membership", "Press", "Judging", "Original contribution",
        "Scholarly articles", "Critical employment", "High remuneration"
    ]
    
    category_ratings = []
    qualifying_achievements = []
    overall_rating = "low"
    rating_counts = {"low": 0, "medium": 0, "high": 0}
    
    for category in categories:
        evaluation = evaluate_category(category, further_enriched_cv)
        category_rating = CategoryRating(
            category=category,
            rating=evaluation["rating"],
            justification=evaluation["justification"],
            information_used=evaluation["information_used"],
            information_unused=evaluation["information_unused"]
        )
        category_ratings.append(category_rating)
        
        # Count ratings for overall assessment
        rating_counts[evaluation["rating"]] += 1
        
        # Collect qualifying achievements
        if evaluation["rating"] in ["medium", "high"]:
            qualifying_achievements.extend(evaluation["information_used"])
    
    # Determine overall rating
    if rating_counts["high"] >= 3 or (rating_counts["high"] + rating_counts["medium"] >= 5):
        overall_rating = "high"
    elif rating_counts["high"] >= 1 or rating_counts["medium"] >= 3:
        overall_rating = "medium"
    
    o1a_evaluation = O1AEvaluation(
        name=further_enriched_cv["name"],
        email=further_enriched_cv["email"],
        education=further_enriched_cv["education"],
        category_ratings=category_ratings
    )
    
    # Prepare the final output
    output = {
        "raw_data": further_enriched_cv,
        "o1a_evaluation": o1a_evaluation.model_dump(),
        "qualifying_achievements": qualifying_achievements,  # No need to remove duplicates as they're now complex objects
        "overall_rating": overall_rating,
        "insights": insights
    }
    
    return output

def generate_markdown_summary(output: dict) -> str:
    summary = f"# O1A Visa Evaluation Summary for {output['o1a_evaluation']['name']}\n\n"
    summary += f"## Applicant Information\n"
    summary += f"- Name: {output['o1a_evaluation']['name']}\n"
    summary += f"- Email: {output['o1a_evaluation']['email']}\n\n"
    summary += f"## Education\n"
    for edu in output['o1a_evaluation']['education']:
        summary += f"- {edu['degree']} from {edu['school']} ({edu['year']})\n"
    summary += f"\n## Overall O-1A Qualification Rating: {output['overall_rating'].upper()}\n"
    summary += f"\n## Qualifying Achievements\n"
    for achievement in output['qualifying_achievements']:
        summary += f"- {json.dumps(achievement)}\n"
    summary += f"\n## Category Evaluations\n"
    for rating in output['o1a_evaluation']['category_ratings']:
        summary += f"### {rating['category']}\n"
        summary += f"- Rating: {rating['rating']}\n"
        summary += f"- Justification: {rating['justification']}\n"
        summary += f"- Information used:\n"
        for info in rating['information_used']:
            summary += f"  - {json.dumps(info)}\n"
        summary += "\n"
    summary += f"## Insights\n{output['insights']}\n"
    return summary

if __name__ == "__main__":
    pdf_path = "yann_cv.pdf"
    result = process_cv(pdf_path)
    print(json.dumps(result, indent=2))
    
    summary = generate_markdown_summary(result)
    with open("summary.md", "w") as f:
        f.write(summary)
    print("Processing complete. Check the output files for results.")