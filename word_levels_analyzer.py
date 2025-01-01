"""
Program rationale:
As an ELT (English Language Teaching) materials writer, I often need to create 
articles that use a specific number of words from a predefined word levels list. 
This tool automates the process of checking an article against the list. Given 
the size of the list (many thousands of words), manually verifying each word in 
a 300-word article is impractical. 

This tool:
1. Analyzes an input text file (article) to count and categorize words by their 
levels.
2. Outputs the total number of words, the number of words at each level, and 
their percentages.

Input:
1. TEXT_FILE: The article to analyze (plain text file, e.g., `test4.txt`).
2. WORD_LEVELS_FILE: A JSON file containing words and their corresponding levels, 
structured like:
    {
        "word1": "1",
        "word2": "2",
        ...
    }

Output:
- A summary of the number and percentage of words at each level, including 
unknown words.

Usage:
1. Ensure `nltk` is installed:
    pip install nltk
2. Download necessary NLTK data:
    python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
3. Run the program:
    python main.py

Dependencies:
- Python 3.6+
- NLTK (Natural Language Toolkit)

Notes:
- Words are categorized by their lemmatized form (e.g., "cats" -> "cat").
- Non-alphanumeric characters are ignored.
- Unknown words (not in the levels list) are counted separately.

Limitations:
- Designed for English text only.
- Assumes the word levels JSON file is correctly formatted.
"""

import json
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

LEVELS = ['1', '2', '3', '4', '5', '6']
UNKNOWN_KEY = 'unknown'

def tokenize_and_lemmatize(line, lemmatizer):
    """Tokenizes and lemmatizes a line of text."""
    tokens = [word for word in word_tokenize(line) if word.isalnum()]
    return [lemmatizer.lemmatize(word.lower()) for word in tokens]

def categorize(text_file, word_levels, lemmatizer):
    """Categorizes words from the text file into levels."""
    level_counts = {level: 0 for level in LEVELS}
    level_counts[UNKNOWN_KEY] = 0

    with open(text_file, "r") as file:
        for line in file:
            lemmatized_tokens = tokenize_and_lemmatize(line, lemmatizer)
            for lemma in lemmatized_tokens:
                if lemma in word_levels:
                    level = word_levels[lemma]
                    level_counts[level] = level_counts.get(level, 0) + 1
                else:
                    level_counts[UNKNOWN_KEY] += 1

    return level_counts

def print_levels(level_counts):
    """Prints the word levels with percentages."""
    total_words = sum(level_counts.values())
    for level in LEVELS + [UNKNOWN_KEY]:
        count = level_counts[level]
        percentage = (count / total_words) * 100 if total_words > 0 else 0
        print(f"{level.capitalize()} words: {count:>3} (% {percentage:.1f})")
    print(f"Total words: {total_words}")
                    
def main(text_file, word_levels_file):
    """Main function to load data and categorize text."""
    with open(word_levels_file, "r") as file:
        word_levels = json.load(file)
        
    lemmatizer = WordNetLemmatizer()
    level_counts = categorize(text_file, word_levels, lemmatizer)
    print_levels(level_counts)
    
if __name__ == "__main__":
    TEXT_FILE = "test.txt"
    WORD_LEVELS_FILE = "word_levels.json"
    main(TEXT_FILE, WORD_LEVELS_FILE)