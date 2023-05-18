import os
import hashlib
import tkinter as tk
from tkinter import ttk

def binary_to_decimal(binary):
    binary = binary[::-1]  # Reverse the binary string to start from rightmost bit
    decimal = 0
    for i in range(len(binary)):
        decimal += int(binary[i]) * (2**i)
    return decimal

def import_words(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file]
    return words

# import words from a file
word_list = import_words('bip39list.txt')

def generate_binary():
    # Generate 256 random bits
    binary_data = os.urandom(32)  
    binary_str = ''.join(format(byte, '08b') for byte in binary_data)

    # Clear the text fields and labels
    result_text.delete(1.0, tk.END)
    hashed_result_text.delete(1.0, tk.END)
    appended_result_text.delete(1.0, tk.END)
    for row in binary_labels:
        for label in row:
            label['text'] = ''
    for row in decimal_labels:
        for label in row:
            label['text'] = ''
    for row in word_labels:
        for label in row:
            label['text'] = ''

    # Insert the new binary string into the text field
    result_text.insert(tk.END, binary_str)

def generate_sha256():
    # Retrieve binary from text field
    binary_str = result_text.get(1.0, tk.END).strip()

    # Convert binary to bytes
    binary_bytes = bytes(int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8))

    # Calculate SHA256 hash
    sha256 = hashlib.sha256(binary_bytes).digest()

    # Convert hash to binary
    sha256_binary = ''.join(format(byte, '08b') for byte in sha256)

    # Clear the hashed result text field
    hashed_result_text.delete(1.0, tk.END)

    # Insert the new binary hash into the hashed result text field
    hashed_result_text.insert(tk.END, sha256_binary)

    # Append first 8 bits of SHA256 to original binary and display in appended result text field
    appended_binary = binary_str + sha256_binary[:8]
    appended_result_text.delete(1.0, tk.END)
    appended_result_text.insert(tk.END, appended_binary)

    # Split appended binary into chunks of 11 bits and display in labels
    for i in range(6):
        for j in range(4):
            binary_chunk = appended_binary[(i*4+j)*11:(i*4+j+1)*11]
            binary_labels[i][j]['text'] = binary_chunk

            # Convert binary to decimal and display in decimal labels
            decimal = binary_to_decimal(binary_chunk)
            decimal_labels[i][j]['text'] = str(decimal)

            # Look up word in list and display in word labels
            word = word_list[decimal]
            word_labels[i][j]['text'] = word

# Create the main window
root = tk.Tk()
root.title("Seed Phrase Generator")

# Create a frame for the buttons and text fields
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a button that will call generate_binary when clicked
generate_button = ttk.Button(frame, text="Entropy", command=generate_binary)
generate_button.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a label
result_label = ttk.Label(frame, text="Produce 256 bits of entropy somehow:")
result_label.grid(row=1, column=0, sticky=(tk.W))

# Create a text field to display the binary
result_text = tk.Text(frame, width=40, height=10)
result_text.grid(row=1, column=6, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a button that will call generate_sha256 when clicked
hash_button = ttk.Button(frame, text="Generate", command=generate_sha256)
hash_button.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a label
hashed_result_label = ttk.Label(frame, text="Take the SHA256 of that entropy, jam the\nfirst 8 bits of the result to the end of that entropy\n(gives you 264 bits in total):")
hashed_result_label.grid(row=3, column=0, sticky=(tk.W))

# Create a text field to display the hashed binary
hashed_result_text = tk.Text(frame, width=40, height=10)
hashed_result_text.grid(row=3, column=6, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a label
appended_result_label = ttk.Label(frame, text="Now split this into 24 groups of 11 bits,\nconvert to decimal, and map the decimal to\nthe appropriate index in the BIP39 list:")
appended_result_label.grid(row=4, column=0, sticky=(tk.W))

# Create a text field to display the appended binary
appended_result_text = tk.Text(frame, width=40, height=10)
appended_result_text.grid(row=4, column=6, sticky=(tk.W, tk.E, tk.N, tk.S))

howto_label = ttk.Label(frame, text="Convert binary to decimal:\nsum of {bit} * 2 ^ {position}\nafter reversing the string (LSB position 0):")
howto_label.grid(row=7, column=0, sticky=(tk.W))

# Create a 6x4 grid of labels to display binary chunks
binary_labels = [[ttk.Label(frame, text='') for _ in range(4)] for _ in range(6)]
for i in range(6):
    for j in range(4):
        binary_labels[i][j].grid(row=5+i, column=j+1, sticky=(tk.W),pady=3)
        
howto_label2 = ttk.Label(frame, text="Take resulting integers (0-2048)\nand map to the BIP39 list:")
howto_label2.grid(row=13, column=0, sticky=(tk.W))

# Create a 6x4 grid of labels to display decimal equivalents of binary chunks
decimal_labels = [[ttk.Label(frame, text='') for _ in range(4)] for _ in range(6)]
for i in range(6):
    for j in range(4):
        decimal_labels[i][j].grid(row=11+i, column=j+1, sticky=(tk.W),pady=3)


howto_label2 = ttk.Label(frame, text="Your new seed phrase:\n(Adjust entropy, try hit Generate again)")
howto_label2.grid(row=19, column=0, sticky=(tk.W))

# Create a 6x4 grid of labels to display words corresponding to decimal values
word_labels = [[ttk.Label(frame, text='') for _ in range(4)] for _ in range(6)]
for i in range(6):
    for j in range(4):
        word_labels[i][j].grid(row=17+i, column=j+1, sticky=(tk.W),pady=3)

root.mainloop()