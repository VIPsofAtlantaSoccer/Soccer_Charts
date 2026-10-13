
#---------------------------------------------------------------------------------------------------------------#
# Load Modules
#---------------------------------------------------------------------------------------------------------------#

from pathlib import Path
import matplotlib.pyplot as plt


#---------------------------------------------------------------------------------------------------------------#
# Function: Generate_Line_Chart
#
# Generates a line chart containing one or more data series.
# Each series can contain a different number of data points.
# Supports configurable labels, title, colors, and a highlighted series.
# Saves the chart to the specified output file.
#---------------------------------------------------------------------------------------------------------------#
def Generate_Line_Chart( Series_Data, Series_Names, Output_File, Title = "", X_Label = "", Y_Label = "", Color_Map = None, Highlight_Series = None ):

    Figure, Axis = plt.subplots( figsize=( 12, 6 ) )

    for Series_Name, Values in zip( Series_Names, Series_Data ):

        X_Values = list( range( 1, len( Values ) + 1 ) )

        Line_Color = Color_Map.get( str( Series_Name ) ) if ( Color_Map ) else None
        Line_Width = 4.0 if ( str( Series_Name ) == str( Highlight_Series ) ) else 1.0

        Axis.plot( X_Values, Values, label=str( Series_Name ), color=Line_Color, linewidth=Line_Width )

    Axis.set_title( Title )
    Axis.set_xlabel( X_Label )
    Axis.set_ylabel( Y_Label )
    Axis.legend()
    Axis.grid( True, alpha=0.3 )

    Figure.tight_layout()

    Output_File = Path( Output_File )
    Output_File.parent.mkdir( parents=True, exist_ok=True )

    Figure.savefig( Output_File, dpi=150 )
    plt.close( Figure )

    return Output_File
