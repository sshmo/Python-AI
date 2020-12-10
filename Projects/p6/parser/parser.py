import nltk
import sys
import string

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
    S -> VP | NP VP | S Conj S
    AdjP -> Adj | Adj AdjP
    NP -> N | Det N | Det AdjP N | AdjP NP | NP PP | NP AdvP | NP Conj NP
    PP -> P NP
    VP -> V | V NP | V PP | V AdvP | VP Conj VP    
    AdvP -> Adv | AdvP Adv 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Initialize the list of `sentence` words, punctuation and alphabets
    prep_list = []
    punctuations = string.punctuation
    alphabets = 'abcdefghijklmnopqrstuvwxyz'

    # Make a tokenized copy of the `sentence`
    naive_list = nltk.word_tokenize(sentence)
    
    for item in naive_list:
        
        # Ignoring punctuations or digits that obviously 
        # does not contain any alphabetic character
        if item in punctuations or item.isdigit():
            continue
        
        # Ensuring that item contains at least one alphabetic character
        Flag = False
        for char in alphabets:
            if char in item.lower():
                Flage = True
                break
        
        # Add item to the list of Pre-processed words
        if Flage:
            prep_list.append(item.lower())

    return prep_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    # Initialize the list of noun phrases subtrees
    chunks = []

    # Find all subtrees
    subtrees = tree.subtrees()

    for subtree in subtrees:
        
        # Investigate all subtrees with NP label
        if subtree.label() == 'NP':
            
            # Ensuring that the subtree with NP label
            # does not contain any subtree with NP label
            Flag = True
            for i in range(len(subtree)):
                if subtree[i].label() == 'NP':
                    Flag = False
                    break
            
            # Add subtree to the list of noun phrase chunks
            if Flag:
                chunks.append(subtree)

    return chunks


if __name__ == "__main__":
    main()
