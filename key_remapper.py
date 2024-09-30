# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 15:43:25 2024

@author: raxephion


Requirements:
1. Install `pynput` library: 
    
   bash
   pip install pynput
   

"""

import pynput
from pynput.keyboard import Key, Listener, Controller
import json

# Initialize the keyboard controller
controller = Controller()

# Default key mappings - can be customized by the user
key_mapping = {
    'a': 'b',  # Replace 'a' with 'b'
    'b': 'c',  # Replace 'b' with 'c'
    'c': 'a',  # Replace 'c' with 'a'
}

# Function to load key mappings from a JSON file
def load_mappings_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save key mappings to a JSON file
def save_mappings_to_file(filename, mappings):
    with open(filename, 'w') as file:
        json.dump(mappings, file, indent=4)

# Function to remap a key press
def on_press(key):
    try:
        # Check if the key is in the mapping and replace it
        if key.char in key_mapping:
            replacement_key = key_mapping[key.char]
            controller.release(key)  # Release the original key
            controller.press(replacement_key)  # Press the replacement key
            controller.release(replacement_key)  # Release the replacement key
        else:
            # If the key is not in the mapping, press it normally
            controller.press(key)
    except AttributeError:
        # Handling special keys (like Key.enter, Key.space, etc.)
        if key in key_mapping:
            replacement_key = key_mapping[key]
            controller.release(key)
            controller.press(replacement_key)
            controller.release(replacement_key)
        else:
            controller.press(key)

# Function to handle key release events
def on_release(key):
    try:
        if key.char not in key_mapping:
            controller.release(key)
    except AttributeError:
        if key not in key_mapping:
            controller.release(key)

# Main function to run the key remapper
def main():
    global key_mapping
    key_mapping_filename = 'key_mappings.json'
    
    # Load key mappings from file
    key_mapping = load_mappings_from_file(key_mapping_filename)
    
    while True:
        print('Current key mappings:', key_mapping)
        user_input = input("Enter mappings in the format 'key:replacement' (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        try:
            key, replacement = user_input.split(':')
            key_mapping[key] = replacement
            # Save updated mappings to file
            save_mappings_to_file(key_mapping_filename, key_mapping)
        except ValueError:
            print("Invalid format. Please enter mappings in 'key:replacement' format.")
    
    print("Starting key listener...")
    
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()