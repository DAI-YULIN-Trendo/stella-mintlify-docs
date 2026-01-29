
import re

path = '/Users/a1234/Desktop/docs/welcom/agent_v2.1.mdx'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_frontmatter = False
for i, line in enumerate(lines):
    # Handle frontmatter
    if line.strip() == '---':
        if i == 0 or in_frontmatter:
            in_frontmatter = not in_frontmatter
            continue
    
    if in_frontmatter:
        continue

    # Diagnostic 1: Check for unescaped { or }
    unescaped_bracket = re.findall(r'(?<!\\)[{}]', line)
    if unescaped_bracket:
        print(f"Line {i+1}: Unescaped bracket: {line.strip()}")

    # Diagnostic 2: Check for unescaped < (unless it's a valid HTML/MDX tag start)
    # MDX is picky about <
    # Looking for < that is not followed by a tag name or /
    unescaped_less_than = re.findall(r'(?<!\\)<(?![a-zA-Z/])', line)
    if unescaped_less_than:
        print(f"Line {i+1}: Unescaped <: {line.strip()}")
        
    # Diagnostic 3: Check for > that might be misinterpreted
    # Usually > is fine unless it's part of a broken tag
    
    # Diagnostic 4: Check for backticks
    if '`' in line:
        # Check if they are escaped if we don't want them as code
        pass

print("Diagnostic complete.")
