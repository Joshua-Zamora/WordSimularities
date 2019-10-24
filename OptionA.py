# CS2302 DATA STRUCTURES
# Author: Joshua Zamora
# OPTION A (Word Embeddings)
# Instructor: Diego Aguirre
# TA: Gerardo Barraza
# Last Updated 10 / 21 / 2019
# The purpose of this program is to find and store word embeddings
# using tree types such as AVL and Red-Black trees
import re
import os
from gensim.models import KeyedVectors


class Node:
    left = None
    right = None
    key = ""
    item = ""
    height = 0
    parent = None
    color = ""

    def __init__(self, k="", i=""):
        self.key = k
        self.item = i


class AVLTree:
    root = None
    count = 0  # Keeps track of the number of nodes currently in the tree

    def __init__(self, new_node=None):
        self.root = new_node
        if self.root:
            self.count = 1

    @staticmethod
    def update_height(node):
        left_height = -1
        if node.left is not None:
            left_height = node.left.height

        right_height = -1
        if node.right is not None:
            right_height = node.right.height

        node.height = 1 + max(left_height, right_height)

    @staticmethod
    def get_balance(node):
        left_height = -1
        if node.left is not None:
            left_height = node.left.height

        right_height = -1
        if node.right is not None:
            right_height = node.right.height

        return left_height - right_height

    def set_child(self, parent, which_child, child):
        if which_child != "left" and which_child != "right":
            return False

        if which_child == "left":
            parent.left = child
        else:
            parent.right = child
        if child is not None:
            child.parent = parent

        self.update_height(parent)
        return True

    def replace_child(self, parent, current_child, new_child):
        if parent.left is current_child:
            return self.set_child(parent, "left", new_child)

        elif parent.right is current_child:
            return self.set_child(parent, "right", new_child)

        return False

    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent is not None:
            self.replace_child(node.parent, node, node.left)
        else:
            self.root = node.left
            self.root.parent = None

        self.set_child(node.left, "right", node)
        self.set_child(node, "left", left_right_child)

    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent is not None:
            self.replace_child(node.parent, node, node.right)
        else:
            self.root = node.right
            self.root.parent = None

        self.set_child(node.right, "left", node)
        self.set_child(node, "right", right_left_child)

    def re_balance(self, node):
        self.update_height(node)
        if self.get_balance(node) == -2:
            if self.get_balance(node.right) == 1:
                self.rotate_right(node.right)  # double rotation case

            return self.rotate_left(node)

        elif self.get_balance(node) == 2:
            if self.get_balance(node.left) == -1:
                self.rotate_left(node.left)  # double rotation case

            return self.rotate_right(node)

        return node

    def insert(self, node):
        if self.root is None:  # if root is empty assign new node to root
            self.root = node
            self.count = self.count + 1
            node.parent = None
            return

        self.count = self.count + 1
        cur = self.root
        while cur is not None:  # else assign new node as a child
            if node.key < cur.key:  # corresponding to its alphabetic position
                if cur.left is None:
                    cur.left = node
                    node.parent = cur
                    cur = None
                else:
                    cur = cur.left
            else:
                if cur.right is None:
                    cur.right = node
                    node.parent = cur
                    cur = None
                else:
                    cur = cur.right

        node = node.parent
        while node is not None:
            self.re_balance(node)
            node = node.parent


