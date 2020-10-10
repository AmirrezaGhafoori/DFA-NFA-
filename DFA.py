'''
Implementation of DFA machine with python by Amirreza Ghafoori

'''

filename = "DFA_Output_2.txt"



class dfa:

#enter the file name while making object for dfa class
    def __init__(self, filename):
        
        f = open(filename)

        #by using split lines method we will ignore line breaks '\n'
        machine_features = f.read().splitlines()  
        f.close()      
        #first we put featuers in machine_feature array and then assign them
        #to the machine features!!
        
        self.alphabet = machine_features[0].split(" ")
        self.state = machine_features[1].split(" ")
        self.initial_state = machine_features[2].split(" ")
        self.final_state = machine_features[3].split(" ")
        self.function = machine_features[4:]

        #this vairable will hold the current state of machine; at the start it will be equal tu initiate state
        self.current_state = self.initial_state[0]

        print("Alphabet are: ", self.alphabet, "\n")
        print("Initial state is: ", self.initial_state, "\n")
        print("Final states are: ", self.final_state, "\n")
    #This method will check if all of the characters of the string are involved in 
    #this dfa machine alphabet
    def check_alphabet(self,input_string):
        not_valid_counter = 0
        for character in input_string:
            if character not in self.alphabet:
                
                not_valid_counter += 1
        if not_valid_counter > 0:
            print("WARNING!!  This string contain's invalid character. \n")
            return False
        else:
            print("This string is verified and all characters are valid")
            return True
            


    def make_move(self,input_char, current_state):

        #first we find the indices of functions which contain current staet
        # print(current_state)
    
        
        indices = []
        for x in self.function:
            movement = x.split(" ")
            if current_state == movement[0]:
                indices.append(self.function.index(x))
            
        # print(indices)
        #then we check which move should be done

        for index in indices:
            if input_char in self.function[index]:
                # print("function is ", self.function[index])
                state_char_state = self.function[index].split(" ")

                print("Current move is:\n")
                print(state_char_state[0], "---",state_char_state[1],"--->",state_char_state[2],"\n")

                #and here we return the next_state
                return state_char_state[2]

    #this is the main method which will accept or dismiss the string for this machine
    def acceptor(self,input_string):

        if self.check_alphabet(input_string):

            for charachter in input_string:
                self.current_state = self.make_move(charachter, self.current_state)
            
            #at the end of the string we will check if current_state is one of
            #the final states or not
            if self.current_state in self.final_state:
                print("This String is accepted by the machine!")
                return True
            
            else:
                print("This String is NOT accepted by this machine")
                return False


if __name__ == "__main__":
    my_dfa = dfa(filename)

    input_string = input("please enter the string you want to check:\n")

    # print(input_string)
    my_dfa.acceptor(input_string)
