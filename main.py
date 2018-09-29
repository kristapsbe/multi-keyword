import re
import copy

def aho_corasick(string, key_map):
    """
    An implementation of the Aho-Corasick algorithm
    https://cr.yp.to/bib/1975/aho.pdf.

    string      - the string to be searched
    key_map     - a dictionary of rules (used to map keywords to messages)

    return      - a list of decoded messages
    """
    # using this as the list of possible keywords
    keywords = list(sum(key_map, ()))
    # flag for determining that we've hit a state/character
    # combo we haven't seen before
    fail_state = -1
    # a dict for the pattern matchin machine to live in
    # states and state transitions
    transitions = {}
    # the outputs for each of the terminal nodes
    outputs = {}
    #
    fails = {}
    # Algorithm 2.
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
    # Algorithm 3.
    #
    # pre-populate the queue and failure state dictionary
    # so that we can start off by looking at all of the initial
    # letters and can keep track of the states we're supposed to fail to
    queue = []
    for (from_state, char), to_state in transitions.items():
        if from_state == 0 and to_state != 0:
            # only add states that start from the entry state and lead
            # to a non-entry state
            queue.append(to_state)
            fails[to_state] = 0
    while queue:
        # work through the queue till there are no states left to process
        r = queue.pop(0)
        for (from_state, char), to_state in transitions.items():
            if from_state == r:
                # so domething only if the current state matches the from state
                # of the transition
                #
                # add the next state to the end of the queue
                queue.append(to_state)
                state = fails[from_state]
                while True:
                    res = transitions.get((state, char), state and fail_state)
                    if res != fail_state:
                        break
                    state = fails[state]
                failure = transitions.get((state, char), state and fail_state)
                fails[to_state] = failure
                outputs.setdefault(to_state, []).extend(outputs.get(failure, []))
    # setting up vars for the temp mapping
    temp_map = copy.deepcopy(key_map)
    max_prio = -1
    max_message = ""
    max_key = ()
    # Algorithm 1.
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
            # need to avoid having to re-loop the mapping
            matched_keys = [x for x in key_map.keys() if match in x]
            for key in matched_keys:
                if temp_map[key]["prio"] > max_prio:
                    temp_map[key]["rule"] = [x for x in temp_map[key]["rule"] if x != match]
                    if not temp_map[key]["rule"]:
                        max_prio = temp_map[key]["prio"]
                        max_message = temp_map[key]["message"]
                        max_key = key
                elif temp_map[key]["prio"] == -1:
                    if max_prio > -1:
                        results.append((max_key, max_message))
                    temp_map = copy.deepcopy(key_map)
                    max_prio = -1
            pos = i - len(match) + 1
            #results.append((pos, match))
    return results
# preprocessing the string a little bit - we don't really care about the case
# of the letters and the specific numbers (just the fact that nums are present)
input_string = "New item for sale. My old bicycle. It is in very good condition. Selling my old radio. Price is 700€. Condition is good."
input_string = re.sub(r'[0-9]', '0', input_string.lower())
print(input_string)
# the rules that map keywords (or phrases) to secret messages
key_map = {
    ("for sale",): {"prio": 1, "rule": ["for sale"], "message": "URGENT"},
    ("bicycle",): {"prio": 4, "rule": ["bicycle"], "message": "ATTACK"},
    ("good", "condition"): {"prio": 2, "rule": ["good", "condition"], "message": "IMMEDIATELY"},
    ("price is 0",): {"prio": 1, "rule": ["price is 0"], "message": "CALL BASE"},
    (".",): {"prio": -1}, # new sentence
}
print(aho_corasick(input_string, key_map))
