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

import zipfile
from unrar import rarfile
import shutil
from pathlib import Path
import tempfile

if __name__ == "__main__":
    zip_folder = Path("path/to/zip_files")
    output_folder = Path("path/to/output")
    output_folder.mkdir(exist_ok=True, parents=True)

    target_ext = ".txt"

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        for zip_file in zip_folder.glob("*.zip"):
            with zipfile.ZipFile(zip_file, 'r') as z:
                z.extractall(temp_path)
        
        for rar_file in temp_path.glob("*.rar"):
            with rarfile.RarFile(rar_file) as rf:
                for member in rf.infolist():
                    if member.filename.lower().endswith(target_ext):
                        rf.extract(member, temp_path)
                        shutil.copy(temp_path / member.filename, output_folder)

    print(f"All {target_ext} files copied to {output_folder}")
