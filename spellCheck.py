from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from collinsScrape import rmChars
import decorator as dc
import re

close_words_url = "https://www.collinsdictionary.com/spellcheck/english/?q="

def suggest(word, options, dbug):
    req = Request(close_words_url+word.replace(" ", "-"), headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    soup = BeautifulSoup(html.read(), 'html.parser')
    link = soup.main.div.find_next_sibling("div")
    link = link.find_next_sibling("div")
    link = link.find("div", class_="cB")
    link1 = link.find("h1")
    link2 = link.find("h2")
    link3 = link.find("ul", class_="columns2")

    noResults = rmChars(link1, dbug)
    didYouMean = rmChars(link2, dbug)
    suggested = rmChars(link3, dbug)
    dc.printH1(noResults)
    dc.printH2(didYouMean)
    dc.printSuggestedWords(suggested)
    dc.printOptions(options)

    while 1:
        choice = input(dc.txtStyle.green32); print(dc.txtStyle.reset)
        if choice in options: return choice
        elif choice.isdigit() and int(choice) in range(1, len(suggested)+1):
            return suggested[int(choice)-1]
        else:
            message = "Invalid input, did you mean:"
            dc.printError(message)
            dc.printSuggestedWords(suggested)
            dc.printOptions(options)