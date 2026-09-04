import os
import re

base_path = r"C:\Users\smrut\Downloads\stitch_wishlist_intelligence_discovery_engine\stitch_wishlist_intelligence_discovery_engine"
pages_dir = r"C:\Users\smrut\OneDrive\Desktop\Product Management NextLeap\Myntra Wishlist Discovery Engine\frontend\src\pages"
os.makedirs(pages_dir, exist_ok=True)

dirs = [
    ("Overview", "overview_wishlist_intelligence"),
    ("OpportunityRadar", "opportunity_radar_wishlist_intelligence"),
    ("OpportunityDetail", "opportunity_detail_price_value_wishlist_intelligence"),
    ("EvidenceExplorer", "evidence_explorer_wishlist_intelligence"),
    ("DiscoveryCopilot", "discovery_copilot_wishlist_intelligence")
]

def to_jsx(html):
    # Extract body content
    body_match = re.search(r'<body[^>]*>(.*)</body>', html, re.IGNORECASE | re.DOTALL)
    if not body_match:
        return ""
    content = body_match.group(1)
    
    # Replace class with className
    content = content.replace('class=', 'className=')
    content = content.replace('for=', 'htmlFor=')
    
    # SVG attributes to camelCase
    attrs = ['stroke-width', 'stroke-linecap', 'stroke-linejoin', 'fill-rule', 'clip-rule', 'stroke-miterlimit', 'xmlns:xlink', 'xml:space']
    for attr in attrs:
        parts = attr.split('-')
        if len(parts) > 1:
            camel = parts[0] + ''.join(p.capitalize() for p in parts[1:])
        else:
            parts = attr.split(':')
            camel = parts[0] + ''.join(p.capitalize() for p in parts[1:])
        content = content.replace(attr, camel)
        
    # Close self-closing tags
    tags = ['img', 'input', 'path', 'line', 'polyline', 'circle', 'rect', 'br', 'hr']
    for tag in tags:
        content = re.sub(r'(<'+tag+r'\b[^>]*?)(?<!/)>', r'\1 />', content, flags=re.IGNORECASE)
        
    # style="" to style={{}}
    def style_repl(m):
        style_str = m.group(1)
        rules = style_str.split(';')
        style_obj = []
        for r in rules:
            if ':' not in r: continue
            k, v = r.split(':', 1)
            k = k.strip()
            v = v.strip()
            # kebab to camel
            k = re.sub(r'-([a-z])', lambda m2: m2.group(1).upper(), k)
            style_obj.append(f'{k}: "{v}"')
        return 'style={{' + ', '.join(style_obj) + '}}'
        
    content = re.sub(r'style="([^"]*)"', style_repl, content)
    
    # Remove HTML comments
    content = re.sub(r'<!--(.*?)-->', '', content, flags=re.DOTALL)
    
    return content.strip()

for comp_name, d in dirs:
    path = os.path.join(base_path, d, "code.html")
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    jsx = to_jsx(html)
    
    comp_code = f"""import React from 'react';

export default function {comp_name}() {{
  return (
    <>
{jsx}
    </>
  );
}}
"""
    with open(os.path.join(pages_dir, f"{comp_name}.jsx"), "w", encoding="utf-8") as f:
        f.write(comp_code)
    print(f"Generated {comp_name}.jsx")
