def fetch(address):
        index_bits_length = 1
        offset_bits_length = 3
        
        tag = address >> (index_bits_length + offset_bits_length)
        index = (address >> offset_bits_length) ^ (tag<<index_bits_length)
        offset = address ^ (address >> offset_bits_length << offset_bits_length)

        print("Tag:", bin(tag), "Index:", bin(index), "Offset:", bin(offset))

fetch(0b011010010101001)