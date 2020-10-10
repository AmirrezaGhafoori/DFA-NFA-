'''
Converting NFa to DFA, implemented by Amirreza Ghafoori


notice: use "λ" character for "landa" in nontations

'''

import collections

filename = "NFA_Input_22.txt"
target_filename= "DFA_Output_22.txt"

#first we define class for nfa to extract the features from the file

class nfa:

    def __init__(self, filename):
        f = open(filename)

        #by using split lines method we will ignore line breaks '\n'
        machine_features = f.read().splitlines()  
        f.close()
        #first we put featuers in machine_feature array and then assign them
        #to the machine features!!
        
        self.alphabet = machine_features[0].split(" ")
        self.state = machine_features[1].split(" ")
        self.initial_state = machine_features[2].split(" ")[0]
        self.final_state = machine_features[3].split(" ")
        self.function = machine_features[4:]

        #We will save each state's landa closure in this dictionary
        self.landa_closure_dict = {}

        #In this dictionary we save which states are reachable through each state and character
        self.all_reachable_states_dict = {}
        #we use this list to handle landa_closure recursive function
        self.visited = []
        
        #We will initiate the acceptor with this function; after this landa_closure_dict
        #will be filled up
        self.landa_closure()

        #This method will initiate all reachalbe states through all alphabet whithin each state
        self.all_reachable_states()

    #This method will find landa closure of all the states
    def landa_closure(self):

        for x in self.state:
            landa_list = []
            self.recursive_landa_closure(x, landa_list)
            self.visited = []
            self.landa_closure_dict[x] = landa_list

    def all_reachable_states(self):
        for state in self.state:

            state_through_char_list = {}
            for char in self.alphabet:
                state_through_char_list[char] = self.reachable_states(state, char)

            self.all_reachable_states_dict[state] = state_through_char_list

    #this method will check which states are reachable through this given state and character
    def reachable_states(self,state, character):

        reachable_list = []
        state_landa_closure_list = self.landa_closure_dict[state]
        for x in state_landa_closure_list:
            x_character = self.directly_reachable_states(x, character)
            for element in x_character:
                element_land = self.landa_closure_dict[element]
                for y in element_land:
                    if y not in reachable_list:
                        reachable_list.append(y)
        
        return reachable_list
    #this method will return true if the acceptor, accept's landa and false if not
    def check_landa(self):
        
        reachable_states = self.landa_closure_dict[self.initial_state]
        # print("reachable states:  ", reachable_states)
        for x in reachable_states:
            if x in self.final_state:
                return True
            else:
                return False

    def directly_reachable_states(self,state, character):
    

        #here we find which states are directly reachable through certain specified character
        #at the end of this for loop direct_state list will contain direct states from current state
        #through input character
        direct_states = []
        for x in self.function:
            movement = x.split(" ")
            if state== movement[0]:
                if character == movement[1]:
                    direct_states.append(movement[2])

        return direct_states
            
    #In this method we use recursion to find all of the landa closures of a state
    def recursive_landa_closure(self,state, landa_list):

        landa_list.append(state)
        self.visited.append(state)
        neighbors = self.directly_reachable_states(state, "λ")
        for x in neighbors:
            if x not in self.visited:
                self.recursive_landa_closure(x, landa_list)
        


#This is dfa class and we will complete it with nfa information
class dfa:

    def __init__(self):

        self.alphabet = []
        self.state = []
        self.initial_state = []
        self.final_state = []
        self.function = []


#In this method we will extract information from nfa and make the dfa acceptor
def convert_nfa2dfa(nfa, dfa):

    dfa.alphabet = nfa.alphabet
    dfa_state_list = []
    dfa_state_list.append([nfa.initial_state])    
    state_counter = 0
    
    for x in dfa_state_list:
        new_state_list = []
        for character in dfa.alphabet:
            new_state = []        
            reachable = check_reachable_for_list(x, character, nfa.all_reachable_states_dict)
            new_state_list.append(reachable) 
            # print("new state: ",new_state, character)
        #if length of new state = 0 it means there isn't any movement
        #for this state with this char in nfa so we have to make a TRAP
        #state on DFA acceptor and add 2 functions to loop on there

        for new in new_state_list:

            if len(new) == 0:
                if new not in dfa_state_list:
                    dfa_state_list.append(new)
            
                
            else:

                this_is_new = True
                for x in dfa_state_list:
                    if collections.Counter(x) == collections.Counter(new):
                        this_is_new = False
                if this_is_new:
                    dfa_state_list.append(new)
                    
        state_counter += 1
        # print(dfa_state_list)
        # print(dfa.state)
       

    make_function(dfa_state_list, nfa, dfa)

