import os
import json
from typing import List, Dict, Any
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_education(education: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    prompt = f"Analyze the following education data and label each record as 'extraordinary' if it's from a prestigious institution or involves a notable degree. Education data: {json.dumps(education)}"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in evaluating academic credentials."},
            {"role": "user", "content": prompt}
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "label_education",
                "description": "Label education records as extraordinary",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "labeled_education": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "school": {"type": "string"},
                                    "year": {"type": "integer"},
                                    "degree": {"type": "string"},
                                    "extraordinary": {"type": "string"}
                                },
                                "required": ["school", "year", "degree", "extraordinary"]
                            }
                        }
                    },
                    "required": ["labeled_education"]
                }
            }
        }],
        tool_choice={"type": "function", "function": {"name": "label_education"}}
    )
    
    return json.loads(response.choices[0].message.tool_calls[0].function.arguments)["labeled_education"]

def analyze_awards(awards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    prompt = f"Analyze the following awards data and label each record as 'extraordinary' if it's a high-stakes or prestigious award. Awards data: {json.dumps(awards)}"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in evaluating academic and scientific awards."},
            {"role": "user", "content": prompt}
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "label_awards",
                "description": "Label awards as extraordinary",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "labeled_awards": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "award": {"type": "string"},
                                    "year": {"type": "integer"},
                                    "extraordinary": {"type": "string"}
                                },
                                "required": ["award", "year", "extraordinary"]
                            }
                        }
                    },
                    "required": ["labeled_awards"]
                }
            }
        }],
        tool_choice={"type": "function", "function": {"name": "label_awards"}}
    )
    
    return json.loads(response.choices[0].message.tool_calls[0].function.arguments)["labeled_awards"]

def analyze_publications(publications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    prompt = f"Analyze the following publications data and label each record as 'extraordinary' if it has a high citation count or is published in an important journal or conference. Publications data: {json.dumps(publications)}"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in evaluating academic publications."},
            {"role": "user", "content": prompt}
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "label_publications",
                "description": "Label publications as extraordinary",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "labeled_publications": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "venue": {"type": "string"},
                                    "year": {"type": "integer"},
                                    "citation_count": {"type": "integer"},
                                    "extraordinary": {"type": "string"}
                                },
                                "required": ["title", "venue", "year", "citation_count", "extraordinary"]
                            }
                        }
                    },
                    "required": ["labeled_publications"]
                }
            }
        }],
        tool_choice={"type": "function", "function": {"name": "label_publications"}}
    )
    
    return json.loads(response.choices[0].message.tool_calls[0].function.arguments)["labeled_publications"]

def analyze_employment(employment: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    prompt = f"Analyze the following employment data and label each record as 'extraordinary' if it's a high-stakes or prestigious position. Employment data: {json.dumps(employment)}"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in evaluating academic and research positions."},
            {"role": "user", "content": prompt}
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "label_employment",
                "description": "Label employment records as extraordinary",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "labeled_employment": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "organization": {"type": "string"},
                                    "role": {"type": "string"},
                                    "year_start": {"type": "integer"},
                                    "year_end": {"type": ["integer", "null"]},
                                    "is_critical_capacity": {"type": "boolean"},
                                    "extraordinary": {"type": "string"}
                                },
                                "required": ["organization", "role", "year_start", "year_end", "is_critical_capacity", "extraordinary"]
                            }
                        }
                    },
                    "required": ["labeled_employment"]
                }
            }
        }],
        tool_choice={"type": "function", "function": {"name": "label_employment"}}
    )
    
    return json.loads(response.choices[0].message.tool_calls[0].function.arguments)["labeled_employment"]

def analyze_research_fields(cv_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    publications = cv_data['publications']
    predicted_fields = cv_data['predicted_research_fields']
    
    # Create a dictionary to store publications for each field
    field_publications = {field: [] for field in predicted_fields}
    
    # Classify each publication into fields
    for pub in publications:
        prompt = f"Classify the following publication into one or more of these research fields: {', '.join(predicted_fields)}. Publication title: {pub['title']}"
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in classifying academic publications into research fields."},
                {"role": "user", "content": prompt}
            ],
            tools=[{
                "type": "function",
                "function": {
                    "name": "classify_publication",
                    "description": "Classify a publication into research fields",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "fields": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of research fields this publication belongs to"
                            }
                        },
                        "required": ["fields"]
                    }
                }
            }],
            tool_choice={"type": "function", "function": {"name": "classify_publication"}}
        )
        
        fields = json.loads(response.choices[0].message.tool_calls[0].function.arguments)["fields"]
        
        for field in fields:
            if field in field_publications:
                field_publications[field].append(pub)
    
    # Calculate median citation count and publication count for each field
    field_metrics = []
    for field, pubs in field_publications.items():
        publication_count = len(pubs)
        citation_counts = [pub.get('citation_count', 0) for pub in pubs]
        median_citation_count = int(median(citation_counts)) if citation_counts else 0
        
        field_metrics.append({
            "field": field,
            "median_publication_count": publication_count,
            "median_citation_count": median_citation_count
        })
    
    return field_metrics

