
# dbtracks-extras

Python scripts to create extra shapes that complement Norbert Rieger's existing DBTracks shapes.

## Extra shapes available in this package

There are lots of extra custom track sections and shapes available in this package, including:
- Some missing XTracks sections
- XOver7_5d with overhead wire
- Overhead wires without track
- Tunnels without LZB cable
- Tunnels without gantry
- Standalone tunnel gantries
- Short tunnels (0.625d, 1.25d, 2.5d)
- Half Tunnels
- Half Embankments
- Tunnel switches
- Tunnel track sections
- V4hs_RKL single track sections
- V4hs_RKL single tunnel track sections
- V4hs_RKL switches
- V4hs_RKL tunnel switches

For a full of shapes list see [this document](./docs/full-list-of-shapes.md).

<!-- Available for download here: [someplace]() -->

## Creating the modified shapes

### Prerequisites

- Python3
- All DBTracks shapes by Norbert
- Utility programs:
    - [ACE2BMP](https://www.trainsim.com/forums/filelib/search-fileid?fid=89768)
    - [AceIt](https://www.trainsim.com/forums/filelib-search-fileid?fid=67904)
    - ffeditc_unicode.exe (found in MSTS installations)

Download all shapes from [the-train.de](https://the-train.de/downloads/entry-download/11252-dbtracks) and extract all the sub-zipfiles into a single folder.

### Set up a virtual env

Create a virtual env:
```bash
python3 -m venv dbtracks-extras
```

Activate the virtual env:
- Linux / macOS: `source dbtracks-extras/bin/activate`
- Windows (powershell): `dbtracks-extras\Scripts\Activate.ps1`
- Windows (cmd): `dbtracks-extras\Scripts\activate.bat`

### Install dependencies

Install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### Configure paths

Configure the `scripts/config.ini` file with the appropriate paths to `ffeditc_unicode.exe`, the folder with shapes, and to the output-folder.

For example:
```ini
[utilities]
ffeditc_path = C:/path/to/ffeditc_unicode.exe
ace2bmp_path = C:/path/to/ace2bmp.exe
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

[shapes]
input_path = C:/path/to/input/folder/Shapes
output_path = C:/path/to/output/folder/Shapes

[textures]
input_path = C:/path/to/input/folder/Textures
output_path = C:/path/to/output/folder/Textures
```

### Run the zip extraction script

Now extract the DBTracks packages to the input paths using the `extract_zips.py` script:

```bash
python ./scripts/extract_zips.py
```

### Run the scripts

Now you can run each `.py` script to generate the modified shapes. Run the commands from the project root directory.

For example:

```bash
python ./scripts/somefolder/somescript.py
```

You can also run all scripts:

```bash
python ./scripts/run_all.py
```

## Contributing

Contributions of all kinds are welcome. These could be suggestions, issues, bug fixes, documentation improvements, or new scripts.

For more details see the [contribution guidelines](/CONTRIBUTING.md).


## License

The scripts are licensed under [GNU GPL v3](/LICENSE).

All shapes and textures referenced in the scripts are the original work of Norbert Rieger all rights to those belong to him.
