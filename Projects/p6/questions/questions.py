import os
import nltk
import sys
import string
import math
import pandas as pd


FILE_MATCHES = 6
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    # Initialize file dictionary
    dictionary = {}
        
    # Make directory path
    directory_str = '.' + os.sep + directory + os.sep
    directory = os.fsencode(directory_str)

    # Loop over directory path for .txt documents
    for file in os.listdir(directory):
        
        # Get the file name
        filename = os.fsdecode(file)

        # Enshure that file is a .txt documents
        if filename.endswith(".txt"): 
            
            # Make a dictionary of .txt documents
            dictionary[filename] = open(directory_str + filename, "r", encoding="utf8").read()

    return dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    # Initialize the list of words, punctuation and stopwords
    prep_list = []
    punctuations_list = string.punctuation
    stopwords_list = nltk.corpus.stopwords.words("english")

    # Make a naive tokenized copy of the `document`
    naive_list = nltk.word_tokenize(document)

    for item in naive_list:
        
        # Ignore punctuations or stopwords
        if (item in punctuations_list) or (item in stopwords_list):
            continue
        
        # Add document by coverting all words to lowercase
        prep_list.append(item.lower())
    
    return prep_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # Initialize a dictionary that maps words to their IDF values.
    idf_dict = {}

    # Loop over text documents
    for text_name in documents:
        
        # Loop over words in each document
        for word in documents[text_name]:
            
            # continue if the word was already processed in
            # previous documents
            if word in idf_dict:
                continue
            
            # Count number of documents that contain the word
            word_count = 0
            for doc_name in documents:
                if word in documents[doc_name]:
                    word_count += 1
            
            # Calculate and add idf_score(word) = ln(doc_count/word_count)
            idf_dict[word] = math.log(len(documents)/word_count)
    
    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
     
    # Initialize the list of  the `n` top files 
    # and their `total tf-idf` score
    file_scores = []
    file_names = []
    
    # Loop over the list of all the filenames
    for file_name in files:
    
        # Initialize the file `total tf-idf` score as zero
        file_scores.append(0)
        file_names.append(file_name)        
        
        # Loop ower words in the query
        for word in query:
            
            # For query words that appear in file, 
            # update the `total tf-idf` score
            if word in files[file_name]:
                
                # tf_score is the count of word in a document
                tf_word = files[file_name].count(word)

                # Read the idf_score from the provided dictionary
                idf_word = idfs[word]

                # `total tf-idf` score = sum of all (tf_score * idf_score)
                file_scores[-1] += tf_word * idf_word

    # Sort based on the on `total tf-idf` score
    ordered_files = [x for _, x in sorted(zip(file_scores, file_names), reverse=True)]

    # Return top n files
    return ordered_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    # Initialize the list of top sentences
    # and their list of `total idf` score
    # and their list of `query term density` 
    # as a dictionary
    top_sent = {}
    top_sent['score'] = []
    top_sent['density'] = []
    top_sent['names'] = []
    
    # Loop over all given sentences
    for sent_name in sentences:
        
        # Initialize the file `total idf` score
        # and `query term density` as zero
        top_sent['score'].append(0)
        top_sent['density'].append(0)
        top_sent['names'].append(sent_name)        
        
        # Loop ower words in the query
        for word in query:
            
            # For query words that appear in file, update 
            # `total idf` score and `query term density`
            if word in sentences[sent_name]:
                
                top_sent['density'][-1] += sentences[sent_name].count(word)\
                    / len(sentences[sent_name])
                top_sent['score'][-1] += idfs[word]

    # Convert the dictionary to dataframe
    top_sent_df = pd.DataFrame(top_sent)

    # Sort based on the on `total idf` score, then by `query term density`
    top_sent_df.sort_values(by=['score', 'density'], 
                            inplace=True, ascending=False)
    
    # Return top n sentences
    return list(top_sent_df['names'][:n])


if __name__ == "__main__":
    main()