class RedBlackTree:
    root = None
    count = 0  # Keeps track of the number of nodes currently in the tree

    def __init__(self, new_node=None):
        self.root = new_node
        if self.root:
            self.count = 1
            self.root.color = "black"

    @staticmethod
    def update_height(node):
        left_height = -1
        if node.left is not None:
            left_height = node.left.height

        right_height = -1
        if node.right is not None:
            right_height = node.right.height

        node.height = 1 + max(left_height, right_height)

    def set_child(self, parent, which_child, child):
        if which_child != "left" and which_child != "right":
            return False

        if which_child == "left":
            parent.left = child
        else:
            parent.right = child
        if child is not None:
            child.parent = parent

        self.update_height(parent)
        return True

    def replace_child(self, parent, current_child, new_child):
        if parent.left is current_child:
            return self.set_child(parent, "left", new_child)

        elif parent.right is current_child:
            return self.set_child(parent, "right", new_child)

        return False

    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent is not None:
            self.replace_child(node.parent, node, node.left)
        else:
            self.root = node.left
            self.root.parent = None

        self.set_child(node.left, "right", node)
        self.set_child(node, "left", left_right_child)

    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent is not None:
            self.replace_child(node.parent, node, node.right)
        else:
            self.root = node.right
            self.root.parent = None

        self.set_child(node.right, "left", node)
        self.set_child(node, "right", right_left_child)

    def insert(self, node):
        if self.root is None:  # if root is empty assign new node to root
            self.root = node
            self.count = 1
            self.root.color = "black"
            return

        self.count = self.count + 1
        cur = self.root
        while cur is not None:  # else assign new node as a child
            if node.key < cur.key:  # corresponding to its alphabetic position
                if cur.left is None:
                    cur.left = node
                    node.parent = cur
                    cur = None
                else:
                    cur = cur.left
            else:
                if cur.right is None:
                    cur.right = node
                    node.parent = cur
                    cur = None
                else:
                    cur = cur.right

        node.color = "red"
        self.balance(node)
        node = node.parent
        while node is not None:
            self.update_height(node)
            node = node.parent

    @staticmethod
    def get_grandparent(node):
        if node.parent is None:
            return None
        return node.parent.parent

    @staticmethod
    def get_uncle(node):
        grandparent = None
        if node.parent is not None:
            grandparent = node.parent.parent

        if grandparent is None:
            return None

        if grandparent.left is node.parent:
            return grandparent.right
        else:
            return grandparent.left

    def balance(self, node):
        if node.parent is None:
            node.color = "black"
            return

        if node.parent.color == "black":
            return

        parent = node.parent
        grandparent = self.get_grandparent(node)
        uncle = self.get_uncle(node)
        if uncle is not None and uncle.color == "red":
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.balance(grandparent)
            return

        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent

        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent

        parent.color = "black"
        grandparent.color = "red"
        if node is parent.left:
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)


def file_to_avl_tree(filename):
    avl = AVLTree()                                     # creates an empty binary search tree
    file = open(filename, "r", encoding="utf-8")    # opens file and stores it as an object

    with file as f:                             # enables better syntax and exception handling
        line = f.readline().split(None, 1)      # splits after the first word
        while line:                             # checks if file is empty
            if re.compile('[a-zA-Z]').search(line[0][0]) is not None:       # checks if first char is a letter
                avl.insert(Node(line[0], line[1]))            # adds it to bst if so

            line = f.readline().split(None, 1)

    return avl


def file_to_red_black_tree(filename):
    red_black = RedBlackTree()                                    # creates an empty binary search tree
    file = open(filename, "r", encoding="utf-8")    # opens file and stores it as an object

    with file as f:                             # enables better syntax and exception handling
        line = f.readline().split(None, 1)      # splits after the first word
        while line:                             # checks if file is empty
            if re.compile('[a-zA-Z]').search(line[0][0]) is not None:       # checks if first char is a letter
                red_black.insert(Node(line[0], line[1]))            # adds it to bst if so

            line = f.readline().split(None, 1)

    return red_black


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

    text_file.write("%s\n" % node.item)  # writes to given text file

    generate_file_with_tree_content_ascending(text_file, node.left)  # Recursively traverses left sub-tree
    generate_file_with_tree_content_ascending(text_file, node.right)  # Recursively traverses right sub-tree


def generate_file_with_keys_at_depth_d(text_file, d, node):
    if not node:
        return

    if d == 0:
            text_file.write("%s\n" % node.key)  # writes to given text file only at depth d

    generate_file_with_keys_at_depth_d(text_file, d - 1, node.left)  # Recursively traverses left sub-tree
    generate_file_with_keys_at_depth_d(text_file, d - 1, node.right)  # Recursively traverses right sub-tree


def main():
    print('\nEnter the file\'s path: ', end=' ')
    filename = str(input())

    if not os.path.exists(filename):                    # checks if file exists
        print('This file does not exist. Try again.')
        main()
        return

    print('\nAVL or Red/Black tree (Type A or R): ', end=' ')
    answer = str(input())

    while answer.lower() != "a" and answer.lower() != "r":
        print('\nType A or R: ', end=' ')
        answer = str(input())

    print('\nCalculating...')

    if answer.lower() == "a":
        binary_search_tree = file_to_avl_tree(filename)
    else:
        binary_search_tree = file_to_red_black_tree(filename)

    # with open("content_ascending.txt", "a+") as text_file:
    # generate_file_with_tree_content_ascending(text_file, binary_search_tree.root)

    # with open("keys_at_depth.txt", "w+") as text_file_2:
    # generate_file_with_keys_at_depth_d(text_file_2, 4, binary_search_tree.root)

    print('\nThe size of the tree is: ', binary_search_tree.count, ' nodes')
    print('The height of the tree is: ', binary_search_tree.root.height)
    # print(file_to_word_comparison())


main()
