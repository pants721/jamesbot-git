import csv
import random

import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))


symbolBlackList = [",", ".", "`", "'", '"', "?", "!", "(", ")"]

# "Pythons great because you don't have to declare variables before using them"
# I need to do this to feel safe
phraseList = []
authorList = []
tokList = []
taggedList = ""

nounList = []
advList = []
adjList = []
verbList = []
pronList = []
numList = []
adpList = []

# NOUN = NOUN
# ADVERB = ADV
# ADJECTIVE = ADJ
# VERB = VERB
# PRONOUN = PRON
is_noun = lambda pos: pos[:4] == "NOUN"
is_adv = lambda pos: pos[:3] == "ADV"
is_adj = lambda pos: pos[:3] == "ADJ"
is_verb = lambda pos: pos[:4] == "VERB"
is_pron = lambda pos: pos[:4] == "PRON"
is_num = lambda pos: pos[:3] == "NUM"
is_adp = lambda pos: pos[:3] == "ADP"


def genLists():
    """Generates two lists: phraseList and authorList from csv file.

    Stores a string arr of the sentences in phraseList.
    Stores a string arr of the authors for the sentences at corresponding indecies
    in authorList.

    Ex:
    Quote: "Hi, my name is Dan!", Dan
    phraseList[__index] = "Hi, my name is Dan!"
    authorList[__index] = "Dan"
    """
    with open("phrases.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            phraseList.insert(len(phraseList), row[0].lower())
            authorList.insert(len(authorList), row[1].lower())


def tokenizeList(list):
    """Tokenizes a list.

    Args:
        list (string array): a list of strings.
    """
    for x in list:
        tokens = nltk.word_tokenize(x)
        # Removes stop words (ex: the, is, and)
        tokens = [w for w in tokens if not w in stop_words]
        for i in tokens:
            # removes any list items that contain a symbol in symbolBlackList
            if any(c in i for c in symbolBlackList):
                break
            else:
                tokList.insert(len(tokList), i)
    cleanList(tokList)


def cleanList(list):
    """Function to remove any list items that are only a quotation to account for weird csv thing

    Args:
        list (string array): Tokenized List
    """
    for i in range(len(tokList)):
        try:
            list.remove("“")
            list.remove("”")
        except ValueError:
            pass


def sortList(list):
    """Sorts a tagged list using universal taglist into parts of speech in their
    respective arrays

    Args:
        list (sorted list): A sorted list of tokens
    """
    # POS IS PART OF SPEECH NOT POSITION !
    for (word, pos) in list:
        if is_noun(pos):
            nounList.insert(len(nounList), word)
        elif is_adv(pos):
            advList.insert(len(advList), word)
        elif is_adj(pos):
            adjList.insert(len(adjList), word)
        elif is_verb(pos):
            verbList.insert(len(verbList), word)
        elif is_pron(pos):
            pronList.insert(len(pronList), word)
        elif is_num(pos):
            numList.insert(len(numList), word)
        elif is_adp(pos):
            adpList.insert(len(adpList), word)
        else:
            # DEBUG
            # print("Bad input")
            # print(word, pos)
            pass


# basic
def rawSentenceGen(length):
    """Basic function that generates sentences using a few basic sentence structures
    with words chosen from random indecies of the POS arrays

    Args:
        length (int): the number of words in the sentence

    Returns:
        string: The generated sentence (unformatted)
    """
    if length == 2:
        authorRandWord = (
            authorList[random.randint(0, len(authorList) - 1)].strip().capitalize()
        )
        verbRandWord = verbList[random.randint(0, len(verbList)) - 1]
        return f"{authorRandWord} {verbRandWord}."
    elif length == 3:
        randChoice = random.randint(0, 1)
        if randChoice == 0:
            # Pronoun Verb Noun
            pronRandWord = pronList[random.randint(0, len(pronList)) - 1]
            verbRandWord = verbList[random.randint(0, len(verbList)) - 1]
            nounRandWord = nounList[random.randint(0, len(nounList)) - 1]
            return f"{pronRandWord} {verbRandWord} {nounRandWord}."
        elif randChoice == 1:
            # Noun Verb Noun2
            nounRandWord = nounList[random.randint(0, len(nounList)) - 1]
            verbRandWord = verbList[random.randint(0, len(verbList)) - 1]
            nounRandWord2 = nounList[random.randint(0, len(nounList)) - 1]
            return f"{nounRandWord} {verbRandWord} {nounRandWord2}."
    elif length == 4:
        # Noun ADP Noun2 Verb
        nounRandWord = nounList[random.randint(0, len(nounList)) - 1]
        adpRandWord = adpList[random.randint(0, len(adpList)) - 1]
        nounRandWord2 = nounList[random.randint(0, len(nounList)) - 1]
        verbRandWord = verbList[random.randint(0, len(verbList)) - 1]
        return f"{nounRandWord} {adpRandWord} {nounRandWord2} {verbRandWord}."


def generateSentence():
    genLists()
    tokenizeList(phraseList)
    taggedList = nltk.pos_tag(tokList, tagset="universal")
    sortList(taggedList)
    randChoiceNum = random.randint(2, 4)
    randAuthor = authorList[random.randint(0, len(authorList) - 1)]
    return (
        f'"{rawSentenceGen(randChoiceNum).lower().capitalize()}" -{randAuthor.strip()}'
    )


if __name__ == "__main__":
    print(generateSentence())
