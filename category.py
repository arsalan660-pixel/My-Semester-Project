class CategoryNode:
    def __init__(self, name):
        self.name = name          # the category or sub-category's name, e.g. "Electronics"
        self.children = []        # list of CategoryNode objects — this node's sub-categories

    def add_child(self, child_name):
        child = CategoryNode(child_name)   # create a new node for the sub-category
        self.children.append(child)         # attach it as a child of this node
        return child                        # return it, in case the caller wants to add grandchildren to it


def build_category_tree():
    root = CategoryNode("ALL")   # a root node representing "no filter" — the top of the whole tree

    electronics = root.add_child("Electronics")
    electronics.add_child("Mobiles")
    electronics.add_child("Laptops")
    electronics.add_child("TVs")
    electronics.add_child("Accessories")

    fashion = root.add_child("Fashion")
    fashion.add_child("Men")
    fashion.add_child("Women")
    fashion.add_child("Kids")

    furniture = root.add_child("Furniture")
    furniture.add_child("Sofas")
    furniture.add_child("Beds")
    furniture.add_child("Tables")
    furniture.add_child("Chairs")

    automobiles = root.add_child("Automobiles")
    automobiles.add_child("Cars")
    automobiles.add_child("Bikes")
    automobiles.add_child("Parts")

    books = root.add_child("Books")
    books.add_child("Academic")
    books.add_child("Fiction")
    books.add_child("Kids Books")

    other = root.add_child("Other")
    other.add_child("Miscellaneous")

    return root