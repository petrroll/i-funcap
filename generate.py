from io import TextIOWrapper
import os

langs_folder = "langs"
output_folder = "output"
static_folder = "static"

def clear_directory(directory: str):
    if os.path.exists(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                clear_directory(item_path)
            else:
                os.remove(item_path)
        os.rmdir(directory)

def copy_static_folder(src_folder: str, dst_folder: str):
    if os.path.exists(dst_folder):
        clear_directory(dst_folder)
    else:
        os.makedirs(dst_folder)

    for item in os.listdir(src_folder):
        s = os.path.join(src_folder, item)
        d = os.path.join(dst_folder, item)
        if os.path.isdir(s):
            if not os.path.exists(d):
                os.makedirs(d)
            copy_static_folder(s, d)
        else:
            if not os.path.exists(os.path.dirname(d)):
                os.makedirs(os.path.dirname(d))
            with open(s, 'rb') as source_file:
                data = source_file.read()
            with open(d, 'wb') as dest_file:
                dest_file.write(data)

def read_block_lines(f: TextIOWrapper) -> list[str]:
    lines = []
    for line in f:
        line = line.strip()
        if len(line) == 0:
            if len(lines) <= 0:
                raise Exception("Unexpected Empty section")
            break
        else:
            line = line.replace("*", "<b>", 1).replace("*", "</b>", 1).replace(">>", "<span class=\"quote\">", 1).replace("<<", "</span>", 1)
            lines.append(line)
    return lines

def parse_language(file: str):
    print("Processing language: " + file)

    with open(f"{langs_folder}/{file}", 'r', encoding='utf-8') as f:
        description = read_block_lines(f)
        instruction = read_block_lines(f)
        options_explanation = read_block_lines(f)

        form: dict[str, list[str]] = {}
        current_section = None
        for line in f:
            line = line.strip()
            if len(line) == 0: 
                raise Exception("Unexpected Empty line in file")
            elif line[0].isalpha():
                current_section = []
                form[line] = current_section
            elif line[0].isnumeric():
                parts = line.split(' ', 1)
                number = parts[0]
                text = parts[1]
                current_section.append(f"<span class=\"question__number\">{number}</span><span class=\"question__title\">{text}</span>")
        if len(form) <= 0:
            raise Exception("Unexpected no questions")

    return (form, (description, instruction, options_explanation))

def generate_language(data: tuple[dict[str, list[str]], tuple[list[str], list[str], list[str]]], lang: str, variant: str):
    with open("templates/funcap.template.html", 'r', encoding='utf-8') as f:
        funcap_template = f.read()
    with open("templates/question.template.html", 'r', encoding='utf-8') as f:
        questions_template = f.read()
    with open("templates/section.template.html", 'r', encoding='utf-8') as f:
        sections_template = f.read()

    form, (description, instruction, options_explanation) = data

    funcap_html = funcap_template
    funcap_html = funcap_html.replace("<!-- TT LANGUAGE TT -->", lang)
    funcap_html = funcap_html.replace("<!-- TT VARIANT TT -->", variant)

    processed_description = "<br>".join(description).replace("%%", "<br>")
    processed_instruction = "<br>".join(instruction).replace("%%", "<br>")
    funcap_html = funcap_html.replace("<!-- TT DESCRIPTION TT -->", f"<p>\n{processed_description}\n</p>\n<p>{processed_instruction}\n</p>")

    processed_options_explanation = []
    for line in options_explanation:
        parts = line.replace("<b>", "").replace("</b>", "").split(" ", 1)
        if len(parts) == 2:
            number, text = parts
            formatted_line = f"<p class=\"score__line\"><b>{number}</b><span>{text}</span></p>"
            processed_options_explanation.append(formatted_line)

    funcap_html = funcap_html.replace("<!-- TT OPTIONS EXPLANATION TT -->", "".join(processed_options_explanation))

    section_header_html = ""
    for section, questions in form.items():
        section_title = section.split(' ', 1)[1] if ' ' in section else section
        section_header_html += f"<div data-section=\"section{section.split(' ', 1)[0]}\" class=\"result-overview__item\"><p>{section_title}</p><span class=\"result-overview__average\">0</span></div>"

        section_html = sections_template
        section_html = section_html.replace("<!-- TT SECTION LETTER TT -->", section.split(' ', 1)[0])
        section_html = section_html.replace("<!-- TT SECTION TEXT TT -->", section.split(' ', 1)[1])
        section_html = section_html.replace("TT SECTION ID TT", f"section{section[0]}")

        for i, question in enumerate(questions):
            questions_html = questions_template
            questions_html = questions_html.replace("<!-- TT QUESTION TEXT TT -->", question)
            question_id = f"section{section[0]}_question{i}"
            questions_html = questions_html.replace("TT SECTION QUESTION ID TT", question_id)

            for score in range(7):
                explanation = options_explanation[score] if score < len(options_explanation) else ""
                replace_str = f"<!-- TT OPTION LABEL TT -->"
                with_explanation = f"<label class=\"question__label\" for=\"{question_id}_value{score}\">{explanation}</label>"
                questions_html = questions_html.replace(replace_str, with_explanation, 1)

            section_html = section_html.replace("<!-- TT QUESTIONS TT -->", questions_html, 1)
        funcap_html = funcap_html.replace("<!-- TT SECTIONS TT -->", section_html, 1)

    funcap_html = funcap_html.replace("<!-- TT RESULT TT -->", section_header_html)
    open(f"{output_folder}/funcap.{lang}.{variant}.html", 'w', encoding='utf-8').write(funcap_html)
    
def generate_index(variants: list[tuple[str, str]]):
    with open("templates/index.template.html", 'r', encoding='utf-8') as f:
        index_template = f.read()

    lang_options = {lang for lang, _ in variants}
    variant_options = {variant for _, variant in variants}

    lang_options_html = "\n".join([f"<span class='custom-option{' selected' if i == 0 else ''}' data-value='{lang}'>{lang}</span>" for i, lang in enumerate(lang_options)])
    variant_options_html = "\n".join([f"<span class='custom-option{' selected' if i == 0 else ''}' data-value='{variant}'>{variant} questions</span>" for i, variant in enumerate(variant_options)])

    index_html = index_template.replace("<!-- TT LANG OPTIONS TT -->", lang_options_html)
    index_html = index_html.replace("<!-- TT VARIANT OPTIONS TT -->", variant_options_html)

    open(f"{output_folder}/index.html", 'w', encoding='utf-8').write(index_html)

generated_variants: list[tuple[str, str]] = []
for file in os.listdir(langs_folder):
    lang = file.split('_')[1] # questions_en_55.txt -> en
    variant = file.split('_')[2].split('.')[0] # questions_en_55.txt -> en

    parsed_data = parse_language(file)
    generate_language(parsed_data, lang, variant)
    generated_variants.append((lang, variant))

generate_index(generated_variants)
copy_static_folder(f'{static_folder}', f'{output_folder}/{static_folder}')
