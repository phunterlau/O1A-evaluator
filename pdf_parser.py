import os
import json
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
import PyPDF2
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class Education(BaseModel):
    school: str
    year: int
    degree: str

class Award(BaseModel):
    award: str
    year: int

class Publication(BaseModel):
    title: str
    venue: str
    year: int
    doi: Optional[str]
    all_authors: List[str]

class Patent(BaseModel):
    title: str
    year: int
    number: str

class License(BaseModel):
    name: str
    year: int
    issuer: str

class Copyright(BaseModel):
    title: str
    year: int
    number: str

class ConferenceActivity(BaseModel):
    activity_type: str  # e.g., "panel", "peer review", "VC fund review"
    conference_name: Optional[str]
    year: int
    details: str

class Employment(BaseModel):
    organization: str
    role: str
    year_start: int
    year_end: Optional[int]
    is_critical_capacity: bool

class CVData(BaseModel):
    name: str
    email: str
    education: List[Education]
    awards: List[Award]
    academic_membership: List[str]
    publications: List[Publication]
    patents: List[Patent]
    licenses: List[License]
    copyrights: List[Copyright]
    h_index: Optional[int]
    major_awards: List[Award]
    association_memberships: List[str]
    conference_activities: List[ConferenceActivity]
    major_contributions: List[str]
    media_coverage: List[str]
    employment_history: List[Employment]
    highest_salary: Optional[float]

class ResearchFields(BaseModel):
    fields: List[str]

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def parse_cv(cv_text):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a CV parsing expert. Extract the requested information accurately from the given CV text. Leave fields empty if the information is not available."
            },
            {
                "role": "user",
                "content": f"Parse the following CV and extract key information, including additional fields such as patents, licenses, copyrights, h-index, major awards, association memberships, conference activities, major contributions, media coverage, employment history, and highest salary. Leave fields empty if not available:\n\n{cv_text}"
            },
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "extract_cv_data",
                    "description": "Extracts structured data from a CV",
                    "parameters": CVData.model_json_schema()
                }
            }
        ],
        tool_choice={"type": "function", "function": {"name": "extract_cv_data"}}
    )

    return json.loads(completion.choices[0].message.tool_calls[0].function.arguments)

def predict_research_field(cv_text):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in academic research fields. Predict the main research areas based on the given CV."
            },
            {
                "role": "user",
                "content": f"Based on the following CV, predict the person's main research field(s) in up to 3 keywords:\n\n{cv_text}"
            },
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "predict_research_fields",
                    "description": "Predicts research fields based on CV content",
                    "parameters": ResearchFields.model_json_schema()
                }
            }
        ],
        tool_choice={"type": "function", "function": {"name": "predict_research_fields"}}
    )

    return json.loads(completion.choices[0].message.tool_calls[0].function.arguments)

def main(pdf_path):
    try:
        cv_text = extract_text_from_pdf(pdf_path)
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        return
    except PyPDF2.errors.PdfReadError:
        print(f"Error: Unable to read the PDF file '{pdf_path}'. Make sure it's a valid PDF.")
        return

    parsed_cv = parse_cv(cv_text)
    research_fields = predict_research_field(cv_text)

    output = {
        **parsed_cv,
        "predicted_research_fields": research_fields["fields"]
    }

    print(json.dumps(output, indent=2))
    # save JSON to a local file
    with open("cv_data.json", "w") as file:
        json.dump(output, file, indent=2)

if __name__ == "__main__":
    main("yann_cv.pdf")