import sys
import os
from collections import deque
import io
from optparse import OptionParser
from PIL import Image
import operator

def add_tuples(a, b):
    return tuple(map(operator.add, a, b))

def calculate_direction(edge):
    return tuple(map(operator.sub, edge[1], edge[0]))

def normalize_vector(a):
    magnitude = int(pow(pow(a[0], 2) + pow(a[1], 2), .5))
    assert magnitude > 0, "Cannot normalize a zero-length vector"
    return tuple(map(operator.truediv, a, [magnitude]*len(a)))

def create_svg_header(width, height):
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
      "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg width="{width}" height="{height}"
         xmlns="http://www.w3.org/2000/svg" version="1.1">
    """

def convert_rgba_image_to_svg_pixels(image):
    s = io.StringIO()
    s.write(create_svg_header(*image.size))

    width, height = image.size
    for x in range(width):
        for y in range(height):
            here = (x, y)
            rgba = image.getpixel(here)
            if not rgba[3]:
                continue
            s.write(f"""  <rect x="{x}" y="{y}" width="1" height="1" style="fill:rgb{rgba[0:3]}; fill-opacity:{float(rgba[3]) / 255:.3f}; stroke:none;" />\n""")
        print(f"Converting pixels: {x*100/width:.2f}%")
    s.write("""</svg>\n""")
    return s.getvalue()

def find_joined_edges(assorted_edges, keep_every_point=False):
    pieces = []
    piece = []
    directions = deque([(0, 1), (1, 0), (0, -1), (-1, 0)])
    while assorted_edges:
        if not piece:
            piece.append(assorted_edges.pop())
        current_direction = normalize_vector(calculate_direction(piece[-1]))
        while current_direction != directions[2]:
            directions.rotate()
        for i in range(1, 4):
            next_end = add_tuples(piece[-1][1], directions[i])
            next_edge = (piece[-1][1], next_end)
            if next_edge in assorted_edges:
                assorted_edges.remove(next_edge)
                if i == 2 and not keep_every_point:
                    piece[-1] = (piece[-1][0], next_edge[1])
                else:
                    piece.append(next_edge)
                if piece[0][0] == piece[-1][1]:
                    if not keep_every_point and normalize_vector(calculate_direction(piece[0])) == normalize_vector(calculate_direction(piece[-1])):
                        piece[-1] = (piece[-1][0], piece.pop(0)[1])
                pieces.append(piece)
                piece = []
                break
        else:
            raise Exception("Failed to find connecting edge")
    return pieces

def convert_rgba_image_to_svg_contiguous(image, keep_every_point=False):
    adjacent = ((1, 0), (0, 1), (-1, 0), (0, -1))
    visited = Image.new("1", image.size, 0)
    color_pixel_lists = {}
    width, height = image.size
    for x in range(width):
        for y in range(height):
            here = (x, y)
            if visited.getpixel(here):
                continue
            rgba = image.getpixel((x, y))
            if not rgba[3]:
                continue
            piece = []
            queue = [here]
            visited.putpixel(here, 1)
            while queue:
                here = queue.pop()
                for offset in adjacent:
                    neighbour = add_tuples(here, offset)
                    if not (0 <= neighbour[0] < width) or not (0 <= neighbour[1] < height):
                        continue
                    if visited.getpixel(neighbour):
                        continue
                    neighbour_rgba = image.getpixel(neighbour)
                    if neighbour_rgba != rgba:
                        continue
                    queue.append(neighbour)
                    visited.putpixel(neighbour, 1)
                piece.append(here)

            if rgba not in color_pixel_lists:
                color_pixel_lists[rgba] = []
            color_pixel_lists[rgba].append(piece)
        print(f"Converting image: {round(x*100/width, 2):.2f}%")
    del adjacent
    del visited

    edges = {(-1, 0):((0, 0), (0, 1)),
             (0, 1):((0, 1), (1, 1)),
             (1, 0):((1, 1), (1, 0)),
             (0, -1):((1, 0), (0, 0)),
            }

    color_edge_lists = {}

    counter = 0
    for rgba, pieces in color_pixel_lists.items():
        for piece_pixel_list in pieces:
            edge_set = set([])
            for coord in piece_pixel_list:
                for offset, (start_offset, end_offset) in edges.items():
                    neighbour = add_tuples(coord, offset)
                    start = add_tuples(coord, start_offset)
                    end = add_tuples(coord, end_offset)
                    edge = (start, end)
                    if neighbour in piece_pixel_list:
                        continue
                    edge_set.add(edge)
            if rgba not in color_edge_lists:
                color_edge_lists[rgba] = []
            color_edge_lists[rgba].append(edge_set)
        counter += 1
        print(f"Calculating edges: {round(counter*100/len(color_pixel_lists.items()),2):.2f}%")
    del color_pixel_lists
    del edges

    color_joined_pieces = {}

    for color, pieces in color_edge_lists.items():
        color_joined_pieces[color] = []
        for assorted_edges in pieces:
            color_joined_pieces[color].append(find_joined_edges(assorted_edges, keep_every_point))

    s = io.StringIO()
    s.write(create_svg_header(*image.size))

    counter = 0
    for color, shapes in color_joined_pieces.items():
        for shape in shapes:
            s.write(""" <path d=" """)
            for sub_shape in shape:
                here = sub_shape.pop(0)[0]
                s.write(f""" M {here[0]},{here[1]} """)
                for edge in sub_shape:
                    here = edge[0]
                    s.write(f""" L {here[0]},{here[1]} """)
                s.write(""" Z """)
            s.write(f""" " style="fill:rgb{color[0:3]}; fill-opacity:{float(color[3]) / 255:.3f}; stroke:none;" />\n""")
        counter += 1
        print(f"Joining edges: {round(counter*100/len(color_joined_pieces.items()), 2):.2f}%")
    s.write("""</svg>\n""")
    return s.getvalue()

def png_to_svg(filename, contiguous=None, keep_every_point=None):
    try:
        im = Image.open(filename)
    except IOError as e:
        sys.stderr.write(f'{filename}: Could not open as an image file\n')
        sys.exit(1)
    im_rgba = im.convert('RGBA')

    if contiguous:
        return convert_rgba_image_to_svg_contiguous(im_rgba, keep_every_point)
    else:
        return convert_rgba_image_to_svg_pixels(im_rgba)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--pixels", action="store_false", dest="contiguous",
                      help="Generate a separate shape for each pixel; do not group pixels into contiguous areas of the same colour", default=True)
    parser.add_option("-1", "--one", action="store_true", dest="keep_every_point",
                      help="1-pixel-width edges on contiguous shapes; default is to remove intermediate points on straight line edges. ", default=None)
    (options, args) = parser.parse_args()

    if len(sys.argv) < 2:
        for file in os.listdir("."):
            if file.endswith(".png"):
                print(f"Converting {file}")
                with open(file.replace(".png", ".svg"), 'w') as f:
                    f.write(png_to_svg(file, contiguous=options.contiguous, keep_every_point=options.keep_every_point))
    else:
        for file in sys.argv:
            if file.endswith(".png"):
                print(f"Converting {file}")
                with open(file.replace(".png", ".svg"), 'w') as f:
                    f.write(png_to_svg(file, contiguous=options.contiguous, keep_every_point=options.keep_every_point))