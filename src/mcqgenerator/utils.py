import os
import PyPDF2
import json
import traceback
from src.mcqgenerator.logger import logging


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            logging.info(f"Error reading the PDF file: \n {str(e)}")
            raise Exception("error reading the PDF file")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        logging.info(
            f"unsupported file format only pdf and text file suppoted: \n {str(e)}"
        )
        raise Exception("unsupported file format only pdf and text file suppoted")


def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # iterate over the quiz dictionary and extract the required information
        for key, val in quiz_dict.items():
            mcq = val["mcq"]
            options = " || ".join(
                [
                    f"{option}->{option_value}"
                    for option, option_value in val["options"].items()
                ]
            )
            correct = val["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        logging.info(str(e))
        return False
