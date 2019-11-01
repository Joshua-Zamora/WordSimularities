import re
import os
from time import perf_counter
from BTree import BTree
from gensim.models import KeyedVectors


def file_to_b_tree(filename):
    b_tree = BTree(3)  # creates an empty binary search tree
    file = open(filename, "r", encoding="utf-8")  # opens file and stores it as an object

    with file as f:  # enables better syntax and exception handling
        line = f.readline().split(None, 1)  # splits after the first word
        while line:  # checks if file is empty
            if re.compile('[a-zA-Z]').search(line[0][0]) is not None:  # checks if first char is a letter
                b_tree.insert(line)  # adds it to bst if so

            line = f.readline().split(None, 1)

    return b_tree


def file_to_word_comparison():
    # load the Stanford GloVe model
    filename = 'glove.6B.100d.txt.word2vec'
    model = KeyedVectors.load_word2vec_format(filename, binary=False)

    with open('two_words.txt', "r") as f:  # enables better syntax and exception handling
        line = f.readline().split()  # splits after empty space
        while line:  # checks if file is empty
            print(line[0] + " " + line[1] + " " + str(model.similarity(line[0], str(line[1].replace("\n", "")))))
            line = f.readline().split()


def generate_file_with_tree_content_ascending(text_file, node):
    if not node:
        return

    if len(node.children) != 0:
        for child in node.children:
            generate_file_with_tree_content_ascending(text_file, child)

    for key in node.keys:
        text_file.write("%s\n" % key[0])  # writes to given text file


def generate_file_with_keys_at_depth_d(text_file, d, node):
    if not node:
        return

    if d == 0:
        for key in node.keys:
            text_file.write("%s\n" % key[0])  # writes to given text file
        return

    if len(node.children) == 0:
        return

    for child in node.children:
        generate_file_with_keys_at_depth_d(text_file, d - 1, child)


def main():
    print('\nEnter the file\'s path: ', end=' ')
    filename = str(input())

    if not os.path.exists(filename):  # checks if file exists
        print('This file does not exist. Try again.')
        main()
        return

    print('\nCalculating...')

    start = perf_counter()  # timer
    b_tree = file_to_b_tree(filename)
    stop = perf_counter()

    # with open("content_ascending.txt", "w+", encoding="utf-8") as text_file:
    # generate_file_with_tree_content_ascending(text_file, b_tree.root)

    # with open("keys_at_depth.txt", "w+", encoding="utf-8") as text_file_2:
    # generate_file_with_keys_at_depth_d(text_file_2, 0, b_tree.root)

    print('\nTree of degree: ', b_tree.root.max_num_keys)
    print('The size of the tree is: ', b_tree.num_nodes(b_tree.root), ' nodes')
    print('There are: ', b_tree.count, ' keys')
    print('The height of the tree is: ', b_tree.height())
    print('Time elapsed for inserting: ', round(stop - start, 2), ' seconds')


if __name__ == "__main__":

    main()
