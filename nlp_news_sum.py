#Sahil.C : imnotsahil@gmail.com, Sweety : ssweety9643@gmail.com, Mohit Porwal : porwalmohit1999@gmail.com.
#TEAM ID- 1961----
#Analyticscosm internship ----Competition ID AC01----
#Natural Language Processing to Summarize NEWS----
#Approach Used - Extractive Summarization Technique
#Team Contribution:
#-----------------
#!/usr/bin/env python
# coding: utf-8
#importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

#functiom to read the articles that need to be summarized
def read_file(fname):
    file = open(fname, "r")
    fdata = file.readlines()
    article = fdata[0].split(". ")
    sents = []

    for sentence in article:
        print(sentence)
        sents.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sents.pop() 
    
    return sents
#function for checking sentence similarity
def _checking_sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
    
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    w_all = list(set(sent1 + sent2))
 
    #creating vectors
    v1 = [0] * len(w_all)
    v2 = [0] * len(w_all)
 
    # building the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        v1[w_all.index(w)] += 1
 
    # building the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        v2[w_all.index(w)] += 1
 
    return 1 - cosine_distance(v1, v2)#returning cosine _distance vector


#function to build the similarity matrix of the article 
def create_s_matrix(sents, stop_words):
    # Create an empty similarity matrix
    s_matrix = np.zeros((len(sents), len(sents)))
 
    for idx1 in range(len(sents)):
        for idx2 in range(len(sents)):
            if idx1 == idx2: #ignore if both are same sents
                continue 
            s_matrix[idx1][idx2] = _checking_sentence_similarity(sents[idx1], sents[idx2], stop_words)

    return s_matrix #returning the similarity matrix


#function to create summary
def create_summary(fname, top_n=5):
    nltk.download("stopwords")
    stop_words = stopwords.words('english')
    s_text = []

    #reading the input text from the article and splitting
    sents =  read_file(fname)

    #creating a similarity matrix for all the sents of the input text
    _checking_sentence_similarity_martix = create_s_matrix(sents, stop_words)

    #ranking the sents from the similarity matrix
    _checking_sentence_similarity_graph = nx.from_numpy_array(_checking_sentence_similarity_martix)
    scores = nx.pagerank(_checking_sentence_similarity_graph)

    #picking the top ranked sentence from the sinilarity matrix
    r_sent = sorted(((scores[i],s) for i,s in enumerate(sents)), reverse=True)    
    print("Indexes of top r_sent order are ", r_sent)    
    
    #looping and appending ranked sents to the summary
    #thus generating a summary of the article
    for i in range(top_n):
      s_text.append(" ".join(r_sent[i][1]))

    #printing the output of the input article
    print("Summary of the Article: \n", ". ".join(s_text))
    
    

#calling the create summary function to create summary of the specified article
create_summary( "input2.txt", 2)
