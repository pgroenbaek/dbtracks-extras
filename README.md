
# dbtracks-extras

<!-- [![Release v1.0.0](https://img.shields.io/badge/Latest%20Version-v1.0.0-blue?style=flat)]() -->

![No releases](https://img.shields.io/badge/Latest%20Version-no%20releases-red?style=flat)
[![Python 3.7 - 3.13](https://img.shields.io/badge/Python-3.7%20%E2%80%93%203.13-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License GNU GPL v3](https://img.shields.io/badge/License-%20%20GNU%20GPL%20v3%20-lightgrey?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NDAgNTEyIj4KICA8IS0tIEZvbnQgQXdlc29tZSBGcmVlIDYuNy4yIGJ5IEBmb250YXdlc29tZSAtIGh0dHBzOi8vZm9udGF3ZXNvbWUuY29tIExpY2Vuc2UgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbS9saWNlbnNlL2ZyZWUgQ29weXJpZ2h0IDIwMjUgRm9udGljb25zLCBJbmMuIC0tPgogIDxwYXRoIGZpbGw9IndoaXRlIiBkPSJNMzg0IDMybDEyOCAwYzE3LjcgMCAzMiAxNC4zIDMyIDMycy0xNC4zIDMyLTMyIDMyTDM5OC40IDk2Yy01LjIgMjUuOC0yMi45IDQ3LjEtNDYuNCA1Ny4zTDM1MiA0NDhsMTYwIDBjMTcuNyAwIDMyIDE0LjMgMzIgMzJzLTE0LjMgMzItMzIgMzJsLTE5MiAwLTE5MiAwYy0xNy43IDAtMzItMTQuMy0zMi0zMnMxNC4zLTMyIDMyLTMybDE2MCAwIDAtMjk0LjdjLTIzLjUtMTAuMy00MS4yLTMxLjYtNDYuNC01Ny4zTDEyOCA5NmMtMTcuNyAwLTMyLTE0LjMtMzItMzJzMTQuMy0zMiAzMi0zMmwxMjggMGMxNC42LTE5LjQgMzcuOC0zMiA2NC0zMnM0OS40IDEyLjYgNjQgMzJ6bTU1LjYgMjg4bDE0NC45IDBMNTEyIDE5NS44IDQzOS42IDMyMHpNNTEyIDQxNmMtNjIuOSAwLTExNS4yLTM0LTEyNi03OC45Yy0yLjYtMTEgMS0yMi4zIDYuNy0zMi4xbDk1LjItMTYzLjJjNS04LjYgMTQuMi0xMy44IDI0LjEtMTMuOHMxOS4xIDUuMyAyNC4xIDEzLjhsOTUuMiAxNjMuMmM1LjcgOS44IDkuMyAyMS4xIDYuNyAzMi4xQzYyNy4yIDM4MiA1NzQuOSA0MTYgNTEyIDQxNnpNMTI2LjggMTk1LjhMNTQuNCAzMjBsMTQ0LjkgMEwxMjYuOCAxOTUuOHpNLjkgMzM3LjFjLTIuNi0xMSAxLTIyLjMgNi43LTMyLjFsOTUuMi0xNjMuMmM1LTguNiAxNC4yLTEzLjggMjQuMS0xMy44czE5LjEgNS4zIDI0LjEgMTMuOGw5NS4yIDE2My4yYzUuNyA5LjggOS4zIDIxLjEgNi43IDMyLjFDMjQyIDM4MiAxODkuNyA0MTYgMTI2LjggNDE2UzExLjcgMzgyIC45IDMzNy4xeiIvPgo8L3N2Zz4=&logoColor=%23ffffff)](/LICENSE)

Python scripts to create extra shapes that complement Norbert Rieger's existing DBTracks shapes.

> [!NOTE]
> The scripts in this repository are **work in progress**.
> There are no releases yet. And expect the generated shapes to potentially be weird or broken in some way.

## Extra shapes available from this package

Currently there are no releases, but scripts for the following have been made so far:
- Missing XTracks sections for some fb variants
- XOver7_5d with overhead wire
- Some fb track variants without tunnel walls
- V4hs_RKL 1t track sections
- Some V4hs tunnels without tracks

For a full of shapes list see [this document](./docs/full-list-of-shapes.md).

## Planned
- More missing XTracks sections for other b and fb variants
- Overhead wires without track
- Tunnels without LZB cable
- Tunnels without gantry
- Tunnels without track
- Standalone tunnel gantries
- Short tunnels (0.625d, 1.25d, 2.5d)
- Switches/frogs with fb variant embankments
- Half Tunnels
- Half Embankments
- Tunnel switches/frogs
- Tunnel track sections
- V4hs_RKL 1t tunnel track sections
- V4hs_RKL switches/frogs
- V4hs_RKL tunnel switches/frogs


## Generating the modified shapes

### Prerequisites

- Python 3.7 to 3.13
- All DBTracks packages from [the-train.de](https://the-train.de/downloads/entry-download/11252-dbtracks):
    - BAB_DS1.zip
    - DB_Textures.zip
    - DB1.zip
    - DB2.zip
    - DB3.zip
    - DB4.zip
    - DB5.zip
    - NR_Zubehoer.zip
- The ATracks package from [trainsim.com](https://www.trainsim.com/forums/filelib/search-fileid?fid=88570)
- The V4 shapes e.g. from the [NIM](https://the-train.de/downloads/entry/11011-schnellfahrstrecke-n%C3%BCrnberg-ingolstadt-m%C3%BCnchen-v1-0/), [ICE-HB](https://the-train.de/downloads/entry/11282-sfs-hannover-berlin-v3/) and [Köln-Frankfurt](https://the-train.de/downloads/entry/2724-neubaustrecke-k%C3%B6ln-rhein-main-v-1-2/) routes.
- Utility programs:
    - ffeditc_unicode.exe (found in the utils folder of an MSTS installation)
    - ace2png.exe from Pete Willard's [Ace2DDS package](https://github.com/pwillard/Ace2DDS/releases)
    - [AceIt](https://www.trainsim.com/forums/filelib-search-fileid?fid=67904)

### Set up a virtual env

Create a virtual env. You only need to do this once.

```bash
python -m venv dbtracks-extras
```

To activate the virtual env:
- Linux / macOS: `source dbtracks-extras/bin/activate`
- Windows (powershell): `dbtracks-extras\Scripts\Activate.ps1`
- Windows (cmd): `dbtracks-extras\Scripts\activate.bat`

### Install dependencies

Install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### Configure paths

Configure the `scripts/config.ini` file with the appropriate paths to the utility programs, the DBTracks zip-file packages, and to the input/output-folder.

For example:
```ini
[utilities]
ffeditc_path = C:/path/to/ffeditc_unicode.exe
ace2png_path = C:/path/to/ace2png.exe
aceit_path = C:/path/to/aceit.exe

[dbtracks]
babds1_zip_path = C:/path/to/BAB_DS1.zip
db1_zip_path = C:/path/to/DB1.zip
db2_zip_path = C:/path/to/DB2.zip
db3_zip_path = C:/path/to/DB3.zip
db4_zip_path = C:/path/to/DB4.zip
db5_zip_path = C:/path/to/DB5.zip
dbtextures_zip_path = C:/path/to/DB_Textures.zip
dr2_zip_path = C:/path/to/DR2.zip
nrzubehoer_zip_path = C:/path/to/NR_Zubehoer.zip

[atracks]
atracks_zip_path = C:/path/to/default-track-atrack-01apr25.zip

[shapes]
input_path = C:/path/to/input/folder/Shapes
output_path = C:/path/to/output/folder/Shapes

[textures]
input_path = C:/path/to/input/folder/Textures
output_path = C:/path/to/output/folder/Textures
```

### Run the zip extraction script

Now extract the zip-file packages using the `extract_zips.py` script:

```bash
python ./scripts/extract_zips.py
```

This will take all `.s`, `.sd` and `.ace` files from the zip-files and put them into the input folders.

The DBTracks zip-files contain nested rar-files each with subfolders, so it's easier to extract them all through scripting than by hand.

### Run the scripts

Now you can run each `.py` script to generate the modified shapes. Run the commands from the project root directory.

For example:

```bash
python ./scripts/somefolder/somescript.py
```

You can also run all scripts at once:

```bash
python ./scripts/run_all.py
```

## Contributing

Contributions of all kinds are welcome. These could be suggestions, issues, bug fixes, documentation improvements, or new scripts.

For more details see the [contribution guidelines](/CONTRIBUTING.md).


## License

The scripts are licensed under [GNU GPL v3](/LICENSE).

All shapes and textures referenced in the scripts are the original work of Norbert Rieger, and all rights to them belong to him.

