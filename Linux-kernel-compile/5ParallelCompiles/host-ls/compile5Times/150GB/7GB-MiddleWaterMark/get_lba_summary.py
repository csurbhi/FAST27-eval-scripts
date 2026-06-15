import collections
import re

def analyze_smr_logs(filename):
    lba_counts = collections.Counter()
    zone_stats = collections.Counter()
    total_random_sectors = 0
    
    # Regex to grab the values after the labels
    pattern = re.compile(r"LBA:\s+(\d+)\s+zonenr:\s+(\d+).*?nr_sectors:\s+(\d+)")

    with open(filename, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                start_lba = int(match.group(1))
                zone_nr = int(match.group(2))
                nr_sectors = int(match.group(3))

                # Update Zone statistics
                zone_stats[zone_nr] += 1

                total_random_sectors += nr_sectors

                # Calculate how many LBAs this request spans
                # Every 8 sectors = 1 LBA
                num_lbas = (nr_sectors + 7) // 8 
                
                for i in range(num_lbas):
                    lba_counts[start_lba + i] += 1

    # Statistics Calculation
    total_unique_lbas = len(lba_counts)
    repeated_lbas = [lba for lba, count in lba_counts.items() if count > 1]
    
    print(f"Total Sectors in Random Stream: {total_random_sectors}")
    print(f"Total MB: {(total_random_sectors * 512) / (1024**3):.2f} GB")

    print("=== LBA Statistics ===")
    print(f"Total unique LBAs accessed: {total_unique_lbas}")
    print(f"LBAs accessed more than once: {len(repeated_lbas)}")
    if total_unique_lbas > 0:
        print(f"Redundancy Ratio: {(len(repeated_lbas) / total_unique_lbas) * 100:.2f}%")
    
    print("\n=== Top 5 'Hot' LBAs ===")
    for lba, count in lba_counts.most_common(10):
        print(f"LBA {lba}: {count} accesses")

    print("\n=== Zone Statistics ===")
    print(f"Total zones touched: {len(zone_stats)}")
    print("Top 5 active Zones (by request count):")
    for zone, count in zone_stats.most_common(10):
        print(f"Zone {zone}: {count} requests")

if __name__ == "__main__":
    # Replace with your actual filename
    analyze_smr_logs('nr_sectors_random.txt')
    #analyze_smr_logs('nr_seq_sectors.txt')
