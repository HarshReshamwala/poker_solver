"""
import json

def extract_player_names(file_path):
    player_names = set()  # Use a set to avoid duplicate names

    with open(file_path, 'r') as file:
        file_content = file.read().strip()
        
        # Try to load the entire file content as JSON
        try:
            # Assuming the file content is a JSON array
            data = json.loads(file_content)
            
            # Check if data is a list
            if isinstance(data, list):
                for item in data:
                    # Ensure each item is a dictionary
                    if isinstance(item, dict):
                        # Check if the dictionary contains the key 'players'
                        if 'players' in item:
                            # Add player names to the set
                            player_names.update(item['players'])
            else:
                print("File content is not a JSON array.")
        
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    
    return list(player_names)  # Convert set to list if needed

file_path = '/Users/harshreshamwala/Documents/Projects/poker_solver/parsed_files.txt'  # Update with the path to your .txt file
players = extract_player_names(file_path)
print(players)
"""



