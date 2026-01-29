import re

def trace_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all <Accordion and </Accordion>
    # We use regex to find start and end positions
    tags = []
    for m in re.finditer(r'<(Accordion\b|/Accordion>)', content):
        tags.append((m.group(0), m.start()))

    stack = []
    lines = content.split('\n')
    
    def get_line_no(pos):
        current_pos = 0
        for i, line in enumerate(lines):
            if current_pos + len(line) >= pos:
                return i + 1
            current_pos += len(line) + 1 # +1 for newline
        return len(lines)

    for tag_str, pos in tags:
        line_no = get_line_no(pos)
        if tag_str.startswith('<Accordion'):
            stack.append((tag_str, line_no))
            print(f"OPEN:  {tag_str} at line {line_no}")
        else:
            if stack:
                stack.pop()
                print(f"CLOSE: {tag_str} at line {line_no}")
            else:
                print(f"ORPHAN CLOSE: {tag_str} at line {line_no}")

    while stack:
        tag_str, line_no = stack.pop()
        print(f"UNCLOSED OPEN: {tag_str} at line {line_no}")

if __name__ == "__main__":
    trace_tags('/Users/a1234/Desktop/docs/welcom/agent_v2.1.mdx')
