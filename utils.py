def read_file(filename):
    lines_array = []  # List to store non-empty lines (without labels)
    labels_map = {}   # Dictionary to store label -> line number mapping
    line_number = 0   # Counter for non-empty lines
    line_number_original = 0
    last_label = None  # Keep track of labels that appear alone on a line

    with open(filename, "r") as file:
        for line in file:
            line_number_original += 1
            line = line.strip()  # Remove spaces and newlines
            if not line:
                continue

            parts = line.split(":", 1)

            if len(parts) == 2:
                label, instruction = parts[0], parts[1].strip()

                if label.endswith(" "):
                    print("invalid initialisation of label at line ", line_number_original)
                    quit()

                if label.isidentifier():
                    labels_map[label] = line_number
                    if instruction:
                        lines_array.append(instruction)
                        line_number += 1
                    else:
                        if last_label is not None:
                            print("Error no instructions given after label")
                            quit()
                        last_label = label
                    continue

            if last_label is not None:
                labels_map[last_label] = line_number
                last_label = None

            lines_array.append(line)
            line_number += 1

    return lines_array, labels_map
