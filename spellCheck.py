from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

close_words_url = "https://www.collinsdictionary.com/spellcheck/english/?q="

def dummy():
    return