import csv

def csv_to_txt(csv_file, txt_file):
    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        with open(txt_file, 'w') as txt_file:
            for i, row in enumerate(csv_reader):
                if i == 0:  # First row, assuming it contains column names
                    # Prepend column names with asterisks (*) to indicate larger font size
                    formatted_row = ["*{}*".format(col.strip()) if col.strip() else "|" for col in row]
                else:
                    # Replace missing information with "|" and strip the row data
                    formatted_row = ["{} |".format(col.strip()) if col.strip() else "|" for col in row]

                    # Remove empty cells from the row
                    formatted_row = [cell for cell in formatted_row if cell.strip()]

                # Join the row data and add an extra newline for spacing
                stripped_info = " ".join(formatted_row) + "\n\n"  
                txt_file.write(stripped_info)

csv_to_txt("input.csv", "output.txt")
