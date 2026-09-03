import os
import re

d = 'frontend/src/pages'
for f in os.listdir(d):
    if not f.endswith('.jsx'): continue
    if f == 'DiscoveryCopilot.jsx': continue
    
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Strip invalid closing tags
    content = re.sub(r'</(rect|line|circle|path|polyline|img|input|br|hr)>', '', content, flags=re.IGNORECASE)
    
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
