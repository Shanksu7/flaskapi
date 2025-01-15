req_file = "requirements.txt"  # Replace with your input file path

cleaned_lines = []  # List to hold cleaned lines

with open(req_file, "r") as infile:
    for line in infile:
        # Skip lines with local paths (those containing '@ file:///')
        if "@ file:///" not in line:
            cleaned_lines.append(line)

# Now write the cleaned lines back to the output file
with open(req_file, "w") as outfile:
    outfile.writelines(cleaned_lines)

print("Cleaned requirements.txt has been saved.")
