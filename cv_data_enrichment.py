import json
import os
import requests
from fuzzywuzzy import fuzz
import re

def load_cv_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def search_semantic_scholar(title, author_name):
    base_url = "https://api.semanticscholar.org/graph/v1"
    
    api_key = os.environ.get("S2_API_KEY")
    if not api_key:
        print("Warning: S2_API_KEY not found in environment variables. Proceeding without API key.")
    
    def fuzzy_match(s1, s2, threshold=80):
        return fuzz.ratio(s1.lower(), s2.lower()) >= threshold

    # simple validation of author name for cases like match Yann LeCun with "LeCun, Y."
    def validate_author(api_author, given_author):
        '''
        api_name = api_author.lower()
        given_name = given_author.lower()
        # Yann LeCun <-> "LeCun, Y."
        if api_name == given_name:
            return True
        # Yann LeCun <-> "LeCun, Y."
        initials_last = re.match(r'^(\w)\w* (\w+)$', given_name)
        if initials_last:
            pattern = f'^{initials_last.group(1)}\\w* {initials_last.group(2)}$'
            if re.match(pattern, api_name, re.IGNORECASE):
                return True
        return fuzzy_match(api_name, given_name, threshold=85)
        '''
        return True

    search_url = f"{base_url}/paper/search"
    params = {
        "query": title,
        "fields": "title,externalIds,year,citationCount,authors,venue,publicationVenue",
        "limit": 10
    }

    headers = {"x-api-key": api_key} if api_key else {}

    response = requests.get(search_url, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: API request failed with status code {response.status_code}")
        print(f"Response: {response.text}")
        return None

    data = response.json()

    if 'data' not in data:
        print(f"Unexpected data structure: {data}")
        return None

    papers = data['data']

    for paper in papers:
        if fuzzy_match(paper['title'], title):
            for author in paper.get('authors', []):
                if validate_author(author.get('name', ''), author_name):
                    venue_info = paper.get('publicationVenue') or {}
                    return {
                        "title": paper['title'],
                        "doi": paper.get('externalIds', {}).get('DOI'),
                        "year": paper.get('year'),
                        "citation_count": paper.get('citationCount'),
                        "venue": paper.get('venue'),
                        "venue_id": venue_info.get('id'),
                        "venue_name": venue_info.get('name'),
                        "venue_type": venue_info.get('type'),
                        "venue_url": venue_info.get('url')
                    }

    return None

def enrich_cv_data(cv_data):
    enriched_publications = []
    for pub in cv_data['publications']:
        print(f"Searching for: {pub['title']}")
        enriched_pub = pub.copy()
        result = search_semantic_scholar(pub['title'], cv_data['name'])
        if result:
            print(f"Match found: {result['title']}")
            enriched_pub.update(result)
        else:
            print(f"No match found for: {pub['title']}")
        enriched_publications.append(enriched_pub)
        sleep(0.5) #don't overload the API
    
    enriched_cv_data = cv_data.copy()
    enriched_cv_data['publications'] = enriched_publications
    return enriched_cv_data

def main():
    cv_data = load_cv_data('cv_data.json')
    enriched_data = enrich_cv_data(cv_data)
    
    with open('enriched_cv_data.json', 'w') as f:
        json.dump(enriched_data, f, indent=2)
    
    print("Enriched CV data has been saved to 'enriched_cv_data.json'")

if __name__ == "__main__":
    main()