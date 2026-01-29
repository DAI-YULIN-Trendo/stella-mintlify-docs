import re
import sys

def check_mdx(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Check for unclosed code blocks
    code_blocks = re.findall(r'```', content)
    if len(code_blocks) % 2 != 0:
        print(f"ERROR: Unclosed code block in {file_path}")
    else:
        print(f"Code blocks: Balanced ({len(code_blocks)} fences)")

    # 2. Check for unclosed Mintlify components
    components = ['Accordion', 'AccordionGroup', 'Info', 'Note', 'CodeGroup', 'Table', 'Step', 'Steps', 'Card', 'CardGroup']
    for comp in components:
        open_tags = len(re.findall(rf'<{comp}', content))
        close_tags = len(re.findall(rf'</{comp}>', content))
        if open_tags != close_tags:
            print(f"ERROR: Unbalanced {comp} tags: Open={open_tags}, Close={close_tags}")
        elif open_tags > 0:
            print(f"Component <{comp}>: Balanced ({open_tags})")

    # 3. Check for unescaped braces outside code blocks
    # Remove code blocks first for checking
    sanitized = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    unescaped_braces = re.findall(r'(?<!\\)\{', sanitized)
    if unescaped_braces:
        print(f"WARNING: Found {len(unescaped_braces)} potentially unescaped curly braces outside code blocks.")
        # Print lines with unescaped braces
        for i, line in enumerate(sanitized.split('\n')):
            if '{' in line and '\\{' not in line:
                 print(f"  Line {i+1}: {line.strip()}")
    else:
        print("Curly braces: Safe (All escaped outside code blocks)")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_mdx(sys.argv[1])
    else:
        check_mdx('/Users/a1234/Desktop/docs/welcom/agent_v2.1.mdx')
