import json
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def categorize(text_file, word_levels, lemmatizer):
    level_counts = {
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    '6': 0,
    'unknown words': 0}
    
    with open(text_file, "r") as file:
        for line in file:
            cur_line = [word for word in word_tokenize(line) if word.isalnum()]
            for word in cur_line:
                lemma = lemmatizer.lemmatize(word.lower())
                if lemma in word_levels:
                    level_counts[word_levels[lemma]] = level_counts.get(word_levels[lemma], 0) + 1
                elif lemma != " ":
                    level_counts['unknown words'] += 1
    return level_counts

def print_levels(level_counts):
    sum = 0
    for level in level_counts:
        sum += level_counts[level]
    print("Level 1 words:", f"{level_counts['1']:>3}", "(% " + "{:.1f}".format(100*level_counts['1']/sum) + ")")
    print("Level 2 words:", f"{level_counts['2']:>3}", "(% " + "{:.1f}".format(100*level_counts['2']/sum) + ")")
    print("Level 3 words:", f"{level_counts['3']:>3}", "(% " + "{:.1f}".format(100*level_counts['3']/sum) + ")")
    print("Level 4 words:", f"{level_counts['4']:>3}", "(% " + "{:.1f}".format(100*level_counts['4']/sum) + ")")
    print("Level 5 words:", f"{level_counts['5']:>3}", "(% " + "{:.1f}".format(100*level_counts['5']/sum) + ")")
    print("Level 6 words:", f"{level_counts['6']:>3}", "(% " + "{:.1f}".format(100*level_counts['6']/sum) + ")")
    print("unknown words:", f"{level_counts['unknown words']:>3}", "(% " + "{:.1f}".format(100*level_counts['unknown words']/sum) + ")")
    print(" Total words :", sum)
                    
def main(text_file, word_levels_file):
    with open(word_levels_file, "r") as file:
        word_levels = json.load(file)
        
    lemmatizer = WordNetLemmatizer()

    level_counts = categorize(text_file, word_levels, lemmatizer)
    
    print_levels(level_counts)
    
if __name__ == "__main__":
    TEXT_FILE = "test4.txt"
    WORD_LEVELS_FILE = "word_levels.json"
    main(TEXT_FILE, WORD_LEVELS_FILE)