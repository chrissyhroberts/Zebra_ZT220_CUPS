# Zebra_ZT220_CUPS
A cups method for printing labels with barcodes to a ZT220

## Step 1: Add the Zebra ZT220 to macOS via CUPS
Connect the printer with a USB cable. Allow connection if prompted.

### Enable CUPS on macOS:
Open Terminal (Applications > Utilities > Terminal).
Run the following command to enable the CUPS web interface (if not already enabled):

`sudo cupsctl WebInterface=yes`

Enter your laptop password when prompted.

### Access the CUPS Web Interface:

Open a web browser and go to http://localhost:631. 
This is the CUPS web interface where you can manage printers.
You may need to add your laptop user name and password
Add the Zebra ZT220 Printer:
In the CUPS interface, click on Administration at the top.
Click on Add Printer.
If your Zebra ZT220 is properly connected via USB, it should show up in the list of available printers. Select the Zebra ZT220.
Follow the prompts to add the printer. You may be asked to select a printer driver—choose the correct one for the Zebra ZT220 or a Generic Raw driver if no specific ZPL driver is available.
Set Up Printer Driver (if needed):
If the Zebra ZT220 driver is not already installed, you may need to install it manually. You can download Zebra printer drivers for macOS from Zebra's website or use the generic ZPL driver for label printing.

## Step 2 : Test direct method of printing

Make a text file and enter this
```
^XA
^FO00,10^BQN,2,5
^FDQA,1001^FS  # QR code for https://example.com
^FO120,050^A0N,50,50^FD12345^FS  # Text for ID
^XZ
```
Save the file as `test_label.zpl`

### Find the printer's name
On the webpage click `printers` and you should see a list headed 'queue name'
The Zebra should have a name like `Zebra_Technologies_ZTC_ZT220-300dpi_ZPL`

### Send a test command to the printer

`lp -d Zebra_Technologies_ZTC_ZT220-300dpi_ZPL -o raw test_label.zpl`

A label should print.


## Step 3 : Batch mode

### Prepare the CSV file
Add the list of ID numbers to the file `test_label.csv`

```
ID
1001
1002
1003
1004
```
### Run the batch mode print

`python3 test_label.py test_label.csv`

![PHOTO-2024-10-24-13-55-28](https://github.com/user-attachments/assets/1b7b6f4f-651f-428c-b255-6e5f5f073582)


