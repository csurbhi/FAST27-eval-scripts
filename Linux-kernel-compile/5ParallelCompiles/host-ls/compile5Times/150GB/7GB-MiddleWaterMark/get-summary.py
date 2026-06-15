import collections

def analyze_file(filename):
    numbers = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Strip whitespace and attempt to convert to float
                clean_line = line.strip()
                if clean_line:
                    try:
                        numbers.append(float(clean_line))
                    except ValueError:
                        # This skips headers or text lines in the file
                        continue
        
        if not numbers:
            print("No valid numbers found in the file.")
            return

        # Basic Statistics
        smallest = min(numbers)
        largest = max(numbers)
        
        # Frequency Analysis (Mode)
        counts = collections.Counter(numbers)
        most_common_val, frequency = counts.most_common(1)[0]
        
        print(f"--- Analysis for {filename} ---")
        print(f"Smallest Value:    {smallest}")
        print(f"Largest Value:     {largest}")
        print(f"Most Common Value: {most_common_val} (appeared {frequency} times)")
        print("-" * (len(filename) + 22))

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")

# Usage:
# Replace 'your_data_file.txt' with the name of your actual file
analyze_file('nr_sectors_random.txt')
