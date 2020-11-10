import os
import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter
import glob

def cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('pdf_folder', type=str)
    parser.add_argument('output', type=str)
    return parser.parse_args()

def rotate_pages(pdf_path):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(pdf_path)
    # Rotate page 90 degrees to the right
    page_1 = pdf_reader.getPage(0).rotateClockwise(90)
    pdf_writer.addPage(page_1)
    # Rotate page 90 degrees to the left
    page_2 = pdf_reader.getPage(1).rotateCounterClockwise(90)
    pdf_writer.addPage(page_2)
    # Add a page in normal orientation
    pdf_writer.addPage(pdf_reader.getPage(2))

    with open('rotate_pages.pdf', 'wb') as fh:
        pdf_writer.write(fh)


def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        print('Merging pdf {}'.format(path))
        pdf_reader = PdfFileReader(path)
        pdf_writer.addPage(pdf_reader.getPage(0))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    print(txt)
    return information

def main():
    print('Merge tool')
    args = cmd()
    print(args)
    files = glob.glob(os.path.join(args.pdf_folder, '*.pdf'))
    merge_pdfs(files, args.output)
    print("Done.")

if __name__ == '__main__':
    main()