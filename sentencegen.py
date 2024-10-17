import random
import pickle

# Opens the pickle file and saves the transition probabilities to the dictionary transition_probabilities
with open('sentencemodel.pickle', 'rb') as handle:
    transition_probabilities = pickle.load(handle)

# Function to predict the next word given the current word
def predict_next_word(current_word):
    if current_word in transition_probabilities:
        next_words = transition_probabilities[current_word]
        words = list(next_words.keys())
        probabilities = list(next_words.values())
        return random.choices(words, probabilities)[0]
    else:
        return None

# Function to generate a sentence given a starting word
def generate_sentence(start_word):
    sentence = start_word
    current_word = start_word
    while True:
        next_word = predict_next_word(current_word)
        if next_word is None:
            break
        sentence += ' ' + next_word
        if next_word.endswith('.'):
            break
        current_word = next_word
    return sentence


# Loop to generate sentences based on user input
while True:
    firstword = input("Enter the first word (or type ././ to exit): ")
    if firstword == '././':
        break
    print(generate_sentence(firstword))