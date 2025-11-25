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

import shutil
import zipfile
import tempfile
import configparser
from unrar.cffi import rarfile
from pathlib import Path


def extract_from_rars(
    rar_paths: list[Path],
    temp_path: Path,
    targets: dict[str, Path]
):
    """
    Extract selected file types from a list of RAR archives into destination folders.

    This function scans each RAR archive for files matching specific extensions,
    extracts matching files into a temporary directory, and copies the final
    extracted files into the configured output folders. Nested directories inside
    the RAR archives are fully supported.

    Args:
        rar_paths (list[Path]):
            A list of paths to RAR files that should be processed.
        temp_path (Path):
            A temporary directory where RAR members are extracted before final copy.
        targets (dict[str, Path]):
            A mapping where keys are file extensions (e.g., ".s", ".sd", ".ace")
            and values are the destination folders where extracted files should
            be copied.

    Returns:
        None: The function performs file extraction and copying as a side effect.

    Raises:
        FileNotFoundError: If any of the provided RAR paths do not exist.
        rarfile.Error: If a RAR archive is corrupted or cannot be opened.
        shutil.Error: If copying extracted files fails.
    """
    for rar_file in rar_paths:
        print(f"Processing RAR: {rar_file}")

        rf = rarfile.RarFile(str(rar_file))
        for member in rf.infolist():
            filename = member.filename.lower()

            for ext, dest_folder in targets.items():
                if filename.endswith(ext):
                    if member.is_dir():
                        continue

                    data = rf.read(member.filename)
                    dest = dest_folder / Path(member.filename).name
                    dest.parent.mkdir(parents=True, exist_ok=True)

                    with open(dest, "wb") as out_f:
                        out_f.write(data)
                    
                    print(f"  Copied {member.filename} to {dest_folder}")

        print(f"Finished {rar_file}\n")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("scripts/config.ini")

    shape_input_path = Path(config["shapes"]["input_path"])
    texture_input_path = Path(config["textures"]["input_path"])

    shape_input_path.mkdir(exist_ok=True, parents=True)
    texture_input_path.mkdir(exist_ok=True, parents=True)

    zipfile_paths = [
        Path(config["dbtracks"]["babds1_zip_path"]),
        Path(config["dbtracks"]["db1_zip_path"]),
        Path(config["dbtracks"]["db2_zip_path"]),
        Path(config["dbtracks"]["db3_zip_path"]),
        Path(config["dbtracks"]["db4_zip_path"]),
        Path(config["dbtracks"]["db5_zip_path"]),
        Path(config["dbtracks"]["dbtextures_zip_path"]),
        Path(config["dbtracks"]["dr2_zip_path"]),
        Path(config["dbtracks"]["nrzubehoer_zip_path"])
    ]

    targets = {
        ".s": shape_input_path,
        ".sd": shape_input_path,
        ".ace": texture_input_path
    }

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for zip_file in zipfile_paths:
            print(f"Extracting ZIP: {zip_file}")
            with zipfile.ZipFile(zip_file, 'r') as z:
                z.extractall(temp_path)

        rar_files = list(temp_path.rglob("*.rar"))
        extract_from_rars(rar_files, temp_path, targets)

    print("\nAll extraction complete!")
