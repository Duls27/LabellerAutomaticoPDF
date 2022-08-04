import os
from pikepdf import Pdf
from pdf2image import convert_from_path
import tempfile, cv2, numpy as np
import pytesseract

poppler_path=r"C:\Program Files (x86)\Release-22.04.0-0\poppler-22.04.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def get_split_and_names():
    cut_idxs=[]
    name_docs=[]
    images = convert_from_path(path_pdf, poppler_path=poppler_path)
    for i in range(len(images)):
        file_name = str(temp_dir.name) + '\\' + str(i) + '.jpg'
        images[i].save(file_name, 'JPEG')

        img = cv2.imread(file_name)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img)

        if "TITLE" in text:
            splitted = text.split(sep="\n")
            for idx, line in enumerate(splitted):
                if "TITLE" in line:
                    cut_idxs.append(i)
                    name_docs.append(splitted[idx - 2])
    return cut_idxs, name_docs

def split_pdf ():
    pdf = Pdf.open(path_pdf)
    file2pages={}
    for j in range(len(cut_idxs)):
        if j + 1 < len(cut_idxs):
            file2pages[j] = [cut_idxs[j], cut_idxs[j + 1]]
        else:
            file2pages[j] = [cut_idxs[j], len(pdf.pages)]

    new_pdf_files = [Pdf.new() for i in file2pages]
    new_pdf_index = 0

    for n, page in enumerate(pdf.pages):
        if n in list(range(*file2pages[new_pdf_index])):
            # add the `n` page to the `new_pdf_index` file
            new_pdf_files[new_pdf_index].pages.append(page)
            print(f"[*] Assigning Page {n} to the file {new_pdf_index}")
        else:
            output_filename = to + "\\" + name_docs[new_pdf_index] + ".pdf"
            # save the PDF file
            new_pdf_files[new_pdf_index].save(output_filename)
            print(f"[+] File: {output_filename} saved.")
            # go to the next file
            new_pdf_index += 1
            # add the `n` page to the `new_pdf_index` file
            new_pdf_files[new_pdf_index].pages.append(page)
            print(f"[*] Assigning Page {n} to the file {new_pdf_index}")

    # save the last PDF file
    output_filename = to + "\\" + name_docs[new_pdf_index] + ".pdf"
    new_pdf_files[new_pdf_index].save(output_filename)
    print(f"[+] File: {output_filename} saved.")

if __name__ == "__main__":
    # parameter variables
    temp_dir = tempfile.TemporaryDirectory()
    path_pdf = r"C:\Users\simon\Desktop\scan\DOC040822-04082022154311.pdf"
    to = "C:/Users/simon/Desktop/scan/renamed/"

    cut_idxs, name_docs= get_split_and_names()
    split_pdf()

    temp_dir.cleanup()