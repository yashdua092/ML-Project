import sys # will contain everything about the runtime hence all the exeptions occured as well
import logging

def error_message_detail(error, error_detail:sys): # error_detail is provided by the sys module, contains info about line no. filename etc.
    # exc_tb will contain all the info of the exception occured(file, line etc)
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error ocuured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys): # error message is given by the Exception class in except block.
        super().__init__(error_message) # basically done to call the __init__ of Exception class
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message


if __name__ == "__main__":

    try: 
        a = 1/0
    except Exception as e: # error message given by Exception Class stored as e
        logging.info("Divide by 0")
        raise CustomException(e, sys) 