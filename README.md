# PNG-to-SVG

The Python script transforms PNG images to SVG format through two possible methods:

Each pixel within the PNG image finds representation as an independent rectangle in the SVG file; this process is known as pixel-wise conversion.

In contiguous conversion, adjacent pixels of the same color in the PNG image group together and represent as filled shapes within the SVG file.

The script: it engages the Python Imaging Library (PIL) for image data manipulation and employs the OptionParser module--specifically designed for command-line argument parsing. Additionally, through its functionality in string manipulation; it leverages use of the io module. Furthermore - to execute diverse operations on tuples - this script relies upon one key resource: the operator module.

Here's a breakdown of the main functions:

add_tuples: Adds corresponding elements of two tuples.

calculate_direction: Calculates the direction vector between two points.

normalize_vector: Normalizes a vector to have unit magnitude.

create_svg_header: Generates the header for an SVG file with specified width and height.

convert_rgba_image_to_svg_pixels: Converts a PNG image to SVG pixel-wise.

find_joined_edges: Finds connected edges in a set of assorted edges.

convert_rgba_image_to_svg_contiguous: Converts a PNG image to SVG with contiguous color regions.

The 'png_to_svg' serves as the primary function: it opens a PNG file; subsequently, it converts this file to RGBA format--finally calling upon the appropriate conversion function according to designated options.

The script also contains a section for handling command-line options using OptionParser.

When the script executes directly, identified by (__name__ == "__main__"), it undertakes a specific task: either converts all PNG files in the current directory or those designated as command-line arguments into SVG.

This script: a versatile tool for converting PNG images into SVG format, offers several options--pixel-wise or contiguous representations.
