import json
import os
from typing import List, Dict, Any, Union
from pydantic import BaseModel, Field
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class CategoryRating(BaseModel):
    category: str
    rating: str
    justification: str
    information_used: List[Union[str, Dict[str, Any]]] = Field(default_factory=list)
    information_unused: List[Union[str, Dict[str, Any]]] = Field(default_factory=list)

class O1AEvaluation(BaseModel):
    name: str
    email: str
    education: List[Dict[str, Any]]
    category_ratings: List[CategoryRating]

def load_json_data(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)

def evaluate_category(category: str, data: Dict[str, Any]) -> Dict[str, Any]:
    # Prepare relevant data for each category
    category_data = {
        "Awards": data.get("awards", []) + data.get("major_awards", []),
        "Membership": data.get("academic_membership", []) + data.get("association_memberships", []),
        "Press": data.get("media_coverage", []),
        "Judging": data.get("conference_activities", []),
        "Original contribution": data.get("major_contributions", []),
        "Scholarly articles": data.get("publications", []),
        "Critical employment": data.get("employment_history", []),
        "High remuneration": [data.get("highest_salary", None)]
    }

    all_fields = list(data.keys())
    relevant_fields = list(category_data.keys())
    unused_fields = [field for field in all_fields if field not in relevant_fields]

    prompt = f"""
    Based solely on the following data for an O-1A visa applicant, evaluate their qualification for the category: {category}
    
    Relevant data for {category}:
    {json.dumps(category_data[category], indent=2)}
    
    Additional context:
    - For publications and media coverage, consider the 'extraordinary' label, which indicates high citation count, venue reputation, or significance of the coverage.
    - For employment, consider the 'is_critical_capacity' and 'extraordinary' fields.
    - Do not use any preexisting knowledge about the person, only the provided data.
    
    Provide a rating (low, medium, or high) on the chance that this person is qualified for an O-1A immigration visa in the {category} category.
    Justify your rating in up to 200 words using only the related data provided.
    Also, list the specific pieces of information you used in your judgment, and those you didn't use.
    
    Return your response as a JSON object with the following structure:
    {{
        "rating": "low/medium/high",
        "justification": "Your justification here",
        "information_used": ["item1", "item2", ...],
        "information_unused": ["item1", "item2", ...]
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in evaluating O-1A visa applications. Use only the provided data for your evaluation."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    evaluation = json.loads(response.choices[0].message.content)
    evaluation["information_unused"] += [field for field in unused_fields]
    return evaluation

def main():
    data = load_json_data("further_enriched_cv_data.json")
    
    categories = [
        "Awards", "Membership", "Press", "Judging", "Original contribution",
        "Scholarly articles", "Critical employment", "High remuneration"
    ]
    
    category_ratings = []
    for category in categories:
        evaluation = evaluate_category(category, data)
        category_ratings.append(CategoryRating(
            category=category,
            rating=evaluation["rating"],
            justification=evaluation["justification"],
            information_used=evaluation["information_used"],
            information_unused=evaluation["information_unused"]
        ))
    
    o1a_evaluation = O1AEvaluation(
        name=data["name"],
        email=data["email"],
        education=data["education"],
        category_ratings=category_ratings
    )
    
    output = o1a_evaluation.model_dump()
    print(json.dumps(output, indent=2))
    
    with open("o1a_evaluation.json", "w") as file:
        json.dump(output, file, indent=2)

if __name__ == "__main__":
    main()