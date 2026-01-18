"""
This file is part of DBTracks Extras.

Copyright (C) 2026 Peter Grønbæk Andersen <peter@grnbk.io>

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
from shapeio.shape import Shape
from shapeedit import ShapeEditor


def process_trackshape(trackshape: Shape):
    """
    Removes anything other than the tunnel wall and roof from V4hs2tTunS shapes.

    Args:
        trackshape (Shape): The target V4hs2tTunS track shape to modify.

    Returns:
        None
    """
    trackshape_editor = ShapeEditor(trackshape)

    lod_control = trackshape_editor.lod_control(0)

    prim_state_names_to_remove = [
        "mt_trackbase",
        "mb_layer1",
        "mt_tun_rside",
        "mt_tun_rtops",
        "mt_cwire",
    ]

    for lod_dlevel in lod_control.distance_levels():
        for sub_object in lod_dlevel.sub_objects():
            for prim_state_name in prim_state_names_to_remove:
                for primitive in sub_object.primitives(prim_state_name=prim_state_name):
                    primitive.remove_all_triangles()



if __name__ == "__main__":
    print(f"Running ./scripts/V4hs2tTunNoTracks/make_v4hs2ttuns_notracks.py")
    
    config = configparser.ConfigParser()
    config.read("scripts/config.ini")

    ffeditc_path = Path(config["utilities"]["ffeditc_path"])
    input_path = Path(config["shapes"]["input_path"])
    output_path = Path(config["shapes"]["output_path"])

    load_path = input_path
    processed_path = output_path / "V4hs2tTunNoTracks"

    match_files = ["V4hs2tTunS_*.s"]
    ignore_files = ["*Pnt*", "*Frog*", "*Xover*", "*Slip*", "*DKW*", "*.sd"]
    
    os.makedirs(processed_path, exist_ok=True)

    shape_names = shapeio.find_directory_files(load_path, match_files, ignore_files)

    for idx, sfile_name in enumerate(shape_names):
        new_sfile_name = sfile_name.replace(".s", "_nt.s")

        print(f"\tCreating {new_sfile_name} ({idx + 1} of {len(shape_names)})...")

        # Process .s file
        shape_path = load_path / sfile_name
        new_shape_path = processed_path / new_sfile_name

        shapeio.copy(shape_path, new_shape_path)

        pyffeditc.decompress(ffeditc_path, new_shape_path)
        trackshape = shapeio.load(new_shape_path)

        process_trackshape(trackshape)
        
        shapeio.dump(trackshape, new_shape_path)
        pyffeditc.compress(ffeditc_path, new_shape_path)

        # Process .sd file
        sdfile_name = sfile_name.replace(".s", ".sd")
        new_sdfile_name = new_sfile_name.replace(".s", ".sd")

        sdfile_path = load_path / sdfile_name
        new_sdfile_path = processed_path / new_sdfile_name

        shapeio.copy(sdfile_path, new_sdfile_path)
        shapeio.replace_ignorecase(new_sdfile_path, sfile_name, new_sfile_name)