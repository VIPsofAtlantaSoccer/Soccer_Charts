
#---------------------------------------------------------------------------------------------------------------#
# Load Modules
# python -m pip install module
# python -m pip freeze > requirements.txt 
#---------------------------------------------------------------------------------------------------------------#
import sys
import tomllib
from pathlib import Path
from rich import print

Project_Root = Path( __file__ ).resolve().parent.parent
sys.path.insert( 0, str( Project_Root ) )

from Processing.Data_Processing import Load_CSV

#---------------------------------------------------------------------------------------------------------------#
# Function: Load_Config
#
# Load the TOML configuration located alongside this script.
# Returns the configuration as a dictionary.
#---------------------------------------------------------------------------------------------------------------#
def Load_Config():

    Config_Path = Path( __file__ ).resolve().parent / "Config.toml"

    with open( Config_Path, "rb" ) as Config_File:
        Config = tomllib.load( Config_File )

    return Config

#---------------------------------------------------------------------------------------------------------------#
# Function: Load_CSV
#
# Loads match data from a CSV file and validates the required columns.
# Returns a pandas DataFrame containing the match data.
# Raises an exception if the file is missing or its structure is invalid.
#---------------------------------------------------------------------------------------------------------------#
def Load_CSV( CSV_Path ):

    CSV_Path = Path( CSV_Path )
    
#---------------------------------------------------------------------------------------------------------------#
# Main Processing
#---------------------------------------------------------------------------------------------------------------#

if ( __name__ == "__main__" ):

    Config = Load_Config()

    print( f"[green]Configuration loaded successfully[/]" )
    print( f"Selected Team: {Config['Chart']['Team']}" )
    print( f"Chart Title: {Config['Chart']['Title']}" )
    print( f"Output Directory: {Config['Output']['Directory']}" )
