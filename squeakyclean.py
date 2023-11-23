import os
import piexif
from docx import Document
import PyPDF2

def remove_image_metadata(image_path):
    try:
        # Read image metadata
        exif_dict = piexif.load(image_path)

        # Remove metadata
        exif_dict.pop("0th", None)
        exif_dict.pop("Exif", None)
        exif_dict.pop("GPS", None)

        # Save the image without metadata
        piexif.insert(piexif.dump(exif_dict), image_path)
        print(f"Metadata removed from {image_path}")
    except Exception as e:
        print(f"Error removing metadata from {image_path}: {e}")

def remove_docx_metadata(docx_path):
    try:
        # Load Word document
        doc = Document(docx_path)

        # Remove document properties
        for prop in doc.core_properties:
            prop.delete()

        # Save the document without metadata
        doc.save(docx_path)
        print(f"Metadata removed from {docx_path}")
    except Exception as e:
        print(f"Error removing metadata from {docx_path}: {e}")

def remove_pdf_metadata(pdf_path):
    try:
        # Read PDF file
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            pdf_writer = PyPDF2.PdfFileWriter()

            # Copy pages to a new PDF without metadata
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)

            # Save the PDF without metadata
            with open(pdf_path, "wb") as new_pdf_file:
                pdf_writer.write(new_pdf_file)

        print(f"Metadata removed from {pdf_path}")
    except Exception as e:
        print(f"Error removing metadata from {pdf_path}: {e}")

if __name__ == "__main__":
    file_path = input("Enter the file path: ")

    if os.path.exists(file_path):
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension in [".jpg", ".jpeg", ".png", ".tiff", ".gif", ".bmp"]:
            remove_image_metadata(file_path)
        elif file_extension == ".docx":
            remove_docx_metadata(file_path)
        elif file_extension == ".pdf":
            remove_pdf_metadata(file_path)
        else:
            print("Unsupported file format. Metadata removal not supported.")
    else:
        print("File not found. Please provide a valid file path.")
