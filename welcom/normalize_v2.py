import re

def normalize_mdx(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue
            
        if in_code_block:
            # Remove \ escaping inside triple backticks
            line = line.replace('\\{', '{').replace('\\}', '}')
            new_lines.append(line)
            continue

        # Outside triple backticks:
        
        # 1. Remove \ escaping from already backticked snippets
        # `\{var\}` -> `{var}`
        line = re.sub(r'`([^`]*)\\{([^`]*)\\\\}([^`]*)`', r'`\1{\2}\3`', line)
        # Handle cases where multiple \ exist
        while '\\{' in line and '`' in line:
            # This is complex to do with regex perfectly, let's do a smarter replace
            parts = line.split('`')
            for j in range(1, len(parts), 2):
                parts[j] = parts[j].replace('\\{', '{').replace('\\}', '}')
            line = '`'.join(parts)
            break

        # 2. Find {{host}} or {var} that are NOT in backticks and NOT components
        # And escape them or wrap in backticks.
        # Let's try wrapping them in backticks if they aren't already.
        
        # Avoid matching <Component ...>
        # Match {{...}}
        line = re.sub(r'(?<!`)\{\{([^}]+)\}\}(?!`)', r'`{{\1}}`', line)
        # Match {var} if not part of a component or already backticked
        # This is tricky because of components. 
        # For now, let's just fix the known host and UUID ones.
        line = line.replace('\{\{host\}\}', '`{{host}}`')
        line = line.replace('\{authKey\}', '`{authKey}`')
        line = line.replace('\{authSecret\}', '`{authSecret}`')
        line = line.replace('\{timestamp\}', '`{timestamp}`')
        line = line.replace('\{agentUUID\}', '`{agentUUID}`')
        line = line.replace('\{Your Base Url\}', '`{Your Base Url}`')
        
        # Final cleanup for any remaining \{ \} that should be backticked or raw
        # If it's already in backticks, remove \
        parts = line.split('`')
        for j in range(1, len(parts), 2):
            parts[j] = parts[j].replace('\\{', '{').replace('\\}', '}')
        line = '`'.join(parts)

        new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    normalize_mdx('/Users/a1234/Desktop/docs/welcom/agent_v2.1.mdx')
