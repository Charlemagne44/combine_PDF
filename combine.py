import os
import PyPDF2
from tkinter import filedialog
from tkinter import *


def mergePDF(pdfs: tuple, output: str):
    pdfMerger = PyPDF2.PdfMerger()
    for pdf in pdfs:
        pdfMerger.append(pdf)
        with open(output, "wb") as f:
            pdfMerger.write(f)


def main():
    # file dialog to select all PDFs
    pdf_files = filedialog.askopenfilenames(
        multiple=True, title="Choose PDF files to Merge"
    )
    print(f"folder path: {pdf_files}")

    dest_folder = filedialog.askdirectory(
        title="Choose the destination for the merged files"
    )
    print(f"dest folder: {dest_folder}")

    # gather the list of non FD files
    non_fd_list = []
    for pdf in pdf_files:
        if "fd" not in pdf.lower():
            non_fd_list.append(pdf)

    # create the pairings iteratively, and before merging check and make sure it exists
    for pdf in non_fd_list:
        non_fd_filename = pdf.split("/")[-1]
        num = non_fd_filename[:6]
        fd_filename = f"{num}fd.pdf"
        fd_path = ""
        for all_pdf in pdf_files:
            if fd_filename == all_pdf.split("/")[-1]:
                fd_path = all_pdf
        if not fd_path:
            print(
                f"Partnered fd file: {fd_filename} does not exist in the supplied PDF files"
            )
            continue

        new_output = f"{dest_folder}/{num}-merged.pdf"
        mergePDF((pdf, fd_path), new_output)
        print(f"file pairing: {(pdf, fd_path)}")
        print(f"result written to {new_output}")

    input("Press Enter to Exit")  # wait for user input to close the session


if __name__ == "__main__":
    main()
