"""
Query preprocessing for better search results.
"""

import re
from typing import List


def preprocess_query(query: str) -> str:
    """
    Advanced query preprocessing for better search results.
    """
    # Convert to lowercase and strip
    query = query.lower().strip()
    
    # Skip dangerous expansions for policy queries
    if any(policy_term in query for policy_term in ['jlmt', 'policy', 'covered under', 'what are']):
        return query
    
    # Handle common abbreviations and expansions
    abbreviations = {
        'hr': 'human resources',
        'it': 'information technology',
        'admin': 'administration',
        'chp': 'captive power plant',
        'mines': 'mining',
        'procedure': 'procedures',
        'faq': 'frequently asked questions',
        'kyc': 'know your customer',
        'pf': 'provident fund',
        'esic': 'employees state insurance',
        'tds': 'tax deduction at source',
        'leave': 'leave leave holiday vacation time off absence'
    }
    
    # Replace abbreviations
    for abbr, expansion in abbreviations.items():
        query = re.sub(r'\b' + abbr + r'\b', expansion, query)
    
    # Remove extra whitespace
    query = re.sub(r'\s+', ' ', query)
    
    return query.strip()


def expand_query(query: str) -> List[str]:
    """
    Generate query variations for better recall.
    """
    variations = [query]
    
    # Add common variations
    if 'policy' in query:
        variations.append(query.replace('policy', 'policies'))
        variations.append(query.replace('policy', 'guidelines'))
        variations.append(query.replace('policy', 'procedures'))
    
    return list(set(variations))  # Remove duplicates
