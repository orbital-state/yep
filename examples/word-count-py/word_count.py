# word_count.py
import re
import typer
from functools import reduce


def read_file(file_path):
    """Read file and return list of words."""
    with open(file_path, 'r') as file:
        text = file.read()
        # Remove punctuation and convert to lower case
        text = re.sub(r'[^\w\s]', '', text).lower()
        return text.split()


def map_words_to_counts(words):
    """Map words to counts."""
    return [(word, 1) for word in words]


def reduce_word_counts(mapped_words):
    """Reduce mapped words to word counts (producing a histogram dict)."""
    def reducer(acc, pair):
        word, count = pair
        if word in acc:
            acc[word] += count
        else:
            acc[word] = count
        return acc
    # Here we want to apply ReduceByKey strategy, which is a common pattern in MapReduce
    # but for now is replaced by a simple reduce function.
    return reduce(reducer, mapped_words, {})


def main(file_path: str = 'declaration.txt'):
    """Logic of this main function should be auto-generated for local target by yep"""
    words = read_file(file_path)
    mapped_words = map_words_to_counts(words)
    word_counts = reduce_word_counts(mapped_words)
    
    for word, count in word_counts.items():
        print(f"{word}: {count}")


if __name__ == "__main__":
    typer.run(main)
