import os
import re

def is_bip39_phrase(phrase, bip_words):
    words = phrase.split()
    if len(words) in {12, 15, 18, 21, 24} and all(word in bip_words for word in words):
        print("Нашел совпадение: " + phrase)
        return True
    
def normalize_phrase(phrase):
    return ' '.join(phrase.lower().split())

def remove_duplicates(i, o):
    seen_phrases = set()
    unique_phrases = []

    with open(i, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        try:
            phrase, file_path = line.strip().split(' | ')
            normalized_phrase = normalize_phrase(phrase)

            if normalized_phrase not in seen_phrases:
                seen_phrases.add(normalized_phrase)
                unique_phrases.append(line.strip())
        except ValueError:
            continue

    with open(o, 'w', encoding='utf-8') as f:
        for unique_line in unique_phrases:
            f.write(unique_line + '\n')

def parse_phrases(directory, bip_words):
    found_phrases = set()

    for root, _, files in os.walk(directory, bip_words):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    potential_phrases = re.findall(r'\b(?:\w+\s+){11,23}\w+\b', content)

                    for phrase in potential_phrases:
                        normal_phrase = normalize_phrase(phrase)
                        if is_bip39_phrase(normal_phrase, bip_words):
                            found_phrases.add((normal_phrase, file_path))
            except:
                pass

    return found_phrases

if __name__ == "__main__":
    dir = '.'
    with open("bip39_words.txt", "r") as f:
        bip_words = set(f.read().split())
    
    results = parse_phrases(dir, bip_words)
    
    with open("results.txt", 'w', encoding='utf-8') as f:
        for phrase, file_path in results:
            f.write(f"{phrase} | {file_path}\n")
            
    remove_duplicates(i="results.txt", o="uniq_results.txt")