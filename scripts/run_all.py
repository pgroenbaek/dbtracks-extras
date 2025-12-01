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

import subprocess

if __name__ == "__main__":
    scripts = [
        "scripts/DBxfb/convert_db1s_to_db1fb.py",
        "scripts/DBxfb/convert_db1s_to_db2fb.py",
        "scripts/DBxfb/convert_db1s_to_db10fb.py",
        "scripts/DBxfb/convert_db1s_to_db20fb.py",
        "scripts/DBxfb/convert_db1s_to_db22fb.py",
        "scripts/V4hs1t_RKL/convert_db1z1t_to_v4hs1trkl.py",
        "scripts/Xover7_5d/make_ohw_xover7_5d.py",
    ]

    for s in scripts:
        subprocess.run(["python", s])