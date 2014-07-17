#! /usr/bin/env python

"""
Spell Check Challenge

This program implements a spell check algorithm based on edit distance.
The Trie is implemented for the dictionary.

Reference:

http://en.wikipedia.org/wiki/Edit_distance
http://en.wikipedia.org/wiki/Trie
http://en.wikipedia.org/wiki/BK-tree


Junchao Yan <yjc801@gmail.com>

"""

import sys
import re
import time
import random


class Trie:

    count = 0

    def __init__(self):
        '''
        Create a Trie

        Variable:

        count: number of words in the dictionary.
        word: a variable that stores the whole word at the leaf
        children: the descendants of the node

        '''

        self.word = None
        self.children = {}

    def insert(self, word):
        for letter in word:
            if letter not in self.children:
                self.children[letter] = Trie()
            self = self.children[letter]
        self.word = word
        Trie.count += 1

    def has_word(self, word):
        for letter in word:
            if letter not in self.children:
                return False
            self = self.children[letter]
        return True

    def generate_word(self):
        while self.children:
            letters = self.children.keys()
            k = random.randint(0, len(letters)-1)
            self = self.children[letters[k]]
        return self.word


class SpellCheck:

    trie = Trie()

    def check(self, word):
        '''
        check spelling for the input word

        '''

        trie = SpellCheck.trie
        word = word.lower().strip()

        if trie.has_word(word):
            return (word, '')

        # remove repeated letters
        # word = re.sub(r'(.)\1+', r'\1\1', word)
        word = re.sub(r'([^aeiou])\1+', r'\1', word)
        word = re.sub(r'([aeiou])\1+', r'\1\1', word)

        # maximum edit distance for the word
        dist = len(re.findall('[aeiou]', word))

        n, res = len(word), []
        row = range(n+1)

        for letter in trie.children:
            self._helper(trie.children[letter], letter, word, row, res, dist)

        temp = []

        # find the words that has smallest edit distance with the input
        min_dist = min(res, key = lambda x: x[1])[1] if res else float('inf')

        for w, dist in res:
            if dist <= min_dist:
                temp.append(w)
                min_dist = dist

        output = 'NO SUGGESTION'

        if temp:
            output = temp[-1]
            temp.pop()
            # if more than one candidates, then choose the one that has same first letter
            if len(temp) >= 1:
                for w in temp:
                    if w[0] == word[0]:
                        output = w
                        temp.remove(w)
                        break

        return (output, ', '.join(temp))

    def _helper(self, trie, letter, word, prev, res, dist):
        '''
        Computes edit distance recursively

        '''

        n, curr = len(word), [prev[0]+1]

        for i in xrange(1, n+1):
            if word[i-1] == letter:
                k = prev[i-1]
            else:
                # minimum cost of insertion, deletion, and substitude
                k = min(min(curr[i-1], prev[i]), prev[i-1])+1
            curr += [k]

        if curr[-1] <= dist and trie.word:
            res += [(trie.word, curr[-1])]

        if min(curr) <= dist:
            for letter in trie.children:
                self._helper(trie.children[letter], letter,
                             word, curr, res, dist)


def generate_mistake(word):
    '''
    generates words with spelling mistakes in form of repeated letters,
    case errors, and incorrect vowels.

    '''

    return _repeated(_upper(_vowel(word)))


def _repeated(word):
    w = []
    for letter in word:
        w += [random.randint(1, 3)*letter]
    return ''.join(w)


def _upper(word):
    w = []
    for letter in word:
        w += [letter if random.randint(0, 1) else letter.upper()]
    return ''.join(w)


def _vowel(word):
    w = []
    vowel = ['a', 'e', 'i', 'o', 'u']
    for letter in word:
        if letter in vowel:
            w += vowel[random.randint(0, 4)]
        else:
            w += [letter]
    return ''.join(w)


def main():
    '''
    main program
    
    '''

    path = '/usr/share/dict/words'
    checker = SpellCheck()

    # Load the dictionary
    try:
        f = open(path, 'r')
    except IOError:
        sys.stdout.write('Cannot find the dictionary at \'/usr/share/dict/words\'. Please check the path.\n')
        return

    start = time.time()

    for word in f:
        if word.strip().isalpha():
            checker.trie.insert(word.strip().lower())

    end = time.time()

    sys.stdout.write('Loaded %d words in %g seconds.\n' % (checker.trie.count, end-start))
    
    random_test(checker)
    
    while 1:
        word = raw_input('>')
        if not word:
            continue

        output, suggestions = checker.check(word)
        sys.stdout.write('Suggest: %s\n' % output)
        if suggestions:
            sys.stdout.write('Other suggestions: %s\n' % suggestions)


def random_test(checker):

    word = checker.trie.generate_word()

    if not word:
    	return

    sys.stdout.write('\n\nRandom Test\n\nGenerated word: %s\n\n' % word)
    
    r = _repeated(word)
    u = _upper(word)
    v = _vowel(word)
    m  = generate_mistake(word)
    
    sys.stdout.write('Corrected: %s -> %s\n' % (word, checker.check(word)[0]))
    sys.stdout.write('Repeated letter: %s -> %s\n' % (r, checker.check(r)[0]))
    sys.stdout.write('Case error: %s -> %s\n' % (u, checker.check(u)[0]))
    sys.stdout.write('Incorrect vowel: %s -> %s\n' % (v, checker.check(v)[0]))
    sys.stdout.write('Mix errors: %s -> %s\n\n' % (m, checker.check(m)[0]))


if __name__ == '__main__':
    main()
