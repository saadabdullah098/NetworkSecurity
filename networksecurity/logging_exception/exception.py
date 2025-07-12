'''
The goal is to create a custom exception handler in Python. 
It gives detailed error messages, including: what the error was, line it occurred on, in which file
'''

#The sys module in Python provides access to variables and functions 
#that interact closely with the Python interpreter and its runtime environment.
import sys
from networksecurity.logging_exception.logging import logging

def error_message_detail(error,error_detail:sys):
    '''
    Function to run whenever an error is triggered to give user error details 
    '''
    _,_,exc_tb=error_detail.exc_info() #gives exception error details
    file_name = exc_tb.tb_frame.f_code.co_filename #get error file name
    error_message='Error occured in Python script [{0}] line number [{1}] error message [{2}]'.format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message

class CustomException(Exception):
    '''
    This defines a custom error class that inherits from Python's built-in Exception class.
    It means that you can raise this custom error just like any other error using raise.

    error_message: the actual error
    error_detail: the sys module (which is used to get traceback info like file name and line number)
    '''
    def __init__(self, error_message,error_detail:sys):
        #Calls the parent Exception class constructor to store the original error message.
        super().__init__(error_message) 
        
        #Calls the helper function and passes in the error message from above and error details from sys
        self.error_message=error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        '''
        returns the Custom Error Message
        '''
        return self.error_message

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
    