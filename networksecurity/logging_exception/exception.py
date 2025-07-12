'''
    The goal is to create a custom exception handler in Python. 
    It gives detailed error messages, including: what the error was, line it occurred on, in which file
'''

#The sys module in Python provides access to variables and functions 
#that interact closely with the Python interpreter and its runtime environment.
import sys
from logger import logging
class CustomException(Exception):
    '''
        This class defines a custom error class that inherits from Python's built-in Exception class.
    '''
    def __init__(self, error_message, error_details:sys):
        '''
            Function to run whenever an error is triggered to give user error details 
            error_message: the actual error
            error_detail: the sys module (which is used to get traceback info like file name and line number)
        '''
        self.error_message = error_message #actual error message
        _,_,exc_tb = error_details.exc_info()
        self.lineno = exc_tb.tb_lineno #line of error
        self.file_name = exc_tb.tb_frame.f_code.co_filename #file of error

    def __str__(self):
        '''
            This functions returns the Custom Error Message
        '''
        return 'Error occured in Python script [{0}] line number [{1}] error message [{2}]'.format(
        self.file_name, self.lineno, str(self.error_message)
        )


# To test the run
'''
if __name__ == '__main__':
    try:
        a = 1/0
    except Exception as e:
        custom_err = CustomException(e, sys)
        logging.error(custom_err)
        raise custom_err
'''