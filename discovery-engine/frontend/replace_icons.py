import os
import re

d = r'C:\Users\smrut\OneDrive\Desktop\Product Management NextLeap\Myntra Wishlist Discovery Engine\frontend\src\pages'

icon_map = {
    'person': 'User',
    'smart_toy': 'Bot',
    'radar': 'Radar',
    'database': 'Database',
    'science': 'FlaskConical',
    'forum': 'MessageSquare',
    'psychology': 'Brain',
    'favorite': 'Heart',
    'verified': 'CheckCircle',
    'sell': 'Tag',
    'inventory_2': 'Archive',
    'warning': 'AlertTriangle',
    'chevron_right': 'ChevronRight',
    'account_tree': 'Network',
    'dashboard': 'LayoutDashboard',
    'folder_data': 'FolderOpen',
    'settings': 'Settings',
    'info': 'Info',
    'query_stats': 'LineChart',
    'arrow_forward': 'ArrowRight',
    'lightbulb': 'Lightbulb',
    'visibility': 'Eye',
    'arrow_back': 'ArrowLeft',
    'play_arrow': 'Play',
    'phone_iphone': 'Smartphone',
    'smart_display': 'MonitorPlay',
    'insights': 'TrendingUp',
    'price_change': 'BadgeDollarSign',
    'confirmation_number': 'Ticket',
    'hourglass_empty': 'Hourglass',
    'fact_check': 'ClipboardCheck',
    'auto_awesome': 'Sparkles',
    'search': 'Search',
    'verified_user': 'ShieldCheck',
    'help_outline': 'HelpCircle',
    'apparel': 'Shirt',
    'compare': 'GitCompare',
    'play_circle': 'PlayCircle',
    'policy': 'FileCheck',
    'refresh': 'RefreshCw',
    'open_in_new': 'ExternalLink',
    'article': 'FileText',
    'add': 'Plus',
    'close': 'X',
    'menu': 'Menu'
}

def to_lucide(match):
    full_str = match.group(0)
    class_name = match.group(1)
    icon_text = match.group(2).strip()
    
    # Extract extra styles if they exist
    style_match = re.search(r'style={{[^}]*}}', full_str)
    style_str = f" {style_match.group(0)}" if style_match else ""
    
    # Remove 'material-symbols-outlined' from className
    new_class = class_name.replace('material-symbols-outlined', '').strip()
    class_prop = f'className="{new_class}"' if new_class else ''
    
    comp_name = icon_map.get(icon_text, 'Box')
    
    return f'<{comp_name} {class_prop}{style_str} />'

for f in os.listdir(d):
    if not f.endswith('.jsx'): continue
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Collect used icons for import
    used_icons = set()
    for m in re.finditer(r'<span className="(.*?)">([^<]+)</span>', content):
        if 'material-symbols-outlined' in m.group(1):
            icon_text = m.group(2).strip()
            used_icons.add(icon_map.get(icon_text, 'Box'))
            
    if used_icons:
        imports = f"import {{ {', '.join(sorted(list(used_icons)))} }} from 'lucide-react';\n"
        if 'import React' in content:
            content = re.sub(r'(import React.*?;)', r'\1\n' + imports, content, count=1)
        else:
            content = imports + content
            
    # Replace icons
    content = re.sub(r'<span className="([^"]*material-symbols-outlined[^"]*)"[^>]*>([^<]+)</span>', to_lucide, content)
    
    # Fix bottom nav Links
    nav_repl = {
        'overview': '/',
        'discovery-copilot': '/copilot',
        'opportunity-radar': '/radar',
        'evidence-explorer': '/evidence',
        'settings': '/settings'
    }
    
    def nav_link_repl(m):
        attrs = m.group(1)
        inner = m.group(2)
        
        # find data-path
        dp_match = re.search(r'data-path="([^"]+)"', attrs)
        if dp_match:
            path_id = dp_match.group(1)
            to_val = nav_repl.get(path_id, '#')
            # remove href="#" and data-path
            attrs = re.sub(r'href="[^"]*"', '', attrs)
            attrs = re.sub(r'data-path="[^"]*"', '', attrs)
            return f'<Link to="{to_val}" {attrs}>{inner}</Link>'
        return m.group(0)
        
    if '<nav' in content:
        # Add Link import if not present
        if 'react-router-dom' not in content:
            content = re.sub(r'(import React.*?;)', r"\1\nimport { Link } from 'react-router-dom';", content, count=1)
        content = re.sub(r'<a([^>]+)>(.*?)</a>', nav_link_repl, content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
