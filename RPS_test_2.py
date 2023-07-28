import random
import numpy as np


# Innitializations
game_items = ["R", "P", "S"]
opponent_history = []
match = 100



def _random_choice_generator_1(match):
    opponent_history = []
    for _ in range(match):
          opponent_choice = random.choice(game_items)
          opponent_history.append(opponent_choice)
    return opponent_history
"""
building the 2D matrix of 2choice pattterns and 3 choice patterns
"""

"""
picking out high frequent pattern from the 2pattern and 2 pattern frequency dictionary
"""
def _building_2D_patterns_1choices(pattern_list):
        

        # 2D pattern
        if len(pattern_list) % 2 == 0:
            rows = len(pattern_list) // 2
            np_list_choice_2pattern = np.array(pattern_list,dtype ='<U10').reshape(rows,2)
        else:
            popped_element = pattern_list.pop()
            rows = len(pattern_list) // 2
            np_list_choice_2pattern = np.array(pattern_list,dtype= '<U10').reshape(rows,2)
            # Create a new row with zeros and update the desired element with the popped element
            new_row = np.zeros((1, 2), dtype='<U10')
            new_row[0][0] = popped_element
            np_list_choice_2pattern = np.vstack([np_list_choice_2pattern, new_row])
        
        # for 1 choice pattern
        choice_2pattern_dict = {}
        for value in np_list_choice_2pattern:
            tuple_value = tuple(value)
            if tuple_value in choice_2pattern_dict:
                choice_2pattern_dict[tuple_value] += 1
            else:
                choice_2pattern_dict[tuple_value] = 1

        #print(np_list_choice_2pattern,choice_2pattern_dict)
        maximum_pattern_keys = sorted(choice_2pattern_dict, key= choice_2pattern_dict.get)
        # sorted sequence percentage
        for patterns in maximum_pattern_keys:
            pattern_percentage = round((choice_2pattern_dict[patterns]/match)*100,2)
            #print(patterns,":",pattern_percentage)
        
        # Sorting based on the same starting letter
        sorted_keys_2p = sorted(choice_2pattern_dict.keys(), key=lambda k: (k[0], list(choice_2pattern_dict.keys()).index(k)))
        # tracking what followed what
        sequence_tracker2p = {}
        for key in sorted_keys_2p:
                sequence_tracker2p[key] = choice_2pattern_dict[key]
        # Splitting the dictionary by different starting letters
        split_dict_2p = {}  
        for key, value in sequence_tracker2p.items():
                starting_letter = key[0]
                if starting_letter in split_dict_2p:
                    split_dict_2p[starting_letter][key] = value
                else:
                    split_dict_2p[starting_letter] = {key: value}    
        #picking up high frequent sequence in terms of starting choice
        higher_frequent_sequence_2p = {}
        for key,value in split_dict_2p.items():
                maximum_value = max(value.values())
                higher_frequent_sequence_2p[key] = {k for k, v in value.items() if v == maximum_value}
                pattern_percentage = round((maximum_value/match)*100,2)
                #print(f"for 2p {maximum_value}, {pattern_percentage} : {key}", higher_frequent_sequence_2p[key])

        #print(choice_2pattern_dict,"\n\n", choice_3pattern_dict,"\n",maximum_pattern_keys)
        return  np_list_choice_2pattern,choice_2pattern_dict,higher_frequent_sequence_2p


def _building_2D_patterns_2choices(pattern_list):
    rows = len(pattern_list) // 3 
    element_to_popped = len(pattern_list) - (rows*3)
    popped_element0 = []
    for _ in range(element_to_popped):
        popped_element0.append(pattern_list.pop())
    np_list_choice_3pattern = np.array(pattern_list, dtype='<U10').reshape(rows, 3)

    # Create the new row with zeros
    new_row = np.zeros((1, 3), dtype='<U10')

    # Check if there are enough elements in popped_element
    if len(popped_element0) >= 2:
        new_row[0][0] = popped_element0[0]
        new_row[0][1] = popped_element0[1]
    elif len(popped_element0) == 1:
        new_row[0][0] = popped_element0[0]

    # Vertically stack new_row on top of np_list_choice_3pattern
    np_list_choice_3pattern = np.vstack([np_list_choice_3pattern, new_row])


    choice_3pattern_dict = {}
    # for 2 choice pattern
    for value in np_list_choice_3pattern:
        tuple_value = tuple(value)
        if tuple_value in choice_3pattern_dict:
            choice_3pattern_dict[tuple_value] += 1
        else:
            choice_3pattern_dict[tuple_value] = 1
    

    #print(np_list_choice_2pattern,choice_2pattern_dict)
    maximum_pattern_keys = sorted(choice_3pattern_dict, key= choice_3pattern_dict.get)
    # sorted sequence percentage
    for patterns in maximum_pattern_keys:
        pattern_percentage = round((choice_3pattern_dict[patterns]/match)*100,2)
        #print(patterns,":",pattern_percentage)
        
     # Sorting based on the same starting letter
    sorted_keys_3p = sorted(choice_3pattern_dict.keys(), key=lambda k: (k[0], list(choice_3pattern_dict.keys()).index(k)))
    # tracking what followed what
    sequence_tracker3p = {}
    for key in sorted_keys_3p:
            sequence_tracker3p[key] = choice_3pattern_dict[key]
    # Splitting the dictionary by different starting letters
    split_dict_3p = {}  
    for key, value in sequence_tracker3p.items():
            starting_letter = key[0]
            if starting_letter in split_dict_3p:
                split_dict_3p[starting_letter][key] = value
            else:
                split_dict_3p[starting_letter] = {key: value}    
    #picking up high frequent sequence in terms of starting choice
    higher_frequent_sequence_3p = {}
    for key,value in split_dict_3p.items():
            maximum_value = max(value.values())
            higher_frequent_sequence_3p[key] = {k for k, v in value.items() if v == maximum_value}
            pattern_percentage = round((maximum_value/match)*100,2)
            #print(f"for 3p {maximum_value}, {pattern_percentage} : {key}", higher_frequent_sequence_3p[key])

    #print(np_list_choice_3pattern,choice_3pattern_dict)
    return np_list_choice_3pattern,choice_3pattern_dict,higher_frequent_sequence_3p


