import os

langs_folder = "langs"
output_folder = "output"

def parse_language(file):
    print("Processing language: " + file)

    with open(f"{langs_folder}/{file}", 'r', encoding='utf-8') as f:
        form = {}
        current_section = None

        for line in f:
            line = line.strip()
            if len(line) == 0: 
                pass
            elif line[0].isalpha():
                current_section = []
                form[line] = current_section
            elif line[0].isnumeric():
                current_section.append(line)

    return form

def generate_language(form, lang):
    with open("templates/funcap.template.html", 'r', encoding='utf-8') as f:
        funcap_template = f.read()
    with open("templates/question.template.html", 'r', encoding='utf-8') as f:
        questions_template = f.read()
    with open("templates/section.template.html", 'r', encoding='utf-8') as f:
        sections_template = f.read()

    funcap_html = funcap_template
    funcap_html = funcap_html.replace("<!-- LANGUAGE -->", lang)
    for section, questions in form.items():
        section_html = sections_template
        section_html = section_html.replace("<!-- SECTION TEXT -->", section)
        section_html = section_html.replace("SECTION ID", f"section{section[0]}")
        for i, question in enumerate(questions):
            questions_html = questions_template
            questions_html = questions_html.replace("<!-- QUESTION TEXT -->", question)
            questions_html = questions_html.replace("SECTION NAME QUESTION NAME", f"section{section[0]}_question{i}")
            section_html = section_html.replace("<!-- QUESTIONS -->", questions_html)
        funcap_html = funcap_html.replace("<!-- SECTIONS -->", section_html)
    
    open(f"{output_folder}/funcap.{lang}.html", 'w', encoding='utf-8').write(funcap_html)
    

for file in os.listdir(langs_folder):
    lang = file.split('_')[1].split('.')[0] # questions_en.txt -> en
    parsed_form = parse_language(file)
    generate_language(parsed_form, lang)

