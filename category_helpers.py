from category import build_category_tree

category_tree = build_category_tree()


def get_subcategories(category_name):
    for node in category_tree.children:
        if node.name == category_name:
            return [child.name for child in node.children]
    return []