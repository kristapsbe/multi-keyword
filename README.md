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

## Further reading / Alternative approaches

* Commentz-Walter: Any Better than Aho-Corasick for Peptide Identification? https://pdfs.semanticscholar.org/6ee4/c69e14c1c9997c741780180557815a4e78d0.pdf
* Analysis of Multiple String Pattern Matching Algorithms http://elvedit.com/journals/IJACSIT/wp-content/uploads/2014/09/IJACSIT-3402-AoMSPMA.pdf
* String Matching Methodologies: A Comparative Analysis https://pdfs.semanticscholar.org/5ed4/52b42f81b6efb9e68b8428c5e992b4d4d143.pdf
* Towards optimal packed string matching http://www.cs.haifa.ac.il/~oren/Publications/bpsm.pdf
* The Exact String Matching Problem: A Comprehensive Experimental Evaluation https://arxiv.org/pdf/1012.2547.pdf
* Simple Real-Time Constant-Space String Matching https://pdfs.semanticscholar.org/e880/29ee3f1b881ad1d0fcdff97bfe6eebc1b645.pdf
