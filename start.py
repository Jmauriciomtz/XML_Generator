import PIL
import PIL.ImageTk as imageTk
import PIL.Image as image
import tkinter as tk
from tkinter import *
from io import StringIO
from io import BytesIO
import requests 
from front import set_info


def callSet():
    set_info(main_root, choosen.get())


# Start Program
main_root = tk.Tk()
main_root.title("EELCO Software")
main_root.configure(bg="SlateBlue4")

# Create "Trade Mark"
canvas = Canvas(main_root, width=640, height=80, bg="white")
canvas.grid(row=24, column=0, columnspan=6, padx=5, pady=5)
canvas.create_text(320, 20, font="Times 14 bold",
                   text="Property of Eduardo Lozano and Company")
# Get Logo
url = requests.get(
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4mMNjNXhWYcpEIoLuGY13chy-b1N1DLDnsQ&usqp=CAU")
image_open = image.open(BytesIO(url.content))
my_image = imageTk.PhotoImage((image_open).resize((640, 240)))
my_label = Label(image=my_image)
my_label.grid(row=0, column=0, rowspan=3, columnspan=8,
              sticky=W+E+N+S, padx=5, pady=5)
# Place Banner
canvas2 = Canvas(main_root, width=640, height=50, bg="white")
canvas2.grid(row=6, column=0, columnspan=6, padx=5, pady=5)
canvas2.create_text(320, 20, font="Times 24 bold", text="XML Converter")

# Create Dropdown
company_options = [
    "Truck-Lite", "Hussmann"
]
choosen = StringVar()
choosen.set("Truck-Lite")

drop = OptionMenu(main_root, choosen, *company_options)

drop.grid(row=7, column=1, columnspan=1, sticky=EW, padx=5, pady=5)

company_label = Label(main_root, text="Select Customer", bg="white",
                      font=('Times New Roman', 14))
company_label.grid(row=7, column=0, columnspan=1, sticky=EW, padx=5, pady=5)

# Start Program on Submit
start_function = tk.Button(main_root, text="Start",
                           font="Times 24", command=callSet)
start_function.grid(row=9, column=5, columnspan=1, sticky=EW, padx=5, pady=5)

main_root.mainloop()
