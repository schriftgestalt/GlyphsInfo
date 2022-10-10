import argparse
import sys
from pathlib import Path

from lxml import etree

parser = argparse.ArgumentParser()
parser.add_argument(
    "xml_files", nargs="+", type=Path, help="The GlyphData XML files to check."
)
parsed_args = parser.parse_args()

found_error = False
for xml_file in parsed_args.xml_files:
    parser = etree.XMLParser(dtd_validation=True, recover=True)
    xml = xml_file.read_bytes()
    _ = etree.fromstring(xml, parser)
    for error in parser.error_log:
        found_error = True
        print(xml_file, error)

if found_error:
    sys.exit(1)
