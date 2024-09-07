import requests
from fuzzywuzzy import fuzz
import re
import os

def search_semantic_scholar(query, author_name):
    base_url = "https://api.semanticscholar.org/graph/v1"
    
    # Load API key from environment variable
    api_key = os.environ.get("S2_API_KEY")
    if not api_key:
        print("Warning: S2_API_KEY not found in environment variables. Proceeding without API key.")
    
    # Function to perform fuzzy matching on strings
    def fuzzy_match(s1, s2, threshold=80):
        return fuzz.ratio(s1.lower(), s2.lower()) >= threshold

    # Function to validate author name
    def validate_author(api_author, given_author):
        api_name = api_author.lower()
        given_name = given_author.lower()
        
        # Check for exact match
        if api_name == given_name:
            return True
        
        # Check for first initial + last name
        initials_last = re.match(r'^(\w)\w* (\w+)$', given_name)
        if initials_last:
            pattern = f'^{initials_last.group(1)}\\w* {initials_last.group(2)}$'
            if re.match(pattern, api_name, re.IGNORECASE):
                return True
        
        # Fuzzy match for cases with middle names or slight variations
        return fuzzy_match(api_name, given_name, threshold=85)

    # Use the search endpoint for all queries
    search_url = f"{base_url}/paper/search"
    params = {
        "query": query,
        "fields": "title,externalIds,year,citationCount,authors,venue,publicationVenue",
        "limit": 10
    }

    # Prepare headers with API key if available
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
        if 'title' not in paper:
            print(f"Warning: 'title' not found in paper data: {paper}")
            continue

        # Check if the paper matches the query (either by title or DOI)
        if fuzzy_match(paper['title'], query) or query.lower() in paper.get('externalIds', {}).get('DOI', '').lower():
            for author in paper.get('authors', []):
                if 'name' not in author:
                    print(f"Warning: 'name' not found in author data: {author}")
                    continue
                if validate_author(author['name'], author_name):
                    venue_info = paper.get('publicationVenue', {})
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

def main():
    # Test examples
    test_cases = [
        ("Attention is All you Need", "Ashish Vaswani"),
        ("10.1038/nature14539", "Volodymyr Mnih"),
        ("BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "Jacob Devlin"),
        ("Mastering the game of Go with deep neural networks and tree search", "D Silver"),
        ("Nonexistent paper title", "Fake Author")
    ]

    for title_or_doi, author in test_cases:
        result = search_semantic_scholar(title_or_doi, author)
        if result:
            print(f"Found paper: {result['title']}")
            print(f"DOI: {result['doi']}")
            print(f"Year: {result['year']}")
            print(f"Citation count: {result['citation_count']}")
            print(f"Venue: {result['venue']}")
            print(f"Venue ID: {result['venue_id']}")
            print(f"Venue Name: {result['venue_name']}")
            print(f"Venue Type: {result['venue_type']}")
            print(f"Venue URL: {result['venue_url']}")
        else:
            print(f"No matching paper found for '{title_or_doi}' with author '{author}'")
        print("---")

if __name__ == "__main__":
    main()