
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

from Processing import Data_Processing


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
# Main Processing
#---------------------------------------------------------------------------------------------------------------#

if ( __name__ == "__main__" ):

    Config = Load_Config()

    print( f"[green]Configuration loaded successfully[/]" )
    print( f"Selected Team: {Config['Chart']['Team']}" )
    print( f"Chart Title: {Config['Chart']['Title']}" )
    print( f"Output Directory: {Config['Output']['Directory']}" )

    Selected_Team = Config["Chart"]["Team"]
    CSV_Path = Config["Teams"][Selected_Team]["CSV"]

    Match_Data = Data_Processing.Load_CSV( CSV_Path )

    print( f"CSV Records Loaded: {len( Match_Data )}" )
