
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
import json

Project_Root = Path( __file__ ).resolve().parent.parent
sys.path.insert( 0, str( Project_Root ) )

from Processing import Data_Processing
from Processing import Soccer_Processing
from Graphing import Chart_Lines


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
# Function: Load_Colors
#
# Loads a JSON file containing series names and their assigned colors.
# Ignores the optional _notes section used to document color selections.
# Resolves the file path relative to the Points_Per_Season directory.
# Returns a dictionary mapping series names to hexadecimal colors.
#---------------------------------------------------------------------------------------------------------------#
def Load_Colors( Color_File ):

    Color_Path = ( Path( __file__ ).resolve().parent / Color_File ).resolve()

    with open( Color_Path, "r", encoding="utf-8" ) as File:
        Colors = json.load( File )

    Colors.pop( "_notes", None )

    return Colors

#---------------------------------------------------------------------------------------------------------------#
# Function: Get_Selected_Teams
#
# Determines which teams to process based on the Chart.Team configuration.
# Supports an individual team or ALL configured teams with CSV files.
# Validates that a specifically selected team exists.
# Returns a list of team identifiers.
#---------------------------------------------------------------------------------------------------------------#
def Get_Selected_Teams( Config ):

    Selected_Team = Config["Chart"]["Team"]

    if ( Selected_Team == "ALL" ):
        Teams = [Team for Team, Settings in Config["Teams"].items() if ( Settings.get( "CSV" ) )]
    else:
        if ( Selected_Team not in Config["Teams"] ):
            raise ValueError( f"Unknown team: {Selected_Team}" )

        Teams = [Selected_Team]

    return Teams


#---------------------------------------------------------------------------------------------------------------#
# Function: Load_Match_Data
#
# Loads the selected team's CSV using the generic Data_Processing module.
# Removes duplicate matches and applies the team's configured inclusion and exclusion rules.
# Displays record counts using Rich.
# Returns the filtered match DataFrame.
#---------------------------------------------------------------------------------------------------------------#
def Load_Match_Data( Config, Team ):

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

    return Match_Data


#---------------------------------------------------------------------------------------------------------------#
# Function: Prepare_Season_Data
#
# Calculates match points using the team's configured scoring system.
# Extracts the season from each match date and calculates cumulative points within each season.
# Assigns sequential match numbers, allowing seasons of different lengths.
# Returns the prepared match DataFrame.
#---------------------------------------------------------------------------------------------------------------#
def Prepare_Season_Data( Config, Team, Match_Data ):

    Team_Config = Config["Teams"][Team]
    Points_System = Team_Config["Points_System"]

    Match_Data = Soccer_Processing.Calculate_Match_Points( Match_Data, Points_System )

    print( f"Matches With Valid Results: {len( Match_Data )}" )
    print( f"Total Match Points: {Match_Data['Points'].sum()}" )

    Match_Data["Date"] = pd.to_datetime( Match_Data["Date"], errors="raise" )
    Match_Data["Season"] = Match_Data["Date"].dt.year

    Match_Data = Data_Processing.Calculate_Cumulative( Match_Data, "Season", "Points", "Date", "Cumulative_Points" )

    Match_Data["Match_Number"] = Match_Data.groupby( "Season" ).cumcount() + 1

    return Match_Data


