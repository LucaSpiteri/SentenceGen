import numpy as np
from collections import defaultdict
import pickle
from tqdm import tqdm
from datasets import load_dataset

ds = load_dataset("community-datasets/generics_kb", "generics_kb_best")

# Extract words from the dataset and store them in the array words
words = []
for example in tqdm(ds['train'], ascii=True):
    words.extend(example['generic_sentence'].split())

transition_counts = defaultdict(lambda: defaultdict(int))

# Count the transitions between words
for i in tqdm(range(len(words) - 1), ascii=True):
    current_word = words[i]
    next_word = words[i + 1]
    transition_counts[current_word][next_word] += 1

# Convert counts to probabilities
transition_probabilities = defaultdict(dict)
for current_word, next_words in tqdm(transition_counts.items(), ascii=True):
    total_count = sum(next_words.values())
    for next_word, count in next_words.items():
        transition_probabilities[current_word][next_word] = count / total_count

# Check that the total transition probabilities add up to 1
for current_word, next_words in tqdm(transition_probabilities.items(), ascii=True):
    total_probability = sum(next_words.values())
    assert np.isclose(total_probability, 1.0), f"Probabilities for '{current_word}' do not add up to 1: {total_probability}"

with open('sentencemodel.pickle', 'wb') as handle:
    pickle.dump(transition_probabilities, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("Model saved to sentencemodel.pickle")