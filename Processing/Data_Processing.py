
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

    Data = pd.read_csv( CSV_Path, comment="#" )

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


#---------------------------------------------------------------------------------------------------------------#
# Function: Remove_Duplicates
#
# Removes duplicate rows from a pandas DataFrame using the specified columns.
# Keeps the first occurrence of each duplicate.
# Returns a new DataFrame without modifying the original.
#---------------------------------------------------------------------------------------------------------------#
def Remove_Duplicates( Data, Columns = None ):

    if ( Columns is not None ):
        Missing_Columns = [Column for Column in Columns if ( Column not in Data.columns )]

        if ( Missing_Columns ):
            raise ValueError( f"Columns do not exist: {', '.join( Missing_Columns )}" )

        return Data.drop_duplicates( subset=Columns, keep="first" ).copy()

    return Data.drop_duplicates( keep="first" ).copy()


#---------------------------------------------------------------------------------------------------------------#
# Function: Calculate_Cumulative
#
# Calculates a running total for a numeric column within each group.
# Sorts records by the specified column before calculating cumulative values.
# Returns a new DataFrame without modifying the original.
#---------------------------------------------------------------------------------------------------------------#
def Calculate_Cumulative( Data, Group_Column, Value_Column, Sort_Column, Output_Column ):

    Required_Columns = [Group_Column, Value_Column, Sort_Column]
    Missing_Columns = [Column for Column in Required_Columns if ( Column not in Data.columns )]

    if ( Missing_Columns ):
        raise ValueError( f"Columns do not exist: {', '.join( Missing_Columns )}" )

    Result_Data = Data.sort_values( [Group_Column, Sort_Column] ).copy()
    Result_Data[Output_Column] = Result_Data.groupby( Group_Column )[Value_Column].cumsum()

    return Result_Data