"""
determining which pattern tracking alogrithm to use
"""
def determine_pattern_tracking(opponent_history, counter_choice_func, tracking_2pattern_func, tracking_3pattern_func):
    choice_list = opponent_history
    prev_move = choice_list[len(choice_list) - 1]

    if len(choice_list) <= 10:
        player_choice = counter_choice_func(prev_move)
       
    elif len(choice_list) >= 11:
        np_list_choice_2pattern, choice_2pattern_dict, higher_frequent_sequence_2p = tracking_2pattern_func(choice_list)

        if prev_move in higher_frequent_sequence_2p:
            pattern_one_move = list(higher_frequent_sequence_2p[prev_move])
            best_possible_one_nextmove = pattern_one_move[0][1]
        else:
            best_possible_one_nextmove = counter_choice_func(prev_move)

        np_list_choice_3pattern, choice_3pattern_dict, higher_frequent_sequence_3p = tracking_3pattern_func(choice_list)

        best_possible_two_nextmoves = []
        if prev_move in higher_frequent_sequence_3p:
            pattern_2_move = list(higher_frequent_sequence_3p[prev_move])
            best_possible_two_nextmoves.append(pattern_2_move[0][1])
            best_possible_two_nextmoves.append(pattern_2_move[0][2])
        else:
            best_possible_two_nextmoves.append(counter_choice_func(prev_move))
            best_possible_two_nextmoves.append(random.choice(game_items))
        print(best_possible_one_nextmove, best_possible_two_nextmoves)
        return best_possible_one_nextmove, best_possible_two_nextmoves

"""
enereating random opponent choice 
# I think opponent_random_choice shoudnt be the list,
 it should return one random choice at a time and apppend to opponent_history in play_func
"""

# choosing next choice by countering opponent previous choice
def random_counter_choice(prev_move):
    if prev_move == "Rock":
        next_move = "Paper"
    elif prev_move == "Paper":
        next_move = "Scissor"
    elif prev_move == "Scissor":
        next_move = "Rock"
    else:
        next_move = random.choice(game_items)
    return next_move


match = 100 
    #play(random_choice_generator)
def determine_pattern_tracking_looping(counter_choice_func, tracking_2pattern_func, tracking_3pattern_func):
    player_score = 0
    opponent_score = 0
    choice_list = []
    global match 
    for _ in range(match):
            opponent_choice = random.choice(game_items)
            choice_list.append(opponent_choice)
            print("Oppo:",opponent_choice)

            if len(choice_list ) < 2:
                 player_choice = random.choice(game_items)
                
            elif len(choice_list) >=2 and len(choice_list) < 20:
                    prev_move = choice_list[- 2]
                    player_choice = counter_choice_func(prev_move)
                    print("player",player_choice)
            elif len(choice_list) >= 20 and len(choice_list) < 84:
                    prev_move = choice_list[- 2]
                    print(prev_move)
                    np_list_choice_2pattern, choice_2pattern_dict, higher_frequent_sequence_2p = tracking_2pattern_func(choice_list)

                    if prev_move in higher_frequent_sequence_2p:
                        pattern_one_move = list(higher_frequent_sequence_2p[prev_move])
                        player_choice = pattern_one_move[0][1]
                        print(player_choice)
                    else:
    
                        player_choice = counter_choice_func(prev_move)
            elif len(choice_list) >= 84:
                    prev_move = choice_list[- 2]       
                    np_list_choice_3pattern, choice_3pattern_dict, higher_frequent_sequence_3p = tracking_3pattern_func(choice_list)
                    best_possible_two_nextmoves = []
                    if prev_move in higher_frequent_sequence_3p:
                        pattern_2_move = list(higher_frequent_sequence_3p[prev_move])
                        best_possible_two_nextmoves.append(pattern_2_move[0][1])
                        best_possible_two_nextmoves.append(pattern_2_move[0][2])
                    else:
                        best_possible_two_nextmoves.append(counter_choice_func(prev_move))
                        best_possible_two_nextmoves.append(random.choice(game_items))
                    player_choice = best_possible_two_nextmoves           
                    
            if player_choice == opponent_choice:
                continue
            elif (player_choice == "R" and opponent_choice == "S") or \
                    (player_choice == "P" and opponent_choice == "R") or \
                    (player_choice == "S" and opponent_choice == "P"):
                player_score += 1
            else:
                opponent_score += 1
            print(len(choice_list))
         
    print(choice_list)
    print(f"Player score: {player_score}")
    print(f"Opponent score: {opponent_score}")    

determine_pattern_tracking_looping(random_counter_choice,_building_2D_patterns_1choices,_building_2D_patterns_2choices)
