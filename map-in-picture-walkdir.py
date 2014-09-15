import sys, os
from os import listdir
from os.path import isfile, join

'''
Usage: python map-in-picture-walkpir.py c:/temp/images_for_livejoural/

'''

print "*" * 20
for infile in sys.argv[1:]:
        input_patch = os.path.splitext(infile)[0]

onlyfiles = [ f for f in listdir(input_patch) if isfile(join(input_patch,f)) ]

for filename in onlyfiles:
    path = 'python map-in-picture.py '+input_patch+'\\'+filename
    print path
    os.system(path)
