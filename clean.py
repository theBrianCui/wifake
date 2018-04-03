import os
import re

# removes all junk files produced from being in monitor mode
for f in os.listdir("."):
    if re.search("test-[0-9]+", f):
        os.remove(f)

print("Done")
