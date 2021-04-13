from datetime import datetime, timedelta
import numpy as np
import pdfplumber
import re

def find_page(pdf2read):

        pages = pdf2read.pages
        #regex = ".*(ΖΑΚΥΝΘΟΥ).*"

        for index,pg in enumerate(pages):
            rows = pages[index].extract_text().split('\n')
            print ("-------------------", pg, "-------------------")
            print(rows, "\n")
            #Find the string below in one of the pdf pages
            if any("ΠΕΡΙΦΕΡΕΙΑΚΗ ΕΝΟΤΗΤΑ" in words for words in rows):
                #regex.search(rows):
                return (index)
        return (-1)

def create_list(elements):
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

        #Sorting through the second half of the line and creating a list
        if len(float_positions) == 2:
            diff = float_positions[1] - float_positions[0]
            if diff == 4:
                regional_unit = ''.join(elements[float_positions[1] - 1])
            elif diff == 5:
                regional_unit = elements[float_positions[1] - 2] + ' ' + elements[float_positions[1] - 1]
            elif diff == 6:
                regional_unit = elements[float_positions[1] - 3] + ' ' + elements[float_positions[1] - 2] + ' ' + elements[float_positions[1] - 1]

            L2.insert(0, regional_unit)
            L2.insert(1, elements[float_positions[1]])
            L2.insert(2, elements[float_positions[1] + 1])
            L2.insert(3, elements[float_positions[1] + 2])

        #Add each list to the List of Lists
            final_list.insert(0, L2)

        final_list.insert(0, L1)

    if float_positions == []:
         return ()

def ymd():
    now = datetime.now() + timedelta(days=-1)
    year = str(now.year)

    if now.month < 10:
        month = "0" + str(now.month)
    else:
        month = str(now.month)

    if now.day < 10:
        day = "0" + str(now.day)
    else:
        day = str(now.day)

    YMD = year + month + day

    return(YMD)

if __name__ == '__main__':

    YMD = ymd()

    final_list = []
    with pdfplumber.open('pdfs/covid-gr-daily-report-' + YMD + '.pdf') as pdf:
        page_num = find_page(pdf)
        if page_num < 0:
            print("[WARN] Table not found in current pdf document!")
            pdf.close()
            exit()
        else:
            print("[INFO] Table found on page:", page_num + 1, "\n")

        page = pdf.pages[page_num]
        text = page.extract_text()

        print(":::::::::::::::::::::::::::::::::::::::::::::::: Extracted Text :::::::::::::::::::::::::::::::::::::::::::::::::")
        print(text)
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
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

        regex = re.compile(r'(^\w+) (\d+|-?\w+) (\d+,?\d{0,2}|\w+) ?(\d+,?\d+) ?(\d+,?\d+|) ?(\d+,\d+|)')

        for line in re.split('\n', text):
            if regex.match(line):
                #replaced_line = line.replace(",", ".")

                #Splitting up each line and placing it in an array
                if (len(line.split()) >= 4) and (len(line.split()) <= 6):
                    result = re.split(r'(^\w+) (\d+|\w+) (\d+,?\d+|\w+) ?(\d+,?\d+) ?(\d+,?\d+|) ?(\d+,?\d+|)', line)
                else:
                    result = re.split(r'^(\w+) (\d+|-?\w+) (\d+,?\d{0,2}|\w+) (\d+,?\d+) (\d+,\d+|) ?(\d+,\d+|) ?(\w+) (\d+|-?\w+) (\d+,?\d{0,2}|\w+) (\d+,?\d+) ?(\d+,\d+|) ?(\d+,\d+|) ?',line)

                #Remove all empty elements from the list
                clean_list = [elmnt for elmnt in result if elmnt != ""]
                create_list(clean_list)
            else:
                print("[WARN] The following line is not a match!")
                print(line)
    pdf.close()

    final_list.insert(0, ["Regional Unit", "Cases", "7 Day Average", "Cases/100,000 ppl"])

    np_array = np.array(final_list)
    print("===================================================================================\n", np_array)#final_list)
    print("=============================== Number of Lists:", len(final_list), "===============================")

    #Returns a list based on a regional search string
    search_item = "ΒΟΡΕΙΟΥ ΤΟΜΕΑ ΑΘΗΝΩΝ"#"ΛΕΣΒΟΥ"#"ΝΟΤΙΟΥ ΤΟΜΕΑ ΑΘΗΝΩΝ"
    for sublist in final_list:
        if sublist[0] == search_item:
            print('{0:25} {1:8} {2:15} {3:15}'.format(final_list[0][0], final_list[0][1], final_list[0][2], final_list[0][3]))
            print('{0:25} {1:8} {2:15} {3:15}'.format(sublist[0], sublist[1], sublist[2], sublist[3]))
            break
