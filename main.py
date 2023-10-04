# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Automate:
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    def is_deterministic(self):
        for state in self.states:
            transitions = [transition for transition in self.transitions if transition[0] == state]
            for symbol in self.alphabet:
                symbols = [transition for transition in transitions if transition[1] == symbol]
                if len(symbols) > 1 or self.has_epsilon_transitions() :
                    return False
        return True

    def has_epsilon_transitions(self):
        for transition in self.transitions:
            if transition[1] == '':
                return True
        return False

    def determinize(self):
        # Initializing the new deterministic automaton
        alphabet = self.alphabet
        states = {frozenset({self.initial_state})}
        transitions = []
        initial_state = frozenset({self.initial_state})
        final_states = set()
        unmarked_states = [initial_state]

        # Main loop of the determinization algorithm
        while unmarked_states:
            current_states = unmarked_states.pop(0)
            for symbol in alphabet:
                next_states = set()
                for state in current_states:
                    for transition in self.transitions:
                        if transition[0] == state and transition[1] == symbol:
                            next_states.add(transition[2])
                if next_states:
                    next_state = frozenset(next_states)
                    if next_state not in states:
                        states.add(next_state)
                        unmarked_states.append(next_state)
                    transitions.append((current_states, symbol, next_state))
            if current_states.intersection(self.final_states):
                final_states.add(current_states)

        # Creating and returning the new deterministic automaton
        new_alphabet = alphabet
        new_states = states
        new_initial_state = initial_state
        new_final_states = final_states
        new_transitions = transitions

        return Automate(new_alphabet, new_states, new_initial_state, new_final_states, new_transitions)

    def display(self):
        print(f"Alphabet: {self.alphabet}")
        states = str(self.states)
        states = states.replace("frozenset(", "").replace(")", "")
        print(f"States: {states}")
        initial_state = str(self.initial_state)
        initial_state = initial_state.replace("frozenset(", "").replace(")", "")
        print(f"Initial state: {initial_state}")
        final_states = str(self.final_states)
        final_states = final_states.replace("frozenset(", "").replace(")", "")
        print(f"Final states: {final_states}")
        print("Transitions:")
        for transition in self.transitions:
            source = str(transition[0])
            source = source.replace("frozenset(", "").replace(")", "")
            dest = str(transition[2])
            dest = dest.replace("frozenset(", "").replace(")", "")
            symbol = transition[1] if transition[1] != '' else 'ε'
            print(f"    {source} --({symbol})--> {dest}")

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for transition in self.transitions:
                if transition[0] == state and transition[1] == '':
                    next_state = transition[2]
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return frozenset(closure)

    def determinize_with_epsilon(self):
        # Compute epsilon closure of initial state
        initial_state = self.epsilon_closure([self.initial_state])

        # Initializing the new deterministic automaton
        alphabet = self.alphabet
        states = set([initial_state])  # Add initial state to set of states
        transitions = []
        final_states = set()
        unmarked_states = [initial_state]

        # Main loop of the determinization algorithm
        while unmarked_states:
            current_states = unmarked_states.pop(0)
            for symbol in alphabet:
                next_states = set()
                for state in current_states:
                    for transition in self.transitions:
                        if transition[0] == state and transition[1] == symbol:
                            next_states.add(transition[2])
                if next_states:
                    next_state = self.epsilon_closure(next_states)
                    if next_state not in states:
                        states.add(next_state)
                        unmarked_states.append(next_state)
                    transitions.append((current_states, symbol, next_state))
            if current_states.intersection(self.final_states):
                final_states.add(current_states)

        # Create new deterministic automaton object
        new_automaton = Automate(alphabet=list(alphabet), states=list(states),
                                 initial_state=initial_state, final_states=list(final_states),
                                 transitions=transitions)
        return new_automaton

    def accepts_string(d_automaton, input_string):
        current_state = d_automaton.initial_state
        for symbol in input_string:
            next_state = None
            for transition in d_automaton.transitions:
                if transition[0] == current_state and transition[1] == symbol:
                    next_state = transition[2]
                    break
            if next_state is None:
                return False
            current_state = next_state
        return current_state in d_automaton.final_states


if __name__ == '__main__':
    d_automate=None
    # Example given
    alphabet = ['a', 'b', 'c']
    states = ['q1', 'q2', 'q3', 'q4']
    initial_state = 'q1'
    final_states = ['q2', 'q4']
    transitions = [('q1', 'a', 'q2'),
                   ('q2', 'a', 'q2'),
                   ('q2', 'b', 'q3'),
                   ('q3', 'c', 'q4'),
                   ('q4', 'a', 'q2')]
    input_string = 'aaaaaaaaaaaaaaaaabc'

    # exemple non deterministic without epsilon transition
    alphabet = ['a', 'b']
    states = ['q1', 'q2', 'q3', 'q4']
    initial_state = 'q1'
    final_states = ['q3', 'q4']
    transitions = [('q1', 'a', 'q2'),
                   ('q1', 'a', 'q3'),
                   ('q2', 'b', 'q4')]
    input_string = 'a'

    # exemple non deterministic with epsilon transition
    alphabet = ['a', 'b']
    states = ['q0','q1', 'q2', 'q3', 'q4']
    initial_state = 'q0'
    final_states = ['q4']
    transitions = [('q0', 'a', 'q1'),
                   ('q1', '', 'q2'),
                   ('q1', '', 'q4'),
                   ('q2', 'b', 'q3'),
                   ('q3', 'a', 'q2'),
                   ('q3', '', 'q4')]
    input_string = 'abababababab'

    # exemple non deterministic without epsilon transition
    alphabet = ['a', 'b']
    states = ['q1', 'q2', 'q3', 'q4']
    initial_state = 'q1'
    final_states = ['q3', 'q4']
    transitions = [('q1', 'a', 'q2'),
                   ('q1', 'a', 'q3'),
                   ('q2', 'b', 'q4')]
    input_string = 'ab'

    automate = Automate(alphabet, states, initial_state, final_states, transitions)
    #Display the input Automate
    print("afficher l'automate entrée")
    automate.display()
    if automate.is_deterministic():
        print("L'automate est déterministe.")
    else:
        print("L'automate n'est pas déterministe.")
        # determinize the automaton
        if automate.has_epsilon_transitions()==False:
            print("L'automate n'utilise pas d'epsilon-transitions.")
            d_automate = automate.determinize()
            print("Nouvelle automate déterministe:")
            # print the information of the new deterministic automaton
            d_automate.display()
        else:
            print("L'automate utilise des epsilon-transitions.")
            d_automate = automate.determinize_with_epsilon()
            print("Nouvelle automate déterministe:")
            # print the information of the new deterministic automaton
            d_automate.display()

    if d_automate!=None:
        automate = d_automate
    if automate.accepts_string(input_string):
        print(f"The automaton accepts the input string '{input_string}'")
    else:
        print(f"The automaton does not accept the input string '{input_string}'")




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
