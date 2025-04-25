import sys
import os

# Add project root to Python path for package imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from phishnet.logging import logger

class PhishnetException(Exception):
    """
    Custom exception class for handling phishnet application specific exceptions.
    Captures the error message, line number and file name where the error occurred.
    """
    
    def __init__(self,error_message,error_details:sys):
        """
        Initialize the PhishnetException with error details
        
        Args:
            error_message: The error message to be displayed
            error_details: sys module containing exception info
        """
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()
        
        # Extract line number and file name from traceback
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename 
    
    def __str__(self):
        """
        String representation of the exception
        
        Returns:
            str: Formatted error message with file name, line number and error details
        """
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.lineno, str(self.error_message))
        

# For testing purposes, uncomment the following lines to see how the exception works
    
# if __name__=='__main__':
#     try:
#         logger.logging.info("Entering try block")
#         # This will raise a ZeroDivisionError
#         a=1/0
#         print("This will not be printed",a)
#     except Exception as e:
#            # Raise custom exception with error details
#            raise PhishnetException(e,sys)