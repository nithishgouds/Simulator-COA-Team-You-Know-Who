import math

class CacheLine:
    def __init__(self, block_size):
        self.block_size = block_size
        self.tag = None
        self.any_value_changed = False
        self.block = [0] * (block_size // 4) 


class CacheSet:
    def __init__(self, associativity, block_size):
        self.associativity = associativity
        self.cache_set = [CacheLine(block_size) for i in range(associativity)]


class Cache:
    def __init__(self, cache_size, block_size, associativity, replacement_policy):
        # replacement_policy: 0 for LRU, 1 for SRRIP
        self.cache_size = cache_size
        self.block_size = block_size
        self.associativity = associativity
        self.replacement_policy = replacement_policy  # 0 for LRU, 1 for SRRIP
        
        # Calculate cache parameters correctly for any cache size
        self.number_of_blocks = self.cache_size // self.block_size
        self.number_of_sets = self.number_of_blocks // self.associativity
        
        # print("number of sets", self.number_of_sets)
        # print("number of blocks", self.number_of_blocks)
        # print("associativity", self.associativity)
        
        # Calculate bit lengths properly
        self.offset_bits_length = int(math.log2(self.block_size))
        # Handle non-power-of-2 number of sets by using the next power of 2
        if self.number_of_sets & (self.number_of_sets - 1) == 0:
            # Power of 2
            self.index_bits_length = int(math.log2(self.number_of_sets))
        else:
            # Not a power of 2, use next power of 2
            self.index_bits_length = int(math.log2(self.number_of_sets)) + 1
            
        # print("offset bits length", self.offset_bits_length)
        # print("index bits length", self.index_bits_length)
        
        # Create the actual sets based on calculated number of sets
        self.c = [CacheSet(self.associativity, self.block_size) for _ in range(self.number_of_sets)]
        self.cache_accesses = 0
        self.cache_misses = 0

        self.lru = [[0]*self.associativity for _ in range(self.number_of_sets)] 
        # For SRRIP - M-bit RRPV counter per cache line (typically 2 bits, values 0-3)
        self.max_rrpv = 3
        self.rrpv = [[0]*self.associativity for _ in range(self.number_of_sets)]
        self.init_lru()
        self.init_rrpv()

    def init_lru(self):
        for i in range(self.number_of_sets):
            for j in range(self.associativity):
                self.lru[i][j] = j

    def init_rrpv(self):
        for i in range(self.number_of_sets):
            for j in range(self.associativity):    
                self.rrpv[i][j] = self.max_rrpv   # Initialize all to max_rrpv for SRRIP
    
    def get_index_from_address(self, address):
        # For non-power-of-2 set counts, we need to handle index calculation differently
        # Extract the bits that would be used for the index
        raw_index = (address >> self.offset_bits_length) % self.number_of_sets
        return raw_index
                          
    def fetch(self, address):
        self.cache_accesses += 1
        
        # Calculate address components
        offset = address % self.block_size
        index = self.get_index_from_address(address)
        tag = address // (self.number_of_sets * self.block_size)

        for i in range(len(self.c[index].cache_set)):
            cache_line = self.c[index].cache_set[i]
            if cache_line.tag == tag:
                # Cache hit
                if self.replacement_policy == 0:  # LRU
                    self.update_lru(index, i)
                else:  # SRRIP
                    self.update_rrpv_hit(index, i)
                return cache_line.block[offset//4]

        self.cache_misses += 1    
        return None
    
    def check_in_cache(self, address):
        # Calculate address components
        offset = address % self.block_size
        index = self.get_index_from_address(address)
        tag = address // (self.number_of_sets * self.block_size)

        for i in range(len(self.c[index].cache_set)):
            cache_line = self.c[index].cache_set[i]
            if cache_line.tag == tag:
                # Cache hit
                return True
            
        return False
    
    def store(self, address, data):
        self.cache_accesses += 1
        
        # Calculate address components
        offset = address % self.block_size
        index = self.get_index_from_address(address)
        tag = address // (self.number_of_sets * self.block_size)

        for i in range(len(self.c[index].cache_set)):
            cache_line = self.c[index].cache_set[i]
            if cache_line.tag == tag:
                # Cache hit
                if self.replacement_policy == 0:  # LRU
                    self.update_lru(index, i)
                else:  # SRRIP
                    self.update_rrpv_hit(index, i)
                cache_line.any_value_changed = True
                cache_line.block[offset//4] = data
                return True
                
        self.cache_misses += 1    
        return False  # on cache miss, need to again update the cache line

    def update_lru(self, index, cache_line_index):
        for i in range(self.associativity):
            if self.lru[index][i] < self.lru[index][cache_line_index]:
                self.lru[index][i] += 1
        self.lru[index][cache_line_index] = 0 

    def update_rrpv_hit(self, index, cache_line_index):
        # On hit, set RRPV to 0 (indicating immediate re-reference)
        self.rrpv[index][cache_line_index] = 0

    def update_rrpv_insert(self, index, cache_line_index):
        # On insertion, set RRPV to (max - 1) for SRRIP
        self.rrpv[index][cache_line_index] = self.max_rrpv - 1

    def get_replace_block_lru(self, index):
        for i in range(self.associativity):
            if self.lru[index][i] == self.associativity-1:
                return i
    
    def get_replace_block_srrip(self, index):
        # First look for an empty line
        for i in range(self.associativity):
            if self.c[index].cache_set[i].tag is None:
                return i
                
        # Then look for any line with max_rrpv
        for i in range(self.associativity):
            if self.rrpv[index][i] == self.max_rrpv:
                return i
                
        # If no line has max_rrpv, increment all RRPV values and try again
        while True:
            # Increment all RRPV values that are less than max
            for i in range(self.associativity):
                if self.rrpv[index][i] < self.max_rrpv:
                    self.rrpv[index][i] += 1
                    
            # Check if any line now has max_rrpv
            for i in range(self.associativity):
                if self.rrpv[index][i] == self.max_rrpv:
                    return i

    def get_replace_block(self, index):
        if self.replacement_policy == 0:  # LRU
            return self.get_replace_block_lru(index)
        else:  # SRRIP
            return self.get_replace_block_srrip(index)

    def replace_line(self, address, cache_line_data, any_value_changed):
        if address is None or cache_line_data is None:
            return None, None, None
        
        # Calculate address components
        offset = address % self.block_size
        index = self.get_index_from_address(address)
        tag = address // (self.number_of_sets * self.block_size)

        line_to_replace_index = self.get_replace_block(index)
        line_to_replace = self.c[index].cache_set[line_to_replace_index]
        should_replace = True
        if line_to_replace.tag is None:
            should_replace = False
        cache_line_data_to_return = None
        address_to_return = None

        if should_replace:
            # Create a list of the proper size and then copy values
            cache_line_data_to_return = [0] * len(line_to_replace.block)
            for i in range(len(line_to_replace.block)):
                cache_line_data_to_return[i] = line_to_replace.block[i]
            
            # Reconstruct the base address of the replaced block
            address_to_return = (line_to_replace.tag * self.number_of_sets + index) * self.block_size

        line_to_replace.tag = tag
        
        for i in range(self.block_size // 4):
            line_to_replace.block[i] = cache_line_data[i]    

        if self.replacement_policy == 0:  # LRU
            self.update_lru(index, line_to_replace_index)
        else:  # SRRIP
            self.update_rrpv_insert(index, line_to_replace_index)
            
        any_value_changed_to_return = line_to_replace.any_value_changed
        line_to_replace.any_value_changed = any_value_changed
        
        if should_replace:
            return address_to_return, cache_line_data_to_return, any_value_changed_to_return
        else:
            return None, None, None
        
    def get_line_data(self, address):
        # Calculate address components
        offset = address % self.block_size
        index = self.get_index_from_address(address)
        tag = address // (self.number_of_sets * self.block_size)

        index_of_line = None
        for i in range(len(self.c[index].cache_set)):
            cache_line = self.c[index].cache_set[i]
            if cache_line.tag == tag:
                index_of_line = i
                break

        if index_of_line is None:
            return None, None, None
            
        # Create a list of the proper size and then copy values
        cache_line = self.c[index].cache_set[index_of_line]
        cache_line_data_to_return = list(cache_line.block)  # Make a copy
        
        # Reconstruct the base address of the block
        address_to_return = (cache_line.tag * self.number_of_sets + index) * self.block_size
        
        any_value_changed_to_return = cache_line.any_value_changed

        # Remove from cache
        self.c[index].cache_set[index_of_line].tag = None

        return address_to_return, cache_line_data_to_return, any_value_changed_to_return