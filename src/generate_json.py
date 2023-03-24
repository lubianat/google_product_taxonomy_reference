import pandas as pd
import json

"""
Create hierarchical json object in the style of https://github.com/d3/d3-hierarchy/blob/main/README.md#hierarchy

"""

df = pd.read_excel('../data/taxonomy-with-ids.en-US.xls', header=None)

taxonomy = [
    {
        "name": "Root",
        "google_id": 0,
        "children": []
    }
]


def add_child(taxonomy, tree_path, child):
    current_level = taxonomy[0]
    if len(current_level['children']) > 0:
        for path_item in tree_path[:-1]:
            for next_level in current_level['children']:
                if next_level['name'] == path_item:
                    current_level = next_level
    current_level['children'].append(child)
    return taxonomy


for index, row in df.iterrows():
    google_product_id = row[0]
    tree_path = ["Root"]
    for i in range(1, 7):
        if not pd.isna(row[i]):
            tree_path.append(row[i])

    new_product_category = tree_path[-1:][0]
    product_entry = {
        "name": new_product_category,
        "google_id": google_product_id,
        "children": []
    }
    add_child(taxonomy, tree_path, product_entry)

with open('taxonomy.json', 'w') as f:
    json.dump(taxonomy, f)
