from datetime import datetime, timedelta
import numpy as np
import os
import pdfplumber
import re
from sqlite3 import Error
import sqlite3


def find_page(pdf2read):
        pages = pdf2read.pages

        for index,pg in enumerate(pages):
            rows = pages[index].extract_text().split('\n')
            print ("[INFO] Searching on", pg)
            #print(rows, "\n")
            #Find the string below in one of the pdf pages
            if any("ΠΕΡΙΦΕΡΕΙΑΚΗ ΕΝΟΤΗΤΑ" in words for words in rows):
                return (index)
        return (-1)


def create_list(elements, current_date):
    #enumerating the list to find the first float after a string
    float_positions = []
    for idx, items in enumerate(elements):
         try :
             if float(elements[idx]):
                float_positions.append(idx)
         except ValueError:
             continue
    #Sorting through the first half of the line and creating a list
    L1 = []
    L2 = []

    if float_positions != []:
        if float_positions[0] == 1:
            regional_unit = ''.join(elements[float_positions[0] - 1])
        elif float_positions[0] == 2:
            regional_unit = elements[float_positions[0] - 2] + ' ' + elements[float_positions[0] - 1]
        elif float_positions[0] == 3:
            regional_unit = elements[float_positions[0] - 3] + ' ' + elements[float_positions[0] - 2] + ' ' + elements[float_positions[0] - 1]
        L1.insert(0, regional_unit)
        L1.insert(1, elements[float_positions[0]])
        L1.insert(2, elements[float_positions[0] + 1])
        L1.insert(3, elements[float_positions[0] + 2])
        L1.insert(4, current_date)

        #Sorting through the second half of the line and creating a list
        if len(float_positions) == 6:
            diff = float_positions[3] - float_positions[0]
            if diff == 4:
                regional_unit = ''.join(elements[float_positions[3] - 1])
            elif diff == 5:
                regional_unit = elements[float_positions[3] - 2] + ' ' + elements[float_positions[3] - 1]
            elif diff == 6:
                regional_unit = elements[float_positions[3] - 3] + ' ' + elements[float_positions[3] - 2] + ' ' + elements[float_positions[3] - 1]
            L2.insert(0, regional_unit)
            L2.insert(1, elements[float_positions[3]])
            L2.insert(2, elements[float_positions[3] + 1])
            L2.insert(3, elements[float_positions[3] + 2])
            L2.insert(4, current_date)
            #Add each list to the List of Lists
            final_list.insert(0, L2)
        final_list.insert(0, L1)

    if float_positions == []:
        print("[INFO] Unable to find float positions")
        return()


def ymd(fname, format):

    int_position = []
    array = re.split(r'-|\.', fname)
    for idx, items in enumerate(array):
         try :
             if int(array[idx]):
                int_position.append(idx)
         except ValueError:
             continue

    YMD_dt = array[idx - 1][0:4] + "-" + array[idx - 1][4:6] + "-" + array[idx -1][6:8]

    if format == "filename":
        YMD_dt = YMD_dt.replace('-', '')
    elif format == "dt":
        return(YMD_dt)
    elif format == "url":
        YMD_dt = YMD_dt.replace('-', '/')
    else:
        YMD_dt = YMD_dt.replace('-', '\\')
    return(YMD_dt)


def sql_connection():
    try:
        con = sqlite3.connect('gr-covid.db')
        return con
    except Error:
        print('[ERROR] SQLite3 Connection Error: {}'.format(Error))


def sql_table(con):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("CREATE TABLE if not exists summary(id integer PRIMARY KEY autoincrement, region text, cases integer, avg7day real, per100k real, dt date)")
        con.commit()
        print('[INFO] sqlite3: Table \'summary\' has been created or already exists.')
    except Error:
        print('[ERROR] SQLite3 Execution Error: {}'.format(Error))
        print('[INFO] Please check the sqlite3 Database file.')
        print('[INFO] Exiting the application.')
        exit()


def sql_insert(con):
    try:
        cursorObj = con.cursor()
        cursorObj.executemany("INSERT INTO summary VALUES(null, ?, ?, ?, ?, ?)", final_list)
        con.commit()
    except Error:
        print('[ERROR] SQLite3 Insert Records Error: {}'.format(Error))



