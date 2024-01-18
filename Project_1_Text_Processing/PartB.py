import sys

def read_file(filename):
    tokens = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                cleaned_line = ''.join(char.lower() if (char.isdigit() or char.isalpha() and char.encode('ascii', 'ignore').decode() != '') else ' ' for char in line)
                words = cleaned_line.split()
                tokens.extend(words)
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    return tokens

def find_common_tokens(tokens1, tokens2):
    set1 = set(tokens1)
    set2 = set(tokens2)
    return set1.intersection(set2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py [file1] [file2]")
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        tokens1 = read_file(file1)
        tokens2 = read_file(file2)
        common_tokens = find_common_tokens(tokens1, tokens2)
        print(len(common_tokens))