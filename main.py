FAIL = -1

def aho_corasick(string, keywords):
    transitions = {}
    outputs = {}
    fails = {}

    new_state = 0

    for keyword in keywords:
        state = 0

        for j, char in enumerate(keyword):
            res = transitions.get((state, char), FAIL)
            if res == FAIL:
                break
            state = res

        for char in keyword[j:]:
            new_state += 1
            transitions[(state, char)] = new_state
            state = new_state

        outputs[state] = [keyword]

    queue = []
    for (from_state, char), to_state in transitions.items():
        if from_state == 0 and to_state != 0:
            queue.append(to_state)
            fails[to_state] = 0

    while queue:
        r = queue.pop(0)
        for (from_state, char), to_state in transitions.items():
            if from_state == r:
                queue.append(to_state)
                state = fails[from_state]

                while True:
                    res = transitions.get((state, char), state and FAIL)
                    if res != FAIL:
                        break
                    state = fails[state]

                failure = transitions.get((state, char), state and FAIL)
                fails[to_state] = failure
                outputs.setdefault(to_state, []).extend(
                    outputs.get(failure, []))

    state = 0
    results = []
    for i, char in enumerate(string):
        while True:
            res = transitions.get((state, char), state and FAIL)
            if res != FAIL:
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
    "good", # prio 2 / IMMEDIATELY
    "condition", # prio 2 / IMMEDIATELY
    "price is", # prio 1 / CALL BASE
    "." # new sentence
]

print(aho_corasick(input_string, key_map))
