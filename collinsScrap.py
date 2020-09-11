from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from vocab import Vocab, div
import decorator as dc
import copy
import re



query_url = "https://www.collinsdictionary.com/dictionary/english/"
dict_ = "cbr" # used dictionary


def query(word, dbug):
    global dict_

    req = Request(query_url+word.replace(" ", "-"), headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    soup = BeautifulSoup(html.read(), 'html.parser')
    link = soup.main.div.find_next_sibling("div")
    link = link.find_next_sibling("div")
    link = link.div.find_next_sibling("div")
    link = link.div.div.div.div.find("div", class_="dictlink")
    if link is None: return 1

    if dbug: print(dc.txtStyle.bold + dc.txtStyle.red31 + "-----------html-----------" + dc.txtStyle.reset); printList(link)
    if dbug: print(dc.txtStyle.bold + dc.txtStyle.red31 + "----------scrape----------" + dc.txtStyle.reset)

    word = h2_entry(link, dbug)
    pronun = mini_h2(link, dbug)
    defs, thes, cpRght = contDef(link, dbug)
    
    if dbug:
        print("word:", word)
        print("pronunciation:", pronun)
        for e in defs: print("definitions:", e)
        print("thesaurus:", thes)
        print("copyrights:", cpRght)


    v = Vocab(word)
    v.dict_ = dict_
    v.cpRght = cpRght

    word = div(word, 1)
    pronun = div(pronun, 1)
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

    if dbug: print("return!")
    return 0



def h2_entry(link, dbug):
    cB_h = link.find("div", class_="cB-h")
    title_container = cB_h.find("div", class_="title_container")
    h2_entry = title_container.find("h2", class_="h2_entry")
    return "".join(rmChars(h2_entry, dbug))



def mini_h2(link, dbug):
    mini_h2 = link.find("div", class_="mini_h2")
    return "".join(rmChars(mini_h2, dbug))[1:]



def contDef(link, dbug):
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
    defs = [hom(d, dbug) for d in defs]

    thes = link.find_next_sibling("div", class_="thes")
    if thes is not None: thes = "".join(rmChars(thes, dbug))

    cpRght = link.find("div", class_="copyright")
    if cpRght is not None: cpRght = "".join(rmChars(cpRght, dbug))

    return defs, thes, cpRght



def hom(link, dbug):
    # Sense number
    senseNum = link.find("span", class_="sensenum")
    if senseNum is not None: senseNum = "".join(rmChars(senseNum, dbug))

    # Part of Speech
    pos = link.find("span", class_="pos")
    lbl = link.find_all("span", class_="lbl")
    if pos is not None:
        pos = "".join(rmChars(pos, dbug))
        if lbl is not None:
            lbl = "".join(["".join(rmChars(e, dbug)) for e in lbl])
            pos += lbl

    # Definition, examples & thesuarus
    sense = link.find("div", class_="sense")
    if sense is not None: sense = defExThes(sense, dbug)

    # Other word forms
    other = link.find("div", class_="re")
    if other is not None: other = re_sense(other, dbug)

    return senseNum, pos, sense, other



def defExThes(link, dbug):
    """
    Input: bs4.element.Tag
    Output: dictionary
    """
    # Definition
    def_ = link.find("div", class_="def")
    if def_ is None: def_ = link
    def_ = "".join(rmChars(def_, dbug))

    # Cit type-examples
    ex = link.find_all("div", class_="cit type-example")
    if ex!=[]:
        ex = ["".join(rmChars(e, dbug)) for e in ex]
        for i in range(len(ex)):
            if ex[i][0]==" ": ex[i] = ex[i][1:]
    
    # Thesaurus
    thes = link.find("div", class_="thes")
    if thes is not None: thes = "".join(rmChars(thes, dbug)[:-1])[:-1]

    return {"definition": def_, "examples": ex, "thesaurus": thes}



def re_sense(link, dbug):
    """
    Input: bs4.element.Tag
    Output: dictionary
    """
    # Word, part of speech, & lbl
    word = link.find("span", class_="orth")
    if word is not None: word = "".join(rmChars(word, dbug))

    pos = link.find("span", class_="pos")
    if pos is not None: pos = "".join(rmChars(pos, dbug))

    lbl = link.find_all("span", class_="lbl")
    if lbl is not None:
        lbl = "".join(["".join(rmChars(e, dbug)) for e in lbl])
        pos += lbl
    
    # Cit type-example
    ex = link.find_all("div", class_="cit type-example")
    if ex!=[]:
        ex = ["".join(rmChars(e, dbug)) for e in ex]
        for i in range(len(ex)):
            if ex[i][0]==" ": ex[i] = ex[i][1:]

    return {"r_word": word, "r_partOfSpeech":pos, "r_examples":ex}



def rmChars(link, dbug):
    lst = []
    try:
        if dbug: print(dc.txtStyle.red31 + "----------rmChars---------" + dc.txtStyle.reset)

        for part in link.children:
            if dbug: print("PART:", part)

            line = str(part)
            item = re.sub(r"<.*?>", "", line, flags=re.S)
            lst += list(filter(lambda x: len(x.strip()) != 0, item.split('\n')))
            
            if dbug: print("ITEM:", item)

        for i in range(len(lst)-1):
            if lst[i][-1].isalpha() and lst[i+1][0].isalpha(): lst[i] = lst[i] + " "

    except AttributeError:
        return

    return lst


# def rmUnwanted(in_lst):
#     if dbug: print(dc.txtStyle.bold + dc.txtStyle.red31 + "-----------in_lst-----------" + dc.txtStyle.reset); printList(in_lst)
#     lst = in_lst[:]
#     out_lst = []
#     for i in range(len(lst)):
#         s = lst[i]; boo = 1
#         if isInDict(s):
#             lst[i] = "1. " + s
#             lst[i+1] = lst[i+1].capitalize()
#         elif s[:16]=="More Synonyms of": boo = 0
#         elif s[:21]=="  See full dictionary": break
#         elif s[:16]=="COBUILD Advanced": break
#         elif s[-24:]=="HarperCollins Publishers": break
#         elif s[:38]=="Webster’s New World College Dictionary": break
#         elif unWanted(s): boo = 0
#         else:
#             for j in range(len(s)):
#                 char = s[j]
#                 if char=="<" or char==">" or char=="{" or char=="}" or char=="=" or char=='"':
#                     boo = 0; break
#                 elif char=="]" and j+1!=len(s):
#                     out_lst.append(s[:j+1])
#                     out_lst.append(s[j+1:])
#                     boo = 0; break
#             if boo:
#                 for j in range(len(s)):
#                     char = s[j]
#                     if char.isupper() and s[j-1].islower() and j!=0:
#                         if isInDict(s[:j]): out_lst.append("1. " + s[:j])
#                         else: out_lst.append(s[:j])
#                         out_lst.append(s[j:])
#                         boo = 0; break
#                     elif char.isdigit() and s[j-1].islower() and j!=0:
#                         out_lst.append(s[:j])
#                         out_lst.append(s[j:])
#                         boo = 0; break

#         if boo: out_lst.append(lst[i])
#     out_lst[0] = "\n" + out_lst[0].upper()
#     return out_lst

# def str2lines(in_lst):
#     if dbug: print(dc.txtStyle.bold + dc.txtStyle.red31 + "-----------rmUnwanted-----------" + dc.txtStyle.reset); printList(in_lst)
#     text = "|".join(in_lst)
#     if dbug: print(dc.txtStyle.bold + dc.txtStyle.red31 + "-----------text-----------" + dc.txtStyle.reset); printList(text)
#     lines = [""]
#     idx = 0; skip = 0
#     for i in range(len(text)-2):
#         if skip: skip = 0
#         else:
#             if text[i]=="|":
#                 prev2 = text[i-2]
#                 prev1 = text[i-1]
#                 next1 = text[i+1]
#                 next2 = text[i+2]
#                 if next1.isdigit():
#                     idx += 1
#                     lines.append("\n")
#                 elif prev1=="." or prev1=="!" or prev1=="?":
#                     if next1!=" ":
#                         idx += 1
#                         lines.append("")
#                     else:
#                         if next2==" ": skip = 1
#                         elif next2=="." or next2=="[" or next2.isupper():
#                             skip = 1
#                             idx += 1
#                             lines.append("")
#                 elif prev1=="]":
#                     if next1==" ": skip = 1
#                     idx += 1
#                     lines.append("")
#                 elif prev1.isalpha():
#                     if next1.isupper():
#                         idx += 1
#                         lines.append("")
#                     elif next1.isalpha(): lines[idx] += " "
#                 elif prev1!=" ":
#                     if next1.isalpha():
#                         if prev1=="'" and prev2==" ": pass
#                         else:
#                             idx += 1
#                             lines.append("")
#                     elif next1.isdigit():
#                         idx += 1
#                         lines.append("")
#                     elif next1==" ":
#                         idx += 1
#                         lines.append("1.")
#             else: lines[idx] += text[i]
#     lines[-1] = lines[-1] + text[-2] + text[-1] + "\n"
#     return lines


# def isInDict(in_str):
#     partOfSpeech = {
#         "countable noun":1, 
#         "uncountable noun":1, 
#         "variable noun":1, 
#         "verb":1, 
#         "verb transitive":1, 
#         "verb intransitive":1, 
#         "noun":1, 
#         "adjective":1, 
#         "adverb":1, 
#         "conjunction":1, 
#         "suffix":1, 
#         "suffix forming nouns":1, 
#         "preposition":1, 
#         "conjunction, preposition":1, 
#         "plural pronoun":1,
#         "abbreviation for":1, 
#         "prefix":1, 
#         "the internet domain name for":1, 
#         "modifier":1, 
#         "transitive verb":1, 
#         "pronoun":1, 
#         "singular pronoun":1, 
#         "title noun":1, 
#         "exclamation":1, 
#         "the chemical symbol for":1, 
#         "convention":1, 
#         "sentence substitute":1, 
#         "adverb, interjection":1, 
#         "interjection":1, 
#         "phrase":1, 
#         "combing form":1, 
#         "intransitive verb":1, 
#         "verb intransitive, verb transitive":1, 
#         "singular noun":1, 
#         "plural noun":1, 
#         "phrasal verb":1, 
#         "colour":1, 
#         "noun obsolete":1, 
#         " noun Economics":1,
#     }
    
#     try: return partOfSpeech[in_str.lower()]
#     except: return 0

# def unWanted(in_str):
#     unWantedList = {
#         "Word Frequency":1,
#         "Share":1,
#         "×":1,
#         "Credits":1,
#         "Word origin":1,
#         "COBUILD Advanced English Dictionary. Copyright © HarperCollins Publishers":1,
#         "Houghton Mifflin Harcourt. All rights reserved.":1,
#         "Webster’s New World College Dictionary, 4th Edition. Copyright © 2010 by":1
#     }

#     try: return unWantedList[in_str]
#     except: return 0


def printList(input):
    try:
        if type(input)==str: print(input); print()
        else:
            for i in input: print(i); print()
    except:
        print(dc.txtStyle.bold + dc.txtStyle.red31 + "Nontype" + dc.txtStyle.reset)