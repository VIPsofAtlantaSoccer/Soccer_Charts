
#---------------------------------------------------------------------------------------------------------------#
# Load Modules
#---------------------------------------------------------------------------------------------------------------#

import sys
from pathlib import Path

Project_Root = Path( __file__ ).resolve().parent.parent
sys.path.insert( 0, str( Project_Root ) )

from Graphing import Chart_Lines


#---------------------------------------------------------------------------------------------------------------#
# Function: Test_Line_Chart
#
# Tests the generic line-chart generator with two series of different lengths.
# Saves the generated chart to the project's Output directory.
#---------------------------------------------------------------------------------------------------------------#
def Test_Line_Chart():

    Output_File = Project_Root / "Output" / "tests" / "Chart_Line.jpg"

    Chart_Lines.Generate_Line_Chart(
        Series_Data=[ [0, 3, 4, 7], [0, 1, 4, 4, 7, 10] ],
        Series_Names=[ "Series A", "Series B" ],
        Output_File=Output_File,
        Title="Chart Test",
        X_Label="Match Number",
        Y_Label="Points"
    )

    print( f"Chart generated: {Output_File}" )


#---------------------------------------------------------------------------------------------------------------#
# Main Processing
#---------------------------------------------------------------------------------------------------------------#
if ( __name__ == "__main__" ):

    Test_Line_Chart()
