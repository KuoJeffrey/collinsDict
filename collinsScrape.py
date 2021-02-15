from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from vocab import Vocab, Vocab2, div
import decorator as dc
import copy
import re



query_url = "https://www.collinsdictionary.com/dictionary/english/"


def query(word):
    
    req = Request(query_url+word.replace(" ", "-"), headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    soup = BeautifulSoup(html.read(), 'html.parser')
    link = soup.main.div.find_next_sibling("div")
    link = link.find_next_sibling("div")
    link = link.div.find_next_sibling("div")
    link = link.div.div.div.div.find("div", class_="dictlink")
    
    word = title(soup)
    blocks = dictLink(soup)
    if blocks == []: return 1

    pronuns = mini_h2(soup)
    dict_s = [cB_def(block) for block in blocks]

    vocab = Vocab2(word)
    for dict_ in dict_s:
        if dict_ == "cobuild br":
            pass
        elif dict_ == "ced":
            pass
        elif dict_ == "american":
            pass
        elif dict_ == "dictionary american Penguin":
            pass
        else:
            pass





    defs, thes, cpRght = contDef(link)
    
    v = Vocab(word)
    v.dict_ = dict_
    v.cpRght = cpRght

    word = div(word, 1)
    pronun = div(pronuns[0], 1)
    dict_ = div(dict_, 1)
    v.insert(v.root, word)
    v.insert(word, pronun)
    v.insert(pronun, dict_)

    trace = dict_; i = 1
    for def_ in defs:
        if def_[0] is None: v.insert(trace, div("None", 2))
        else: v.insert(trace, div(def_[0], 2))
        if i: trace = trace.child; i = 0
        else: trace = trace.rsibling
        if def_[1] is None: v.insert(trace, div("None", 2))
        else: v.insert(trace, div(def_[1], 2))

        v.insert(trace.rsibling, div("sense", 3))
        if def_[2] is None:
            v.insert(trace.rsibling.child, div("None", 4))
        else:
            if def_[2]["definition"] is None: v.insert(trace.rsibling.child, div("None", 4))
            else: v.insert(trace.rsibling.child, div(def_[2]["definition"], 4))
            trace_exp = trace.rsibling.child.child
            for exp in def_[2]["examples"]:
                v.insert(trace_exp, div(exp, 4))
                trace_exp = trace_exp.rsibling
            if def_[2]["thesaurus"] is None: v.insert(trace_exp, div("None", 4))
            else: v.insert(trace_exp, div(def_[2]["thesaurus"], 4))

        v.insert(trace.rsibling.child, div("resense", 3))
        if def_[3] is None: v.insert(trace.rsibling.child.rsibling, div("None", 4))
        else:
            v.insert(trace.rsibling.child.rsibling, div(def_[3]["r_word"], 4))
            v.insert(trace.rsibling.child.rsibling.child, div(def_[3]["r_partOfSpeech"], 4))
            trace_rexp = trace.rsibling.child.rsibling.child.rsibling
            for rexp in def_[3]["r_examples"]:
                v.insert(trace_rexp, div(rexp, 4))
                trace_rexp = trace_rexp.rsibling

        trace = trace.rsibling

    v.printDict()

    return 0

def title(link):
    return link.title.string.split(" definition")[0]


def dictLink(link):
    return link.find_all("div", class_="dictlink")


def mini_h2(link):
    mini_h2s = link.find_all("div", class_="mini_h2")
    return ["".join(rmChars(mini_h2))[1:] for mini_h2 in mini_h2s]

def cB_def(link):
    dict_ = link.div.get("class")
    return  " ".join(dict_[2:])


def contDef(link):
    global dict_

    cbr = link.find("div", class_="content definitions cobuild br")
    if cbr is not None: link = cbr; dict_ = "cbr"
    else:
        ced = link.find("div", class_="content definitions ced")
        if ced is not None: link = ced; dict_ = "ced"
        else:
            amr = link.find("div", class_="content definitions american")
            if amr is not None: link = amr; dict_ = "amr"
            else:
                amp = link.find("div", class_="content definitions dictionary american Penguin")
                if amp is not None: link = amp; dict_ = "amp"
                else:
                    esp = link.find("div", class_="content definitions esp")
                    if esp is not None: link = esp; dict_ = "esp"

    defs = link.find_all("div", class_="hom")
    defs = [hom(d) for d in defs]

    thes = link.find_next_sibling("div", class_="thes")
    if thes is not None: thes = "".join(rmChars(thes))

    cpRght = link.find("div", class_="copyright")
    if cpRght is not None: cpRght = "".join(rmChars(cpRght))

    return defs, thes, cpRght



def hom(link):
    # Sense number
    senseNum = link.find("span", class_="sensenum")
    if senseNum is not None: senseNum = "".join(rmChars(senseNum))

    # Part of Speech
    pos = link.find("span", class_="pos")
    lbl = link.find_next_sibling("span", class_="lbl")
    if pos is not None:
        pos = "".join(rmChars(pos))
        if lbl is not None:
            lbl = "".join(["".join(rmChars(e)) for e in lbl])
            pos += lbl

    # Definition, examples & thesuarus
    sense = link.find("div", class_="sense")
    if sense is not None: sense = defExThes(sense)

    # Other word forms
    other = link.find("div", class_="re")
    if other is not None: other = re_sense(other)

    return senseNum, pos, sense, other



def defExThes(link):
    """
    Input: bs4.element.Tag
    Output: dictionary
    """
    # Definition
    def_ = link.find("div", class_="def")
    if def_ is None: def_ = link
    def_ = "".join(rmChars(def_))

    # Cit type-examples
    ex = link.find_all("div", class_="cit type-example")
    if ex!=[]:
        ex = ["".join(rmChars(e)) for e in ex]
        for i in range(len(ex)):
            if ex[i][0]==" ": ex[i] = ex[i][1:]
    
    # Thesaurus
    thes = link.find("div", class_="thes")
    if thes is not None: thes = "".join(rmChars(thes)[:-1])[:-1]

    return {"definition": def_, "examples": ex, "thesaurus": thes}



def re_sense(link):
    """
    Input: bs4.element.Tag
    Output: dictionary
    """
    # Word, part of speech, & lbl
    word = link.find("span", class_="orth")
    if word is not None: word = "".join(rmChars(word))

    pos = link.find("span", class_="pos")
    if pos is not None: pos = "".join(rmChars(pos))

    lbl = link.find_all("span", class_="lbl")
    if lbl is not None:
        lbl = "".join(["".join(rmChars(e)) for e in lbl])
        pos += lbl
    
    # Cit type-example
    ex = link.find_all("div", class_="cit type-example")
    if ex!=[]:
        ex = ["".join(rmChars(e)) for e in ex]
        for i in range(len(ex)):
            if ex[i][0]==" ": ex[i] = ex[i][1:]

    return {"r_word": word, "r_partOfSpeech":pos, "r_examples":ex}



def rmChars(link):
    lst = []
    try:

        for part in link.children:
            line = str(part)
            item = re.sub(r"<.*?>", "", line, flags=re.S)
            lst += list(filter(lambda x: len(x.strip()) != 0, item.split('\n')))

        for i in range(len(lst)-1):
            if lst[i][-1].isalpha() and lst[i+1][0].isalpha(): lst[i] = lst[i] + " "

    except AttributeError:
        return

    return lst




def printList(input):
    try:
        if type(input)==str: print(input); print()
        else:
            for i in input: print(i); print()
    except:
        print(dc.txtStyle.bold + dc.txtStyle.red31 + "Nontype" + dc.txtStyle.reset)
