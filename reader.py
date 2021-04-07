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

def split_items():
    return (1)


if __name__ == '__main__':

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
            print("TEXT--------------:", line)
            if regex.match(line):
                print("Line match:", line)

                replaced_line = line.replace(",", ".")


                print ("THIS IS THE LENGTH OF LINE: ", len(line))
                print ("THIS IS THE LENGTH OF REPLACED_LINE: ", len(replaced_line))

                print (regex.match(replaced_line).group(2))

                try :
                    print (float(regex.match(replaced_line).group(2)))
                except ValueError:
                    print ("NOT A FLOAT")
                # if isinstance(regex.match(line).group(2), int):
                #     print("INT")
                # if isinstance(regex.match(line).group(2), str):
                #     print("STR")
                # if isinstance(regex.match(line).group(2), float):
                #     print("FLOAT")

                #print("str:", str)

                cases = line.split(' ')[1]
                avg = line.split(' ')[2]
                hungyk = line.split(' ')[3]
                #print("Coronavirus Cases: ", cases)
                #print("7 Day Case Average:", avg)
                #print("Cases/100,000 ppl: ", hungyk)

                #Splitting up each line and placing it in an array
                result = re.split(r'^([Α-ΩΪ]+) (\d+|[Α-Ω]+) (\d+.?\d+|[Α-Ω]+) (\d+.?\d+) (\d+.?\d+|) ?(\d+.?\d+|) ?', replaced_line)

                print ("THIS IS THE LENGTH OF RESULT: ", len(result))

                print("Array:", result)
            else:
                print("[INFO] This line isn't a match!")
    pdf.close()
