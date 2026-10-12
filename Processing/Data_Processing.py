
#---------------------------------------------------------------------------------------------------------------#
# Load Modules
#---------------------------------------------------------------------------------------------------------------#

from pathlib import Path
import pandas as pd


#---------------------------------------------------------------------------------------------------------------#
# Function: Load_CSV
#
# Loads data from a CSV file into a pandas DataFrame.
# Returns the DataFrame without modifying or filtering its contents.
# Raises an exception if the file does not exist or cannot be read.
#---------------------------------------------------------------------------------------------------------------#
def Load_CSV( CSV_Path ):

    CSV_Path = Path( CSV_Path )

    if ( not CSV_Path.is_file() ):
        raise FileNotFoundError( f"CSV file does not exist: {CSV_Path}" )

    Data = pd.read_csv( CSV_Path )

    return Data
