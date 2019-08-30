# NLP - Topic modeling


In this project, I experiement with topic modelling, in the context of natural language processing, using the popular Latent Dirichlet Allocation (LDA) method.

The question I try to answer is "What main topics can be found in the novels of my favorite science-fiction writers?".
Even though each novel is unique, there are typically some thematic environement or context in which the stories take place, which I try to extract from textual data (e.g. time travel, space exploration, robots, etc.)

The work is diveded in three steps:
1. Extracting the textual data: I use the information about SF novels found on Wikipedia, using its convenient API.
2. Processing the texts: this includes
    - selecting the relevant information
    - tokenization, 
    - cleaning-up (e.g. stopwords), 
    - lemmatization, 
    - POS tagging.

3. Building and training a model: I use an author-topic LDA model, which extends LDA to include authorship information.


The results are two-fold:
1. From all the texts found on the pages about SF novels on Wikipedia, the LDA model can build human-interpretable topics based on keywords.
For instance: `topic 1: 'space', 'ship', 'planet', ...` `topic 2: 'human', 'society', 'robot', ...`, etc.. Each word in the dictionary (set of all words occuring in the data) is given a weight, and the top keywords are those with a high weight. 

2. Given an author, the model tells us how much of each topic is found in his/her novels (at least those with a Wikipedia page). E.g., if there are three topics, the result for one author may be: `topic 1: 30%, topic 2: 0%, topic 3: 70%`.



## Files

- [text_mining_and_processing.ipynb](https://nbviewer.jupyter.org/github/adrienbolens/NLP-topic-modeling/blob/master/text_mining_and_processing.ipynb): Jupyter notebook dealing with text mining from Wikipedia and processing it into a corpus that can be used for LDA.
- [extract_wikipedia_data.py](extract_wikipedia_data.py): Python script containing custom functions used by the notebook for text mining and processing.
- [Author-Topic-LDA.ipynb](https://nbviewer.jupyter.org/github/adrienbolens/NLP-topic-modeling/blob/master/Author-Topic-LDA.ipynb): Jupyter notebook dealing with training the LDA model and getting results.


## Packages

I use the Wikipedia API for text mining, as well as [this Python wrapper](https://pypi.org/project/Wikipedia-API/), the [spaCy](https://spacy.io/) library for text processing, and [gensim](https://radimrehurek.com/gensim/) for LDA.

## References

Details about LDA and the methods used in the gensim library are found the following papers:
- LDA: [Blei, Ng, & Jordan, 2003](http://www.jmlr.org/papers/v3/blei03a.html).
- Online variational Bayes for LDA used by gensim: [Hoffman, Bach, & Blei, 2010](http://papers.nips.cc/paper/3902-online-learning-for-latentdirichlet-allocation!) .
- Author-Topic model: [Rosen-Zvi, Griffiths, Steyvers, & Smyth, 2012](https://arxiv.org/abs/1207.4169).
