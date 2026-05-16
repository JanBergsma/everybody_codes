import re
import xml.etree.ElementTree as ET

svg_path = r'Echoes of Enigmatus [ No. 1 ]\src\imgs\quest2_part1_tree_actions_line-1.svg'
tree = ET.parse(svg_path)
root = tree.getroot()

# Get namespace
ns_match = root.tag
if '}' in ns_match:
    ns = ns_match.split('}')[0][1:]
    print(f'Namespace: {ns}')
else:
    ns = None
    print('No namespace found')

# Find circles and paths with namespace-aware iteration
circles = []
paths = []

for elem in root.iter():
    tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
    if tag == 'circle':
        circles.append(elem)
    elif tag == 'path':
        paths.append(elem)

print(f'\nFound {len(circles)} circles')
for c in circles[:5]:
    print(f'  {c.get("id")}: cx={c.get("cx")}, cy={c.get("cy")}')

print(f'\nFound {len(paths)} paths')

# Filter paths that are not in defs
layer = None
for elem in root.iter():
    tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
    if tag == 'g' and elem.get('id') == 'layer1':
        layer = elem
        break

if layer:
    print('Found layer1')
    layer_paths = []
    for p in layer.iter():
        tag = p.tag.split('}')[-1] if '}' in p.tag else p.tag
        if tag == 'path':
            layer_paths.append(p)

    print(f'Found {len(layer_paths)} paths in layer1')
    for p in layer_paths[:5]:
        d = p.get('d', '')
        coords = re.findall(r'[-+]?\d*\.?\d+', d)
        print(f'  d={d}')
        print(f'    coords={coords}')

    # Check layer transform
    transform = layer.get('transform')
    print(f'\nLayer transform: {transform}')