if __name__ == '__main__':

    con = sql_connection()
    sql_table(con)

    path = "./pdfs"
    files = os.listdir(path)

    for f in files:
        final_list = []

        with pdfplumber.open('pdfs/' + f) as pdf:#'pdfs/covid-gr-daily-report-' + YMD + '.pdf') as pdf:
            print('[INFO] Opening pdfs/' + f)
            #print('[INFO] Opening pdfs/covid-gr-daily-report-' + YMD + '.pdf')
            print('[INFO] Searching for the Coronavirus table...')
            page_num = find_page(pdf)

            if page_num < 0:
                print("[WARN] Table not found in current pdf document!")
                pdf.close()
                exit()
            else:
                print("[INFO] Table found on <Page:" + str(page_num + 1) + ">")

            print("[INFO] Extracting text found on <Page:" + str(page_num + 1) + ">")
            page = pdf.pages[page_num]
            text = page.extract_text()
            #print(":::::::::::::::::::::::::::::::::::::::::::::::: Extracted Text :::::::::::::::::::::::::::::::::::::::::::::::::")
            #print(text)
            #print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

            # #Testing with numpy arrays#
            # table = page.extract_table()
            # print(table)
            # nplist = np.array([linez.split('\n') for linez in table[2]])
            # new_nplist = nplist.flatten()
            # ###########################
            # print("----------------------------------------------------------------------------------------")
            # print(new_nplist)
            # print("----------------------------------------------------------------------------------------")
            # ###########################

            print("[INFO] Regex matching on text extracted from the table")
            regex = re.compile(r'(^\w+) (\d+|-?\w+) (\d+[,.]?\d{0,2}|\w+) ?(\d+[,.]?\d+) ?(\d+[,.]?\d+|) ?(\d+[,.]\d+|)')

            for line in re.split('\n', text):
                if regex.match(line):
                    #Some pdfs need a bit of a clean up
                    clean_up = line.replace("  ", " ")
                    replaced_line = clean_up.replace(",", ".")

                    found = replaced_line.find('ΥΠΟ ΔΙΕΡΕΥΝΗΣΗ')
                    #If the string is not found at the start of the line.
                    if found > 0:
                        ui_record = replaced_line[found:]
                        replaced_line = replaced_line[:found]
                        ui_record = ui_record + " 0 0"
                        ui_record = ui_record.split(' ')
                        create_list(ui_record, ymd(f, "dt"))

                    #Splitting up each line and placing it in an array
                    if (len(replaced_line.split()) >= 4) and (len(replaced_line.split()) <= 6):
                        result = re.split(r'(^\w+) (\d+|-?\w+) (\d+\.?\d+|\w+) ?(\d+\.?\d+) ?(\d+\.?\d+|) ?(\d+\.?\d+|)', replaced_line)
                    else:
                        result = re.split(r'^(\w+) (\d+|-?\w+) (\d+\.?\d{0,2}|\w+) (\d+\.?\d+) (\d+\.\d+|) ?(\d+\.\d+|) ?(\w+) (\d+|-?\w+) (\d+\.?\d{0,2}|\w+) (\d+\.?\d+) ?(\d+\.\d+|) ?(\d+\.\d+|) ?',replaced_line)

                    #Remove all empty elements from the list
                    clean_list = [elmnt for elmnt in result if elmnt != ""]
                    create_list(clean_list, ymd(f, "dt"))
                else:
                    print("[WARN] The line below does not match.")
                    print("[WARN]", line)
        pdf.close()

        #final_list.insert(0, ["Regional Unit", "Cases", "7 Day Average", "Cases/100,000 ppl", "Date"])

        np_array = np.array(final_list)
        print("===================================== Array of Extracted Data =====================================\n", np_array)#final_list)
        print("=============================== Number of Regions:", len(final_list), "===============================")

        #Time to insert records into the database!
        sql_insert(con)

        #Returns a list based on a regional search string
        search_item = "ΖΑΚΥΝΘΟΥ"#"ΒΟΡΕΙΟΥ ΤΟΜΕΑ ΑΘΗΝΩΝ"#"ΛΕΣΒΟΥ"#"ΝΟΤΙΟΥ ΤΟΜΕΑ ΑΘΗΝΩΝ"
        for sublist in final_list:
            if sublist[0] == search_item:
                #print('{0:25} {1:8} {2:15} {3:18} {4:10}'.format(final_list[0][0], final_list[0][1], final_list[0][2], final_list[0][3], final_list[0][4]))
                print('{0:25} {1:8} {2:15} {3:18} {4:10}'.format("Region", "Cases", "7 Day Average", "Cases/100,000 ppl", "Date"))
                print('{0:25} {1:8} {2:15} {3:18} {4:10}'.format(sublist[0], sublist[1], sublist[2], sublist[3], sublist[4]))
                break
    con.close()
