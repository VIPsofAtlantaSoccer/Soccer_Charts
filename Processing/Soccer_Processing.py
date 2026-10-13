#---------------------------------------------------------------------------------------------------------------#
# Load Modules
#---------------------------------------------------------------------------------------------------------------#


#---------------------------------------------------------------------------------------------------------------#
# Function: Calculate_Match_Points
#
# Calculates points earned for each match using the specified scoring system.
#
# Supported Points_System values:
#
#   Standard:
#       Used by leagues such as MLS, NWSL, and most traditional soccer competitions.
#       Win                  = 3 points
#       Draw                 = 1 point
#       Loss                 = 0 points
#
#   Shootout:
#       Used by competitions such as MLS NEXT Pro that award additional points
#       through a shootout when a match finishes tied in regulation.
#       Regulation Win       = 3 points
#       Draw + Shootout Win  = 2 points
#       Draw + Shootout Loss = 1 point
#       Regulation Loss      = 0 points
#
#       Requires the CSV columns "Result" and "Shootout Result".
#       Shootout results must be recorded as "W" or "L".
#
# The scoring system is selected through Points_System in Config.toml.
# Matches without a valid W, D, or L result are excluded.
#
# Returns a new DataFrame containing a calculated "Points" column.
# Does not modify the original DataFrame.
#---------------------------------------------------------------------------------------------------------------#
def Calculate_Match_Points( Match_Data, Points_System ):

    if ( Points_System not in [ "Standard", "Shootout" ] ):
        raise ValueError( f"Unsupported points system: {Points_System}" )

    Required_Columns = [ "Result" ]

    if ( Points_System == "Shootout" ):
        Required_Columns.append( "Shootout Result" )

    Missing_Columns = [ Column for Column in Required_Columns if ( Column not in Match_Data.columns ) ]

    if ( Missing_Columns ):
        raise ValueError( f"Missing required columns: {', '.join( Missing_Columns )}" )

    Match_Data = Match_Data.loc[ Match_Data["Result"].isin( [ "W", "D", "L" ] ) ].copy()

    Point_Map = { "W": 3, "D": 1, "L": 0 }
    Match_Data["Points"] = Match_Data["Result"].map( Point_Map ).astype( int )

    if ( Points_System == "Shootout" ):
        Shootout_Wins = ( Match_Data["Result"] == "D" ) & ( Match_Data["Shootout Result"] == "W" )
        Match_Data.loc[ Shootout_Wins, "Points" ] = 2

    return Match_Data