
import re

path = '/Users/a1234/Desktop/docs/welcom/agent_v2.1.mdx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Strip all code fences just to be safe (client wants clean text for now)
content = content.replace('```', '')

# 2. Normalize: Remove all backslashes before { } < >
content = re.sub(r'\\([{}<>])', r'\1', content)
# And handle double-escaped ones too
content = re.sub(r'\\([{}<>])', r'\1', content) 

# 3. Preserve Frontmatter
fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
if fm_match:
    fm = fm_match.group(0)
    body = content[len(fm):]
else:
    fm = ""
    body = content

# 4. Escape exactly once
# We escape {, }, <
# We don't necessarily need to escape > but let's be safe.
body = body.replace('{', '\\{').replace('}', '\\}').replace('<', '\\<')

# 5. Check for @ and $ just in case
# body = body.replace('@', '\\@').replace('$', '\\$')
# Actually MDX doesn't usually mind @ or $ in text, but let's see.

final_content = fm + body

with open(path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Normalization and single-escape applied.")
