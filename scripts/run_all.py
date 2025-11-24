import subprocess

if __name__ == "__main__":
    scripts = [
        "scripts/DBxfb/convert_db1s_to_db1fb.py",
        "scripts/V4hsRKL1t/convert_db1z1t_to_v4hsrkl1t.py",
        "scripts/XOver7_5d/make_ohw_xover7_5d.py",
    ]

    for s in scripts:
        subprocess.run(["python", s])