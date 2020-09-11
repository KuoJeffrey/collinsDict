import decorator as dc


class div:
    def __init__(self, in_str, level):
        self.parent = None
        self.child = None
        self.rsibling = None
        self.content = in_str
        self.level = level
    
    def __eq__(self, other):
        if isinstance(other, div):
            return self.level == other.level

        return False

    def __str__(self):
        return self.content

    def __copy__(self):
        return div(self.content, self.level)
    

class Vocab:
    def __init__(self, in_word):
        self.size = 0
        self.depth = 0
        self.root = div(in_word, 0)
        self.dict_ = None
        self.cpRght = None

    def insert(self, prev, node):
        node.parent = prev
        if prev.level==node.level:
            if prev.rsibling is None: prev.rsibling = node
            else:
                node.rsibling = prev.rsibling
                prev.rsibling.parent = node
                prev.rsibling = node

        else:
            if prev.child is None: prev.child = node
            else:
                node.rsibling = prev.child
                prev.child.parent = node
                prev.child = node
    
    def delete(self, node=None):
        # delete whole subtree
        if node is None: node = self.root
        if node.parent is None: pass

        elif node.parent.child==node:
            if node.rsibling is not None:
                node.parent.child = node.rsibling
                node.rsibling.parent = node.parent
                node.rsibling = None
            else: node.parent.child = None
            node.parent = None

        elif node.parent.rsibling==node:
            if node.rsibling is not None:
                node.parent.rsibling = node.rsibling
                node.rsibling.parent = node.parent
                node.rsibling = None
            else: node.parent.rsibling = None
            node.parent = None
        # self.deleteTree(node)

    # def deleteTree(self, cur):
    #     if cur.child is not None: self.deleteTree(cur.child)
    #     if cur.rsibling is not None: self.deleteTree(cur.rsibling)
    #     print("Delete", cur.content)

    def find(self, node):
        pass

    def __str__(self):
        return self.root.content

    def printTree(self, order=None, cur=None):
        if order is None:
            order = "preorder" # default: preorder
        if cur is None: cur = self.root

        if order=="preorder":
            # Pre-order traversal
            print(cur.content)
            if cur.child is not None: self.printTree(order, cur.child)
            if cur.rsibling is not None: self.printTree(order, cur.rsibling)
        elif order=="inorder":
            # In-order traversal
            if cur.child is not None: self.printTree(order, cur.child)
            print(cur.content)
            if cur.rsibling is not None: self.printTree(order, cur.rsibling)
        elif order=="postorder":
            # Post-order traversal
            if cur.child is not None: self.printTree(order, cur.child)
            if cur.rsibling is not None: self.printTree(order, cur.rsibling)
            print(cur.content)
    
    def printDict(self, cur=None):
        if cur is None: cur = self.root.child

        # Pre-order traversal
        if cur.content=="None": pass
        elif cur.content=="cbr" or cur.content=="ced" or cur.content=="amr" or cur.content=="amp" or cur.content=="esp": pass
        elif cur.content=="sense" or cur.content=="resense": print()
        else: print(cur.content)
        if cur.child is not None: self.printDict(cur.child)
        if cur.rsibling is not None: self.printDict(cur.rsibling)

    def __copy__(self):
        return Vocab(self.root)