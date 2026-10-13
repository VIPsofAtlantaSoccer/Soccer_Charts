
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


#---------------------------------------------------------------------------------------------------------------#
# Function: Apply_Filters
#
# Applies optional inclusion and exclusion rules to a pandas DataFrame.
# Inclusion rules retain records matching any listed criterion.
# Exclusion rules remove records matching any listed criterion.
# Returns a filtered DataFrame without modifying the original.
#---------------------------------------------------------------------------------------------------------------#
def Apply_Filters( Data, Includes = None, Excludes = None ):

    Filtered_Data = Data.copy()

    if ( Includes ):
        Include_Mask = pd.Series( False, index=Filtered_Data.index )

        for Rule in Includes:
            Column, Value = Rule.split( "=", 1 )

            if ( Column not in Filtered_Data.columns ):
                raise ValueError( f"Column does not exist: {Column}" )

            Include_Mask |= Filtered_Data[Column].astype( str ) == Value

        Filtered_Data = Filtered_Data.loc[Include_Mask ].copy()

    if ( Excludes ):
        Exclude_Mask = pd.Series( False, index=Filtered_Data.index )

        for Rule in Excludes:
            Column, Value = Rule.split( "=", 1 )

            if ( Column not in Filtered_Data.columns ):
                raise ValueError( f"Column does not exist: {Column}" )

            Exclude_Mask |= Filtered_Data[Column].astype( str ) == Value

        Filtered_Data = Filtered_Data.loc[ ~Exclude_Mask ].copy()

    return Filtered_Data
