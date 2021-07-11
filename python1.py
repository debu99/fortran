import sys
from datetime import datetime
from random import randrange
if len(sys.argv) > 1:
    filename = "py1_output_" + sys.argv[1] + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(randrange(0, 1000)) + ".bin"
    print(filename)
else:
    sys.exit(1)