#This is a funciton that gets a list of states and a char and return union of all reachable states
#through states in the list with a given char
def check_reachable_for_list(state_list, character, all_reachable_states_dict):

    target_list = []
    for state in state_list:
        slist = all_reachable_states_dict[state][character]
        for x in slist:
            if x not in target_list:
                target_list.append(x)
    
    return target_list
#in this function we will creat all needed functions in new acceptor            
def make_function(states, nfa, dfa):
    print("DFA states before rename: ",states)
    new_state_name = []
    new_state_list = states
    function_list = []
    final_states = []
    for i in range(len(new_state_list)) : 
        new_name = "Q" + str(i)
        new_state_name.append(new_name)

    all_reachable_states = nfa.all_reachable_states_dict
    for state in new_state_list: 

        #This loop will make function for a char for upper state 
        for char in nfa.alphabet:
            reachable_state = []
            dst_new_index = 0
            #This loop indicates which states are reachable from X through char
            for x in state:
                reachable = nfa.all_reachable_states_dict[x][char]
                for y in reachable:
                    if y not in reachable_state:
                        reachable_state.append(y)
        
            for element in new_state_list:
                if collections.Counter(element) == collections.Counter(reachable_state):
                    dst_new_index = new_state_list.index(element)
            src_new_index = new_state_list.index(state)
            function = new_state_name[src_new_index] + " " + char + " " + new_state_name[dst_new_index]
            function_list.append(function)
    
    #we determine final states of dfa here
    for x in new_state_list:
        for char in nfa.final_state:
            if char in x:
                final_states.append(new_state_name[new_state_list.index(x)])
                
    #we check if landa is accepted in nfa acceptor to specify initial state as final state in dfa or not
   
    if nfa.check_landa():
        if new_state_name[0] not in final_states:
            final_states.append(new_state_name[0])
        
    
    # print("new namesss: ",new_state_name)
    # print("functions: ", function_list)
    # print("Finite stats: ", final_states)

    dfa.alphabet = nfa.alphabet
    dfa.state = new_state_name
    dfa.initial_state = [new_state_name[0]]
    dfa.final_state = final_states
    dfa.function = function_list


def make_text(dfa):

    alphabet = ""
    for i in range(len(dfa.alphabet)):
        alphabet += dfa.alphabet[i]

        if i == len(dfa.alphabet) - 1:
            break
        alphabet += " "

    states = ""
    for i in range(len(dfa.state)):
        states += dfa.state[i]

        if i == len(dfa.state) - 1:
            break
        states += " "
    
    initial_state = ""
    for i in range(len(dfa.initial_state)):
        initial_state += dfa.initial_state[i]

        if i == len(dfa.initial_state) - 1:
            break
        initial_state += " "
    
    final_states = ""
    for i in range(len(dfa.final_state)):
        final_states += dfa.final_state[i]

        if i == len(dfa.final_state) - 1:
            break
        final_states += " "

    f = open(target_filename, "w+")

    
    f.write(alphabet)
    f.write("\n")
    f.write(states)
    f.write("\n")
    f.write(initial_state)
    f.write("\n")
    f.write(final_states)
    f.write("\n")

    for i in range(len(dfa.function)):

        f.write(dfa.function[i])
        f.write("\n")

    f.close()

if __name__ == "__main__":
    nfa = nfa(filename)
    dfa = dfa()
    # print(nfa.all_reachable_states_dict)
    convert_nfa2dfa(nfa, dfa)
    print("Dfa : ", dfa.alphabet, "\n", dfa.state, "\n", dfa.initial_state, "\n" ,dfa.final_state,"\n", dfa.function)
    make_text(dfa)
