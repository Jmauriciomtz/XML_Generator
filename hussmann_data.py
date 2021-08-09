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

def get_infoPDFHus(main_root):
    InvoiceCounter = 0 # increments each time new pdf keyWord found
    lineItemCounter = 0 # holds the line quantity based on Keyword "PZ"
    productKeyList = [] # holds complete list of productKeys per PDF
    sixMonthTwoLetterCountry = ['BR','CA','CN','DE','DK','GB','ID','IN','IS','IT','JP','MX','PH','SK','TR','TW','US','VN'] # orgin list/db
    filteredOrginVsOrginDb = [] # crossed refrenced list against orgin list
    orginFinalList = [] # final/complete orgin list
    weightFinalList = [] # final/complete weight list
    qtyFinalList = [] # final/complete quantity list
    priceBeforeQty = [] # Unit price only per line
    priceFinalList = [] # final/complete line amount price
    popExchangeRate = True # used to pop first element from list priceBeforeQty
    index4Price = 0 # this int will be used as index for multiplcation method(s) of qty and unitPrice
    dotDelimitedValues = [] # this list/array will be used for the holding ready to us unitPrice multiplcation value 
    index4Multi = 0 # this index will be used for the multiplication used for the
    priceFinalList = [] # list holds total line item amount after qty and unit price multiplication
    entry_list = []
    root2 = Toplevel(main_root)

    # Select the PDF
    filep = filedialog.askopenfile(initialdir="/", title="Select a File",
                                filetypes=(("PDF File", ".pdf*"), ("All Files", "*.*")))
    fp = open(
    filep.name, 'rb')

    # Go through each page and extract the text
    for page in PDFPage.get_pages(fp,maxpages=0 ,caching=True, check_extractable=False):
        outputString = StringIO()
        rsrmger = PDFResourceManager()
        device = TextConverter(rsrmger, outputString, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrmger, device)
        interpreter.process_page(page)
        text = outputString.getvalue()
        entry_dict = {}
        print(text)

        # ----------------------------------------
        # Get Number of Commercial Invoices in PDF
        # Clear global fields when new commercial Invoice is found

        try:
            newPdfKey = re.findall(r"EXPORT COMMERCIAL INVOICE", text)
            print(len(newPdfKey))
            print(newPdfKey)
            if newPdfKey: # None empty list return True
                # updates global
                # return global fields back to new/empty/none/zero
                InvoiceCounter += 1 # updates global variable
                lineItemCounter = 0 # holds the line quantity based on Keyword "PZ"
                productKeyList = [] # holds complete list of productKeys per PDF
                filteredOrginVsOrginDb = [] # crossed refrenced list against orgin list
                orginFinalList = [] # final/complete orgin list
                weightFinalList = [] # final/complete weight list
                qtyFinalList = [] # final/complete quantity list
                priceBeforeQty = [] # Unit price only per line
                priceFinalList = [] # final/complete line amount price
                popExchangeRate = True # used to pop first element from list priceBeforeQty
                index4Price = 0 # this int will be used as index for multiplcation method(s) of qty and unitPrice
                dotDelimitedValues = [] # this list/array will be used for the holding ready to us unitPrice multiplcation value 
                index4Multi = 0 # this index will be used for the multiplication used for the
                priceFinalList = [] # list holds total line item amount after qty and unit price multiplication
                previousePageLimeAmount = 0 # refrence of the 
        except:
            None

        #-----------------------------------------
        # Get amount of pages per Invoice
        try:
            # Picks up the range of pages per invoice
            _pagesIn_invoice = re.search(r"(?<=PAGINA/PAGE)\s*(.)*", text)
            _pagesIn_invoice = _pagesIn_invoice.group(0).replace("\n\n", "")
            print(_pagesIn_invoice)
            # picks up total amount of pages
            # this can help us decide how many objects to expect in invoice
            # and how many objects skip until we reach the last page object
            _pagesIn_invoice = re.search(r"(?<=1/)(\d)*", text)
            if (_pagesIn_invoice != None):
                print("Total amount of pages in current invoice below.")
                _pagesIn_invoice = _pagesIn_invoice.group(0)
                print(_pagesIn_invoice)
                entry_dict["invoicePages"] = _pagesIn_invoice
        except:
            None

        # ----------------------------------------
        # Get Importer Name
        try:
            _importer_name = re.search(r".*\s*(?=CARRETERA)", text)
            if (_importer_name == None): # Single Check Condition skipping exceptions for multiPage
                pass
            _importer_name = _importer_name.group(0)
            _importer_name = _importer_name.replace("\n", "")
            print(_importer_name)
            entry_dict["importerName"] = _importer_name
        except:
            None

        # ----------------------------------------
        # Get Invoice Number
        try:
            _invoice_number = re.search(r"(?<=SELLER)\s*[0-9]*", text)
            _invoice_number = _invoice_number.group(0)
            _invoice_number = _invoice_number.replace("\n\n", "")
            print(_invoice_number)
            entry_dict["invoiceNumber"] = _invoice_number
        except:
            None


        # ---------------------------------------
        #Get Date
        try:
            _date = re.search(r"(?<=SELLER)\s*[0-9]*\s*(.)*", text) # abstracts Invoice number and date
            _date = _date.group(0) 
            _date = re.search(r"\D\D\D\/\d\d\/\d\d\d\d", _date) # abstracts date only
            _date = _date.group(0)
            _date = _date.replace("\n", "")
            print(_date)
            entry_dict["date"] = _date
        except:
            None

        # -------------------------------------
        #Get Consignee
        try:
            _consignee = re.search(r"(?<=SOLD TO)\s*(.)*", text)
            _consignee = _consignee.group(0)
            _consignee = _consignee.replace("\n\n", "")
            print(_consignee)
            if (_consignee == "SHIP TO :"): # Will only execute for first page of the Inv.
                _consignee = re.search(r"(?<=R.F.C. :)\s*(\d)*\s*(.)*", text)
                _consigneeArray = _consignee.group(0).split("\n")
                print(_consigneeArray)
                _consignee = _consigneeArray[-1]
            print(_consignee)
            entry_dict["consignee"] = _consignee
        except:
            None

        # --------------------------------------
        # Get Trailer Number
        try:
            _trailer = re.search(r"(?<=CON. ECONOMIC N.:)\s*(\w)*\s*[A-Za-z0-9]*", text) # abstracts Region and trailer number
            _trailer = _trailer.group(0)
            _trailer = _trailer.split(" ") #splits string into list by spaces
            print(_trailer[1])
            entry_dict["trailer"] = _trailer[1]
        except:
            None

        # -------------------------------------
        # Get Referencia (Used for CustomerKey and ImporterKey)
        try:
            _referencia = re.search(r"(?<=Referencia:)\s*\D\D", text)
            _referencia = _referencia.group(0)
            _referencia = _referencia.lstrip() # removes left trailing and tabs
            print(_referencia)
            entry_dict["referencia"] = _referencia
        except:
            None

        # ------------------------------------
        # Get PO number
        try:
            _po_number_clean = ""
            _po_number = re.search(r"(?<=Referencia:)\s*\D\D\s*(.)*", text) #abstracts referencia and PO number
            _po_number = _po_number.group(0)
            _po_number = _po_number.lstrip() #removes white space before Reference
            _po_number = _po_number.split(" ") # splits referencia and PO number
            _po_number_range = _po_number[1:] #slices out refrence
            for i in range(len(_po_number_range)):
                _po_number_clean += _po_number_range[i]
            print(_po_number_clean)
            entry_dict["poNumber"] = _po_number_clean
        except:
            None

        # --------------------------------------
        # Get Bultos
        try:
            _bultos = re.search(r"(?<=BULTOS:)\s*(.)*", text)
            _bultos = _bultos.group(0)
            print(_bultos)
            entry_dict["bultos"] = _bultos
        except:
            None

        print("----------- Entering lineItems")
        # ---------------------------------------
        # Get Number of line items (refrence)
        try:
            lineQtyRef = re.findall(r"PZ", text) #determines the line item quantity
            for x in range(len(lineQtyRef)): #converts array amount into single digit amount of lineItems by refrencing PZ in line item
                lineItemCounter += 1
            print(lineItemCounter)
            print(lineQtyRef)
            entry_dict["lineAmount"] = lineItemCounter
        except:
            None
        
        print("----------- Entering productKeys")
        # ------------------------------------------
        # Get ProductKey(s)
        try:
            merch = re.findall(r'MERCHANDISE DESCRIPTION', text)
            print(len(merch))
            print(merch)
            if (merch != []):
                merchDescriptionSerial = re.search(r"(MERCHANDISE DESCRIPTION)[\s\S]*(Serial Number:)", text) # string of end to end block of lineItem description
                if (merchDescriptionSerial == None): # If None: serial number not present, thus lineItem probably are parts
                    merchDescription = re.search(r"(MERCHANDISE DESCRIPTION)[\s\S]*(.)*[\s\S]*(.)*[\s\S]*", text)
                    if (merchDescription != None):
                        print("------------------- Printing lineItme description for parts.")
                        merchDescriptionBlock = merchDescription.group(0)
                        merchDescriptionBlockList = merchDescriptionBlock.split('\n')
                        productKey = merchDescriptionBlockList[2]
                        print(productKey)
                        entry_dict['productKey'] = productKey
                elif (merchDescriptionSerial != None):
                    merchDescriptionBlock = merchDescriptionSerial.group(0)
                    merchDescriptionBlockList = merchDescriptionBlock.split('\n')
                    print(merchDescriptionBlockList)
                    # indexElements that end with "/" containt part number in string
                    # condition: when referencia: RE, string ends with PARTS if not pushed to newLIne
                    for e in merchDescriptionBlockList:
                        condition  = '/'
                        if condition in e:
                            semiCleanProductKeyList = e.split(' ')
                            productKeyValue = semiCleanProductKeyList[0] # productKey found in index 0
                            print(productKeyValue)
                            productKeyList.append(productKeyValue)
                    print(len(productKeyList))
                    print(productKeyList)
                    entry_dict['productKey'] = productKeyList
            elif(merch == []):
                print("No New Merch")
                print(productKeyList)
                entry_dict['productKey'] = productKeyList
        except:
            None

        print("----------- Entering orgins")
        # ---------------------------------------------------------------------
        # Get Orgin(s) (part line)
        try: 
            #find returns the the index of the first char mathced from it's first occurance
            indexOfUnit = text.find("UNIT PRICE") # starting index of subString containing. Return type: int
            indexOfPZ = text.find("PZ") # ending index of subString
            beforeFilterOrigin = re.findall(r"\s+\S\S\s+", text) # Picks up two letter word(s) with spaces between two consecutive letters
            print(len(beforeFilterOrigin))
            print(beforeFilterOrigin)
            for orginDb in sixMonthTwoLetterCountry:
                if beforeFilterOrigin != []:
                    for orgin in beforeFilterOrigin:        
                        cleanLeftSpaceOrgin = orgin.lstrip() # removes left trailing spaces and tabs
                        cleanRightSpaceOrgin = cleanLeftSpaceOrgin.rstrip() # removes left leading spaces and and tabs
                        cleanNewLineCharOrgin = cleanRightSpaceOrgin.replace('\n\n','') # removes trailing and leading newLine char from string
                        if (cleanNewLineCharOrgin == orginDb):
                            filteredOrginVsOrginDb.append(cleanNewLineCharOrgin) # filteredOrginsVsOriginDb conatins possible Orgin(s) in order. (needs filtering)
            print(len(filteredOrginVsOrginDb))
            print(filteredOrginVsOrginDb)
            if beforeFilterOrigin != []:
                for orginOurDb in filteredOrginVsOrginDb: #loop possible orgins
                    #find current value index
                    indexOfCurrentValue = text.find(orginOurDb)
                    #compare/check if index is in between limiting indexe(s)
                    if (indexOfCurrentValue >= indexOfUnit and indexOfCurrentValue <= indexOfPZ):
                        #if in between limits it will get appended into final List
                        orginFinalList.append(orginOurDb)
                        text = text.replace(orginOurDb,'',1) # removes country code from document/page so not repeated in search
            print(len(orginFinalList))
            print(orginFinalList)
            entry_dict["orgins"] = orginFinalList # list inside of a directory 
        except:
            None

        print("----------- Entering weight")
        # -----------------------------------------------------------------------
        # Get Net Weight. KGS (part line)
        try:
            threeDecimalNumber = re.findall(r"\s+[\d,]*\.\d\d\d\s+", text)
            #lenOfWeightList = len(threeDecimalNumber)
            #threeDecimalNumber.pop(lenOfWeightList - 1)
            print(len(threeDecimalNumber))
            print(threeDecimalNumber)
            for weight in threeDecimalNumber:
                cleanNewLineCharWeight = weight.replace('\n\n','') # removes trailing and leading newLine char from string
                #print(cleanNewLineCharWeight)
                weightFinalList.append(cleanNewLineCharWeight)
            print(len(weightFinalList))
            print(weightFinalList)
            weightLineItemQty = len(weightFinalList) # len starts at 1 not 0.
            print(weightLineItemQty)
            print(lineItemCounter)
            # if below removes total value from array
            if (weightLineItemQty > lineItemCounter):
                #weightFinalList.pop(weightLineItemQty - 1)
                weightFinalList.pop(-1)
                print(len(weightFinalList))
                print(weightFinalList)
                entry_dict["weight"] = weightFinalList
            # elif below has correct amount of lineItem weight values and lineItems in page
            elif(weightLineItemQty == lineItemCounter):
                print(len(weightFinalList))
                print(weightFinalList)
                entry_dict["weight"] = weightFinalList
            else:
                print("Notify IT of issue.")
        except:
            None

        print("----------- Entering quantity")
        # ------------------------------------------------------------------
        # Get Quantity (part line)
        try:
            twoDecimalNumber = re.findall(r"\s+[\d,]*\.\d\d\s+", text)
            print(len(twoDecimalNumber))
            print(twoDecimalNumber)
            for qty in twoDecimalNumber:
                cleanNewLineCharQty = qty.replace('\n\n','') # removes trailing and leading newLine char from string
                #print(cleanNewLineCharQty)
                qtyFinalList.append(cleanNewLineCharQty)
            print(len(qtyFinalList))
            print(qtyFinalList)
            entry_dict["quantity"] = qtyFinalList
        except:
            None

        print("----------- Entering total price")
        # --------------------------------------------------------------------
        # Get Total Price (part line)

        try:
            # first page findall method will pick up exchange rate in as first element
            # last page findall method will pick up total Commercial Invoice amount
            # when qty is one in line item, it will pick up Unit Price, since findall does not pick up overlapping values
            # Option 1: You can multiply the qty w/ unit price. This will give you Total USD value
            # Observation: findall method only picks up Unit Price. Thus, multiply the unit price * qty to get Total line item Price
            fourDecimalNumber = re.findall(r"\s+[\d,]*\.\d\d\d\d\s+", text)
            print(len(fourDecimalNumber))
            print(fourDecimalNumber)
            iterator = len(fourDecimalNumber) # local int data type value used for multiplication loop
            for price in fourDecimalNumber:
                cleanNewLineCharPrice = price.replace('\n\n','') # removes trailing and leading newLine char from string
                priceBeforeQty.append(cleanNewLineCharPrice)
            print(len(priceBeforeQty))
            print(priceBeforeQty)
            if (newPdfKey != []): # only enters statement when new Invoice found by keyword "Export Commercial Invoice"
                priceBeforeQty.pop(0) # removes exchange rate element appended as first index value
                iterator -= 1 # removes single int value picked up in fourDecimal number
                print("Exchanged Rate Popped")
                print(len(priceBeforeQty))
                print(priceBeforeQty)
                # For single page Inv, you also need to remove the Total Inv value
                if (lineItemCounter < len(priceBeforeQty)):
                    priceBeforeQty.pop(-1)
                    iterator -= 1 # removes single int value picked up in fourDecimal number
                    print("Total Invoice Value Popped")
                    print(len(priceBeforeQty))
                    print(priceBeforeQty)
            lastPageKey = re.findall(r"Alejandra Molina", text) # Alejandra Molina text can only be found in the lastPage of Invoice
            print("If following list contains single element, total value will be popped from list.")
            print(len(lastPageKey))
            print(lastPageKey)
            # Below does not work if totalValue is also included in first page
            if (lastPageKey != []): # only enters statement when in last page of Invoice. All Possible values have been appended into lists
                priceBeforeQty.pop(-1) # removes total value element appended as last index value
                iterator -= 1 # removes single int value picked up in fourDecimal number
                print("Total Value Popped")
                print(len(priceBeforeQty))
                print(priceBeforeQty)
                entry_dict["lastPageKeyValue"] = lastPageKey
            print("Leaving Conditions for last page of Invoice.")
            print(len(priceBeforeQty))
            print(priceBeforeQty)
            # We have the Quantity and Unit Price of each line item
            # Below we need to multiply each element from both list by there same index value.
            # Outcome is total line item Cash amount
            # while loop used for modification values in scope of single page of PDF
            print("Printing iterator lenght amount below.")
            print(iterator) # -------------------------------------------------------------------- only works upto here
            looper = iterator # looper used for conditional control of while loop
            while(iterator > 0):
                noCommaUnitPrice = priceBeforeQty[index4Price].replace(",", "")
                print(noCommaUnitPrice)
                dotDelimitedValues.append(noCommaUnitPrice)
                index4Price += 1 # moves index inside list
                iterator -= 1 # removes int value, thus reaching exit condition for while loop
            print(len(qtyFinalList))
            print(qtyFinalList)
            print(len(dotDelimitedValues))
            print(dotDelimitedValues)
            # while loop used for multiplcation of qty and unitPrice (both same range)
            print(looper)
            while(looper > 0):
                totalLineItemValue = float(qtyFinalList[index4Multi]) * float(dotDelimitedValues[index4Multi])
                print(totalLineItemValue)
                priceFinalList.append(totalLineItemValue)
                index4Multi += 1
                looper -= 1
            print(len(priceFinalList))
            print(priceFinalList)
            entry_dict["finalLinePrice"] = priceFinalList
        except:
            None

        # -----------------------------------------------------
        # Get Signatuere (Alejandra Molina) only present in lastPage of Inv
        try:
            lastPageKey
        except:
            None

        # Appends new entry_dict object into global list
        # Each page gets created as an object
        entry_list.append(entry_dict) # data dictionary appended into list

    # List Object holding all Page Objects gets returned when function called
    return entry_list