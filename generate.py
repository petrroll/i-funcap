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

def generate_language(form, lang, variant):
    with open("templates/funcap.template.html", 'r', encoding='utf-8') as f:
        funcap_template = f.read()
    with open("templates/question.template.html", 'r', encoding='utf-8') as f:
        questions_template = f.read()
    with open("templates/section.template.html", 'r', encoding='utf-8') as f:
        sections_template = f.read()

    funcap_html = funcap_template
    funcap_html = funcap_html.replace("<!-- TT LANGUAGE TT -->", lang)
    funcap_html = funcap_html.replace("<!-- TT VARIANT TT -->", variant)

    for section, questions in form.items():
        section_html = sections_template
        section_html = section_html.replace("<!-- TT SECTION TEXT TT -->", section)
        section_html = section_html.replace("TT SECTION ID TT", f"section{section[0]}")
        for i, question in enumerate(questions):
            questions_html = questions_template
            questions_html = questions_html.replace("<!-- TT QUESTION TEXT TT -->", question)
            questions_html = questions_html.replace("TT SECTION QUESTION ID TT", f"section{section[0]}_question{i}")
            section_html = section_html.replace("<!-- TT QUESTIONS TT -->", questions_html)
        funcap_html = funcap_html.replace("<!-- TT SECTIONS TT -->", section_html)
    
    open(f"{output_folder}/funcap.{lang}.{variant}.html", 'w', encoding='utf-8').write(funcap_html)
    
def generate_index(variants):
    with open("templates/index.template.html", 'r', encoding='utf-8') as f:
        index_template = f.read()
    with open("templates/link.template.html", 'r', encoding='utf-8') as f:
        link_template = f.read()

    index_html = index_template
    for lang, variant in variants:
        link_html = link_template
        link_html = link_html.replace("TT LANG TT", lang)
        link_html = link_html.replace("TT VARIANT TT", variant)
        index_html = index_html.replace("<!-- TT LINKS TT -->", link_html)

    open(f"{output_folder}/index.html", 'w', encoding='utf-8').write(index_html)

generated_variants = []
for file in os.listdir(langs_folder):
    lang = file.split('_')[1] # questions_en_55.txt -> en
    variant = file.split('_')[2].split('.')[0] # questions_en_55.txt -> en
    parsed_form = parse_language(file)
    generate_language(parsed_form, lang, variant)
    generated_variants.append((lang, variant))

generate_index(generated_variants)

