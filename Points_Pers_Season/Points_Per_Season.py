
#---------------------------------------------------------------------------------------------------------------#
# Load Modules
# python -m pip install module
# python -m pip freeze > requirements.txt
#---------------------------------------------------------------------------------------------------------------#
import sys
import tomllib
from pathlib import Path
from rich import print
import pandas as pd

Project_Root = Path( __file__ ).resolve().parent.parent
sys.path.insert( 0, str( Project_Root ) )

from Processing import Data_Processing
from Processing import Soccer_Processing


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

    if ( Selected_Team == "ALL" ):
        Teams = [Team for Team, Settings in Config["Teams"].items() if ( Settings.get( "CSV" ) )]
    else:
        if ( Selected_Team not in Config["Teams"] ):
            raise ValueError( f"Unknown team: {Selected_Team}" )

        Teams = [Selected_Team]

    for Team in Teams:

        Team_Config = Config["Teams"][Team]

        if ( not Team_Config.get( "CSV" ) ):
            raise ValueError( f"No CSV configured for team: {Team}" )

        print( f"\n[cyan]Processing: {Team_Config['Name']}[/]" )

        CSV_Path = Team_Config["CSV"]
        Match_Data = Data_Processing.Load_CSV( CSV_Path )

        print( f"CSV Records Loaded: {len( Match_Data )}" )

        Records_Before = len( Match_Data )

        Match_Data = Data_Processing.Remove_Duplicates( Match_Data, ["Date", "Comp", "Round", "Opponent"] )

        print( f"Duplicate Records Removed: {Records_Before - len( Match_Data )}" )

        Includes = Team_Config.get( "Includes", [] )
        Excludes = Team_Config.get( "Excludes", [] )

        Match_Data = Data_Processing.Apply_Filters( Match_Data, Includes, Excludes )

        print( f"Records After Filtering: {len( Match_Data )}" )

        Points_System = Team_Config["Points_System"]

        Match_Data = Soccer_Processing.Calculate_Match_Points( Match_Data, Points_System )

        print( f"Matches With Valid Results: {len( Match_Data )}" )
        print( f"Total Match Points: {Match_Data['Points'].sum()}" )

        Match_Data["Date"] = pd.to_datetime( Match_Data["Date"], errors="raise" )
        Match_Data["Season"] = Match_Data["Date"].dt.year

        Match_Data = Data_Processing.Calculate_Cumulative( Match_Data, "Season", "Points", "Date", "Cumulative_Points" )

        print( "\nPoints by Season:" )

        for Season, Season_Data in Match_Data.groupby( "Season" ):
            print( f"{Season}: {len( Season_Data )} matches, {Season_Data['Cumulative_Points'].iloc[-1]} points" )
