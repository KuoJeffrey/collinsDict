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
    cbrNum = 1
    def __init__(self, word):
        Vocab2.__init__(self, word)
        self.dict_ = "CBR"
        self.pos = ""
        self.definition = ""
    
    def __str__(self):
        return "Collins Cobuild Advanced Dictionary"
    
    def reset_dictNum(self):
        CBR.cbrNum = 1

    def set_dictNum(self):
        CBR.cbrNum += 1
    
    def set_pos(self, pos):
        self.pos = pos
    
    def set_definition(self, definition):
        self.definition = definition

    def get_dictNum(self):
        return str(CBR.cbrNum).zfill(2)
    
    def get_dict(self):
        return self.dict_
    
    def get_pos(self):
        return self.pos
    
    def get_definition(self):
        return self.definition
    
class MeaningsCBR(CBR):
    meaningNum = 1
    def __init__(self, word):
        CBR.__init__(self, word)
        self.num = MeaningsCBR.meaningNum
        MeaningsCBR.meaningNum += 1
        self.posPunct = ""
        self.punctuation = ""
        self.examples = []
        self.synonyms = []
    
    def __str__(self):
        return "{}".format(self.get_defNum())

    def reset_defNum(self):
        MeaningsCBR.meaningNum = 1

    def set_posPunct(self, posPunct):
        self.posPunct = posPunct

    def set_punctuation(self, punctuation):
        self.punctuation = punctuation

    def set_examples(self, examples):
        self.examples = examples

    def set_synonyms(self, synonyms):
        self.synonyms = synonyms

    def get_defNum(self):
        return self.num

    def get_posPunct(self):
        return self.posPunct

    def get_punctuation(self):
        return self.punctuation

    def get_examples(self,):
        return self.examples

    def get_synonyms(self):
        return self.synonyms


# Collins English Dictionary
class CED(Vocab2):
    cedNum = 1
    def __init__(self, word):
        Vocab2.__init__(self, word)
        self.dict_ = "CED"
        self.pos = ""
        self.firstLine = ""
    
    def __str__(self):
        return "Collins English Dictionary"
    
    def reset_dictNum(self):
        CED.cedNum = 1
    
    def set_dictNum(self):
        CED.cedNum += 1

    def set_pos(self, pos):
        self.pos = pos
    
    def set_firstLine(self, firstLine):
        self.firstLine = firstLine

    def get_dict(self):
        return self.dict_

    def get_dictNum(self):
        return str(CED.cedNum).zfill(2)
    
    def get_pos(self):
        return self.pos
    
    def get_firstLine(self):
        return self.firstLine

class MeaningsCED(CED):
    meaningNum = 1
    def __init__(self, word):
        CED.__init__(self, word)
        self.num = MeaningsCED.meaningNum
        MeaningsCED.meaningNum += 1
        self.sublines = []
        self.examples = []
        # self.wordOrigin = ""
    
    def __str__(self):
        return "{}".format(self.get_defNum())
    
    def decrement_defNum(self):
        MeaningsCED.meaningNum -= 1
    
    def reset_defNum(self):
        MeaningsCED.meaningNum = 1
    
    def set_sublines(self, sublines):
        self.sublines = sublines
    
    def set_examples(self, examples):
        self.examples = examples

    def get_defNum(self):
        return self.num
    
    def get_sublines(self):
        return self.sublines
    
    def get_examples(self):
        return self.examples


# Webster's Dictionary
class WEB(Vocab2):
    num = 1
    def __init__(self, word):
        Vocab2.__init__(self, word)
        self.webNum = WEB.num
        WEB.num += 1
        self.dict_ = "WEB"

    def get_dictNum(self):
        return str(self.webNum).zfill(2)
    
    def get_dict(self):
        return self.dict_
    
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
        self.dict_ = "PEN"
    
    def get_dictNum(self):
        return str(self.penNum).zfill(2)
    
    def get_dict(self):
        return self.dict_
    
    def __str__(self):
        return "Penguin English Dictionary"

    def reset(self):
        PEN.num, self.penNum = 1, 1







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
