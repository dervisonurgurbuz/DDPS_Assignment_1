import requests
import io
import zipfile
import shutil
import gzip
import os

# Get wikipedia dataset
r = requests.get("https://snap.stanford.edu/data/wikipedia.zip")
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("/var/scratch/ddps2202/DDPS_Assignment_1/datasets")

# Get soc-epinions dataset
r = requests.get("https://snap.stanford.edu/data/soc-Epinions1.txt.gz")
open('/var/scratch/ddps2202/DDPS_Assignment_1/datasets/soc-Epinions1.txt.gz', 'wb').write(r.content)
with gzip.open('/var/scratch/ddps2202/DDPS_Assignment_1/datasets/soc-Epinions1.txt.gz', 'rb') as f_in:
    with open('/var/scratch/ddps2202/DDPS_Assignment_1/datasets/soc-Epinions1.txt', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
with open('/var/scratch/ddps2202/DDPS_Assignment_1/datasets/soc-Epinions1.txt') as f:
    lines = f.readlines()
lines = lines[4:] # Remove first 4 lines of txt file
f = open("/var/scratch/ddps2202/DDPS_Assignment_1/datasets/soc-Epinions1.txt", "w")
f.writelines(lines)
f.close()
os.remove('/var/scratch/ddps2202/DDPS_Assignment_1/datasets/soc-Epinions1.txt.gz')

# Get wiki top categories dataset
r = requests.get("https://snap.stanford.edu/data/wiki-topcats.txt.gz")
open('/var/scratch/ddps2202/DDPS_Assignment_1/datasets/wiki-topcats.txt.gz', 'wb').write(r.content)
with gzip.open('/var/scratch/ddps2202/DDPS_Assignment_1/datasets/wiki-topcats.txt.gz', 'rb') as f_in:
    with open('/var/scratch/ddps2202/DDPS_Assignment_1/datasets/wiki-topcats.txt', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
os.remove('/var/scratch/ddps2202/DDPS_Assignment_1/datasets/wiki-topcats.txt.gz')

with open('/var/scratch/ddps2202/DDPS_Assignment_1/datasets/wiki-topcats.txt') as f:
    newText=f.read().replace(' ', '\t')

with open('/var/scratch/ddps2202/DDPS_Assignment_1/datasets/wiki-topcats.txt', "w") as f:
    f.write(newText)