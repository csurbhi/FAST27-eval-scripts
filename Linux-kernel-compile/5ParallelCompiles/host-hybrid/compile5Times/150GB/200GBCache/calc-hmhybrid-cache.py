import re

def calculate_cache_metrics(filename, cache_gb=28, sector_size_bytes=512):
    # Constants
    ZONE_SIZE_MB = 256
    BYTES_PER_MB = 1024**2
    BYTES_PER_GB = 1024**3
    
    # Unit Calculations
    sectors_per_zone = (ZONE_SIZE_MB * BYTES_PER_MB) // sector_size_bytes
    cache_capacity_sectors = (cache_gb * BYTES_PER_GB) // sector_size_bytes
    
    pattern = re.compile(r"LBA:\s*(\d+).*s8:\s*(\d+)")

    # Counters
    eviction_count = 0
    total_zones_processed = 0
    
    # Current state trackers for the active cache cycle
    current_cache_occupancy = 0      # Track actual physical sector allocations (allows duplicates)
    unique_zones_in_cache = set()    # Track distinct zones touched in this cycle
    total_sectors_seen = 0

    print(f"--- Configuration ---")
    print(f"Cache Size: {cache_gb} GB")
    print(f"Zone Size:  {ZONE_SIZE_MB} MB")
    print("-" * 30)

    try:
        with open(filename, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    start_lba = int(match.group(1))
                    num_sectors = int(match.group(2))
                    total_sectors_seen += num_sectors
                    
                    # Process every sector in the incoming write
                    for sector in range(start_lba, start_lba + num_sectors):
                        # Every sector takes space because overwrites are not allowed in-place
                        current_cache_occupancy += 1
                        
                        # Map LBA to Zone ID and record the spatial footprint
                        zone_nr = sector // sectors_per_zone
                        unique_zones_in_cache.add(zone_nr)
                        
                        # Trigger Eviction immediately if the 28GiB allocation capacity is reached
                        if current_cache_occupancy >= cache_capacity_sectors:
                            eviction_count += 1
                            
                            # Add the unique zones tracked in this cycle to the grand total
                            total_zones_processed += len(unique_zones_in_cache)
                            
                            # Reset allocations and zone state for the next clean cache cycle
                            current_cache_occupancy = 0
                            unique_zones_in_cache = set()
                        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    # Handle the remaining data residing in the cache when the trace ends
    #if current_cache_occupancy > 0:
    #    total_zones_processed += len(unique_zones_in_cache)

    # Final Summary
    print("\n--- Final Results ---")
    print(f"Total Cache Evictions:     {eviction_count}")
    print(f"Total Unique Zones Seen:   {total_zones_processed}")
    print(f"Total sectors seen:   {total_sectors_seen}")
    print(f"Total volum seen:   {total_sectors_seen * 512 / (1024 ** 3) }")
    
    # Corrected denominator calculation to match the precise cycle boundaries
    total_cycles = eviction_count + (1 if current_cache_occupancy > 0 else 0)
    if total_cycles > 0:
        avg_zones = total_zones_processed / total_cycles
        print(f"Average Zones per Cycle:   {avg_zones:.2f}")

# Execute
calculate_cache_metrics('nr_sectors_random.txt')
