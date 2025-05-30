# Information Retrieval - Practical Assignment PR02
## Brandenburgische Technische Universität Cottbus - Senftenberg
### Database and Information Systems Group

**Module:** Information Retrieval
**Group Number:** 014
**Assignment:** PR02 - Document Handling, Stop Words, Basic Boolean Retrieval

## Project Description

This project implements a rudimentary information retrieval system as part of the Practical Assignment PR02. The system includes functionalities for handling document collections, performing basic Boolean searches, and applying stop word removal using both list-based and frequency-based methods. The project adheres to the specifications outlined in the `IR_PR02.pdf` task sheet.

## Files Included in Submission

The submission ZIP archive (`group_014_p2.zip`) contains the following source files directly in its root:
* `my_module.py`: Contains the core logic for all implemented information retrieval functionalities.
* `test_wrapper.py`: Acts as a bridge between the internal implementation in `my_module.py` and the provided unit tests. This file has been configured to correctly call the functions in `my_module.py`.
* `document.py`: Contains the provided `Document` class definition.
* `main.py`: A simple text-based user interface to interact with the IR system's functionalities.

## How to Run the Code

1.  Ensure you have Python 3.10 installed, as required by the assignment.
2.  Place all submitted `.py` files (`my_module.py`, `test_wrapper.py`, `document.py`, `main.py`) in the same directory.
3.  Navigate to this directory in your terminal or command prompt.
4.  Run the main user interface using the command:
    ```bash
    python main.py
    ```
5.  Follow the on-screen menu options to:
    * Download and parse a story collection from a URL.
    * Search documents using a single Boolean keyword query.
    * Apply stop word removal (list-based or frequency-based).

## Implemented Features

The project successfully implements the features described in Tasks 1-4 of the assignment sheet:

### Task 1: Basic IR System
* A text-based user interface (`main.py`) allows interaction with all core functionalities.
* Processing logic is separated into `my_module.py`.

### Task 2: Preparation of the document collection
* The system can download plain-text files from a URL.
* It extracts individual stories/chapters based on a user-provided regex pattern, start/end lines, author, and origin information.
* For each story, it identifies the title and main text, tokenizes the text into terms (lowercase, handling punctuation and apostrophes), and creates a `Document` object.
* All `Document` object fields (`document_id`, `title`, `raw_text`, `terms`, `author`, `origin`) are populated.

### Task 3: Simple Linear Search
* The system supports searching for a single term using a Boolean model (documents containing the term are returned with a score of 1, others with 0).
* Matching is case-insensitive.
* Search can be performed on original terms or terms filtered by stop word removal.

### Task 4: Stop Word Removal
* **General**: Stop word removal is case-insensitive. Tokenization handles punctuation and apostrophes as specified.
* **List-based Removal**:
    * Loads a stop word list from a user-specified file.
    * Filters terms in a given document based on this list.
* **Frequency-based Removal (J. C. Crouch's method)**:
    * Computes term frequencies across a provided collection.
    * Selects stop words based on frequency percentiles (too common / too rare).
    * Filters terms in a given document accordingly.
* **Libraries**: No external IR-specific libraries (like NLTK) were used for these core functionalities; only standard Python modules were used.

## Unit Tests
All provided unit tests in the `public_tests/` folder pass with this implementation when run via `test_wrapper.py`.

---