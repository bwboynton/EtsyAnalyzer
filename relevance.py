from collections import defaultdict
from typing import (
    Dict,
    List,
)

import numpy as np
from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfTransformer,
)

from downloader import ShopListing


class Relevance:

    STOP_WORDS_LANG = 'english'

    def __init__(self, shop2listings: Dict[str, List[ShopListing]]) -> None:
        # Concatenate all listing titles and descriptions for each shop to form one long string.
        self._corpus = {shop_id: ' '.join(f'{listing.title} {listing.description}' for listing in listings)
                        for shop_id, listings in shop2listings.items()}

    def compute_relevant_words(self, num_words: int) -> Dict[str, List[str]]:
        '''Returns `num_words` most relevant words for each shop.'''
        # Create a feature for each word in the corpus. Ignore stop words ("the", "a", etc.) and accents.
        vectorizer = CountVectorizer(
            stop_words=self.STOP_WORDS_LANG,
            strip_accents='unicode',
        )
        # Note that "keys()" and "values()" are guaranteed to be in the same order.
        vectors = vectorizer.fit_transform(self._corpus.values())

        # Apply TF-IDF transform to the words counts. This scales down the impack of words that occur frequently
        # throughout the entire corpus.
        #   https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html
        #   https://en.wikipedia.org/wiki/Tf–idf
        transformer = TfidfTransformer()
        vectors_tf_idf = transformer.fit_transform(vectors).todense()

        # Sort each feature vector by decreasing TF-IDF score.
        vectors_tf_idf_argsort = np.flip(np.argsort(
            a=vectors_tf_idf,
            axis=1,
            kind='stable',  # Default is 'quicksort' which is not stable.
        ), axis=1)

        # Compute the mapping from feature index to the corresponding word.
        idx2word = {idx: word for word, idx in vectorizer.vocabulary_.items()}

        # Select the most relevant words (ones with the highest TF-IDF score) for each shop.
        shop2words = defaultdict(list)
        for i, shop_id in enumerate(self._corpus.keys()):
            for j in range(num_words):
                word = idx2word[vectors_tf_idf_argsort[i, j]]
                shop2words[shop_id].append(word)
        return shop2words
