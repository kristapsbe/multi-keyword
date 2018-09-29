# Multi keyword search

Contains an implementation of the Aho-Corasick algorithm in Python
(https://cr.yp.to/bib/1975/aho.pdf), the complexity of the algorithm is O(n + k + z), where n is the length of the input text, k is the total number of characters of all the words in the dictionary and z is total number of occurrences of words in text.

The code is based on https://gist.github.com/atdt/875e0dba6a15e3fa6018.

## Functions

https://www.geeksforgeeks.org/aho-corasick-algorithm-pattern-searching/

### Go To :
```   
This function simply follows edges
of Trie of all words in arr[]. It is
represented as 2D array g[][] where
we store next state for current state
and character.
```

### Failure :
```
This function stores all edges that are
followed when current character doesn't
have edge in Trie.  It is represented as
1D array f[] where we store next state for
current state.
```

### Output :
```
Stores indexes of all words that end at
current state. It is represented as 1D
array o[] where we store indexes
of all matching words as a bitmap for
current state.
```
