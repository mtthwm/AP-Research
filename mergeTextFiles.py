import sys

try:
    filenames = sys.argv[2:len(sys.argv)]
    outname = sys.argv[1]
except IndexError as e:
    print("Please specify an outfile then the list of files to merge.")
    quit()

print(filenames)

with open(outname, 'a') as outfile:
    for x in filenames:
        with open(x, 'r') as readfile:
            for line in readfile:
                outfile.write(line)
