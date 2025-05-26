import re
import os
import json

def parse_game_files(directory):
    # Initialize state counter
    state_counter = 0
    parsed_hands = []
    
    # Iterate through each file in the directory
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.log'):  # Assuming game files are text files
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                file_content = file.read()
                hands, state_counter = parse_game_file(file_content, state_counter)
                parsed_hands.extend(hands)
    
    return parsed_hands

def parse_game_file(file_content, state_counter):
    # Store the parsed hands
    parsed_hands = []
    
    # Split the content by lines
    lines = file_content.splitlines()

    for line in lines:
        if line.startswith("STATE:"):
            parsed_hand, state_counter = parse_state_line(line, state_counter)
            parsed_hands.append(parsed_hand)
    
    return parsed_hands, state_counter

def parse_state_line(line, state_counter):
    # Remove "STATE:" and split the line by ":"
    parts = line[6:].split(":")
    
    # Extract state information
    state_number = state_counter
    state_counter += 1
    actions = parts[1]
    hole_cards = parts[2].split("|")
    if "/" in parts[3]:
        board_cards = parts[3].split("/")
        winnings = list(map(float, parts[4].split("|")))
        players = parts[5].split("|")
    else:
        board_cards = []
        winnings = list(map(float, parts[3].split("|")))
        players = parts[4].split("|")
    
    # Parse the actions
    action_history = parse_actions(actions)

    return {
        'state_number': state_number,
        'actions': action_history,
        'hole_cards': hole_cards,
        'board_cards': board_cards,
        'winnings': winnings,
        'players': players
    }, state_counter

def parse_actions(actions):
    # Split actions into individual player actions and create a list of them
    return re.findall(r'[fcr]\d*', actions)

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
directory_path = '/Users/harshreshamwala/Documents/Projects/poker_solver/Pluribus_Logs'
parsed_data = parse_game_files(directory_path)
save_to_file(parsed_data, 'parsed_files.txt')
