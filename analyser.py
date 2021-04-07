import sys

from etl.extractor.extractor import Extractor

file_id = int(sys.argv[1])

Extractor(file_id).execute()
