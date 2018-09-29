def aho_corasick(string, keywords):
    """
    An implementation of the Aho-Corasick algorithm (https://cr.yp.to/bib/1975/aho.pdf).

    string      - the string to be searched
    keywords    - a list of keywords to search for

    return      - a list of tuples containing the position and keyword of the match
    """
    # flag for determining that we've hit a state/character combo we haven't seen before
    fail_state = -1

    # a dict for the pattern matchin machine to live in
    # states and state transitions
    transitions = {}
    # the outputs for each of the terminal nodes
    outputs = {}
    #
    fails = {}

    # Algorithm 1.
    #
    # construct the finite state pattern matching machine
    # construction of the machine takes time proportional
    # to the sum of the lengths of the keywords
    #
    # keep track of the last state we've added
    new_state = 0
    for keyword in keywords:
        # each keyword starts traversing the machine from the same entry point
        from_state = 0
        for i, char in enumerate(keyword):
            # we have to work out how far can we reuse the trie
            # that's already been constructed (have we seen words/sentences
            # that start with the same characters?)
            next_state = transitions.get((from_state, char), fail_state)
            if next_state == fail_state:
                # haven't seen this sequence before -> start from this state
                break
            # we've seen this character at this state before -> keep looking
            from_state = next_state

        for char in keyword[i:]:
            # loop through the keyword starting from the first character we
            # haven't seen before and add the rest of the keyword
            # to the pattern matching machine
            new_state += 1
            transitions[(from_state, char)] = new_state
            from_state = new_state

        # finish off by noting which state is supposed to return
        # the current keyword
        outputs[from_state] = [keyword]

    # ?
    queue = []
    for (from_state, char), to_state in transitions.items():
        if from_state == 0 and to_state != 0:
            queue.append(to_state)
            fails[to_state] = 0

    print(queue)

    while queue:
        r = queue.pop(0)
        for (from_state, char), to_state in transitions.items():
            if from_state == r:
                queue.append(to_state)
                state = fails[from_state]

                while True:
                    res = transitions.get((state, char), state and fail_state)
                    if res != fail_state:
                        break
                    state = fails[state]

                failure = transitions.get((state, char), state and fail_state)
                fails[to_state] = failure
                outputs.setdefault(to_state, []).extend(
                    outputs.get(failure, []))

    state = 0
    results = []
    # work our way through the string
    for i, char in enumerate(string):
        while True:
            res = transitions.get((state, char), state and fail_state)
            if res != fail_state:
                state = res
                break
            state = fails[state]

        for match in outputs.get(state, ()):
            pos = i - len(match) + 1
            results.append((pos, match))

    return results

input_string = "New item for sale. My old bicycle. It is in very good condition. Selling my old radio. Price is 700€. Condition is good."

key_map = [
    "for sale", # prio 1 / URGENT
    "bicycle", # prio 4 / ATTACK
    "bike", # dummy
    "good", # prio 2 / IMMEDIATELY
    "condition", # prio 2 / IMMEDIATELY
    "price is", # prio 1 / CALL BASE
    "." # new sentence
]

print(aho_corasick(input_string, key_map))
