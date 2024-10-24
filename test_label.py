import csv
import os
import sys

# Check if the CSV file path was provided as an argument
if len(sys.argv) != 2:
    print("Usage: python3 print_labels.py <csv_file_path>")
    sys.exit(1)

# Get the CSV file path from the command line arguments
csv_file_path = sys.argv[1]

# Printer name (as it appears in CUPS)
printer_name = 'Zebra_Technologies_ZTC_ZT220-300dpi_ZPL'  # Replace with your actual printer name

# Initialize a variable to hold all ZPL commands in one batch
batch_zpl = ""

# Add the thermal transfer and disable ribbon detection commands at the beginning of the batch
batch_zpl += "^XA^MTT^MNR^XZ"  # Set to thermal transfer mode and disable ribbon detection

# Open and read the CSV file
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Loop over each row in the CSV, keeping count for every 50 labels
    count = 0
    for row in reader:
        id_number = row['ID']  # Assuming your CSV has a column named 'ID'
        
        # Generate ZPL for each label
        zpl = f"""
        ^XA
        ^FO20,10^BQN,2,5
        ^FDQA,{id_number}^FS  # QR code for the ID
        ^FO150,30^A0N,50,50^FD{id_number}^FS  # Text for ID
        ^XZ
        """
        
        # Add the ZPL for this label to the batch
        batch_zpl += zpl

        # Recalibrate the printer every 50 labels
        count += 1
        if count % 50 == 0:
            # Add recalibration command
            batch_zpl += "^XA^JC^XZ"  # ^JC command to recalibrate the media

# Save the entire batch of ZPL commands to a temporary file
zpl_file_path = '/tmp/batch_label.zpl'
with open(zpl_file_path, 'w') as zpl_file:
    zpl_file.write(batch_zpl)

# Send the entire batch of ZPL commands to the printer in one go
os.system(f'lp -d {printer_name} -o raw {zpl_file_path}')

print("All labels sent to printer.")
