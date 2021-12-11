import random

with open('corpus.txt', 'r', encoding='utf-8') as f:    # Reading of corpus
    tokens = f.read().split()   # tokenization
    bigrams = []    # bigrams list. It isn't using now in this program
    for i in range(len(tokens) - 1):    # Creating of bigrams list
        bigrams.append((tokens[i], tokens[i + 1]))

    trigrams = []   # trigrams list
    for i in range(len(tokens) - 2):    # Creating trigrams list
        trigrams.append((tokens[i] + ' ' + tokens[i + 1], tokens[i + 2]))

    markov_chain = dict()   # Markov's chain
    for i, j in trigrams:   # Creating Markov's chain
        markov_chain.setdefault(i, dict()).setdefault(j, 0)
        markov_chain[i][j] += 1

    # List with heads, which can be chosen like first pair of word in our text
    first_heads = list(filter(lambda w: w.split()[0][-1] not in '.!?' and w.istitle() and w[0].isalpha(),
                              list(markov_chain.keys())))
    # Generation of pseudo-text
    for i in range(10):
        selected_head_word = random.choice(first_heads)
        markov_chain_keys = list(markov_chain[selected_head_word].keys())
        markov_chain_values = list(markov_chain[selected_head_word].values())
        selected_tail_word = random.choices(markov_chain_keys, markov_chain_values)[0]
        print(selected_head_word, selected_tail_word, end=' ')
        counter = 3
        while True:
            selected_head_word = selected_head_word.split()[1] + ' ' + selected_tail_word
            markov_chain_keys = list(markov_chain[selected_head_word].keys())
            markov_chain_values = list(markov_chain[selected_head_word].values())
            selected_tail_word = random.choices(markov_chain_keys, markov_chain_values)[0]
            print(selected_tail_word, end=' ')
            counter += 1
            if selected_tail_word[-1] in '.!?' and counter >= 5:
                break
        print()