import re
import statistics

def analyze_gc_log_detailed(filename):
    times = []
    sectors = []
    
    # Regex to capture total time and gc_writes (sectors)
    pattern = re.compile(r"total time:\s+(\d+)\s+\(milliseconds\)\s+gc_writes:\s+(\d+)")

    try:
        with open(filename, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    times.append(int(match.group(1)))
                    sectors.append(int(match.group(2)))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    if len(times) < 4:
        print("Not enough data points to calculate quartiles.")
        return

    # Calculate 4KB Blocks (8 sectors per block)
    blocks = [s / 8 for s in sectors]

    def print_full_stats(label, data, unit=""):
        q1, q2, q3 = statistics.quantiles(data, n=4)
        print(f"=== {label} Statistics ===")
        print(f"  Min:      {min(data):,.2f} {unit}")
        print(f"  Q1:       {q1:,.2f} {unit} (Median of lower half)")
        print(f"  Median:   {q2:,.2f} {unit}")
        print(f"  Q3:       {q3:,.2f} {unit}")
        print(f"  Max:      {max(data):,.2f} {unit}")
        print(f"  Average:  {statistics.mean(data):,.2f} {unit}")
        print(f"  Total:    {sum(data):,.2f} {unit}")
        print("-" * 30)

    print_full_stats("Total Time", times, "ms")
    print_full_stats("Sectors (nr_sectors)", sectors, "sectors")
    print_full_stats("4KB Blocks", blocks, "blocks")

if __name__ == "__main__":
    # Ensure your log file is named correctly here
    analyze_gc_log_detailed('gc_logs.txt')
