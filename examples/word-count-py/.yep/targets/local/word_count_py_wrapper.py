# Wrapper for local target
from word_count import read_file, map_words_to_counts, reduce_word_counts, print_word_counts


def run(vars):
    defaults = {'file_path': 'declaration.txt'}
    vars = {**defaults, **(vars or {})}
    words = read_file(**vars)
    mapped_words = map_words_to_counts(words)
    word_counts = reduce_word_counts(mapped_words)
    return print_word_counts(word_counts)


if __name__ == '__main__':
    print(run({}))
