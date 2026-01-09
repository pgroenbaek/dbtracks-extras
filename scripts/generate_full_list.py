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


def natsort(s: str):
    """
    Generate a natural-sort key for a string.

    This function splits the input string into numeric and non-numeric
    components. Numeric parts are converted to integers so that sorting
    correctly handles values like `file2` < `file10`. Non-numeric parts
    are lowercased for case-insensitive comparison.

    Args:
        s (str): The input string to generate a sort key for.

    Returns:
        list: A list of integers and strings representing the sortable key.
    """
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]


def count_shapes_in_folder(path: str, recursive: bool = False) -> int:
    """
    Count `.s` files in a folder.

    Counts all regular files ending with the `.s` extension
    (case-insensitive). When `recursive` is True, all subfolders
    are scanned; otherwise, only the top-level folder is inspected.

    Args:
        path (str): The folder to scan.
        recursive (bool, optional): Whether to include subfolders.
            Defaults to False.

    Returns:
        int: Number of `.s` files found.

    Raises:
        FileNotFoundError: If the path does not exist.
        NotADirectoryError: If the path is not a folder.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Not a directory: {path}")

    iterator = (
        os.walk(path)
        if recursive
        else [(path, [], os.listdir(path))]
    )

    count = 0
    for root, dirs, files in iterator:
        for f in files:
            if f.lower().endswith(".s"):
                full = os.path.join(root, f)
                if os.path.isfile(full):
                    count += 1

    return count


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
        (f for f in os.listdir(path)
        if f.lower().endswith(".s") and os.path.isfile(os.path.join(path, f))),
        key=natsort
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
    config = configparser.ConfigParser()
    config.read("scripts/config.ini")

    output_path = config["shapes"]["output_path"]
    num_shapes_total = count_shapes_in_folder(output_path, recursive=True)

    folders = sorted(
        (item for item in os.listdir(output_path)
        if os.path.isdir(os.path.join(output_path, item))),
        key=natsort
    )

    # Header
    document = ["\n# Full list of shapes\n\n"]

    # Description
    document.append("This is the full list of shapes included in the DBTracks Extras package. None of these exist in Norbert's original packages - they serve as complementary additions to the original shapes.\n\n")
    document.append(f"Total number of shapes: {num_shapes_total}\n\n")

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
        num_shapes = count_shapes_in_folder(f"{output_path}/{folder}")
        document.append(f"Number of shapes: {num_shapes}\n\n")

        if os.path.exists(f"./images/{folder}.png"):
            document.append(f"![{folder}](./images/{folder}.png)\n\n")
        
        html_table = make_shapes_table_from_folder(f"{output_path}/{folder}", columns=4)
        document.append(f"{html_table}\n\n")

    os.makedirs("./docs", exist_ok=True)

    with open("./docs/full-list-of-shapes.md", "wt", encoding="utf-8") as f:
        f.write("".join(document))
