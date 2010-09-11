from DataFactory import dbPages
import logging

def build_tree(nodes):
    # create empty tree to fill
    tree = {}
    # fill in tree starting with roots (those with no parent)
    build_tree_recursive(tree, None, nodes)
    
    return tree

def build_tree_recursive(tree, parent, nodes):
    # find root children
    if parent is None:
        children  = [n for n in nodes if n.parentKey == None]
    # find children
    else:
        children  = [n for n in nodes if n.parentKey is not None and n.parentKey.key() == parent]
        
    # build a subtree for each child
    for child in children:
        # start new subtree
        key = child.key()
        tree[key] = { 'page' : child, 'children' : {}}
        # call recursively to build a subtree for current node
        build_tree_recursive(tree[key]['children'], key, nodes)