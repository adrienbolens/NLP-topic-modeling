import re
import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('en')

import spacy
spacy_nlp = spacy.load('en_core_web_sm')


def get_categorymembers(category,
                        n_pages_per_level_threshold=0,
                        level=0,
                        max_level=0,
                        pages=None,
                        verbose=False):
    """
    Return a list of all wikipedia pages from a given category.

    Categories are themselves pages, but only non-category (namespace=0)
    pages are returned.  Pages of subcategories (i.e. at a higher "level") are
    also considered recursively, up to level `max_level`. Altenatively, the
    recursion is stopped for categories with a number of pages higher than a
    given threshold (`n_pages_per_level_threshold`).

    NOTE: duplicates are not removed.

    Args:
    ----
        category (wikipediaapi.WikipediaPage, must be a category, i.e. ns=14)
        n_pages_per_level_threshold (int): stop the recursion if the number of
            pages for a category is exceeded.
            If None, the condition is ignored.
        level (int): current level of the category
        max_level (int): stop the recursion after a certain level is reached.
            If None, the condition is ignored.
        pages (list of wikipediaapi.WikipediaPage): list to which the pages are
            appended
        verbose (bool)

    Returns:
    -------
        pages (list of wikipediaapi.WikipediaPage)
    """

    if pages is None:
        pages = []
    members = category.categorymembers
    subcategories = []
    n_pages = 0
    for page in members.values():

        # Pages (non-category):
        if page.ns == wikipediaapi.Namespace.MAIN:
            n_pages += 1
            pages.append(page)
            if verbose:
                print("{0:70.70}{1:>27}".format(get_info_str(page, level),
                                                'PAGE ADDED'))
        # Categories:
        elif page.ns == wikipediaapi.Namespace.CATEGORY:
            subcategories.append(page)

    # Repeat for subcategories if conditions for recursion are satisfied:
    if (
        (n_pages_per_level_threshold is None or
            n_pages < n_pages_per_level_threshold) and
        (max_level is None or level < max_level)
    ):
        for cat in subcategories:
            if verbose:
                print("(SUBCATEGORY)", get_info_str(cat, level))
            get_categorymembers(cat,
                                n_pages_per_level_threshold,
                                level+1,
                                max_level=max_level,
                                pages=pages,
                                verbose=verbose)
    elif verbose and len(subcategories) > 0:
        print(f"IGNORING {len(subcategories)} CATEGORIES:")
        for cat in subcategories:
            print(' '*4, cat.title)

    return pages


def get_info_str(page, level):
    return "{0:s}: {1:s} (ns: {2:d})".format('*' * (level + 1),
                                             page.title, page.ns)


def get_page_text(page, keywords=None, verbose=True,
                  use_summary_if_empty=True):
    """
    Returns a list of strings containing the texts of all the sections and
    their subsections (recursively).
    A filter can also be applied on the outermost sections, in order to only
    keep sections with a title containing at least one of the `keywords`.
    """
    page_text = []
    #  if keywords is None:
    #      keywords = ['plot', 'character', 'summary', 'topic', 'theme',
    #                  'summari', 'background', 'origin', 'introduction',
    #                  'concept', 'symbol']
    if verbose:
        print(f"In page '{page.title}':")
    for s in page.sections:
        if keywords is None or filter_by_keywords(s.title, keywords):
            if verbose:
                print(' '*4, f"Using text of section '{s.title}'")
            page_text += get_section_text(s)
        elif verbose:
            print(' '*4, f"Ignoring section '{s.title}'")

    if use_summary_if_empty and len(page_text) == 0:
        page_text.append(page.summary)

    if verbose:
        print()
    return page_text


def filter_by_keywords(text, keywords):
    return bool(re.search('|'.join(keywords), text.lower()))


def get_section_text(section, section_text_list=None):
    """Returns a list of strings containing the texts of the section and all
    its subsections (recursively)"""

    if section_text_list is None:
        section_text_list = []

    if section.text != '':
        section_text_list.append(section.text)
    for s in section.sections:
        get_section_text(s, section_text_list)

    return section_text_list


def prepare_text_for_lda(text, lemmatize=True, pos_tagging=True, min_len=3):
    if type(text) == str:
        tokens = tokenize(text, remove_stopwords=True, min_len=min_len)
    elif hasattr(text, '__iter__'):
        if len(text) == 0:
            return []
        elif type(text[0]) == str:
            tokens = []
            for t in text:
                tokens += tokenize(t, remove_stopwords=True, min_len=min_len)
    else:
        raise TypeError('`text` must be a string or an iterable of string.')

    if pos_tagging:
        tokens = [t for t in tokens
                  if t.pos_ in ['NOUN', 'VERB', 'ADJ', 'ADV']]
    if lemmatize:
        tokens = [t.lemma_.lower() for t in tokens]
    else:
        tokens = [t.text.lower() for t in tokens]
    return tokens


def tokenize(text, remove_stopwords=True, min_len=0):
    tokens = []
    doc = spacy_nlp(text)
    if remove_stopwords:
        tokens = [token for token in doc if
                  (len(token.text) >= min_len and not token.is_stop)]
    else:
        tokens = [token for token in doc if len(token.text) >= min_len]
    return tokens
