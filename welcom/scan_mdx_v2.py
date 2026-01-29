import re

def find_mdx_issues(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    
    # 1. Look for unescaped < outside code blocks and known tags
    known_components = ['Accordion', 'AccordionGroup', 'Info', 'Note', 'CodeGroup', 'Table', 'Step', 'Steps', 'Card', 'CardGroup']
    
    # Remove code blocks for scanning
    temp_content = re.sub(r'```.*?```', 'CODE_BLOCK', content, flags=re.DOTALL)
    temp_content = re.sub(r'`.*?`', 'INLINE_CODE', temp_content)
    
    print("--- Searching for stray angle brackets ---")
    for i, line in enumerate(temp_content.split('\n')):
        # Find < that is not part of a known tag or self-closing/closing tag of known components
        # Also ignore HTML comments <!-- -->
        tag_matches = re.finditer(r'<([^/! >]+)', line)
        for m in tag_matches:
            tag_name = m.group(1)
            if tag_name not in known_components:
                # Check if it's line number in original
                print(f"Potential invalid tag <{tag_name}> at line {i+1} (sanitized): {line.strip()}")

    # 2. Look for single { or } that are not escaped
    print("\n--- Searching for unescaped braces ---")
    unescaped_braces = re.finditer(r'(?<!\\)[{}]', temp_content)
    for m in unescaped_braces:
        # Find line number
        pos = m.start()
        line_no = temp_content[:pos].count('\n') + 1
        print(f"Unescaped brace '{m.group(0)}' at line {line_no} (sanitized)")

    # 3. Look for pipes in tables that might break them
    print("\n--- Searching for suspicious pipes ---")
    for i, line in enumerate(lines):
        if line.strip().startswith('|') and line.strip().endswith('|'):
            # Count columns
            pipes = line.count('|')
            # Check for | that are not escaped \|
            raw_pipes = len(re.findall(r'(?<!\\)\|', line))
            if raw_pipes > 5: # More than expected for a 4-column table
                 print(f"Suspicious pipe count ({raw_pipes}) at line {i+1}: {line.strip()}")

if __name__ == "__main__":
    find_mdx_issues('/Users/a1234/Desktop/docs/welcom/agent_v2.1.mdx')
