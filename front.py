import PIL
import PIL.ImageTk as imageTk
import PIL.Image as image
import tkinter as tk
from tkinter import *
from io import StringIO
from io import BytesIO
import requests
import time
from tkinter import messagebox
from truck_lite_data import get_infoPDF
from hussmann_data import get_infoPDFHus
from xml_file import put_infoXML
import sys


def set_info(main_root, _company):
    # Set variables to StringVar
    value = StringVar()
    weight = StringVar()
    trailer = StringVar()
    invoices = StringVar()
    bundles = StringVar()
    us_carrier = StringVar()
    scac = StringVar()
    invoices_pages = StringVar()
    email_date = StringVar()

    # Create popup window
    root = Toplevel(main_root) #Toplevel (Window Manager). Makes connection between windows
    root.title("Data to XML formater")
    root.configure(bg="SlateBlue4")

    # Place "Trade Mark"
    canvas = Canvas(root, width=640, height=80, bg="white")
    canvas.grid(row=25, column=0, columnspan=6, padx=5, pady=5)
    canvas.create_text(320, 20, font="Times 14 bold",
                       text="Property of Eduardo Lozano and Company")
    # Place Logo
    url = requests.get(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4mMNjNXhWYcpEIoLuGY13chy-b1N1DLDnsQ&usqp=CAU")

    image_open = image.open(BytesIO(url.content))
    my_img = imageTk.PhotoImage((image_open).resize((640, 240)))
    my_label = Label(image=my_img)
    my_label.grid(row=0, column=0, rowspan=3, columnspan=8,
                  sticky=W+E+N+S, padx=5, pady=5)
    # Create Banner
    canvas2 = Canvas(root, width=640, height=50, bg="white")
    canvas2.grid(row=6, column=0, columnspan=6, padx=5, pady=5)
    canvas2.create_text(320, 20, font=("Times", 24,  "bold"),
                        text="XML Program")

    # Fix function to get info from email later
    # def get_value():
    #     val = "$1,250.00"
    #     return val

    # Get User Input
    
    def getValues():

        data_entry = {}
        # Get submitted value
        sub_value = value.get()
        data_entry['value'] = sub_value
        # Get submitted weight
        sub_weight = weight.get()
        data_entry['weight'] = sub_weight
        # Get submitted trailer
        sub_trailer = trailer.get()
        data_entry['trailer'] = sub_trailer
        # Get submitted invoices
        sub_invoices = invoices.get()
        data_entry['invoice'] = sub_invoices
        # Get submitted bundles
        sub_bundles = bundles.get()
        data_entry['bundles'] = sub_bundles
        # Get submitted us carrier
        sub_us_carrier = us_carrier.get()
        data_entry['carrier'] = sub_us_carrier
        # Get submitted scac
        sub_scac = scac.get()
        data_entry['scac'] = sub_scac
        # Get email date 
        sub_email_date = email_date.get()
        data_entry['emailDate'] = sub_email_date
        # Get confirmation
        sub_invoices_pages = invoices_pages.get()
        answer = messagebox.askquestion('Yes|No', 'Is the information correct?' +
                                        '\nValue:\t'+sub_value + '\nWeight:\t'+sub_weight + '\nTrailer:\t' + sub_trailer + '\nInvoices:\t' + sub_invoices + '\nBundles:\t' + sub_bundles + '\nCarrier:\t' + sub_us_carrier +
                                        '\nScac:\t' + sub_scac + '\nInvPgs:\t' + sub_invoices_pages + '\nEmail Date:\t'+sub_email_date)
        if answer == "yes":
            if _company == "Truck-Lite":
                # Get list from PDF
                entry_list = get_infoPDF(root) # root is the connection from main-root passed when called in starFile
                # Pass
                put_infoXML(_company, entry_list, data_entry) # _company -> startFile, entry_list -> created localy, but linked -> CxPDF, -->
                                                            # data_entry -> local data (UserInput)
            if _company == "Hussmann":
                # Get list from PDF
                entry_list = get_infoPDFHus(root)
                # Pass
                put_infoXML(_company, entry_list, data_entry)
        else:                                               
            sys.exit()

    # Values of Pop Up
    value_label = Label(root, text="Value", bg="white",
                        font=('Times New Roman', 24, 'bold'))
    value_label.grid(row=7, column=0, columnspan=1,
                     sticky=EW, padx=5, pady=5)

    value_entry = Entry(root, textvariable=value,
                        font=('Times New Roman', 24, 'bold'))
    value_entry.grid(row=7, column=1, columnspan=1,
                     sticky=W, padx=5, pady=5)

    weight_label = Label(root, text="Weight", bg="white",
                         font=('Times New Roman', 24, 'bold'))
    weight_label.grid(row=9, column=0, columnspan=1,
                      sticky=EW, padx=5, pady=5)

    weight_entry = Entry(root, textvariable=weight,
                         font=('Times New Roman', 24, 'bold'))
    weight_entry.grid(row=9, column=1, columnspan=1,
                      sticky=W, padx=5, pady=5)

    trailer_label = Label(root, text="Trailer", bg="white",
                          font=('Times New Roman', 24, 'bold'))
    trailer_label.grid(row=11, column=0, columnspan=1,
                       sticky=EW, padx=5, pady=5)

    trailer_entry = Entry(root, textvariable=trailer,
                          font=('Times New Roman', 24, 'bold'))
    trailer_entry.grid(row=11, column=1, columnspan=1,
                       sticky=W, padx=5, pady=5)

    invoices_label = Label(root, text="Invoices", bg="white",
                           font=('Times New Roman', 24, 'bold'))
    invoices_label.grid(row=13, column=0, columnspan=1,
                        sticky=EW, padx=5, pady=5)

    invoices_entry = Entry(root, textvariable=invoices,
                           font=('Times New Roman', 24, 'bold'))
    invoices_entry.grid(row=13, column=1, columnspan=1,
                        sticky=W, padx=5, pady=5)

    bundles_label = Label(root, text="Bundles", bg="white",
                          font=('Times New Roman', 24, 'bold'))
    bundles_label.grid(row=15, column=0, columnspan=1,
                       sticky=EW, padx=5, pady=5)

    bundles_entry = Entry(root, textvariable=bundles,
                          font=('Times New Roman', 24, 'bold'))
    bundles_entry.grid(row=15, column=1, columnspan=1,
                       sticky=W, padx=5, pady=5)

    us_carrier_label = Label(root, text="US Carrier", bg="white",
                             font=('Times New Roman', 24, 'bold'))
    us_carrier_label.grid(row=17, column=0, columnspan=1,
                          sticky=EW, padx=5, pady=5)

    us_carrier_entry = Entry(root, textvariable=us_carrier,
                             font=('Times New Roman', 24, 'bold'))
    us_carrier_entry.grid(row=17, column=1, columnspan=1,
                          sticky=W, padx=5, pady=5)

    scac_label = Label(root, text="Scac Code", bg="white",
                       font=('Times New Roman', 24, 'bold'))
    scac_label.grid(row=19, column=0, columnspan=1, sticky=EW, padx=5, pady=5)

    scac_entry = Entry(root, textvariable=scac,
                       font=('Times New Roman', 24, 'bold'))
    scac_entry.grid(row=19, column=1, columnspan=1, sticky=W, padx=5, pady=5)

    email_date_label = Label(root, text="Email Date", bg="white",
                       font=('Times New Roman', 24, 'bold'))
    email_date_label.grid(row=21, column=0, columnspan=1, sticky=EW, padx=5, pady=5)

    email_date_entry = Entry(root, textvariable=email_date,
                       font=('Times New Roman', 24, 'bold'))
    email_date_entry.grid(row=21, column=1, columnspan=1, sticky=W, padx=5, pady=5)

    invoices_pages_label = Label(root, text="Invoices & Pages", bg="white",
                                 font=('Times New Roman', 24, 'bold'))
    invoices_pages_label.grid(
        row=23, column=0, columnspan=1, sticky=EW, padx=5, pady=5)

    invoices_pages_entry = Entry(root, textvariable=invoices_pages,
                                 font=('Times New Roman', 24, 'bold'))
    invoices_pages_entry.grid(
        row=23, column=1, columnspan=1, sticky=W, padx=5, pady=5)

    submit_function = tk.Button(root, text="Submit",
                                font="Times 24", command=getValues)
    submit_function.grid(row=24, column=5, columnspan=1,
                         sticky=EW, padx=5, pady=5)

    root.mainloop()
