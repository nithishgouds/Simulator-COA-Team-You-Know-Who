def not_endswith(label: str, suffix: str) -> bool:
    return not label.endswith(suffix)

def bin_to_signed_decimal(binary_str):
    num = int(binary_str, 2)
    if binary_str[0] == '1':
        num -= 2**32
    return num

def hex_to_signed_decimal(hex_str):
    num = int(hex_str, 16)
    if num >= 2**31:  # 32-bit signed range check
        num -= 2**32
    return num

def read_scp(filename):
    labels_map_scp = {}
    data_array_scp = []
    line_number_original=0
    data_store=False
    data_array_index=0

    with open(filename, "r") as file:
        for line in file:
            line_number_original += 1

            line=line.split("#", 1)[0]
            line = line.strip()
            if not line:
                continue
            
            if line==".data_scp":
                data_store=True
                continue
            if line==".data" or line==".text":
                if data_store==False:
                    return labels_map_scp,data_array_scp,0
                return labels_map_scp,data_array_scp,line_number_original
                

            if data_store:
                line=line.replace(',', ' ')
                if ":" in line:
                    parts = line.split(":", 1)
                    if parts[0]=="":
                        print("invalid declaration of data in line:",line_number_original)
                        exit()
                    address_label=parts[0]
                    sub_parts=parts[1].split()
                    if sub_parts[0] != ".word":
                        print("invalid declaration of data in line:",line_number_original)
                        exit()

                    for i in range(1,len(sub_parts)):
                        if i==1:
                            if address_label not in labels_map_scp:
                                labels_map_scp[address_label]=data_array_index
                            else:
                                print("label:",address_label," is declared multiple times")
                                exit()
                        if sub_parts[i].startswith("0x"):  # Hexadecimal
                            data_array_scp.append(hex_to_signed_decimal(sub_parts[i]))
                        elif sub_parts[i].startswith("0b"):  # Binary
                            data_array_scp.append(bin_to_signed_decimal(sub_parts[i]))
                        else:
                            data_array_scp.append(int(sub_parts[i]))
                        data_array_index+=1
                else:
                    sub_parts=line.split()
                    if sub_parts[0] != ".word":
                        print("invalid declaration of data in line:",line_number_original)
                        exit()

                    for i in range(1,len(sub_parts)):
                        if sub_parts[i].startswith("0x"):  # Hexadecimal
                            data_array_scp.append(hex_to_signed_decimal(sub_parts[i]))
                        elif sub_parts[i].startswith("0b"):  # Binary
                            data_array_scp.append(bin_to_signed_decimal(sub_parts[i]))
                        else:
                            data_array_scp.append(int(sub_parts[i]))
                        data_array_index+=1
        
        return labels_map_scp,data_array_scp,0






def read_file(filename):
    lines_array = []  # List to store non-empty lines (without labels)
    labels_map = {}   # Dictionary to store label -> line number mapping
    
    line_number = 0   # Counter for non-empty lines
    line_number_original = 0
    last_label = None  # Keep track of labels that appear alone on a line
    data_store=False
    data_array = []
    data_array_index=0
    labels_map_scp,data_array_scp,line_number_scp = read_scp(filename)
    line_number_original += line_number_scp

    lines_skipped=0


    with open(filename, "r") as file:
        for line in file:
            line_number_original += 1
            
            if lines_skipped<line_number_scp-1:
                lines_skipped+=1
                continue

            line=line.split("#", 1)[0]
            line = line.strip()
            if not line:
                continue
            
            #print(line)

            if line==".data":
                data_store=True
                continue
            if line==".text":
                data_store=False
                continue

            
            if data_store:
                #print(line)
                line=line.replace(',', ' ')
                if ":" in line:
                    parts = line.split(":", 1)
                    if parts[0]=="":
                        print("invalid declaration of data in line:",line_number_original)
                        exit()
                    address_label=parts[0]
                    sub_parts=parts[1].split()
                    #print("sp",sub_parts,parts)
                    if sub_parts[0] != ".word":
                        print("invalid declaration of data in line:",line_number_original)
                        exit()

                    for i in range(1,len(sub_parts)):
                        if i==1:
                            if address_label not in labels_map:
                                labels_map[address_label]=data_array_index
                            else:
                                print("label:",address_label," is declared multiple times")
                                exit()
                        if sub_parts[i].startswith("0x"):  # Hexadecimal
                            data_array.append(hex_to_signed_decimal(sub_parts[i]))
                        elif sub_parts[i].startswith("0b"):  # Binary
                            data_array.append(bin_to_signed_decimal(sub_parts[i]))
                        else:
                            data_array.append(int(sub_parts[i]))
                        data_array_index+=1
                    
                else:
                    sub_parts=line.split()
                    if sub_parts[0] != ".word":
                        print("invalid declaration of data in line:",line_number_original)
                        exit()

                    for i in range(1,len(sub_parts)):
                        if sub_parts[i].startswith("0x"):  # Hexadecimal
                            data_array.append(hex_to_signed_decimal(sub_parts[i]))
                        elif sub_parts[i].startswith("0b"):  # Binary
                            data_array.append(bin_to_signed_decimal(sub_parts[i]))
                        else:
                            data_array.append(int(sub_parts[i]))
                        data_array_index+=1
                

            else:
                parts = line.split(":", 1)

                if len(parts) == 2:
                    label, instruction = parts[0], parts[1].strip()

                    if label.endswith(" "):
                        print("invalid initialisation of label at line ", line_number_original)
                        quit()

                    if label.isidentifier():
                        # if label not in labels_map:
                        #     labels_map[label] = line_number
                        # else:
                        #     print("label:",label," is already declared")
                        #     exit()
                        if instruction:
                            if label not in labels_map:
                                labels_map[label] = line_number
                            else:
                                print("label:",label," is declared multiple times")
                                exit()
                            lines_array.append(instruction)
                            line_number += 1
                        else:
                            if last_label is not None:
                                print("Error no instructions given after label")
                                quit()
                            last_label = label
                        continue

                if last_label is not None:
                    if last_label not in labels_map:
                        labels_map[last_label] = line_number
                    else:
                        print("label:",last_label," is declared multiple times")
                        exit()  
                    last_label = None

                lines_array.append(line)
                line_number += 1

    return lines_array, labels_map,data_array,labels_map_scp,data_array_scp
