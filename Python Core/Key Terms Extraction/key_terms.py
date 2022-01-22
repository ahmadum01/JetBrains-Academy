import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from lxml import etree
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer


def most_frequent_words(texts_: list, num: 'int number of returning words') -> list:
    """Return list of most frequent by TF-IDF words"""
    list_of_tokens = []
    for i in range(len(texts_)):
        list_of_tokens.append(tokenization(texts_[i]))
        list_of_tokens[i] = lemmatization(list_of_tokens[i])
        list_of_tokens[i] = remove_punctuation(list_of_tokens[i])
        list_of_tokens[i] = remove_stop_words(list_of_tokens[i])
        list_of_tokens[i] = remove_not_noun(list_of_tokens[i])

    tf_idf_dicts = tf_idf(list_of_tokens)

    result = []
    for freq_dict in tf_idf_dicts:  # Sorting
        result_words = []
        for i in range(num):
            max_value = 0
            max_key = ''
            for key in freq_dict:
                if freq_dict[key] > max_value or (freq_dict[key] == max_value and key > max_key):
                    max_key = key
                    max_value = freq_dict[key]
            del freq_dict[max_key]  # delete the max element from dict
            result_words.append(max_key)
        result.append(result_words)
    return result


def tf_idf(tokens: list) -> list[dict]:
    dataset = tokens[:]
    for i in range(len(dataset)):
        dataset[i] = ' '.join(dataset[i])

    vectorizer = TfidfVectorizer(input='content', use_idf=True, lowercase=False,
                                 analyzer='word', ngram_range=(1, 1),
                                 stop_words=None)

    tfidf_matrix = vectorizer.fit_transform(dataset)
    vocabulary = vectorizer.get_feature_names_out()
    result = []
    for i in range(len(dataset)):
        result.append(dict(zip(vocabulary, tfidf_matrix.toarray()[i])))
    return result


def tokenization(text):
    return word_tokenize(text.lower())


def lemmatization(tokens: list) -> list:
    lemmatizer = WordNetLemmatizer()
    result = []
    for token in tokens:
        result.append(lemmatizer.lemmatize(token, pos='n'))
    return result


def remove_punctuation(tokens: list) -> list:
    result = []
    for token in tokens:
        if token not in punctuation:
            result.append(token)
    return result


def remove_not_noun(tokens: list):
    result = []
    for token in tokens:
        if nltk.pos_tag([token])[0][1] == 'NN':
            result.append(token)
    return result


def remove_stop_words(tokens: list) -> list:
    result = []
    for token in tokens:
        if token not in stopwords.words('english') + ['ha', 'wa', 'u', 'a']:
            result.append(token)
    return result


if __name__ == '__main__':
    tree = etree.parse('news.xml')  # reading xml file
    root = tree.getroot()
    heads, texts = [], []
    for block in root[0].iter():
        match block.get("name"):
            case 'head': heads.append(block.text + ':')
            case 'text': texts.append(block.text)
    # And finally print result
    for head, frequent_words in zip(heads, most_frequent_words(texts, 5)):
        print(head)
        print(*frequent_words)