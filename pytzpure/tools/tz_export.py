from sys import argv, exit

from pytzpure.tz_export import export

if len(argv) < 2:
    print("Please provide a root-path.")
    exit(1)

root_path = argv[1]

export(root_path)

