import re
import statistics

def analyze_cache_performance(filename, max_entries=191172, max_gb=28.0):
    # Constants for Zone calculation
    # 256MB Zone / 512B Sector = 524,288 sectors per zone
    SECTORS_PER_ZONE = (256 * 1024 * 1024) // 512
    
    # Updated regex to capture both LBA and nr_sectors
    #pattern = re.compile(r"LBA:\s+(\d+).*nr_sectors:\s+(\d+)")
    pattern = re.compile(r"LBA:\s*(\d+).*s8:\s*(\d+)")

    run_sizes_gb = []
    total_unique_zones_evicted = 0
    
    current_entries = 0
    current_sectors = 0
    current_run_zones = set() # Track unique zones for the current run
    current_cache_lbas = set() # Track unique LBAs currently in the cache for this run

    try:
        with open(filename, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    lba = int(match.group(1))
                    sectors = int(match.group(2))
                    
                    # If the LBA is already found in the cache, it can be modified in place.
                    # We do not increment the size calculation or the number of entries calculation.
                    if lba in current_cache_lbas:
                        # Update zone tracking to ensure any zones covered by this overwrite are recorded
                        for s in range(lba, lba + sectors):
                            zone_id = s // SECTORS_PER_ZONE
                            current_run_zones.add(zone_id)
                        continue
                    
                    # Calculate potential GB if we add this entry
                    # (Based on your formula: sectors/8 * 4096 bytes)
                    potential_gb = ((current_sectors + sectors) / 8) * 4096 / (1024 ** 3)

                    # Trigger Eviction if entries exceed limit OR capacity exceeds 28GB
                    if current_entries >= max_entries or potential_gb > max_gb:
                        final_gb = (current_sectors / 8) * 4096 / (1024 ** 3)
                        run_sizes_gb.append(final_gb)
                        
                        # Add unique zones in this run to the global counter
                        total_unique_zones_evicted += len(current_run_zones)

                        # Reset for next run
                        current_entries = 0
                        current_sectors = 0
                        current_run_zones = set()
                        current_cache_lbas = set()

                    # Update current run stats
                    current_entries += 1
                    current_sectors += sectors
                    current_cache_lbas.add(lba)
                    
                    # Calculate Zone IDs for this write and add to set
                    # We check every sector in the write to ensure zone boundaries are caught
                    for s in range(lba, lba + sectors):
                        zone_id = s // SECTORS_PER_ZONE
                        current_run_zones.add(zone_id)

            # Capture the final run remaining in the buffer
            if current_entries > 0:
                final_gb = (current_sectors / 8) * 4096 / (1024 ** 3)
                run_sizes_gb.append(final_gb)
                total_unique_zones_evicted += len(current_run_zones)

    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return

    if not run_sizes_gb:
        print("No data found to analyze.")
        return

    # Results Output
    print(f"=== Cache Run Summary ({filename}) ===")
    print(f"Total Runs (Evictions):      {len(run_sizes_gb)}")
    print(f"Total Unique Zones Evicted:  {total_unique_zones_evicted}")
    print("-" * 40)
    print(f"Max Run Size:                {max(run_sizes_gb):.4f} GB")
    print(f"Min Run Size:                {min(run_sizes_gb):.4f} GB")
    print(f"Average Run Size:            {statistics.mean(run_sizes_gb):.4f} GB")
    print(f"Average Zones per Eviction:  {total_unique_zones_evicted / len(run_sizes_gb):.2f}")
    print(f"Total Data Processed:        {sum(run_sizes_gb):.2f} GB")

if __name__ == "__main__":
    analyze_cache_performance('nr_sectors_random.txt')
