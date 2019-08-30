# NLP - Topic modelling


In this project, I try hand at topic modelling, in the context of natural language processing, using the popular Latent Dirichlet Allocation (LDA) method.

The question I try to answer is "What are the main themes in the novels of my favorite science-fiction writer?".

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
For instance: `topic 1: 'space', 'ship', 'planet', ...` `topic 2: 'human', 'society', 'robot', ...`, etc.. Each word in the dictionary (i.e. set of all words occuring in the data) is given a weight, and the keywords are those with a high weight. 

2. Given an author, the model tells us how much each topic is touched upon by the author in his/her novels (at least those with a Wikipedia page). E.g., if there are three topic, the result for one author may be: `topic 1: 30%, topic 2: 0%, topic 3: 70%`.



## Files

-[text_mining_and_processing.ipynb](text_mining_and_processing.ipynb): Jupyter notebook dealing with text mining from Wikipedia and processing it into a corpus that can be used for LDA.
-[extract_wikipedia_data.py](extract_wikipedia_data.py): Python script containing custom functions used by the notebook for text mining and processing.
-[Author-Topic_LDA.ipynb](Author-Topic_LDA.ipynb): Jupyter notebook dealing with training the LDA model and getting results.


## Packages

I use the Wikipedia API for text mining, as well as [this Python wrapper](https://pypi.org/project/Wikipedia-API/), the [spaCy](https://spacy.io/) library for text processing, and [gensim](https://radimrehurek.com/gensim/) for LDA.

## References

Details about LDA and the methods used in the gensim library are found the following papers:
-LDA: [Blei, Ng, & Jordan, 2003](http://www.jmlr.org/papers/v3/blei03a.html)
-online variational Bayes for LDA use by gensim: [Hoffman, Bach, & Blei, 2010](http://papers.nips.cc/paper/3902-online-learning-for-latentdirichlet-allocation!) 
-Author-Topic model:[Rosen-Zvi, Griffiths, Steyvers, & Smyth, 2012](https://arxiv.org/abs/1207.4169)