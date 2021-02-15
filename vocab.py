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
    

class Vocab2(object):
    def __init__(self, word):
        self.word = word
    
    def __str__(self):
        return self.word

# Collins Cobuild Advanced Dictionary
class CBR(Vocab2):
    num = 1
    def __init__(self, word):
        Vocab2.__init__(self, word)
        self.cbrNum = CBR.num
        CBR.num += 1
        self.dict = "CBR"
    
    def get_dictNum(self):
        return str(self.cbrNum).zfill(2)
    
    def __str__(self):
        return "Collins Cobuild Advanced Dictionary"
    
    def reset(self):
        CBR.num, self.cbrNum = 1, 1

class MeaningsCBR(CBR):
    def __init__(self, word):
        CBR.__init__(self, word)
        CBR.num -= 1
        self.cbrNum -= 1
        self.sense = ""
        self.sensePunct = ""
        self.definition = ""
        self.punctuation = ""
        self.examples = []
        self.exPuncts = []
        self.synonyms = ""
    
    def set_sense(self, sense):
        pass

    def set_sensePunct(self, sensePunct):
        pass

    def set_definition(self, definition):
        pass

    def set_punctuation(self, punctuation):
        pass

    def set_examples(self, examples):
        pass

    def set_exPuncts(self, exPuncts):
        pass

    def set_synonyms(self, synonyms):
        pass

    def get_sense(self, sense):
        return self.sense

    def get_sensePunct(self, sensePunct):
        return self.sensePunct

    def get_definition(self, definition):
        return self.definition

    def get_punctuation(self, punctuation):
        return self.punctuation

    def get_examples(self, examples):
        return self.examples

    def get_exPuncts(self, exPuncts):
        return self.exPuncts

    def get_synonyms(self, synonyms):
        return self.synonyms

# Collins English Dictionary
class CED(Vocab2):
    num = 1
    def __init__(self, word):
        Vocab2.__init__(self, word)
        self.cedNum = CED.num
        CED.num += 1
        self.dict = "CED"
    
    def get_dictNum(self):
        return str(self.cedNum).zfill(2)
    
    def __str__(self):
        return "Collins English Dictionary"

    def reset(self):
        CED.num, self.cedNum = 1, 1

# Webster's Dictionary
class WEB(Vocab2):
    num = 1
    def __init__(self, word):
        Vocab2.__init__(self, word)
        self.webNum = WEB.num
        WEB.num += 1
        self.dict = "WEB"

    def get_dictNum(self):
        return str(self.webNum).zfill(2)
    
    def __str__(self):
        return "Webster's Dictionary"
    
    def reset(self):
        WEB.num, self.webNum = 1, 1

# Penguin English Dictionary
class PEN(Vocab2):
    num = 1
    def __init__(self, word):
        Vocab2.__init__(self, word)
        self.penNum = PEN.num
        PEN.num += 1
        self.dict = "PEN"
    
    def get_dictNum(self):
        return str(self.penNum).zfill(2)
    
    def __str__(self):
        return "Penguin English Dictionary"

    def reset(self):
        PEN.num, self.penNum = 1, 1

# a = Vocab2("qwerty")
# b = CBR(a)
# c = CBR(a)
# print(b.get_dictNum())
# print(c.get_dictNum())

# b.reset()

# d = Vocab2("as")
# e = CBR(d)
# f = MeaningsCBR(e)
# print(e.get_dictNum())

class Vocab(object):
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

    def find(self, in_cont):
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
        if cur.content=="None" or cur.content=="": pass
        elif cur.content==self.root.content: dc.printH1(self.root.content.upper())
        elif cur.content[0]=="(": dc.printH4(cur.content)
        elif cur.content=="cbr" or cur.content=="ced" or cur.content=="amr" or cur.content=="amp" or cur.content=="esp": pass
        elif cur.content=="sense" or cur.content=="resense": pass
        elif cur.content[0].isdigit(): print(); print(cur.content, end="")
        elif cur.content[:8]=="Synonyms": dc.printH4(cur.content)
        else: print(cur.content)
        if cur.child is not None: self.printDict(cur.child)
        if cur.rsibling is not None: self.printDict(cur.rsibling)

    def __copy__(self):
        return Vocab(self.root)
