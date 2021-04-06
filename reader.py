import pdfplumber
import re

def find_page(pdf2read):

        pages = pdf2read.pages
        regex = ".*(ΖΑΚΥΝΘΟΥ).*"

        for index,pg in enumerate(pages):
            rows = pages[index].extract_text().split('\n')
            print ("-------------------", pg, "-------------------")
            print(rows)
            #if search in rows:
            if any("ΠΕΡΙΦΕΡΕΙΑΚΗ ΕΝΟΤΗΤΑ" in words for words in rows):
                #regex.search(rows):
                return (index)
        return (-1)


if __name__ == '__main__':

    with pdfplumber.open('pdfs/covid-gr-daily-report-20210405.pdf') as pdf:

        page_num = find_page(pdf)
        if page_num < 0:
            print("[INFO] Table not found in current pdf dcoument!")
            pdf.close()
            exit()
        else:
            print("[INFO] Text found on page:", page_num + 1)

        page = pdf.pages[page_num]
        text = page.extract_text()

        site = re.compile(r'^([Α-ΩΪ]+) ([0-9]+|[Α-Ω]+) ([0-9]+,?[0-9]+|[Α-Ω]+) ([0-9]+,?[0-9]+)')

        for line in text.split('\n'):
            if site.match(line):
                print(line)

                str = line.replace(",", ".")
                print(str)

                cases = line.split(' ')[1]
                avg = line.split(' ')[2]
                hungyk = line.split(' ')[3]
                print("Coronavirus Cases: ", cases)
                print("7 Day Case Average:", avg)
                print("Cases/100,000 ppl: ", hungyk)

                result = re.split(r'^([Α-ΩΪ]+) ([0-9]+|[Α-Ω]+) ([0-9]+,?[0-9]+|[Α-Ω]+) ([0-9]+,?[0-9]+) ([0-9]+,?[0-9]+|) ?([0-9]+,?[0-9]+|)', line)
                print("Array:", result)
    pdf.close()
