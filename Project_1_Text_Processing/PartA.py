import sys

def read_file(filename):
    tokens = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Removing non-alphanumeric characters and converting to lowercase
                cleaned_line = ''.join(char.lower() if char.isalnum() else ' ' for char in line)
                words = cleaned_line.split()
                tokens.extend(words)
        return tokens
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def computeWordFrequencies(tokens):
    frequencies = {}
    for token in tokens:
        frequencies[token] = frequencies.get(token, 0) + 1
    return frequencies

def printFrequencies(frequencies):
    # Sorting by frequency and then alphabetically
    sorted_frequencies = sorted(frequencies.items(), key=lambda x: (-x[1], x[0]))
    print("Token\tFrequency")
    for token, freq in sorted_frequencies:
        print(f"{token}\t{freq}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python PartA.py [filename]")
    else:
        filename = sys.argv[1]
        tokens = read_file(filename)
        frequencies = computeWordFrequencies(tokens)
        printFrequencies(frequencies)