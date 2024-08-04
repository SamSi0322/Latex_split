import re
import os

def parse_latex_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    section_pattern = r'(\\section\{.*?\})(.*?)(?=(\\section\{)|\Z)'
    sections = re.findall(section_pattern, content, re.DOTALL)

    if not os.path.exists('sections'):
        os.makedirs('sections')

    main_content = ''
    for i, (section_header, section_content, _) in enumerate(sections):
        section_filename = f'section_{i+1}.tex'
        section_path = os.path.join('sections', section_filename)
        with open(section_path, 'w', encoding='utf-8') as section_file:
            section_file.write(section_header + section_content)
        main_content += f'\\include{{sections/{section_filename.replace(".tex", "")}}}\n'

    return main_content

def update_main_latex_file(input_file, main_content):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    updated_content = re.sub(r'\\section\{.*?\}.*?(?=(\\section\{)|\Z)', '', content, flags=re.DOTALL)
    updated_content = updated_content.strip() + '\n' + main_content

    with open(input_file, 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == '__main__':
    input_file = 'main.tex'
    main_content = parse_latex_file(input_file)
    update_main_latex_file(input_file, main_content)
