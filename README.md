
# dbtracks-extras

Python scripts to create extra shapes that complement Norbert Rieger's existing DBTracks shapes.

## Extra shapes available in this package

There are lots of extra custom track sections and shapes available in this package, including:
- Some missing XTracks sections
- XOver7_5d with overhead wire
- Overhead wires without track
- Tunnels without LZB cable
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

## Running the scripts

Download all shapes from [the-train.de](https://the-train.de/downloads/entry-download/11252-dbtracks) and extract all the sub-zipfiles into a single folder.

Create a virtual env:
```python

```

Configure the `.ini` file with the appropriate paths to `ffeditc_unicode.exe`, the folder with shapes, and to the output-folder.

Now you can run each `.py` script to generate the modified shapes.


## Contributing

Contributions of all kinds are welcome. These could be suggestions, issues, bug fixes, documentation improvements, or new features.

For more details see the [contribution guidelines](/CONTRIBUTING.md).


## License

The scripts are licensed under [GNU GPL v3](/LICENSE).

All shapes and textures referenced in the scripts are the original work of Norbert Rieger all rights to those belong to him.
