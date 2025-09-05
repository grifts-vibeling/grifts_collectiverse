import json
import random
import os

def load_data(file_path):
    """Loads a JSON file from the specified path."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}.")
        return None

def open_pack(pack_name, characters_data, packs_data):
    """
    Simulates opening a Grift Pack and returns the cards received.
    
    Args:
        pack_name (str): The name of the pack to open.
        characters_data (list): List of character dictionaries.
        packs_data (list): List of pack dictionaries.
        
    Returns:
        list: A list of character dictionaries from the pack.
    """
    pack_info = next((p for p in packs_data if p['name'] == pack_name), None)
    if not pack_info:
        print(f"Pack '{pack_name}' not found.")
        return []

    probabilities = pack_info['contents']['characters']
    
    # Create pools of characters for each rarity
    character_pools = {
        rarity: [c for c in characters_data if c['rarity'].lower() == rarity]
        for rarity in ['common', 'uncommon', 'rare', 'mythic']
    }

    # Define the number of cards to pull for each rarity based on probabilities
    pack_composition = []
    
    # Simple logic for a 5-card pack for MVP
    # This can be made more complex later, but for now, we'll draw one card per rarity tier
    # and fill the rest with the highest probability cards.
    
    # Pull one card from a guaranteed rarity
    guaranteed_mythic = random.random() < (probabilities['mythic'] / 100)
    
    # Pull 5 cards based on the probabilities
    rarities = ['mythic', 'rare', 'uncommon', 'common']
    cards_in_pack = []
    
    # Generate choices based on weighted probabilities
    all_characters = characters_data
    
    # Create weights based on the pack's defined percentages
    rarity_weights = {
        'common': probabilities.get('common', 0),
        'uncommon': probabilities.get('uncommon', 0),
        'rare': probabilities.get('rare', 0),
        'mythic': probabilities.get('mythic', 0)
    }

    # Prepare a flat list of characters and their corresponding weights
    weighted_choices = []
    for char in all_characters:
        weight = rarity_weights.get(char['rarity'].lower(), 0)
        weighted_choices.append((char, weight))
    
    # Use random.choices to pick 5 characters based on the weights
    if all(weight == 0 for _, weight in weighted_choices):
        print("Error: No valid probabilities defined for the pack.")
        return []
        
    chosen_characters = random.choices(
        [char for char, weight in weighted_choices],
        weights=[weight for char, weight in weighted_choices],
        k=5 # The number of cards in a pack
    )
    
    return chosen_characters

if __name__ == "__main__":
    print("--- Simulating a Grift Pack Opening ---")
    
    # Assume data files are in the same directory, or you can specify a full path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, '..', 'data')

    characters = load_data(os.path.join(data_dir, 'characters.json'))
    packs = load_data(os.path.join(data_dir, 'packs.json'))

    if characters and packs:
        opened_pack_cards = open_pack("First Rift Pack", characters, packs)
        
        if opened_pack_cards:
            print("\nCongratulations! You opened your First Rift Pack and received:")
            for card in opened_pack_cards:
                print(f"- {card['name']} ({card['rarity']})")
        else:
            print("Failed to open pack. Please check your data files.")