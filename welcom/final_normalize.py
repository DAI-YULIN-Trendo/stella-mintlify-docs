import re

def final_normalize_mdx(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. First, remove all existing \ escapes for { }
    content = content.replace('\\{', '{').replace('\\}', '}')
    
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
            
        # Outside triple backticks:
        
        # A. Cleanup existing backticks to avoid double-nesting
        # Step: Convert `...{var}...` to placeholder
        # We'll do a simple replace for now: remove all backticks and then re-add them to variables.
        # But some are already in tables.
        
        # Better approach: Match any {{...}} or {...} that isn't a component tag
        # Component tags look like <Component ...> or </Component>
        
        # First, wrap {{...}} in backticks if not already
        line = re.sub(r'(?<!`)\{\{([^}]+)\}\}(?!`)', r'`{{\1}}`', line)
        
        # Next, wrap {VarName} if it's alphanumeric and not a component
        # {agentUUID}, {authKey}, etc.
        line = re.sub(r'(?<![<`/])\{([a-zA-Z0-9 _]+)\}(?!`)', r'`{\1}`', line)

        # Fix specific cases found:
        # MD5(`{authKey}``{authSecret}``{timestamp}`) -> `MD5({authKey}{authSecret}{timestamp})`
        line = line.replace('MD5(`{authKey}``{authSecret}``{timestamp}`)', '`MD5({authKey}{authSecret}{timestamp})`')
        line = line.replace('`http://`{Your Base Url}`/`', '`http://{Your Base Url}/` ')
        
        # Fix URL lines to be fully backticked if they contain variables
        if '{{host}}' in line or '{agentUUID}' in line:
            # If it's a list item like - {{host}}...
            line = re.sub(r'(- )([^`\n]+host[^`\n]+)', r'\1` \2 `', line)
            # Remove any double backticks created
            line = line.replace('``', '`')
            
        # Standardize table pipes
        if line.strip().startswith('|'):
             line = line.replace('|', ' | ')
             line = re.sub(r' +', ' ', line)
             line = line.strip()
             if not line.startswith('|'): line = '| ' + line
             if not line.endswith('|'): line = line + ' |'

        new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

if __name__ == "__main__":
    final_normalize_mdx('agent_v2.1.mdx')