#---------------------------------------------------------------------------------------------------------------#
# Function: Generate_Charts
#
# Groups prepared match data by season and creates cumulative points series.
# Displays season-by-season match counts and final point totals.
# Generates a line chart using the reusable Chart_Lines module.
# Saves the chart to the configured output directory.
# Returns the generated chart file path.
#---------------------------------------------------------------------------------------------------------------#
def Generate_Charts( Config, Team, Match_Data ):

    Team_Config = Config["Teams"][Team]

    print( "\nPoints by Season:" )

    Series_Data = []
    Series_Names = []

    for Season, Season_Data in Match_Data.groupby( "Season" ):
        print( f"{Season}: {len( Season_Data )} matches, {Season_Data['Cumulative_Points'].iloc[-1]} points" )

        Series_Names.append( str( Season ) )
        Series_Data.append( Season_Data["Cumulative_Points"].tolist() )

    Output_Directory = ( Path( __file__ ).resolve().parent / Config["Output"]["Directory"] ).resolve()
    Color_Map = None

    if ( Team_Config.get( "Colors" ) ):
        Color_Map = Load_Colors( Team_Config["Colors"] )


    #---------------------------------------------------------------------------------------------------------------#
    # Configure the line chart
    #---------------------------------------------------------------------------------------------------------------#
    Chart = Chart_Lines.Line_Chart_Generator()

    Chart.Set_Data( Series_Data, Series_Names=Series_Names, Color_Map=Color_Map )

    Chart.Set_Highlight(
        Series_Name=str( Config["Chart"]["Highlight_Season"] ),
        Linewidth=5.0,
        Default_Linewidth=0.75
    )

    Chart.Set_Labels(
        X_Label=Config["Chart"]["X_Label"],
        Y_Label=Config["Chart"]["Y_Label"],
        Title=f"{Config['Chart']['Title']}{Team_Config['Name']}",
        Label_Postfix="points"
    )

    Chart.Set_Style(
        Figure_Size=( 12, 6 ),
        Title_Font_Size=18,
        Label_Font_Size=14,
        Tick_Font_Size=10,
        Background_Color="black"
    )

    #---------------------------------------------------------------------------------------------------------------#
    # Generate full and limited charts
    #---------------------------------------------------------------------------------------------------------------#
    Output_Format = Config["Output"]["Format"]
    Output_File_Full = Output_Directory / "Points_Per_Season" / f"{Team}_Points_Per_Season_Full.{Output_Format}"
    Output_File_Limited = Output_Directory / "Points_Per_Season" / f"{Team}_Points_Per_Season_Limited.{Output_Format}"

    Chart.Plot_Chart_Full( Output_File_Full )
    Chart.Plot_Chart_Limited( Output_File_Limited )

    print( f"[green]Full chart generated:[/] {Output_File_Full}" )
    print( f"[green]Limited chart generated:[/] {Output_File_Limited}" )

    return Output_File_Full, Output_File_Limited


#---------------------------------------------------------------------------------------------------------------#
# Function: Display_Social_Message
#
# Displays the social-media message for the selected team.
# Uses the highlighted season's match count and the team's configured signature.
# Does not create files or publish to social platforms.
#---------------------------------------------------------------------------------------------------------------#
def Display_Social_Message( Config, Team, Match_Data ):

    Team_Config = Config["Teams"][Team]
    Highlight_Season = Config["Chart"]["Highlight_Season"]

    Season_Data = Match_Data.loc[ Match_Data["Season"] == Highlight_Season ]

    if ( Season_Data.empty ):
        print( f"[yellow]No match data for highlighted season: {Highlight_Season}[/]" )
        return

    Number_Of_Games = len( Season_Data )
    Signature = Team_Config.get( "Signature", "" )

    Message = f"Number of Points Each Season through {Number_Of_Games} games"

    if ( Signature ):
        Message += f"\n{Signature}"

    print( f"\n[cyan]{Message}[/]" )

#---------------------------------------------------------------------------------------------------------------#
# Main Processing
#
# Loads application configuration, determines the selected teams, and coordinates
# data loading, season calculations, and chart generation for each team.
#---------------------------------------------------------------------------------------------------------------#
if ( __name__ == "__main__" ):

    Config = Load_Config()

    print( f"[green]Configuration loaded successfully[/]" )
    print( f"Selected Team: {Config['Chart']['Team']}" )
    print( f"Chart Title: {Config['Chart']['Title']}" )
    print( f"Output Directory: {Config['Output']['Directory']}" )

    Teams = Get_Selected_Teams( Config )

    for Team in Teams:
        Match_Data = Load_Match_Data( Config, Team )
        Match_Data = Prepare_Season_Data( Config, Team, Match_Data )

        Generate_Charts( Config, Team, Match_Data )
        Display_Social_Message( Config, Team, Match_Data )
