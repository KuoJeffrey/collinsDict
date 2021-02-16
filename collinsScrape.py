from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from vocab import div, Vocab, MeaningsCBR, MeaningsCED
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

    idx = 0
    dictList = []
    for dict_ in dict_s:
        if dict_ == "cobuild br":
            defNum, poss, posPuncts, definitions, examples, synonyms = cbr(blocks[idx])
            # # Debug # #
            # print("defNum: {}".format(defNum))
            # print("poss: {}".format(poss))
            # print("posPuncts: {}".format(posPuncts))
            # print("definitions: {}".format(definitions))
            # print("examples: {}".format(examples))
            # print("synonyms: {}".format(synonyms))

            tmpList = []
            for i in range(defNum):
                tmp = MeaningsCBR(word)
                tmp.set_pos(poss[i])
                tmp.set_posPunct(posPuncts[i])
                tmp.set_definition(definitions[i])
                tmp.set_examples(examples[i])
                tmp.set_synonyms(synonyms[i])
                tmpList.append(tmp)
                # # Debug # #
                # print(tmp.get_pos())
                # print(tmp.get_posPunct())
                # print(tmp.get_definition())
                # print(tmp.get_examples())
                # print(tmp.get_synonyms())
                # print()
            try:
                tmp.reset_defNum()
                dictList.append(tmpList)
            except UnboundLocalError:
                print("Sorry, no contents available.......")

        elif dict_ == "ced":
            posNum, defNum, poss, firstLines, definitions, examples = ced(blocks[idx])
            # # Debug # #
            # print("posNum: {}".format(posNum))
            # print("defNum: {}".format(defNum))
            # print("poss: {}".format(poss))
            # print("firstLines: {}".format(firstLines))
            # print("definitions: {}".format(definitions))
            # print("examples: {}".format(examples))
            tmpList = []
            for p in range(posNum):
                for d in range(len(definitions[p])):
                    tmp = MeaningsCED(word)
                    if definitions[p][d] == []:
                        tmp.decrement_defNum()
                    else:
                        if firstLines[p][d] == "":
                            tmp.set_firstLine(definitions[p][d][0])
                            if len(definitions[p][d]) > 1:
                                tmp.set_sublines(definitions[p][d][1:])
                        else:
                            tmp.set_firstLine(firstLines[p][d])
                            tmp.set_sublines(definitions[p][d])
                        tmp.set_pos(poss[p])
                        tmp.set_examples(examples[p][d])
                        tmpList.append(tmp)
                        # # Debug # #
                        # print(tmp.get_defNum())
                        # print(tmp.get_pos())
                        # print(tmp.get_firstLine())
                        # print(tmp.get_sublines())
                        # print(tmp.get_examples())
                        # print()
            tmp.set_dictNum()
            tmp.reset_defNum()
            dictList.append(tmpList)

        elif dict_ == "american":
            web(blocks[idx])

        elif dict_ == "dictionary american Penguin":
            pen(blocks[idx])

        else:
            other(blocks[idx])

        idx += 1



    defs, thes, cpRght = contDef(link)
    
    v = Vocab(word)
    v.dict_ = dict_s[0]
    v.cpRght = cpRght

    word = div(word, 1)
    pronun = div(pronuns[0], 1)
    dict_ = div(dict_s[0], 1)
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


def cbr(link):
    # Part of Speech & word's part of speech usage
    homs = link.find_all("div", class_="hom")
    gramGrps = [hom.find("span", class_="gramGrp") for hom in homs if hom.find("span", class_="gramGrp") is not None]
    poss, posPuncts = [], []
    for gramGrp in gramGrps:
        g = gramGrp.find("span", class_="pos")
        if g is None:
            poss.append("".join(rmChars(gramGrp)))
            posPuncts.append("")
        else:
            poss.append("".join(rmChars(g)))
            posPuncts.append("".join(rmChars(gramGrp.find("span", class_="lbl")))[1:])

    # Number of Definitions
    defNum = len(poss)

    # Definitions
    def_s = link.find_all("div", class_="def")
    definitions = ["".join(rmChars(def_)) for def_ in def_s]

    # Examples
    quotes = [hom.find_all("span", class_="quote") for hom in homs]
    examples = []
    for quote in quotes:
        if quote == []:
            examples.append([""])
        else:
            examples.append(["".join(rmChars(q))[1:] for q in quote])

    # Synonyms
    thess = [hom.find_all(class_="form") for hom in homs]
    synonyms = []
    for thes in thess:
        if thes == []:
            synonyms.append([""])
        else:
            tmp = []
            for t in thes:
                try:
                    tmp.append("".join(rmChars(t)))
                except TypeError:
                    tmp.append("")
            synonyms.append(tmp)

    return defNum, poss, posPuncts, definitions, examples, synonyms

def ced(link):
    link = link.find("div", class_="content definitions ced")

    # Part of Speech
    gramGrps = link.find_all("span", class_="pos")
    poss = ["".join(rmChars(gramGrp)) for gramGrp in gramGrps]

    lblss, def_ss, exampless = [], [], []
    homs = link.find_all("div", class_="hom")
    for hom in homs:
        first_sense = hom.find("div", class_="sense")
        senses = [first_sense] + first_sense.find_next_siblings("div", class_="sense")
        
        lbls, def_s, examples = [], [], []
        for sense in senses:
            # First line (lbls)
            spans = sense.find_all("span", class_="lbl")
            if spans == []:
                lbls.append("")
            else:
                lbls.append(" ".join(["".join(rmChars(span))[1:] for span in spans]))

            # Definitions
            def_divs = sense.find_all("div", class_="def")
            if def_divs == []:
                def_s.append([])
            else:
                def_s.append(["".join(rmChars(def_div)) for def_div in def_divs])
            
            # Examples
            quotes = sense.find_all("div", class_="type-example")
            if quotes == []:
                examples.append([])
            else:
                examples.append(["".join(rmChars(quote))[1:] for quote in quotes])
        
        def_ss.append(def_s)
        lblss.append(lbls)
        exampless.append(examples)

    senseLen = 0
    for lbls in lblss:
        senseLen += len(lbls)
    
    return len(poss), senseLen, poss, lblss, def_ss, exampless
    
            
        


def web(link):
    pass

def pen(link):
    pass

def other(link):
    pass



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
