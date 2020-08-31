from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

query_url = "https://www.collinsdictionary.com/dictionary/english/"

# str -> list[str]
def query(word):
    req = Request(query_url+word.replace(" ", "-"), headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    soup = BeautifulSoup(html.read(), 'html.parser')
    link = soup.main.div.find_next_sibling("div")
    link = link.find_next_sibling("div")
    link = link.div.find_next_sibling("div")
    link = link.div.div.div.div.div.div

    lst = []
    if link is None: return word, lst
    for part in link.children:
        item = re.sub(r'<.*?>', '', str(part))
        lst += list(filter(lambda x: len(x.strip()) != 0, item.split('\n')))
    lst = rmUnwanted(lst)
    lines = str2lines(lst)

    word = ""
    for char in html.geturl()[::-1]:
        if (char!="/"): word += char
        else: break
    word = word[::-1].replace("-", " ")
    
    return word, lines


def rmUnwanted(in_lst):
    lst = in_lst[:]
    out_lst = []
    for i in range(len(lst)):
        s = lst[i]; boo = 1
        if isInDict(s):
            lst[i] = "1. " + s
            lst[i+1] = lst[i+1].capitalize()
        elif (s[:16]=="More Synonyms of"): boo = 0
        elif (s[:21]=="  See full dictionary"): break
        elif (s[:16]=="COBUILD Advanced"): break
        elif (s[-24:]=="HarperCollins Publishers"): break
        elif (s[:38]=="Webster’s New World College Dictionary"): break
        elif unWanted(s): boo = 0
        else:
            for j in range(len(s)):
                char = s[j]
                if (char=="<" or char==">" or char=="{" or char=="}" or char=="=" or char=='"'):
                    boo = 0; break
                elif (char=="]" and j+1!=len(s)):
                    out_lst.append(s[:j+1])
                    out_lst.append(s[j+1:])
                    boo = 0; break
            if (boo):
                for j in range(len(s)):
                    char = s[j]
                    if (char.isupper() and s[j-1].islower() and j!=0):
                        if (isInDict(s[:j])): out_lst.append("1. " + s[:j])
                        else: out_lst.append(s[:j])
                        out_lst.append(s[j:])
                        boo = 0; break
                    elif (char.isdigit() and s[j-1].islower() and j!=0):
                        out_lst.append(s[:j])
                        out_lst.append(s[j:])
                        boo = 0; break

        if (boo): out_lst.append(lst[i])
    out_lst[0] = "\n" + out_lst[0].upper()
    return out_lst

def str2lines(in_lst):
    text = "|".join(in_lst)
    lines = [""]
    idx = 0; skip = 0
    for i in range(len(text)-2):
        if skip: skip = 0
        else:
            if (text[i]=="|"):
                prev2 = text[i-2]
                prev1 = text[i-1]
                next1 = text[i+1]
                next2 = text[i+2]
                if (next1.isdigit()):
                    idx += 1
                    lines.append("\n")
                elif (prev1=="." or prev1=="!" or prev1=="?"):
                    if (next1!=" "):
                        idx += 1
                        lines.append("")
                    else:
                        if (next2==" "): skip = 1
                        elif (next2=="." or next2=="[" or next2.isupper()):
                            skip = 1
                            idx += 1
                            lines.append("")
                elif (prev1=="]"):
                    if (next1==" "): skip = 1
                    idx += 1
                    lines.append("")
                elif (prev1.isalpha()):
                    if (next1.isupper()):
                        idx += 1
                        lines.append("")
                    elif (next1.isalpha()): lines[idx] += " "
                elif (prev1!=" "):
                    if (next1.isalpha()):
                        if (prev1=="'" and prev2==" "): pass
                        else:
                            idx += 1
                            lines.append("")
                    elif (next1.isdigit()):
                        idx += 1
                        lines.append("")
                    elif (next1==" "):
                        idx += 1
                        lines.append("1.")
            else: lines[idx] += text[i]
    lines[-1] = lines[-1] + text[-2] + text[-1] + "\n"
    return lines


def isInDict(in_str):
    partOfSpeech = {
        "countable noun":1, 
        "uncountable noun":1, 
        "variable noun":1, 
        "verb":1, 
        "verb transitive":1, 
        "verb intransitive":1, 
        "noun":1, 
        "adjective":1, 
        "adverb":1, 
        "conjunction":1, 
        "suffix":1, 
        "suffix forming nouns":1, 
        "preposition":1, 
        "conjunction, preposition":1, 
        "plural pronoun":1,
        "abbreviation for":1, 
        "prefix":1, 
        "the internet domain name for":1, 
        "modifier":1, 
        "transitive verb":1, 
        "pronoun":1, 
        "singular pronoun":1, 
        "title noun":1, 
        "exclamation":1, 
        "the chemical symbol for":1, 
        "convention":1, 
        "sentence substitute":1, 
        "adverb, interjection":1, 
        "interjection":1, 
        "phrase":1, 
        "combing form":1, 
        "intransitive verb":1, 
        "verb intransitive, verb transitive":1, 
        "singular noun":1, 
        "plural noun":1, 
        "phrasal verb":1, 
        "colour":1, 
        "noun obsolete":1, 
        " noun Economics":1,
    }
    
    try: return partOfSpeech[in_str.lower()]
    except: return 0

def unWanted(in_str):
    unWantedList = {
        "Word Frequency":1,
        "Share":1,
        "×":1,
        "Credits":1,
        "Word origin":1,
        "COBUILD Advanced English Dictionary. Copyright © HarperCollins Publishers":1,
        "Houghton Mifflin Harcourt. All rights reserved.":1,
        "Webster’s New World College Dictionary, 4th Edition. Copyright © 2010 by":1
    }

    try: return unWantedList[in_str]
    except: return 0