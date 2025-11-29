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


def make_shapes_table_from_folder(path, columns=4):
    """
    Generates an HTML <table> with N columns from .s files in a folder.

    Parameters:
        path (str): Path to the folder.
        columns (int): Number of columns in the table.

    Returns:
        str: HTML table as a string.
    """
    files = sorted(
        f for f in os.listdir(path)
        if f.lower().endswith(".s") and os.path.isfile(os.path.join(path, f))
    )
    rows = []

    for i in range(0, len(files), columns):
        chunk = files[i:i+columns]
        tds = "".join(f"      <td>{name}</td>\n" for name in chunk)
        row = "    <tr>\n" + tds + "    </tr>"
        rows.append(row)

    table = "<table>\n  <tbody>\n" + "\n".join(rows) + "\n  </tbody>\n</table>"
    return table



if __name__ == "__main__":
    document = []
    folders = [
        #"DB1fb",
        #"V4hs1t_RKL",
        "Xover7_5d",
    ]

    config = configparser.ConfigParser()
    config.read("scripts/config.ini")

    output_path = config["shapes"]["output_path"]

    # Header
    document.append("\n# Full list of shapes\n\n")

    # Description
    document.append("A description\n\n")

    # TOC
    document.append("<details>\n")
    document.append("  <summary>\n    <strong>Table of Contents</strong>\n  </summary>\n\n")
    for folder in folders:
        anchor = folder.lower().replace(" ", "-")
        document.append(f"- [{folder}](#{anchor})\n")
    document.append("\n</details>\n\n")

    # Sections with tables
    for folder in folders:
        document.append(f"## {folder}\n\n")
        if os.path.exists(f"./images/{folder}.png"):
            document.append(f"![{folder}](./images/{folder}.png)\n\n")
        html_table = make_shapes_table_from_folder(f"{output_path}/{folder}", columns=4)
        document.append(f"{html_table}\n\n")

    with open("./docs/full-list-of-shapes.md", "wt", encoding="utf-8") as f:
        f.write("".join(document))
