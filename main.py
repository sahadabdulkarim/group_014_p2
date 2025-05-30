import re
from re import Pattern
from document import Document
import my_module

current_collection: list[Document] = []
collection_details = {
    "url": "",
    "author": "",
    "origin": ""
}

def ui_download_collection():
    global current_collection
    global collection_details

    print("\n--- Download New Collection ---")
    url = input("Enter the URL of the .txt story collection: ")
    author = input("Enter the author of the stories: ")
    origin = input("Enter the origin/book title of the collection: ")

    regex_str = input("Enter the regex pattern to identify title and text (e.g., r'TITLE:(.*?)\\nTEXT:(.*?)'): ")
    try:
        search_pattern: Pattern[str] = re.compile(regex_str, re.IGNORECASE | re.DOTALL)
    except re.error as e:
        print(f"Invalid regex pattern: {e}")
        return
    
    while True:
        try:
            start_line_str = input("Enter the line number to start parsing from (e.g., 0 for beginning): ")
            start_line = int(start_line_str)
            if start_line < 0:
                print("Start line cannot be negative. Please enter a valid number (e.g., 0).")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number for the start line.")

    while True:
        try:
            # For end_line, 0 or negative might mean "to the end" in your module
            end_line_str = input("Enter the line number to end parsing at (e.g., 0 for no limit, or a specific line number): ")
            end_line = int(end_line_str)
            break
        except ValueError:
            print("Invalid input. Please enter a number for the end line.")

    print("\nAttempting to load documents...")
    # Function call
    current_collection = my_module.load_collection_from_url(
        url=url,
        author=author,
        origin=origin,
        start_line=start_line,
        end_line=end_line,
        search_pattern=search_pattern
    )

    if current_collection:
        print(f"Successfully loaded {len(current_collection)} documents.")
        collection_details["url"] = url
        collection_details["author"] = author
        collection_details["origin"] = origin
    else:
        print("Failed to load documents or no documents found.")

def ui_search_documents():
    """Handles the UI for searching documents (stub for now)."""
    global current_collection
    if not current_collection:
        print("No collection loaded. Please download a collection first (Option 1).")
        return
    print("\n--- Search Documents ---")
    query = input("Enter a single keyword to search for: ")

    use_filtered = input("Search with stop words removed? (yes/no): ").lower() == 'yes'

    if use_filtered:
        sample_doc = current_collection[0] if current_collection else None
        if not hasattr(sample_doc, '_filtered_terms') or not sample_doc._filtered_terms:
            print("Stopwords have not been applied/removed yet. Searching on original terms.")
            use_filtered = False

    print(f"\nSearching for '{query}' (stopword_filtered={use_filtered})...")
    results = my_module.linear_boolean_search(query, current_collection, stopword_filtered=use_filtered)
    
    found_documents = []
    for score, doc in results:
        if score == 1:
            found_documents.append(doc)
            
    if found_documents:
        print(f"\nFound {len(found_documents)} document(s) matching your query:")
        for doc in found_documents:
            print(f"  - {doc}")
    else:
        print("No documents found matching your query.")

def ui_apply_stopwords():
    global current_collection
    if not current_collection:
        print("No collection loaded. Please download a collection first (Option 1).")
        return

    print("\n--- Apply Stop Word Removal ---")
    print("Choose stop word removal method:")
    print("1. List-based (from file)")
    print("2. Frequency-based")
    print("3. Back to main menu")
    
    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        stopword_file_path = input("Enter the path to the stopword file (e.g., public_tests/englishST.txt): ")
        try:
            with open(stopword_file_path, "r", encoding='utf-8') as f:
                stopwords_set = {line.strip().lower() for line in f if line.strip()} # Ensure lowercase and non-empty
            
            print(f"\nApplying list-based stop word removal using '{stopword_file_path}'...")
            count_changed = 0
            for doc in current_collection:
                original_terms_count = len(doc.terms)
                filtered = my_module.remove_stop_words(doc.terms, stopwords_set)
                doc._filtered_terms = filtered
                doc.filtered_terms = filtered

                if len(doc.filtered_terms) != original_terms_count:
                    count_changed +=1
            print(f"List-based stop word removal applied. Terms updated for {count_changed}/{len(current_collection)} documents.")
            print(f"You can now search with 'stopword_filtered=True'.")

        except FileNotFoundError:
            print(f"Error: Stopword file not found at '{stopword_file_path}'")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif choice == '2':
        try:
            rare_freq_str = input("Enter the percentile for RARE terms (e.g., 0.9 for bottom 90% of frequencies become stopwords): ")
            common_freq_str = input("Enter the percentile for COMMON terms (e.g., 0.1 for top 10% of frequencies become stopwords): ")
            rare_freq = float(rare_freq_str)
            common_freq = float(common_freq_str)

            if not (0 <= rare_freq <= 1 and 0 <= common_freq <= 1):
                print("Percentiles must be between 0.0 and 1.0.")
                return

            print(f"\nApplying frequency-based stop word removal (rare_percentile={rare_freq}, common_percentile={common_freq})...")
            count_changed = 0
            for doc in current_collection:
                # Similar to list-based, call module's logic and update the document
                original_terms_count = len(doc.terms)
                # This directly calls module's logic
                filtered = my_module.remove_stop_words_by_frequency(doc.terms, current_collection, rare_freq, common_freq)
                doc._filtered_terms = filtered # Store in internal attribute
                doc.filtered_terms = filtered # Set direct attribute if tests rely on it

                if len(doc.filtered_terms) != original_terms_count:
                    count_changed +=1
            print(f"Frequency-based stop word removal applied. Terms updated for {count_changed}/{len(current_collection)} documents.")
            print(f"You can now search with 'stopword_filtered=True'.")

        except ValueError:
            print("Invalid input for frequencies. Please enter numbers (e.g., 0.1).")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    elif choice == '3':
        return
    else:
        print("Invalid choice.")

def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        print("\n===== Information Retrieval System =====")
        print("Current Collection:")
        if current_collection:
            print(f"  Documents: {len(current_collection)}")
            print(f"  Source: {collection_details['origin']} by {collection_details['author']}")
            print(f"  URL: {collection_details['url']}")
        else:
            print("  No collection loaded.")
        print("--------------------------------------")
        print("Options:")
        print("1. Download and parse a new story collection")
        print("2. Search documents (single keyword)")
        print("3. Apply stop word removal (placeholder)")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            ui_download_collection()
        elif choice == '2':
            ui_search_documents()
        elif choice == '3':
            ui_apply_stopwords()
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == '__main__':
    main_menu()