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
import re
import configparser
import pyffeditc
import shapeio
from pathlib import Path
from shapeio.shape import Point, UVPoint, Vector
from shapeedit import ShapeEditor

if __name__ == "__main__":
    print(f"Running ./scripts/DBxfb/convert_db1s_to_db1fb.py")
    
    config = configparser.ConfigParser()
    config.read("scripts/config.ini")

    ffeditc_path = Path(config["utilities"]["ffeditc_path"])
    input_path = Path(config["shapes"]["input_path"])
    output_path = Path(config["shapes"]["output_path"])

    load_path = input_path
    processed_path = output_path / "DB1fb"

    match_files = ["DB1s_*.s"]
    ignore_files = ["*Tun*", "*Pnt*", "*Frog*"]
    
    os.makedirs(processed_path, exist_ok=True)

    shape_names = shapeio.find_directory_files(load_path, match_files, ignore_files)

    for idx, sfile_name in enumerate(shape_names):
        new_sfile_name = sfile_name.replace("DB1s", "DB1fb")

        print(f"\tCreating {new_sfile_name} ({idx + 1} of {len(shape_names)})...")

        # Convert .s file
        shape_path = f"{load_path}/{sfile_name}"
        new_shape_path = f"{processed_path}/{new_sfile_name}"

        shapeio.copy(shape_path, new_shape_path)

        pyffeditc.decompress(ffeditc_path, new_shape_path)
        trackshape = shapeio.load(new_shape_path)

        for idx, image in enumerate(trackshape.images):
            image = re.sub(r"DB_TrackSfs1.ace", "DB_Track1.ace", image, flags=re.IGNORECASE)
            image = re.sub(r"DB_TrackSfs1s.ace", "DB_Track1s.ace", image, flags=re.IGNORECASE)
            image = re.sub(r"DB_TrackSfs1w.ace", "DB_Track1w.ace", image, flags=re.IGNORECASE)
            image = re.sub(r"DB_TrackSfs1sw.ace", "DB_Track1sw.ace", image, flags=re.IGNORECASE)
            trackshape.images[idx] = image

        trackshape_editor = ShapeEditor(trackshape)
        lod_control = trackshape_editor.lod_control(0)

        for lod_dlevel in lod_control.distance_levels():
            for sub_object in lod_dlevel.sub_objects():
                vertices_in_subobject = sub_object.vertices()
                for vertex in vertices_in_subobject:
                    if vertex.point.y == 0.133:
                        vertex.point.y = 0.0833
                    elif vertex.point.y == 0.145:
                        vertex.point.y = 0.0945
        
        shapeio.dump(trackshape, new_shape_path)
        pyffeditc.compress(ffeditc_path, new_shape_path)

        # Process .sd file
        sdfile_name = sfile_name.replace(".s", ".sd")
        new_sdfile_name = new_sfile_name.replace(".s", ".sd")

        sdfile_path = f"{load_path}/{sdfile_name}"
        new_sdfile_path = f"{processed_path}/{new_sdfile_name}"

        shapeio.copy(sdfile_path, new_sdfile_path)
        shapeio.replace_ignorecase(new_sdfile_path, sfile_name, new_sfile_name)