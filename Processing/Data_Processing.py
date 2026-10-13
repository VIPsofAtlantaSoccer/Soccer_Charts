
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


#---------------------------------------------------------------------------------------------------------------#
# Function: Filter_Data
#
# Filters a pandas DataFrame using a specified column and value.
# Returns a new DataFrame containing only matching rows.
# Raises an exception if the specified column does not exist.
#---------------------------------------------------------------------------------------------------------------#
def Filter_Data( Data, Column, Value ):

    if ( Column not in Data.columns ):
        raise ValueError( f"Column does not exist: {Column}" )

    Filtered_Data = Data.loc[ Data[Column] == Value ].copy()

    return Filtered_Data
