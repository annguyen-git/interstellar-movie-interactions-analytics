import requests
import re
import PyPDF2
import pandas as pd
from collections import defaultdict


# Step 1: Download PDF files from urls
def get_files(url_list):
    for name, url in url_list.items():
        response = requests.get(url)
        if response.status_code == 200:
            filename = f'data/{name}.pdf'
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {name}, status code: {response.status_code}")

# Step 2: Convert PDFs to text files
def pdf_to_text(url_list):
    for name in url_list.keys():
        pdf_path = f'data/{name}.pdf'
        output_txt = f'data/{name}.txt'
        
        # Open each PDF and read its content
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''

            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() if page.extract_text() else ''

        # Write the text to a .txt file
        with open(output_txt, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
        print(f"Converted {pdf_path} to {output_txt}")


# Since it is a moie script, it is easy to extract character's names using Regex. I'm looking for any capital line, followed by a whitespace.
def extract_character_names(script_text):
    pattern = r"^\s*([A-Z ']+)\s*$"
    
    names = []
    for line in script_text.splitlines():
        match = re.match(pattern, line)
        if match:
            name = match.group(1).strip()
            if name:
                names.append(name)
    return sorted(set(names))

# Parse the script to get the structure only
def parse_script(script_text):
    # Pattern for scene transitions (INT./EXT.)
    scene_pattern = r'^\s*(INT|EXT)\b.*$'
    # Pattern for character names
    name_pattern = r"^\s*([A-Z '\(\)]+)\s*$"

    # Result list to store parsed elements
    parsed_script = []
    
    for line in script_text.splitlines():
        # Check for scene markers
        if re.match(scene_pattern, line):
            parsed_script.append('SCENE_CHANGE')
        # Check for character names
        elif re.match(name_pattern, line):
            name = re.match(name_pattern, line).group(1).strip()
            parsed_script.append(name)
    return parsed_script

# Count interactions
def count_interactions(parsed_script):
    interactions = defaultdict(lambda: {'direct': 0, 'indirect': 0})
    current_scene_characters = []  # Track characters in the current scene
    
    for i, item in enumerate(parsed_script):
        if item == 'SCENE_CHANGE':
            # Process interactions within the current scene
            for j in range(len(current_scene_characters) - 1):
                for k in range(j + 1, min(j + 3, len(current_scene_characters))):
                    char1 = current_scene_characters[j]
                    char2 = current_scene_characters[k]
                    
                    if char1 != char2:
                        if k == j + 1:
                            interactions[frozenset([char1, char2])]['direct'] += 1
                        elif k == j + 2:
                            interactions[frozenset([char1, char2])]['indirect'] += 1
            # Reset characters for the next scene
            current_scene_characters = []
        else:
            # Add character to current scene
            current_scene_characters.append(item)
    
    return interactions

from collections import defaultdict

def count_interactions_df(parsed_script):
    interactions = defaultdict(lambda: {'direct': 0, 'indirect': 0})
    current_scene_characters = []  # Track characters in the current scene
    
    for i, item in enumerate(parsed_script):
        if item == 'SCENE_CHANGE':
            # Process interactions within the current scene
            for j in range(len(current_scene_characters) - 1):
                for k in range(j + 1, min(j + 3, len(current_scene_characters))):
                    char1 = current_scene_characters[j]
                    char2 = current_scene_characters[k]
                    
                    if char1 != char2:
                        key = tuple(sorted([char1, char2]))
                        if k == j + 1:
                            interactions[key]['direct'] += 1
                        elif k == j + 2:
                            interactions[key]['indirect'] += 1
            # Reset characters for the next scene
            current_scene_characters.clear()
        else:
            # Add character to current scene
            current_scene_characters.append(item)
    
    results = []
    for (char1, char2), counts in interactions.items():
        results.append({
            'character1': char1,
            'character2': char2,
            'direct_interaction': counts['direct'],
            'indirect_interaction': counts['indirect']
        })
    
    # Convert to a DataFrame
    df = pd.DataFrame(results)
    
    return df
