import shutil


class txtStyle:
    reset = "\033[0m"
    bold = "\033[01m"
    disable = "\033[02m"
    underline = "\033[04m"
    blink = "\033[5m"
    reverse = "\033[07m"
    invisible = "\033[08m"
    strikethrough = "\033[09m"
    black30 = "\033[30m"
    red31 = "\033[31m"
    green32 = "\033[32m"
    orange33 = "\033[33m"
    blue34 = "\033[34m"
    purple35 = "\033[35m"
    cyan36 = "\033[36m"
    gray37 = "\033[37m"
    gray90 = "\033[90m"
    red91 = "\033[91m"
    green92 = "\033[92m"
    yellow93 = "\033[93m"
    blue94 = "\033[94m"
    purple95 = "\033[95m"
    cyan96 = "\033[96m"
    white = "\033[97m"

def printTxt(in_word, in_lst):
    printTitle()

    word = cmpModify(in_word, in_lst[0])
    print(txtStyle.bold + txtStyle.white + txtStyle.underline + in_lst[0][:len(word)] + txtStyle.reset, end="")
    print(txtStyle.gray90 + in_lst[0][len(word):] + txtStyle.reset)
    for idx in range(1, len(in_lst)):
        line = in_lst[idx]
        if (line==""): pass
        elif (not line[1].isdigit() and in_lst[idx-1][0]=="\n" and idx!=1):
            print(txtStyle.cyan36 + line + txtStyle.reset)
        elif (line[0]=="\n"):
            print(txtStyle.bold + txtStyle.gray37 + line + txtStyle.reset)
        elif (line[0]=="["):
            print(txtStyle.disable + line + txtStyle.reset)
        elif (line[:11]=="Word forms:"):
            print(txtStyle.gray90 + line + txtStyle.reset)
        else: print(txtStyle.gray37 + line + txtStyle.reset)

def cmpModify(word1, word2):
    counter = 0
    for idx in range(len(word2)):
        if (word2[idx]==word1[counter].upper()): counter += 1
        if (counter==len(word1)): return word2[:idx+1]

def printTitle():
    termSize = shutil.get_terminal_size().columns
    spacesN = (termSize-33)//2

    title = ( txtStyle.bold
            + txtStyle.white
            + "+--------------------------------+".center(termSize)
            + "\n"
            + (spacesN * " "    + "||"
            + txtStyle.gray37   + "||"
            + txtStyle.gray90   + "||"
            + txtStyle.black30  + "||"
            + txtStyle.white    + "COLLINS DICTIONARY"
            + txtStyle.black30  + "||"
            + txtStyle.gray90   + "||"
            + txtStyle.gray37   + "||"
            + txtStyle.white    + "||")
            + "\n"
            + "+--------------------------------+".center(termSize)
            + txtStyle.reset
    ); print(title)