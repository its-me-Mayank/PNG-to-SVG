This Python script seamlessly converts PNG images to SVG format using two distinct methods:

In the pixel-wise conversion, each pixel within the PNG image transforms into an independent rectangle within the SVG file.

For the contiguous conversion, adjacent pixels of the same color in the PNG image unite, forming filled shapes in the SVG file.

The script strategically utilizes the Python Imaging Library (PIL) for efficient image data manipulation. It navigates command-line argument intricacies with the OptionParser module, tailor-made for such tasks. Additionally, in the realm of string manipulation, it deftly employs the io module. To perform an array of operations on tuples, the script turns to the operator module as a key resource.

Main functions:

add_tuples: Summons the sum of corresponding elements from two tuples.

calculate_direction: Orchestrates the computation of the direction vector between two points.

normalize_vector: Ensures the balance by normalizing a vector to possess a unit magnitude.

create_svg_header: Takes on the role of an architect, crafting the header for an SVG file with specified width and height.

convert_rgba_image_to_svg_pixels: Transforms a PNG image into SVG pixel by pixel.

find_joined_edges: Acts as a detective, uncovering connected edges within a set of assorted edges.

convert_rgba_image_to_svg_contiguous: Shapes a PNG image into SVG, creating contiguous color regions.

The pivotal function, 'png_to_svg,' takes the stage: opening a PNG file, converting it to RGBA format, and then summoning the appropriate conversion function based on designated options.

The script also incorporates a segment for deftly handling command-line options using OptionParser.

To use the code, the raster PNG image should be in the same directory.

