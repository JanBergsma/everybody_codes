import xml.etree.ElementTree as ET

svg_path = r'Echoes of Enigmatus [ No. 1 ]\src\imgs\quest2_part1_tree_actions_line-1.svg'
tree = ET.parse(svg_path)
root = tree.getroot()

# Get all element types
elem_types = {}
for elem in root.iter():
    tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
    if tag not in elem_types:
        elem_types[tag] = 0
    elem_types[tag] += 1

print('All element types:')
for tag in sorted(elem_types.keys()):
    print(f'  {tag}: {elem_types[tag]}')

# Look for line elements
lines = list(root.iter())
line_count = sum(
    1 for e in root.iter() if (e.tag.split('}')[-1] if '}' in e.tag else e.tag) == 'line'
)
print(f'\nLine elements: {line_count}')

# Check if any elements have data attributes
print('\nChecking for data attributes on first few elements:')
for i, elem in enumerate(root.iter()):
    if i > 50:
        break
    tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
    attrs = elem.attrib
    # Look for attributes with data or link
    for k, v in attrs.items():
        if 'data' in k.lower() or 'link' in k.lower() or 'ref' in k.lower():
            print(f'  {tag}[{k}]={v}')
