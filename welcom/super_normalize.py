import re

def super_normalize_mdx(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean up messed up backticks first
    # e.g. `{`{host}`}` -> `{{host}}`
    content = content.replace('`{`', '`').replace('`}`', '`')
    content = content.replace('``', '`')
    
    lines = content.split('\n')
    new_lines = []
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue
            
        if in_code_block:
            new_lines.append(line)
            continue

        # 1. Wrap URL-like lines starting with {{host}} or containing it
        # If it's a list item starting with - 
        if line.strip().startswith('-') and '{{host}}' in line:
            # - `{{host}}/path`
            line = re.sub(r'(- )([^`\n]+)', r'\1` \2 `', line)
            line = line.replace('` `', '`').replace('  ', ' ')
            # Clean up double backticks
            line = line.replace('``', '`')

        # 2. Ensure all {{...}} are backticked
        line = re.sub(r'(?<!`)\{\{([^}]+)\}\}(?!`)', r'`{{\1}}`', line)
        
        # 3. Ensure {UUID} etc are backticked
        line = re.sub(r'(?<![<`/])\{([a-zA-Z0-9 _]+)\}(?!`)', r'`{\1}`', line)

        # 4. Final safety cleanup
        line = line.replace('`MD5(`{', '`MD5({')
        line = line.replace('}`)`', '})`')
        line = line.replace('``', '`')

        new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

if __name__ == "__main__":
    super_normalize_mdx('/Users/a1234/Desktop/docs/welcom/agent_v2.1.mdx')
