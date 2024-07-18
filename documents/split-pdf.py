import PyPDF2
import os


def split_pdf(input_file):
    # Check if the file exists
    if not os.path.isfile(input_file):
        print(f"The file {input_file} does not exist.")
        return

    # Open the PDF file
    with open(input_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Get the total number of pages
        num_pages = len(pdf_reader.pages)
        base_filename = os.path.splitext(input_file)[0]

        # Loop through all the pages and save each as a new PDF
        for page_num in range(num_pages):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])

            output_filename = f"{base_filename}_{page_num + 1}.pdf"
            with open(output_filename, 'wb') as output_pdf_file:
                pdf_writer.write(output_pdf_file)
                print(f"Created: {output_filename}")


if __name__ == "__main__":
    input_file = 'vessel_documents.pdf'  # Change this to your PDF file name
    split_pdf(input_file)
