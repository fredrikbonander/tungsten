from DataFactory import dbPages
from DataFactory import dbPageModules
import logging

def build_tree(nodes, *args):
    # create empty tree to fill
    t = {}
    # First group all pages w/ same parent
    for node in nodes:
        if node.parentKey is None:
            key = 'root'
        else:
            key = node.parentKey.key()
            
        if not t.has_key(key):
            t[key] = []
        
        t[key].append({ 'page' : node, 'children' : []})
    
    logging.info(t)
    pageTree = t['root']
    # Iterate over there
    build_page_tree(pageTree, t)
    
    #build_tree_recursive(tree, None, nodes, *args)
    
    return pageTree

def build_page_tree(pageTree, nodes):
    #Loop over selected list
    for parent, node in nodes.iteritems():
        # We don't need to loop over first level node
        if parent is not 'root':
            logging.info(node)
            # Loop over current level in page tree
            for item in pageTree:
                # Match keys
                if item['page'].key() == parent:
                    # Save node as child
                    item['children'] = node
                    # Only need to loop over childs if they are present
                    build_page_tree(item['children'], nodes)
                
                
#def build_page_container_tree(nodes, pageConatiner, *args):
#    # create empty tree to fill
#    tree = {}
#    # fill in tree starting with roots (those with no parent)
#    build_tree_recursive(tree, pageConatiner.key(), nodes, *args)
#    
#    return tree
#
#def build_tree_recursive(tree, parent, nodes, *args):
#    # find root children, first level nodes have no parentKey
#    if parent is None:
#        children  = [n for n in nodes if n.parentKey == None]
#    # find children
#    else:
#        children  = [n for n in nodes if n.parentKey is not None and n.parentKey.key() == parent]
#    
#    # build a subtree for each child
#    for child in children:
#        # start new subtree
#        if not args:
#            key = child.key()
#            # Use page entry key as unique dict key
#            tree[key] = { 'page' : child, 'children' : {}}
#            # call recursively to build a subtree for current node
#            build_tree_recursive(tree[key]['children'], key, nodes)
#        else:
#            lang = args[0]
#            published = args[1]
#            key = child.key()
#            
#            pageModule = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey AND lang = :lang AND published = :published', pageKey = key, lang = lang, published = published).get()
#            
#            if pageModule:
#                tree[key] = { 'name' : pageModule.name, 'path': pageModule.path, 'children' : {}}
#                # call recursively to build a subtree for current node
#                build_tree_recursive(tree[key]['children'], key, nodes, *args)
            