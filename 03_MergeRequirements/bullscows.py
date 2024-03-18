import collections
import os
import sys
import urllib.request
from random import choice
import cowsay


def bullscows(guess: str, secret: str) -> (int, int):
    if len(guess) != len(secret):
        print('Error: Words have different length')
        return -1
    bulls = 0
    for i in range(len(guess)):
        bulls += guess[i] == secret[i]
    return (bulls, (collections.Counter(guess) & collections.Counter(secret)).total())


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = choice(words)
    guess = ''
    attempts = 0
    while guess != secret:
        guess = ask("Type the word: ", words)
        inform("Bulls: {}, Cows: {}", *bullscows(guess, secret))
        attempts += 1
    return attempts


def ask(prompt: str, valid: list[str] = None) -> str:
    s = input(prompt)
    while valid and s not in valid:
        print(cowsay.cowsay("Incorrect word. Try again...", cow=choice(cowsay.list_cows())))
        s = input(prompt)
    return s


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay.cowsay(format_string.format(bulls, cows), cow=choice(cowsay.list_cows())))


def choose_dictionary(url):
    return urllib.request.urlopen(url).read().decode('utf-8').splitlines()


if len(sys.argv) < 2:
    print("Usage: python -m bullscows <словарь> [длина]")
    sys.exit(1)

d = sys.argv[1]
match d:
    case "Russian-Nouns":
        words = choose_dictionary("https://raw.githubusercontent.com/Harrix/Russian-Nouns/main/dist/russian_nouns.txt")
    case "google-10000-english":
        words = choose_dictionary(
            "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt")
    case "english_words_with_5_letters":
        words = choose_dictionary("https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt")
    case _:
        print("Unsupported or unrecognized dictionary")
        sys.exit(1)

word_length = 5
if len(sys.argv) > 2:
    word_length = int(sys.argv[2])
words = list(filter(lambda x: len(x) == word_length, words))
print(f"Congratulations! You won after {gameplay(ask, inform, words)} attempts.")

