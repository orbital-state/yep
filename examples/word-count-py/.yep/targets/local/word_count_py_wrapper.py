# Wrapper for local target
from word_count import read_file, map_words_to_counts, reduce_word_counts


def run(vars):
    words = read_file(**vars)
    mapped_words = map_words_to_counts(words)
    return reduce_word_counts(mapped_words)


if __name__ == '__main__':
    print(run({}))
