import os
import re

d = r'C:\Users\smrut\OneDrive\Desktop\Product Management NextLeap\Myntra Wishlist Discovery Engine\frontend\src\pages'
for f in os.listdir(d):
    if not f.endswith('.jsx'): continue
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    content = re.sub(r'</(rect|line|circle|path|polyline|img|input|br|hr)>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<script.*?</script>', '', content, flags=re.IGNORECASE|re.DOTALL)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
