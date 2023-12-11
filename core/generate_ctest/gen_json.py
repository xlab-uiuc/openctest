import json
import sys


def create_json_from_flattened_key(key, value):
    parts = key.split('.')
    json_obj = {}
    current_level = json_obj


    for i, part in enumerate(parts):
        is_last_part = i == len(parts) - 1


        if part.isdigit():  # If part is a number, handle as a list
            part = int(part)
            # Ensure current level is a list
            if not isinstance(current_level, list):
                current_level = []
            # Expand the list if necessary
            while len(current_level) <= part:
                current_level.append({} if not is_last_part else None)
            if is_last_part:
                current_level[part] = value
            else:
                current_level = current_level[part]
        else:  # Handle as a dict
            if part not in current_level:
                current_level[part] = [] if (i+1 < len(parts) and parts[i+1].isdigit()) else {}
            if is_last_part:
                current_level[part] = value
            else:
                current_level = current_level[part]


    return json_obj


def write_json_to_file(json_data, filename):
    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def main():
    if len(sys.argv) != 4:
        print("Usage: script.py <flattened_key> <value> <output_file>")
        sys.exit(1)


    flattened_key = sys.argv[1]
    value = sys.argv[2]
    output_file = sys.argv[3]


    json_data = create_json_from_flattened_key(flattened_key, value)
    write_json_to_file(json_data, output_file)
    print(f"JSON data written to {output_file}")


if __name__ == "__main__":
    main()