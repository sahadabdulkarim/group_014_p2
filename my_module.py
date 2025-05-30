from document import Document
from re import Pattern
import urllib.request
from http.client import HTTPResponse
import re
import math
from collections import Counter


def remove_stop_words(terms: list[str], stopwords: set[str]) -> list[str]:
    lowercase_stopwords = {sw.lower() for sw in stopwords}
    filtered_list = []
    for term_original_case in terms:
        term_lower = term_original_case.lower()
        if term_lower not in lowercase_stopwords:
            filtered_list.append(term_lower)
    # loggers
    print(f"my_module.remove_stop_words called.")
    print(f"  Original terms (first 10): {terms[:10]}")
    print(f"  Stopwords (first 5 from set): {list(lowercase_stopwords)[:5]}")
    print(f"  Filtered terms (first 10): {filtered_list[:10]}")
    return filtered_list

# Helper function (can remain as is, or be part of the class/module)
def _get_percentile_value(sorted_values: list, percentile: float) -> float:
    """Helper to compute percentile value. Assumes sorted_values is not empty."""
    if not sorted_values:
        return 0.0 

    index = math.ceil(len(sorted_values) * percentile) - 1
    index = max(0, min(index, len(sorted_values) - 1)) 
    return float(sorted_values[index])


def remove_stop_words_by_frequency(terms: list[str], collection: list[Document], low_freq: float, high_freq: float) -> list[str]:
    if not collection:
        return terms
    all_terms_in_collection = []

    for doc_from_coll in collection:
        all_terms_in_collection.extend(doc_from_coll.terms)

    if not all_terms_in_collection:
        return terms
    
    term_counts = Counter(all_terms_in_collection)
    
    if not term_counts:
        return terms
        
    unique_frequencies_sorted = sorted(list(term_counts.values()))

    percentile_for_common_cutoff = 1.0 - high_freq 
    freq_threshold_common = _get_percentile_value(unique_frequencies_sorted, percentile_for_common_cutoff)

    freq_threshold_rare = _get_percentile_value(unique_frequencies_sorted, low_freq)

    stopwords_by_frequency = set()
    for term_val, count in term_counts.items():
        if count >= freq_threshold_common or count <= freq_threshold_rare:
            stopwords_by_frequency.add(term_val)

    final_filtered_terms = []
    
    for input_term in terms:
        if input_term not in stopwords_by_frequency:
            final_filtered_terms.append(input_term)

    return final_filtered_terms

def load_collection_from_url(url: str, search_pattern: Pattern[str], start_line: int, end_line: int, author: str, origin: str) -> list[Document]:
    full_text = ""
    print(f"Attempting to download from: {url}")
    try:
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                charset = response.info().get_content_charset() or 'utf-8'
                full_text = response.read().decode(charset)
                print("Download successful.")
            else:
                print(f"Error downloading URL {url}: HTTP status code {response.getcode()}")
                return []
    except Exception as e:
        print(f"Error downloading URL {url}: {e}")
        return [] # Returning empty list on download failure
    
    lines = full_text.splitlines()
    
    if start_line < 0:
        start_line = 0 # Ensure start_line is not negative.

    if end_line is not None and end_line > 0:
        print(f"Slicing lines from {start_line} to {end_line} (exclusive)")
        selected_lines_list = lines[start_line:end_line]
    else:
        print(f"Slicing lines from {start_line} to the end")
        selected_lines_list = lines[start_line:]

    content_to_parse = "\n".join(selected_lines_list)

    # For debugging:
    print(f"Content to parse (first 500 chars):\n{content_to_parse[:500]}")

    documents: list[Document] = []
    doc_id_counter = 0

    for match in search_pattern.finditer(content_to_parse):
        title = match.group(1).strip()
        story_text_from_regex = match.group(2)

        raw_text = story_text_from_regex.replace('\n', ' ').strip()
        raw_text = re.sub(r'\s+', ' ', raw_text) # Consolidate multiple spaces

        text_for_tokenization = story_text_from_regex.lower()
        terms = re.findall(r"\b[a-z0-9']+\b", text_for_tokenization)

        doc = Document(document_id=doc_id_counter,
                       title=title,
                       raw_text=raw_text,
                       terms=terms,
                       author=author,
                       origin=origin)
        documents.append(doc)
        doc_id_counter += 1

        # For debugging:
        print(f"Created Doc ID: {doc.document_id}, Title: {doc.title}")
        print(f"  Raw text (first 50): {doc.raw_text[:50]}...")
        print(f"  Terms (first 10): {doc.terms[:10]}")

    print(f"Successfully parsed {len(documents)} documents.")
    return documents

def linear_boolean_search(term: str, collection: list[Document], stopword_filtered: bool = False) -> list[tuple[float, Document]]:
    results: list[tuple[int, Document]] = []

    # Convert the search term to lowercase
    search_term_lower = term.lower()

    # print(f"my_module.linear_boolean_search called with term: {term} (searching for '{search_term_lower}'), stopword_filtered: {stopword_filtered}")

    for doc in collection:
        source_terms = []
        if stopword_filtered:
            source_terms = doc._filtered_terms 
        else:
            source_terms = doc.terms
        
        found = False
        for t_doc in source_terms:
            if search_term_lower == t_doc.lower(): # Compare lowercase with lowercase
                found = True
                break
        
        relevance_score = 1 if found else 0
        results.append((relevance_score, doc))

    return results
