# This function will create the XML file with necessary information
def put_infoXML(_company, entry_list, user_input):

    # Check the company // Will expand as more companies are added
    if _company == "Truck-Lite":
        # This data is static for Truck-lite
        company = "Truck Lite S.deRLdeCV"
        company_key = "TRKL2021"
        manuId = "MXTRULIT117CUA"
        module = "CBPENTRY"
        action = "A"
        filer_code = "WF5"
        entry_type = "01"
        mot = "30" 
        customer_key = "004440"
        importer_key = "004440"
        entry_port = "2304"
        location = "V641"
        exp_origen = "MX" 
        deliTerms = "EXW" 
        freighChar = "100"

        # Data Entry data
        sub_value = user_input.get('value')
        sub_weight = user_input.get('weight')
        sub_trailer = user_input.get('trailer')
        sub_invoices = user_input.get('invoice')
        sub_bundles = user_input.get('bundles')
        sub_us_carrier = user_input.get('carrier')
        sub_scac = user_input.get('scac')
        sub_email_date = user_input.get('emailDate')

        # Entries based on information above
        xml_file = open("xml_file.xml", "w+")
        xml_file.write("<Data>\n")
        xml_file.write("\t<ApplicationInformation>\n")
        xml_file.write("\t\t<ImporterName>"+company+"</ImporterName>\n")
        xml_file.write("\t\t<CompanyKey>"+company_key+"</CompanyKey>\n")

        
        xml_file.write("\t\t<Module>"+module+"</Module>\n")
        xml_file.write("\t\t<Action>"+action+"</Action>\n")
        xml_file.write("\t</ApplicationInformation>\n")
        xml_file.write("\t<Entry>\n")
        xml_file.write("\t\t<FilerCode>"+filer_code+"</FilerCode>\n")
        xml_file.write("\t\t<EntryNumber></EntryNumber>\n")
        xml_file.write("\t\t<EntryType>"+entry_type+"</EntryType>\n")
        xml_file.write("\t\t<Mot>"+mot+"</Mot>\n")
        xml_file.write("\t\t<CarrierScac>"+sub_scac+"</CarrierScac>\n")
        xml_file.write("\t\t<CustomerKey>"+customer_key+"</CustomerKey>\n")
        xml_file.write("\t\t<ImporterKey>"+importer_key+"</ImporterKey>\n")
        xml_file.write("\t\t<EntryPort>"+entry_port+"</EntryPort>\n")
        xml_file.write("\t\t<Location>"+location+"</Location>\n")
        xml_file.write("\t\t<EstimatedArrivalDate>"+
                       sub_email_date+"</EstimatedArrivalDate>\n") 
        xml_file.write("\t\t<TrailerNumber>"+sub_trailer+"</TrailerNumber>\n") 
        xml_file.write("\t\t<CustomerRef></CustomerRef>\n")
        xml_file.write("\t\t<BrokerReference></BrokerReference>\n")
        xml_file.write("\t\t\t<EntryInvoices>\n")

        # Entries based of informatione extracted from PDF
        for x in range(len(entry_list)):
            xml_file.write("\t\t\t\t<Invoice>\n")
            # Origin from entry_list
            _origin = entry_list[x].get('origin')
            # Invoice number from entry_list
            _invoice_num = entry_list[x].get('invoiceNum')
            # Date from entry_list
            _date = entry_list[x].get('date')
            # Product Key from entry_list
            _product_key = entry_list[x].get('productKey')
            # Quantity from entry_list
            _quantity = entry_list[x].get('quantity')
            # Product Name from entry_list
            _product_name = entry_list[x].get('productName')
            # Total from entry_list
            _total = entry_list[x].get('total')
            # Product description from entry_list
            _description = entry_list[x].get('description')
            # End of entry_list information

            # entry_list information input into XML
            xml_file.write("\t\t\t\t\t<InvoiceNumber>"+
                           _invoice_num+"</InvoiceNumber>\n")
            xml_file.write("\t\t\t\t\t<Division></Division>\n")
            xml_file.write("\t\t\t\t\t<SoldTo>"+importer_key+"</SoldTo>\n") 
            xml_file.write("\t\t\t\t\t<ConsigneeKey>"+importer_key+"</ConsigneeKey>\n") 
            xml_file.write("\t\t\t\t\t<ConsigneeTaxId></ConsigneeTaxId>\n")
            xml_file.write("\t\t\t\t\t<ConsigneeName></ConsigneeName>\n")
            xml_file.write("\t\t\t\t\t<ConsigneeAddress></ConsigneeAddress>\n")
            xml_file.write("\t\t\t\t\t<ConsigneeCity></ConsigneeCity>\n")
            xml_file.write("\t\t\t\t\t<ConsigneeState></ConsigneeState>\n")
            xml_file.write(
                "\t\t\t\t\t<ConsigneeZipcode></ConsigneeZipcode>\n")
            xml_file.write("\t\t\t\t\t<InvoiceDate>"+_date+"</InvoiceDate>\n")
            xml_file.write("\t\t\t\t\t<ManufactureId>"+manuId+"</ManufactureId>\n")
            xml_file.write(
                "\t\t\t\t\t<QuantityPackages UNIT=\"BDL\" Quantity=\""+sub_bundles+"\" />\n")
            xml_file.write("\t\t\t\t\t<DeliveryTerms>"+deliTerms+"</DeliveryTerms>\n") 
            xml_file.write("\t\t\t\t\t<FreightCharges>"+freighChar+"</FreightCharges>\n") 
            xml_file.write("\t\t\t\t\t<InvoiceLine>\n")
            xml_file.write("\t\t\t\t\t\t<ProductKey>"+_product_key+"</ProductKey>\n") 
            xml_file.write("\t\t\t\t\t\t<ProductName>"+_description+"</ProductName>\n") ##################
            xml_file.write("\t\t\t\t\t\t<CountryOfOrigin>"+_origin+"</CountryOfOrigin>\n") 
            xml_file.write("\t\t\t\t\t\t<CountryOfExport>"+exp_origen+"</CountryOfExport>\n")
            xml_file.write(
                "\t\t\t\t\t\t<Quantity UNIT = \"PZ\" Quantity = \""+_quantity+"\" />\n")
            xml_file.write("\t\t\t\t\t\t<HtsForProduct></HtsForProduct>\n")
            xml_file.write("\t\t\t\t\t\t<HtsProductValue>"+_total+"</HtsProductValue>\n")
            xml_file.write("\t\t\t\t\t\t<ProductWeight></ProductWeight>\n")
            xml_file.write("\t\t\t\t\t\t<Serials></Serials>\n")
            xml_file.write("\t\t\t\t\t</InvoiceLine>\n")
            xml_file.write("\t\t\t\t</Invoice>\n")
        xml_file.write("\t\t\t</EntryInvoices>\n")
        xml_file.write("\t</Entry>\n")
        xml_file.write("</Data>\n")
        xml_file.close()
    
    if _company == "Hussmann":
        print("Below we print complete list with page/objects.")
        print(entry_list)
        for j in range(len(entry_list)):
            # Below gets number of pages / invoice
            _pageAmount_perInvoice = entry_list[j].get('invoicePages')
            # Skips none 1st page related information
            if (_pageAmount_perInvoice == None):
                print("Not first page/object of Invoice")
            # extracts 1st page related information
            elif (_pageAmount_perInvoice != None):
                print("Page amount of current Invoice below.")
                print(_pageAmount_perInvoice)
                # Below gets two items that are needed for first block of XML
                customer_key = entry_list[j].get('referencia') # Referencia: RE, KR ....
                importer_key = entry_list[j].get('consignee') # Sold to: cx

        # This data is static for Hussmann
        company = "HUSSMANN AMERICAN, S. DE R.L. DE C.V."
        company_key = "ComKey" # getReynaldo
        manuId = "MXHUSAME1009CIE" #lineItem
        module = "CBPENTRY"
        action = "A"
        filer_code = "WF5"
        entry_type = "01"
        mot = "30" 
        entry_port = "2304"
        location = "V641"
        exp_origen = "MX" #lineItem
        deliTerms = "EXW"
        freighChar = "150"

        # Data Entry data
        sub_value = user_input.get('value')
        sub_weight = user_input.get('weight')
        sub_trailer = user_input.get('trailer')
        sub_invoices = user_input.get('invoice')
        sub_bundles = user_input.get('bundles')
        sub_us_carrier = user_input.get('carrier')
        sub_scac = user_input.get('scac')
        sub_email_date = user_input.get('emailDate')

        # Entries based on information above
        xml_file = open("xml_file.xml", "w+")
        xml_file.write("<Data>\n")
        xml_file.write("\t<ApplicationInformation>\n")
        xml_file.write("\t\t<ImporterName>"+company+"</ImporterName>\n")
        xml_file.write("\t\t<CompanyKey>"+company_key+"</CompanyKey>\n")
        xml_file.write("\t\t<Module>"+module+"</Module>\n")
        xml_file.write("\t\t<Action>"+action+"</Action>\n")
        xml_file.write("\t</ApplicationInformation>\n")
        xml_file.write("\t<Entry>\n")
        xml_file.write("\t\t<FilerCode>"+filer_code+"</FilerCode>\n")
        xml_file.write("\t\t<EntryNumber></EntryNumber>\n")
        xml_file.write("\t\t<EntryType>"+entry_type+"</EntryType>\n")
        xml_file.write("\t\t<Mot>"+mot+"</Mot>\n")
        xml_file.write("\t\t<CarrierScac>"+sub_scac+"</CarrierScac>\n")
        xml_file.write("\t\t<CustomerKey>"+customer_key+"</CustomerKey>\n")
        xml_file.write("\t\t<ImporterKey>"+importer_key+"</ImporterKey>\n")
        xml_file.write("\t\t<EntryPort>"+entry_port+"</EntryPort>\n")
        xml_file.write("\t\t<Location>"+location+"</Location>\n")
        xml_file.write("\t\t<EstimatedArrivalDate>"+
                       sub_email_date+"</EstimatedArrivalDate>\n") 
        xml_file.write("\t\t<TrailerNumber>"+sub_trailer+"</TrailerNumber>\n") 
        xml_file.write("\t\t<CustomerRef></CustomerRef>\n")
        xml_file.write("\t\t<BrokerReference></BrokerReference>\n")
        xml_file.write("\t\t\t<EntryInvoices>\n")
        
        # Entries based of information extracted from PDF
        for x in range(len(entry_list)):
            # the x itself is a number starting at 0
            # information below can only be found in the first page
            _invoice_page_count = entry_list[x].get('invoicePages')
            _importer_nameHus = entry_list[x].get('importerName') # USED FOR COMBINATION
            _invoice_numberHus = entry_list[x].get('invoiceNumber')
            _dateHus = entry_list[x].get('date')
            _consigneeHus = entry_list[x].get('consignee') # USED FOR COMBINATION
            _referenciaHus = entry_list[x].get('referencia') # USED FOR COMBINATION
            _po_numberHus = entry_list[x].get('poNumber') # ASK REYNALDO
            _bultosHus = entry_list[x].get('bultos')
            # information above can be found on both pages
            _lineItemCounter = entry_list[x].get('lineAmount')
            _product_keyArray = entry_list[x].get('productKey')
            _orginHusArray = entry_list[x].get('orgins')
            _weightHusArray = entry_list[x].get('weight')
            _quantityHusArray = entry_list[x].get('quantity')
            _invLastPageKey = entry_list[x].get('lastPageKeyValue')
            _finalLinePriceArray = entry_list[x].get('finalLinePrice')

            # Entry_list information input upto not including <InvoiceLine> into XML
            if (_invoice_page_count != None):
                xml_file.write("\t\t\t\t<Invoice>\n")
                xml_file.write("\t\t\t\t\t<InvoiceNumber>"+
                            _invoice_numberHus+"</InvoiceNumber>\n")
                xml_file.write("\t\t\t\t\t<Division></Division>\n")
                xml_file.write("\t\t\t\t\t<SoldTo>"+importer_key+"</SoldTo>\n") 
                xml_file.write("\t\t\t\t\t<ConsigneeKey>"+importer_key+"</ConsigneeKey>\n")
                xml_file.write("\t\t\t\t\t<ConsigneeTaxId></ConsigneeTaxId>\n")
                xml_file.write("\t\t\t\t\t<ConsigneeName></ConsigneeName>\n")
                xml_file.write("\t\t\t\t\t<ConsigneeAddress></ConsigneeAddress>\n")
                xml_file.write("\t\t\t\t\t<ConsigneeCity></ConsigneeCity>\n")
                xml_file.write("\t\t\t\t\t<ConsigneeState></ConsigneeState>\n")
                xml_file.write(
                    "\t\t\t\t\t<ConsigneeZipcode></ConsigneeZipcode>\n")
                xml_file.write("\t\t\t\t\t<InvoiceDate>"+_dateHus+"</InvoiceDate>\n")
                xml_file.write("\t\t\t\t\t<ManufactureId>"+manuId+"</ManufactureId>\n")
                xml_file.write(
                    "\t\t\t\t\t<QuantityPackages UNIT=\"BDL\" Quantity=\""+_bultosHus+"\" />\n")
                xml_file.write("\t\t\t\t\t<DeliveryTerms>"+deliTerms+"</DeliveryTerms>\n") 
                xml_file.write("\t\t\t\t\t<FreightCharges>"+freighChar+"</FreightCharges>\n")
            elif(_invoice_page_count == None):
                print("Below printing the lineItem counter for current page.")
                print(_lineItemCounter)
                # if statement below will be used to identify the last inv object by unique key-value pair
                if (_invLastPageKey != None):
                    print(_lineItemCounter)
                    lineCounterLooper = _lineItemCounter
                    # loop below will be used to create multiple lineItem blocks inside invoice tag
                    for y in range(_lineItemCounter): # index starts at 0
                        lineCounterLooper -= 1
                        print(lineCounterLooper)

                        _product_key = _product_keyArray[y]
                        _orginHus = _orginHusArray[y]
                        _weightHus = _weightHusArray[y]
                        _quantityHus = _quantityHusArray[y]
                        _finalLinePriceHus = _finalLinePriceArray[y]

                        xml_file.write("\t\t\t\t\t<InvoiceLine>\n")
                        xml_file.write("\t\t\t\t\t\t<ProductKey>"+_product_key+"</ProductKey>\n") 
                        xml_file.write("\t\t\t\t\t\t<ProductName>""</ProductName>\n") 
                        xml_file.write("\t\t\t\t\t\t<CountryOfOrigin>"+_orginHus+"</CountryOfOrigin>\n") 
                        xml_file.write("\t\t\t\t\t\t<CountryOfExport>"+exp_origen+"</CountryOfExport>\n")
                        xml_file.write(
                            "\t\t\t\t\t\t<Quantity UNIT = \"PZ\" Quantity = \""+_quantityHus+"\" />\n")
                        xml_file.write("\t\t\t\t\t\t<HtsForProduct></HtsForProduct>\n")
                        xml_file.write("\t\t\t\t\t\t<HtsProductValue>"+str(_finalLinePriceHus)+"</HtsProductValue>\n")
                        xml_file.write("\t\t\t\t\t\t<ProductWeight>"+_weightHus+"</ProductWeight>\n")
                        xml_file.write("\t\t\t\t\t\t<Serials></Serials>\n")
                        xml_file.write("\t\t\t\t\t</InvoiceLine>\n")
                        if (lineCounterLooper == 0):
                            xml_file.write("\t\t\t\t</Invoice>\n")

        xml_file.write("\t\t\t</EntryInvoices>\n")
        xml_file.write("\t</Entry>\n")
        xml_file.write("</Data>\n")
        xml_file.close()