def estimate_field_statistics(fields: List[str]) -> List[Dict[str, Any]]:
    prompt = f"""
    For each of the following research fields, estimate the median annual publication count and median career citation count for researchers in that field. Consider that:
    1. Different fields may have varying publication rates and citation patterns.
    2. These are rough estimates for an average researcher over their career.
    3. Some fields may have higher publication rates but lower citation counts, or vice versa.

    Research fields: {json.dumps(fields)}

    Provide your best estimate for each field, based on general trends in academia.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in academic research trends across various fields."},
            {"role": "user", "content": prompt}
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "estimate_field_statistics",
                "description": "Estimate median publication and citation counts for researchers in each field",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "field_statistics": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {"type": "string"},
                                    "median_annual_publication_count": {"type": "number"},
                                    "median_career_citation_count": {"type": "integer"}
                                },
                                "required": ["field", "median_annual_publication_count", "median_career_citation_count"]
                            }
                        }
                    },
                    "required": ["field_statistics"]
                }
            }
        }],
        tool_choice={"type": "function", "function": {"name": "estimate_field_statistics"}}
    )
    
    return json.loads(response.choices[0].message.tool_calls[0].function.arguments)["field_statistics"]

def analyze_researcher_impact(cv_data: Dict[str, Any], field_statistics: List[Dict[str, Any]]) -> Dict[str, Any]:
    researcher_stats = {
        "total_publications": len(cv_data['publications']),
        "total_citations": sum(p.get('citation_count', 0) for p in cv_data['publications']),
        "years_active": max(p['year'] for p in cv_data['publications']) - min(p['year'] for p in cv_data['publications']) + 1
    }
    
    researcher_stats["annual_publication_rate"] = researcher_stats["total_publications"] / researcher_stats["years_active"]
    
    impact_analysis = []
    for field in field_statistics:
        field_stats = next((f for f in field_statistics if f["field"] == field["field"]), None)
        if field_stats:
            impact_analysis.append({
                "field": field["field"],
                "publication_rate_comparison": researcher_stats["annual_publication_rate"] / field_stats["median_annual_publication_count"],
                "citation_impact_comparison": researcher_stats["total_citations"] / field_stats["median_career_citation_count"]
            })
    
    return {
        "researcher_statistics": researcher_stats,
        "field_impact_analysis": impact_analysis
    }

def analyze_media_coverage(media_coverage: List[Dict[str, Any]], researcher_name: str) -> List[Dict[str, Any]]:
    prompt = f"""
    Analyze the following media coverage for {researcher_name}. Label each item as 'extraordinary' if:
    1. The report is directly related to the researcher and their work.
    2. The report appears positive or highlights the researcher's achievements.
    3. The report is from a reputable source.

    If the information is missing or the criteria are not met, leave the label value as an empty string.

    Media coverage data: {json.dumps(media_coverage)}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in analyzing media coverage of scientific researchers."},
            {"role": "user", "content": prompt}
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "label_media_coverage",
                "description": "Label media coverage as extraordinary",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "labeled_media_coverage": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "media_name": {"type": "string"},
                                    "media_domain": {"type": "string"},
                                    "title": {"type": "string"},
                                    "url_source": {"type": "string"},
                                    "description": {"type": "string"},
                                    "published_time": {"type": "string"},
                                    "extraordinary": {"type": "string"}
                                },
                                "required": ["media_name", "media_domain", "title", "url_source", "description", "published_time", "extraordinary"]
                            }
                        }
                    },
                    "required": ["labeled_media_coverage"]
                }
            }
        }],
        tool_choice={"type": "function", "function": {"name": "label_media_coverage"}}
    )
    
    return json.loads(response.choices[0].message.tool_calls[0].function.arguments)["labeled_media_coverage"]

def analyze_cv(cv_data: Dict[str, Any]) -> Dict[str, Any]:
    enriched_cv = cv_data.copy()
    
    enriched_cv['education'] = analyze_education(cv_data['education'])
    enriched_cv['awards'] = analyze_awards(cv_data['awards'])
    enriched_cv['publications'] = analyze_publications(cv_data['publications'])
    enriched_cv['employment_history'] = analyze_employment(cv_data['employment_history'])
    enriched_cv['media_coverage'] = analyze_media_coverage(cv_data['media_coverage'], cv_data['name'])
    
    return enriched_cv

def generate_insights(enriched_cv: Dict[str, Any]) -> str:
    prompt = f"""
    Generate insights about the researcher's extraordinary capabilities and contributions to the science research community based on the following enriched CV data:
    1. Analyze their education, awards, publications, and employment history.
    2. Consider their media coverage and its implications for their public profile and impact.
    3. Highlight any areas where they significantly outperform or have made groundbreaking contributions.
    4. Consider their overall impact across multiple research fields if applicable.

    Enriched CV data: {json.dumps(enriched_cv)}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in analyzing academic and research profiles. Provide concise and meaningful insights about the researcher's extraordinary capabilities and contributions, including their impact in different research fields and public recognition."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def main():
    with open("enriched_cv_data.json", "r") as file:
        cv_data = json.load(file)
    
    enriched_cv = analyze_cv(cv_data)
    insights = generate_insights(enriched_cv)
    
    print("Enriched CV Data:")
    print(json.dumps(enriched_cv, indent=2))
    print("\nInsights:")
    print(insights)
    
    # Save the enriched CV data to a new JSON file
    with open("further_enriched_cv_data.json", "w") as file:
        json.dump(enriched_cv, file, indent=2)

if __name__ == "__main__":
    main()