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
import tempfile
import subprocess
from pathlib import Path
from shapeio.shape import Shape
from shapeedit import ShapeEditor
from PIL import Image, ImageChops


def process_trackshape(trackshape: Shape):
    """
    Removes anything other than the tunnel wall and roof from DB1s Tun and RndTun shapes.

    Args:
        trackshape (Shape): The target DB1s Tun and RndTun track shape to modify.

    Returns:
        None
    """
    trackshape_editor = ShapeEditor(trackshape)

    trackshape_editor.replace_texture_image("DB_TunWallSFS1.ace", "DB_TunWallSFS1L.ace")

    lod_control = trackshape_editor.lod_control(0)

    prim_state_names_to_remove = [
        "mt_trackbed",
        "mb_trackbed",
        "mt_tun_rtops",
        "mb_layer1",
        "mt_tun_rside",
        "mt_cwire",
        "mt_tgantry",
        "mt_trackbase",
    ]

    for lod_dlevel in lod_control.distance_levels():
        for sub_object in lod_dlevel.sub_objects():
            for prim_state_name in prim_state_names_to_remove:
                for primitive in sub_object.primitives(prim_state_name=prim_state_name):
                    primitive.remove_all_triangles()


def process_texture(png_path: str):
    """
    Creates the modified texture where the tunnel light is contained within the 10m track piece.

    Args:
        png_path (str): Path of the .png image to modify.

    Returns:
        None
    """
    with Image.open(png_path) as image:

        # Move left by 160 pixels
        shifted = ImageChops.offset(image, -160, 0)

        shifted.save(png_path)



if __name__ == "__main__":
    print(f"Running ./scripts/DBTunNoTracks/make_dbstun_notracks.py")
    
    config = configparser.ConfigParser()
    config.read("scripts/config.ini")

    ffeditc_path = Path(config["utilities"]["ffeditc_path"])
    input_path = Path(config["shapes"]["input_path"])
    output_path = Path(config["shapes"]["output_path"])

    load_path = input_path
    processed_path = output_path / "DBTunNoTracks"

    match_files = ["DB1s_a1t10mStrtRndTun.s", "DB1s_a2t10mStrtRndTun.s", "DB1s_a1t10mStrtTun.s", "DB1s_a2t10mStrtTun.s"]
    ignore_files = ["*Pnt*", "*Frog*", "*Xover*", "*Slip*", "*DKW*", "*.sd", "*_g.s*", "*6m.s*"]
    
    os.makedirs(processed_path, exist_ok=True)

    shape_names = shapeio.find_directory_files(load_path, match_files, ignore_files)

    for idx, sfile_name in enumerate(shape_names):
        new_sfile_name = sfile_name.replace(".s", "_l_nt.s")
        new_sfile_name = new_sfile_name.replace("DB1s_", "DBs_")

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

    # Create the modified texture
    aceit_path = Path(config["utilities"]["aceit_path"])
    ace2png_path = Path(config["utilities"]["ace2png_path"])
    texture_input_path = Path(config["textures"]["input_path"])
    texture_output_path = Path(config["textures"]["output_path"])
    
    os.makedirs(texture_output_path, exist_ok=True)

    print(f"\tCreating DB_TunWallSFS1L.ace...")

    with tempfile.TemporaryDirectory() as temp_dir:
        ace_input_path = texture_input_path / "DB_TunWallSFS1.ace"
        ace_output_path = texture_output_path / "DB_TunWallSFS1L.ace"
        png_temp_path = os.path.join(temp_dir, "DB_TunWallSFS1.png")

        subprocess.run(
            [str(ace2png_path), "-o", temp_dir, str(ace_input_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

        process_texture(png_temp_path)

        subprocess.run(
            [str(aceit_path), png_temp_path, str(ace_output_path), "-q"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )