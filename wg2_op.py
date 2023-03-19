import random
import nltk
from collections import Counter
from tqdm import tqdm

try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

word_list = nltk.corpus.words.words()
five_letter_words = [word.lower() for word in word_list if len(word) == 5]

def eliminate_words(guess, feedback, words):
    remaining_words = []
    for word in words:
        correct_letters = sum([1 for i in range(5) if guess[i] == word[i]])
        total_letters = sum([min(guess.count(l), word.count(l)) for l in 'abcdefghijklmnopqrstuvwxyz'])
        if correct_letters == feedback[0] and total_letters == sum(feedback):
            remaining_words.append(word)
    return remaining_words

def calculate_information_gain(guess, remaining_words):
    remaining_counts = Counter(remaining_words)
    feedback_counts = Counter()
    for word in remaining_words:
        correct_letters = sum([1 for i in range(5) if guess[i] == word[i]])
        total_letters = sum([min(guess.count(l), word.count(l)) for l in 'abcdefghijklmnopqrstuvwxyz'])
        feedback_counts[(correct_letters, total_letters-correct_letters)] += remaining_counts[word]
    information_gain = sum([remaining_counts[word] * sum([(feedback_counts[feedback] / sum(feedback_counts.values()))**2 for feedback in set(feedback_counts)]) for word in remaining_words])
    return information_gain

remaining_words = five_letter_words.copy()
guess = random.choice(five_letter_words)
print(f"Guessing word: {guess}")
while True:
    feedback = input("Enter feedback (e.g., '2 1'): ").split()
    if feedback[0].lower() == 'n':
        remaining_words = five_letter_words.copy()
        guess = random.choice(five_letter_words)
        print(f"New word: {guess}")
        continue
    feedback = [int(x) for x in feedback]
    remaining_words = eliminate_words(guess, feedback, remaining_words)
    if len(remaining_words) == 1:
        print(f"The word is {remaining_words[0]}!")
        break
    guess_info_gain = []
    with tqdm(total=len(remaining_words), desc="Calculating information gain") as pbar:
        for word in remaining_words:
            guess_info_gain.append((word, calculate_information_gain(word, remaining_words)))
            pbar.update(1)
    guess = min(guess_info_gain, key=lambda x: x[1])[0]
    print(f"Guessing word: {guess}")

# Enter feedback (e.g., '2 1') // 'fst snd' - fst = nr green tiles, snd = nr yellow tiles