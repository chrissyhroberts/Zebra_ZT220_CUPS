import csv
import os
import sys

# --- 1. Parse CLI -------------------------------------------------------------
if len(sys.argv) != 2:
    print("Usage: python3 print_labels.py <csv_file_path>")
    sys.exit(1)

csv_file_path = sys.argv[1]

# --- 2. Printer settings ------------------------------------------------------
PRINTER_NAME = "Zebra_Technologies_ZTC_ZT220-300dpi_ZPL"  # ⬅ adjust if needed
BATCH_ZPL = "^XA^MTT^MNR^XZ"   # thermal-transfer + disable ribbon detection

# --- 3. Build ZPL for every record -------------------------------------------
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    count = 0
    for row in reader:
        id_text   = row["ID"].strip()
        date_text = row["DATE"].strip()      # expects format like 2025-02-02

        # ── ZPL for ONE label ────────────────────────────────────────────────
        zpl = f"""
^XA
^FO50,30^A0N,50,50^FD{id_text}^FS        # Line 1: ID  (X=50, Y=30)
^FO50,90^A0N,40,40^FD{date_text}^FS      # Line 2: DATE (X=50, Y=90)
^XZ
"""
        BATCH_ZPL += zpl

        # Re-calibrate every 50 labels
        count += 1
        if count % 50 == 0:
            BATCH_ZPL += "^XA^JC^XZ"

# --- 4. Send the batch to the printer ----------------------------------------
tmp_path = "/tmp/batch_label.zpl"
with open(tmp_path, "w") as f:
    f.write(BATCH_ZPL)

os.system(f"lp -d {PRINTER_NAME} -o raw {tmp_path}")
print("All labels sent to printer.")
