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
    #print(float_positions)

    LoL = []
    L1 = []
    L2 = []
    #Sorting through the first half of the list
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

        #Sort through the second half of the list
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


        LoL = [L1 , L2]
        print(LoL)

    if float_positions == []:
         return (LoL)
    else:
         return(LoL)


if __name__ == '__main__':

    new_list = []
    with pdfplumber.open('pdfs/covid-gr-daily-report-20210405.pdf') as pdf:

        page_num = find_page(pdf)
        if page_num < 0:
            print("[WARN] Table not found in current pdf dcoument!")
            pdf.close()
            exit()
        else:
            print("[INFO] Table found on page:", page_num + 1, "\n")

        page = pdf.pages[page_num]
        text = page.extract_text()

        regex = re.compile(r'^([Α-ΩΪ]+) (\d+|[Α-Ω]+) (\d+.?\d+|[Α-Ω]+) (\d+.?\d+) (\d+.?\d+|) ?(\d+.?\d+|) ?')

        for line in re.split('\n', text):
            #print("TEXT--------------:", line)
            if regex.match(line):
                #print("Line match:", line)

                #replaced_line = line.replace(",", ".")


                #print ("THIS IS THE LENGTH OF LINE: ", len(line))
                #print ("THIS IS THE LENGTH OF REPLACED_LINE: ", len(replaced_line))

                cases = line.split(' ')[1]
                avg = line.split(' ')[2]
                hungyk = line.split(' ')[3]
                #print("Coronavirus Cases: ", cases)
                #print("7 Day Case Average:", avg)
                #print("Cases/100,000 ppl: ", hungyk)

                #Splitting up each line and placing it in an array
                #result = re.split(r'^([Α-ΩΪ]+) (\d+|[Α-Ω]+) (\d+,?\d+|[Α-Ω]+) (\d+,?\d+) (\d+,?\d+|) ?(\d+,?\d+|) ?([Α-ΩΪ]+) (\d+|[Α-Ω]+) (\d+,?\d+|[Α-Ω]+) (\d+,?\d+|) ?(\d+,\d+|) ?(\d+,\d+|)', line)
                result = re.split(r'(^\w+) (\d+|\w+) (\d+,?\d+|\w+) (\d+,?\d+) (\d+,?\d+|) ?(\d+,?\d+|) ?(\w+) (\d+|\w+) (\d+,?\d+|\w+) (\d+,?\d+) ?(\d+,\d+|) ?(\d+,\d+|)', line)
                #print ("THIS IS THE LENGTH OF RESULT: ", len(result))

                clean_list = [elmnt for elmnt in result if elmnt != ""]

                new_list.append(create_list(clean_list))

            else:
                print("[WARN] The following line is not a match!")
                print(line)
    pdf.close()

    print(new_list)
