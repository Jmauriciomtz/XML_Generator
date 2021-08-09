from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
import os
import re
import sys
from os import listdir
from io import StringIO
from tkinter import Toplevel
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk


def get_infoPDF(main_root):
    entry_list = []
    root2 = Toplevel(main_root)

    # Select the PDF
    filep = filedialog.askopenfile(initialdir="/", title="Select a File",
                                   filetypes=(("PDF File", ".pdf*"), ("All Files", "*.*")))
    fp = open(
        filep.name, 'rb')

    # Go through each page and extract the text
    for page in PDFPage.get_pages(fp, caching=True, check_extractable=False):
        outputString = StringIO()
        rsrmger = PDFResourceManager()
        device = TextConverter(rsrmger, outputString, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrmger, device)
        interpreter.process_page(page)
        text = outputString.getvalue()
        entry_dict = {}

        # Get Origin
        try:
            _origin = re.search(r"(?<=Origen: )[A-Za-z]+", text)
            _origin = _origin.group(0)
            # Origin
            if (_origin == "Mexico"):
                _origin = "MX"
            print(_origin)
            entry_dict["origin"] = _origin
        except:
            error = tk.messagebox.showerror(
                title="Error", message="Couldn't get Origin")
            if error == "ok":
                sys.exit()

        # ----------------------------------------

        # Get Invoice Number
        try:
            _invoice_number = re.search(
                r"(?<=Invoice Number: )[0-9A-Z]+", text)
            _invoice_number = _invoice_number.group(0)
            # Invoice Num
            entry_dict["invoiceNum"] = _invoice_number
        except:
            error = tk.messagebox.showerror(
                title="Error", message="Couldn't get Invoice Number")
            if error == "ok":
                sys.exit()

        # ----------------------------------------

                    # Get date
        try:
            _date = re.search(r"(?<=Currency:  USD)\s*[0-9\/]+", text)
            if (_date == None):
                _date = re.search(r"(?<=Currency:)\s*[0-9\/]+", text)
            _date = _date.group(0)
            _date = _date.replace("\n", "")
            # Date
            entry_dict["date"] = _date
        except:
            error = tk.messagebox.showerror(
                title="Error", message="Couldn't get Date")
            if error == "ok":
                sys.exit()

        # ----------------------------------

        # Get Quantity and Product Key
        try:
            qty_part = re.search(
                r"(?<=Description)\s*[0-9\.]+\s*[0-9]+\s*[0-9A-Z]+", text) #object Original
            qty_part_PO = re.search(
                r"(?<=Your Part Number)\s*[0-9\.]+\s*[0-9]+\s*[0-9A-Z]+", text) #object when PO present
                                          #line num #line qty #product key   
            #qty_part_doubleKey = (r"Line#", text) #objects when productKey is repeated

            if (qty_part != None):
                print(qty_part)
                print("qty_part not empty")
                qty_part_info = qty_part.group(0).strip() #shows line, qty and our part number, when PO not present
                qty = re.search(r"(?<=\s)[0-9]+", qty_part_info) 
                _xml_quantity = qty.group(0)
                part = re.search(
                    r"(?<="+qty.group(0)+")\s*[0-9A-Z]+", qty_part_info)
                if part.group(0).strip()[:2] == "MX":
                    _xml_productkey = part.group(0).strip()[2:]
                else:
                    _xml_productkey = part.group(0).strip()
                # Product Key
                _product_key = part.group(0).strip()
                entry_dict["productKey"] = _xml_productkey
                # Quantity
                entry_dict["quantity"] = _xml_quantity
                print(_product_key)
                print(_xml_quantity)
                print(_xml_productkey)
            elif (qty_part_PO != None):
                print(qty_part_PO) ##### object
                print("qty_part_po not empty")
                qty_part_info_PO = qty_part_PO.group(0).strip()
                print(qty_part_info_PO)
                qty_PO = re.search(r"(?<=\s)[0-9]+", qty_part_info_PO) 
                _xml_quantity = qty_PO.group(0)
                print(_xml_quantity)

                partPO = re.search(
                    r"(?<="+qty_PO.group(0)+")\s*[0-9A-Z]+", qty_part_info_PO)
                print(partPO) #####object
                if partPO.group(0).strip()[:2] == "MX":
                    _xml_productkey = partPO.group(0).strip()[2:]
                else:
                    _xml_productkey = partPO.group(0).strip()
                # Product Key
                _product_key = partPO.group(0).strip()
                entry_dict["productKey"] = _xml_productkey
                # Quantity
                entry_dict["quantity"] = _xml_quantity
                print(_product_key)
                print(_xml_quantity)
                print(_xml_productkey)
        except:
            error = tk.messagebox.showerror(
                title="Error", message="Couldn't get Quantity or Product Key")
            if error == "ok":
                sys.exit()

        # --------------------------------------
        # Get total
        try:
            total = re.search(r"(?<=Order Total:\s\s\s)[$0-9\,\.]+", text)
            if (total == None):
                total = re.search(r"(?<=Order Total:)\s*[$0-9\,\.]+", text)
            xml_producttotal = total.group(0)
            noDollarXmlProductValue = xml_producttotal.replace("$","")
            noCommaXmlProductValue = noDollarXmlProductValue.replace(",","")
            # Product Total
            entry_dict["total"] = noCommaXmlProductValue
        except:
            error = tk.messagebox.showerror(
                title="Error", message="Couldn't get Total")
            if error == "ok":
                sys.exit()
        

        # --------------------------------------
        # Product description
        try:
            description = re.search(r"(?<=Total)\s*[A-Za-z0-9-,_/\s\"]*\s+", text) #just gets first letter description
            xml_productDescription = description.group(0).strip()
            entry_dict["description"] = xml_productDescription
        except:
            error = tk.messagebox.showerror(
                title="Error", message="Couldn't get Product description")
            if error == "ok":
                sys.exit()

        entry_list.append(entry_dict)
    return entry_list
