import re
import statistics

def analyze_gc_log_with_quartiles(filename):
    times = []
    writes = []
    
    pattern = re.compile(r"total time:\s+(\d+)\s+\(milliseconds\)\s+gc_writes:\s+(\d+)")

    try:
        with open(filename, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    times.append(int(match.group(1)))
                    writes.append(int(match.group(2)))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    if len(times) < 4:
        print("Not enough data points to calculate quartiles.")
        return

    # Calculate Quartiles
    # n=4 gives us the boundaries for 25%, 50%, and 75%
    q1, q2, q3 = statistics.quantiles(times, n=4)

    print("=== GC Total Time Distribution (ms) ===")
    print(f"  Lowest (Min):      {min(times):,}")
    print(f"  First Quartile (Q1): {q1:,}  <-- 'Median of the lower half'")
    print(f"  Median (Q2):       {q2:,}")
    print(f"  Third Quartile (Q3):  {q3:,}")
    print(f"  Highest (Max):     {max(times):,}")
    print(f"  -----------------------------")
    print(f"  Interquartile Range: {q3 - q1:,} ms")
    print(f"  Total GC Time:       {sum(times):,} ms")

if __name__ == "__main__":
    analyze_gc_log_with_quartiles('gc_logs.txt')
