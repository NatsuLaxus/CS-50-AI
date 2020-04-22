import nltk
import sys
from nltk.corpus import stopwords
import string
from nltk.tokenize import RegexpTokenizer
import os
import math
nltk.download('stopwords')

FILE_MATCHES = 1
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
    files = dict()
    for file in os.listdir(directory):
        contents = ''
        with open(os.path.join(directory, file),encoding="utf8") as f:
            contents = f.read().replace('\n','')
        files[file] = contents
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # raise NotImplementedError
    document = document.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    document = tokenizer.tokenize(document)
    document = [word for word in document if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    document = [word for word in document if not word in stop_words]
    return document


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # raise NotImplementedError
    idfs = {}
    words = set()
    for doc in documents:
        words.update(documents[doc])

    for word in words:
        f = sum(word in documents[doc] for doc in documents)
        idf = float(math.log(len(documents)/f))
        idfs[word] = idf
    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # raise NotImplementedError
    tfidf = []
    # print(query)
    tfidfs = dict()
    frequency = dict()
    for file in files:
        freq = dict()
        for words in files[file]:
            if words not in freq:
                freq[words] = 1
            else:
                freq[words] += 1
        frequency[file] = freq
    for file in files:
        tfidfs[file]=0
        # print(file)
        for q in query:
            # print("1")
            if q in files[file]:
                # print(q)
                tf = frequency[file][q]
                # print(tf)
                # print(idfs[q])
                tfidfs[file] += tf*idfs[q]
        # print(tfidfs[file])
        # print("123")
    # print(sorted(tfidfs.items(),key=lambda tfidf: tfidf[1], reverse=True))
    tfidf = sorted(tfidfs.items(),key=lambda tfidf: tfidf[1], reverse=True)
    # tfi = (tfidf.keys())
    # print(tfidf)
    t = [tfi[0] for tfi in tfidf]
    t = t[:n]
    print(t)
    return t


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # raise NotImplementedError
    idf = []
    idfsum = dict()
    count = dict()
    for sentence in sentences:
        idfsum[sentence] = ()
        count[sentence] = 0
        c = 0
        for q in query:
            if q in sentence:
                c += idfs[q]
                count[sentence] += 1
        count[sentence] = count[sentence]/len(sentence)
        idfsum[sentence] = (c,count[sentence])
    idf = sorted(idfsum.items(), key = lambda idfsum:(idfsum[1][0],idfsum[1][1]), reverse = True)
    print(idf[:10])
    i = [id[0] for id in idf]
    i = i[:n]
    return i


if __name__ == "__main__":
    main()
