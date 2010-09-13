from DataFactory import dbPages
from DataFactory import dbPageModules
import logging

def build_tree(nodes, *args):
    # create empty tree to fill
    tree = {}
    # fill in tree starting with roots (those with no parent)
    build_tree_recursive(tree, None, nodes, *args)
    
    return tree

def build_tree_recursive(tree, parent, nodes, *args):
    # find root children
    if parent is None:
        children  = [n for n in nodes if n.parentKey == None]
    # find children
    else:
        children  = [n for n in nodes if n.parentKey is not None and n.parentKey.key() == parent]
        
    # build a subtree for each child
    for child in children:
        # start new subtree
        if not args:
            key = child.key()
            tree[key] = { 'page' : child, 'children' : {}}
            # call recursively to build a subtree for current node
            build_tree_recursive(tree[key]['children'], key, nodes)
        else:
            lang = args[0]
            published = args[1]
            key = child.key()
            
            pageModule = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey AND lang = :lang AND published = :published', pageKey = key, lang = lang, published = published).get()
            
            if pageModule:
                tree[key] = { 'name' : pageModule.name, 'path': pageModule.path, 'children' : {}}
                # call recursively to build a subtree for current node
                build_tree_recursive(tree[key]['children'], key, nodes, *args)
            