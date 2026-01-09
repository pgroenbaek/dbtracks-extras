"""
This file is part of DBTracks Extras.

Copyright (C) 2025 Peter Grønbæk Andersen <peter@grnbk.io>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import configparser
import pyffeditc
import shapeio
from pathlib import Path
from urllib.request import urlopen
from shapeio.shape import Shape
from shapeedit import ShapeEditor
from shapeedit.math import coordinates


def process_trackshape(trackshape: Shape, cwire_shape: Shape):
    """
    Transfers catenary-wire geometry from one of Norbert Rieger's DblSlip7_5d shapes into
    into one of his Xover7_5d shapes.

    Inserts all vertices and triangles from the catenary-wire primitives into the track shapes's
    `Rails` primitive. Vertex positions and normals are remapped between the internal coordinate
    systems used within the shapes.

    Args:
        trackshape (Shape): The target Xover7_5d track shape to modify.
        cwire_shape (Shape): The source DblSlip7_5d shape containing catenary-wire geometry.

    Returns:
        None
    """
    cwire_shape_editor = ShapeEditor(cwire_shape)
    cwire_sub_object = cwire_shape_editor.lod_control(0).distance_level(200).sub_object(3)
    cwire_primitives = cwire_sub_object.primitives(prim_state_name="mt_cwire")

    shape_editor = ShapeEditor(trackshape)
    sub_object = shape_editor.lod_control(0).distance_level(200).sub_object(0)

    primitive = sub_object.primitives(prim_state_name="Rails")[0]
    to_matrix = primitive.matrix
    
    for cwire_primitive in cwire_primitives:
        cwire_vertices = cwire_primitive.vertices()
        cwire_triangles = cwire_primitive.triangles()
        from_matrix = cwire_primitive.matrix

        # Insert vertices from 'cwire_primitive' into 'primitive'.
        new_vertex_lookup = {} # Key is vertex index within cwire_sub_object, value is new_vertex.

        for idx, cwire_vertex in enumerate(cwire_vertices):
            print(f"\tInserting vertex {idx + 1} of {len(cwire_vertices)}", end='\r')

            new_vertex = primitive.add_vertex(cwire_vertex.point, cwire_vertex.uv_point, cwire_vertex.normal)

            new_vertex.point = coordinates.remap_point(new_vertex.point, from_matrix, to_matrix)
            new_vertex.point.z = new_vertex.point.z + 10
            new_vertex.normal = coordinates.remap_normal(new_vertex.normal, from_matrix, to_matrix)

            if cwire_vertex.index not in new_vertex_lookup:
                new_vertex_lookup[cwire_vertex.index] = new_vertex
        
        print("")

        # Insert triangles from 'cwire_primitive' into 'primitive'.
        for idx, cwire_triangle in enumerate(cwire_triangles):
            print(f"\tInserting triangle {idx + 1} of {len(cwire_triangles)}", end='\r')

            cwire_triangle_vertices = cwire_triangle.vertices()

            vertex1 = new_vertex_lookup[cwire_triangle_vertices[0].index]
            vertex2 = new_vertex_lookup[cwire_triangle_vertices[1].index]
            vertex3 = new_vertex_lookup[cwire_triangle_vertices[2].index]

            new_triangle = primitive.insert_triangle(vertex1, vertex2, vertex3)
            new_triangle.face_normal = coordinates.remap_normal(new_triangle.face_normal, from_matrix, to_matrix)
        
        print("")



if __name__ == "__main__":
    print(f"Running ./scripts/XOver7_5d/make_ohw_xover7_5d.py")

    config = configparser.ConfigParser()
    config.read("scripts/config.ini")

    ffeditc_path = Path(config["utilities"]["ffeditc_path"])
    input_path = Path(config["shapes"]["input_path"])
    output_path = Path(config["shapes"]["output_path"])

    load_path = input_path
    processed_path = output_path / "Xover7_5d"

    match_files = ["DB*_A1tXover7_5d.s"]
    ignore_files = ["*.sd"]
    
    os.makedirs(processed_path, exist_ok=True)

    print("\tFetching Norbert Rieger's DB22f_A1tDblSlip7_5d.s shape from GitHub...")
    print("\tThis particular shape is not part of the DBTracks packages and we need it for the overhead wire.")
    cwire_shape_url = "https://github.com/pgroenbaek/dblslip7_5d-ohw/raw/refs/heads/master/data/DB22f_A1tDblSlip7_5d.s"
    with urlopen(cwire_shape_url) as response:
        cwire_shape_text = response.read().decode("utf-16-le")
    cwire_shape = shapeio.loads(cwire_shape_text)

    shape_names = shapeio.find_directory_files(load_path, match_files, ignore_files)

    for idx, sfile_name in enumerate(shape_names):
        new_sfile_name = sfile_name.replace("_A1tXover7_5d", "f_A1tXover7_5d")

        print(f"\tCreating {new_sfile_name} ({idx + 1} of {len(shape_names)})...")

        # Process .s file
        shape_path = load_path / sfile_name
        new_shape_path = processed_path / new_sfile_name

        shapeio.copy(shape_path, new_shape_path)

        pyffeditc.decompress(ffeditc_path, new_shape_path)
        trackshape = shapeio.load(new_shape_path)

        process_trackshape(trackshape, cwire_shape)

        shapeio.dump(trackshape, new_shape_path)
        pyffeditc.compress(ffeditc_path, new_shape_path)

        # Process .sd file
        sdfile_name = sfile_name.replace(".s", ".sd")
        new_sdfile_name = new_sfile_name.replace(".s", ".sd")

        sdfile_path = load_path / sdfile_name
        new_sdfile_path = processed_path / new_sdfile_name

        shapeio.copy(sdfile_path, new_sdfile_path)
        shapeio.replace_ignorecase(new_sdfile_path, sfile_name, new_sfile_name)
