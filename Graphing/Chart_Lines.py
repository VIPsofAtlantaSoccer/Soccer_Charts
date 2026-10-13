
#---------------------------------------------------------------------------------------------------------------#
# Load Modules
#---------------------------------------------------------------------------------------------------------------#

from pathlib import Path

import seaborn as sns
import matplotlib.pyplot as plt


#---------------------------------------------------------------------------------------------------------------#
# Class: Line_Chart_Generator
#
# Creates line charts from multiple numeric data series, supporting series of different lengths.
# Annotates each series endpoint with its name, final value, and optional postfix.
#
# Supports:
#   - Custom series colors or an automatically generated seaborn color palette.
#   - Highlighting a selected series with increased linewidth and opacity.
#   - Configurable chart labels, fonts, figure dimensions, and background colors.
#   - Full charts showing every data point.
#   - Limited charts truncating all series to the highlighted series length.
#
# The class is independent of soccer data and can be reused by other applications.
#---------------------------------------------------------------------------------------------------------------#
class Line_Chart_Generator:

    #---------------------------------------------------------------------------------------------------------------#
    # Function: __init__
    #
    # Initializes the chart with default data, labels, style, and highlighting settings.
    #---------------------------------------------------------------------------------------------------------------#
    def __init__( self ):

        # Data and series attributes
        self.Series_Data = []
        self.Series_Names = []
        self.Series_Colors = None
        self.Color_Map = None

        # Chart labels and title
        self.X_Axis_Label = ""
        self.Y_Axis_Label = ""
        self.Chart_Title = ""
        self.Label_Postfix = ""

        # Style settings
        self.Figure_Size = ( 8, 6 )
        self.Title_Font_Size = 14
        self.Label_Font_Size = 12
        self.Tick_Font_Size = 8
        self.Legend_Font_Size = 10
        self.Line_Label_Font_Size = 8
        self.Background_Color = None
        self.DPI = 400

        # Highlight settings
        self.Highlight_Series_Name = None
        self.Highlight_Linewidth = 4.0
        self.Default_Linewidth = 0.7

        # Default seaborn styling
        sns.set_style( "darkgrid" )


    #---------------------------------------------------------------------------------------------------------------#
    # Function: Set_Data
    #
    # Assigns numeric data series, series names, and optional colors.
    # Validates that the supplied lists contain matching numbers of series.
    # Colors may be supplied individually or through a dictionary keyed by series name.
    # Returns: None
    #---------------------------------------------------------------------------------------------------------------#
    def Set_Data( self, Series_Data, Series_Names = None, Series_Colors = None, Color_Map = None ):

        if ( not isinstance( Series_Data, ( list, tuple ) ) or
             any( not isinstance( Series, ( list, tuple ) ) for Series in Series_Data ) ):
            raise ValueError( "Series_Data must be a list of lists or tuples of numeric values." )

        self.Series_Data = [ list( Series ) for Series in Series_Data ]
        Number_Of_Series = len( self.Series_Data )

        if ( Series_Names is not None ):
            if ( not isinstance( Series_Names, ( list, tuple ) ) or len( Series_Names ) != Number_Of_Series ):
                raise ValueError( "Series_Names must have the same length as Series_Data." )

            self.Series_Names = list( Series_Names )
        else:
            self.Series_Names = [ None ] * Number_Of_Series

        if ( Series_Colors is not None ):
            if ( not isinstance( Series_Colors, ( list, tuple ) ) or len( Series_Colors ) != Number_Of_Series ):
                raise ValueError( "Series_Colors must have the same length as Series_Data." )

            self.Series_Colors = list( Series_Colors )
        else:
            self.Series_Colors = None

        self.Color_Map = None

        if ( Color_Map is not None ):
            if ( not isinstance( Color_Map, dict ) ):
                raise ValueError( "Color_Map must be a dictionary mapping series names to colors." )

            self.Color_Map = Color_Map
            self.Series_Colors = [ Color_Map.get( str( Name ) ) for Name in self.Series_Names ]


    #---------------------------------------------------------------------------------------------------------------#
    # Function: Set_Labels
    #
    # Configures the X-axis label, Y-axis label, chart title, and endpoint label postfix.
    # Returns: None
    #---------------------------------------------------------------------------------------------------------------#
    def Set_Labels( self, X_Label = None, Y_Label = None, Title = None, Label_Postfix = None ):

        if ( X_Label is not None ):
            self.X_Axis_Label = X_Label

        if ( Y_Label is not None ):
            self.Y_Axis_Label = Y_Label

        if ( Title is not None ):
            self.Chart_Title = Title

        if ( Label_Postfix is not None ):
            self.Label_Postfix = Label_Postfix


    #---------------------------------------------------------------------------------------------------------------#
    # Function: Set_Style
    #
    # Configures figure dimensions, font sizes, background color, and rendering resolution.
    # Settings not supplied retain their existing values.
    # Returns: None
    #---------------------------------------------------------------------------------------------------------------#
    def Set_Style( self, Figure_Size = None, Title_Font_Size = None, Label_Font_Size = None, Tick_Font_Size = None, Background_Color = None, Legend_Font_Size = None, Line_Label_Font_Size = None, DPI = None ):

        if ( Figure_Size is not None ):
            self.Figure_Size = Figure_Size

        if ( Title_Font_Size is not None ):
            self.Title_Font_Size = Title_Font_Size

        if ( Label_Font_Size is not None ):
            self.Label_Font_Size = Label_Font_Size

        if ( Tick_Font_Size is not None ):
            self.Tick_Font_Size = Tick_Font_Size

        if ( Background_Color is not None ):
            self.Background_Color = Background_Color

        if ( Legend_Font_Size is not None ):
            self.Legend_Font_Size = Legend_Font_Size

        if ( Line_Label_Font_Size is not None ):
            self.Line_Label_Font_Size = Line_Label_Font_Size

        if ( DPI is not None ):
            self.DPI = DPI


    #---------------------------------------------------------------------------------------------------------------#
    # Function: Set_Highlight
    #
    # Selects a series to emphasize using increased linewidth and full opacity.
    # Configures the line widths for highlighted and non-highlighted series.
    # Returns: None
    #---------------------------------------------------------------------------------------------------------------#
    def Set_Highlight( self, Series_Name = None, Linewidth = None, Default_Linewidth = None ):

        if ( Series_Name is not None ):
            self.Highlight_Series_Name = str( Series_Name )

        if ( Linewidth is not None ):
            self.Highlight_Linewidth = Linewidth

        if ( Default_Linewidth is not None ):
            self.Default_Linewidth = Default_Linewidth


    #---------------------------------------------------------------------------------------------------------------#
    # Function: Plot_Chart
    #
    # Generates the chart using the configured data and style.
    #
    # Full:
    #   Displays all data points in every series.
    #
    # Limited:
    #   Truncates each series to the number of data points in the highlighted series.
    #   Shorter series retain their original lengths.
    #
    # Returns the Matplotlib Figure and Axes objects.
    # Raises ValueError if no valid data series are available.
    #---------------------------------------------------------------------------------------------------------------#
    def Plot_Chart( self, Limited = False ):

        if ( not self.Series_Data or all( len( Series ) == 0 for Series in self.Series_Data ) ):
            raise ValueError( "No data series provided. Use Set_Data() before plotting." )

        Data = self.Series_Data

        if ( Limited and self.Highlight_Series_Name in [ str( Name ) for Name in self.Series_Names ] ):
            Series_Index = [ str( Name ) for Name in self.Series_Names ].index( self.Highlight_Series_Name )
            Maximum_Length = len( Data[Series_Index] )
            Data = [ Series[:Maximum_Length] for Series in Data ]

        Number_Of_Series = len( self.Series_Data )
        Default_Colors = sns.color_palette( n_colors=Number_Of_Series )

        if ( self.Series_Colors is None ):
            Colors = Default_Colors
        else:
            Colors = [
                Color if ( Color is not None ) else Default_Colors[Index]
                for Index, Color in enumerate( self.Series_Colors )
            ]

        Figure, Axis = plt.subplots( figsize=self.Figure_Size, dpi=self.DPI )

        if ( self.Background_Color is not None ):
            Figure.patch.set_facecolor( self.Background_Color )
            Axis.set_facecolor( self.Background_Color )

        for Index, Series in enumerate( Data ):

            if ( len( Series ) == 0 ):
                continue

            Series_Name = self.Series_Names[Index]
            Series_Label = str( Series_Name ) if ( Series_Name is not None ) else None
            Series_Color = Colors[Index]

            if ( Series_Label == self.Highlight_Series_Name ):
                Line_Width = self.Highlight_Linewidth
                Line_Alpha = 1.0
            else:
                Line_Width = self.Default_Linewidth
                Line_Alpha = 0.6

            # Match numbers begin at 1 rather than 0
            X_Values = list( range( 1, len( Series ) + 1 ) )

            Axis.plot(
                X_Values,
                Series,
                label=Series_Label,
                color=Series_Color,
                linewidth=Line_Width,
                alpha=Line_Alpha
            )

            # Add the series name and final value beside the endpoint
            if ( Series_Label is not None ):

                X_End = X_Values[-1]
                Y_End = Series[-1]

                Annotation = f"{Series_Label} - {Y_End}"

                if ( self.Label_Postfix ):
                    Annotation += f" {self.Label_Postfix}"

                # Add a consistent horizontal gap between the line endpoint and its label
                X_End = X_End + .5

                Axis.text(
                    X_End,
                    Y_End,
                    Annotation,
                    ha="left",
                    va="center",
                    fontdict={
                        "family": "sans-serif",
                        "size": self.Line_Label_Font_Size,
                        "color": Series_Color
                    }
                )

        # Chart title
        if ( self.Chart_Title ):
            Axis.set_title(
                self.Chart_Title,
                fontdict={
                    "family": "sans-serif",
                    "color": "#FFFFFF",
                    "weight": "normal",
                    "size": self.Title_Font_Size
                }
            )

        # X-axis label
        if ( self.X_Axis_Label ):
            Axis.set_xlabel(
                self.X_Axis_Label,
                fontdict={
                    "family": "sans-serif",
                    "color": "#FFFFFF",
                    "weight": "normal",
                    "size": self.Label_Font_Size
                }
            )

        # Y-axis label
        if ( self.Y_Axis_Label ):
            Axis.set_ylabel(
                self.Y_Axis_Label,
                fontdict={
                    "family": "sans-serif",
                    "color": "#FFFFFF",
                    "weight": "normal",
                    "size": self.Label_Font_Size
                }
            )

        # Legend
        if ( any( Name is not None for Name in self.Series_Names ) ):
            Axis.legend(
                facecolor="black",
                loc="upper left",
                frameon=False,
                prop={
                    "size": self.Legend_Font_Size,
                    "family": "sans-serif",
                    "weight": "normal",
                    "style": "italic"
                }
            )

        # Axis labels and ticks
        Axis.tick_params( axis="both", labelsize=self.Tick_Font_Size )

        # Disable gridlines
        Axis.grid( False )

        # Hide upper and right spines
        Axis.spines["top"].set_visible( False )
        Axis.spines["right"].set_visible( False )

        # Preserve original bottom and left spine widths
        Axis.spines["bottom"].set_linewidth( 1.0 )
        Axis.spines["left"].set_linewidth( 1.0 )

        # Leave room for endpoint annotations without adding excess space on the left
        Axis.margins( x=0 )
        Axis.set_xlim( left=0, right=max( len( Series ) for Series in Data ) + 4 )
        
        Figure.tight_layout()

        return Figure, Axis


    #---------------------------------------------------------------------------------------------------------------#
    # Function: Plot_Chart_Full
    #
    # Generates and saves the full chart, displaying all available data points.
    # Returns the output file path.
    #---------------------------------------------------------------------------------------------------------------#
    def Plot_Chart_Full( self, Filename ):

        Figure, Axis = self.Plot_Chart( Limited=False )

        Output_File = Path( Filename )
        Output_File.parent.mkdir( parents=True, exist_ok=True )

        Figure.savefig( Output_File, bbox_inches="tight", facecolor=Figure.get_facecolor() )
        plt.close( Figure )

        return Output_File


    #---------------------------------------------------------------------------------------------------------------#
    # Function: Plot_Chart_Limited
    #
    # Generates and saves a chart truncated to the highlighted series length.
    # Returns the output file path.
    #---------------------------------------------------------------------------------------------------------------#
    def Plot_Chart_Limited( self, Filename ):

        Figure, Axis = self.Plot_Chart( Limited=True )

        Output_File = Path( Filename )
        Output_File.parent.mkdir( parents=True, exist_ok=True )

        Figure.savefig( Output_File, bbox_inches="tight", facecolor=Figure.get_facecolor() )
        plt.close( Figure )

        return Output_File


    #---------------------------------------------------------------------------------------------------------------#
    # Function: Save_Chart
    #
    # Generates and saves the full chart to the specified file.
    # Returns the output file path.
    #---------------------------------------------------------------------------------------------------------------#
    def Save_Chart( self, File_Name ):

        return self.Plot_Chart_Full( File_Name )


#---------------------------------------------------------------------------------------------------------------#
# Function: Generate_Line_Chart
#
# Provides compatibility with applications already using the function-based interface.
# Creates and configures a Line_Chart_Generator instance, then saves a full chart.
# Returns the output file path.
#---------------------------------------------------------------------------------------------------------------#
def Generate_Line_Chart( Series_Data, Series_Names, Output_File, Title = "", X_Label = "", Y_Label = "", Color_Map = None, Highlight_Series = None, Label_Postfix = "", Background_Color = "black" ):

    Chart = Line_Chart_Generator()

    Chart.Set_Data( Series_Data, Series_Names=Series_Names, Color_Map=Color_Map )

    Chart.Set_Labels( X_Label=X_Label, Y_Label=Y_Label, Title=Title, Label_Postfix=Label_Postfix )

    Chart.Set_Highlight( Series_Name=Highlight_Series, Linewidth=5.0, Default_Linewidth=0.75 )

    Chart.Set_Style(
        Figure_Size=( 12, 6 ),
        Title_Font_Size=18,
        Label_Font_Size=14,
        Tick_Font_Size=10,
        Background_Color=Background_Color
    )

    return Chart.Plot_Chart_Full( Output_File )
