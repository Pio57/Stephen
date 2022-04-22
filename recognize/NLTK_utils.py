import nltk
#nltk.download('punkt')
#from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer
import numpy as np

#stemmar = PorterStemmer()
stemmar = SnowballStemmer('italian')

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stemming(word):
    return stemmar.stem(word.lower())

def bag_of_words(tokenize_sentence, all_words):
    tokenize_sentence = [stemming(w) for w in tokenize_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenize_sentence:
            bag[idx] = 1.0

    return bag

"""
sentence = ["hello", "how", "are", "you"]
all_words = ["hello", "hi", "i", "you", "bye", "thank", "cool"]
bag = bag_of_words(sentence,all_words)
print(bag)


words = ['correre', 'corro', 'corriamo', 'correremo', 'bambino', 'bambini', 'bambina', 'bambine']
tokenize_sentence = [stemming(w) for w in words]
print(tokenize_sentence)

"""
