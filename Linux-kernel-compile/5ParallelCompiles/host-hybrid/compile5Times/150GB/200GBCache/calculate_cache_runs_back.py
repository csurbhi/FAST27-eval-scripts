import re

def calculate_cache_runs(filename, max_entries=191172, max_gb=28.0):
    # Pattern to extract nr_sectors
    pattern = re.compile(r"nr_sectors:\s+(\d+)")
    
    runs = []
    current_entries = 0
    current_sectors = 0
    
    with open(filename, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                sectors = int(match.group(1))
                
                # Check if this entry would exceed the 28GB limit
                # Math: (sectors / 8) * 4096 / 1024^3
                potential_gb = ((current_sectors + sectors) / 8) * 4096 / (1024 ** 3)
                
                # If we've hit max entries or the next entry would push us over 28GB
                if current_entries >= max_entries or potential_gb > max_gb:
                    final_gb = (current_sectors / 8) * 4096 / (1024 ** 3)
                    runs.append((current_entries, final_gb))
                    # Reset for the next run
                    current_entries = 0
                    current_sectors = 0
                
                current_entries += 1
                current_sectors += sectors

        # Final cleanup for the last run
        if current_entries > 0:
            final_gb = (current_sectors / 8) * 4096 / (1024 ** 3)
            runs.append((current_entries, final_gb))
            
    return runs

if __name__ == "__main__":
    # Update with your filename
    cache_runs = calculate_cache_runs('nr_sectors_random.txt')
    
    print(f"{'Run #':<10} | {'Entries':<12} | {'Cache Size (GB)':<15}")
    print("-" * 45)
    for i, (entries, gb) in enumerate(cache_runs, 1):
        print(f"{i:<10} | {entries:<12,} | {gb:<15.4f}")
