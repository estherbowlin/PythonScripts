import arcpy

arcpy.env.overwriteOutput = True

arcpy.env.workspace = "C:\\Users\\esther\\Desktop\\Python"

inputPath = "C:\\Users\\esther\\Desktop\\Python\\four_table.txt"
fileOutput = "C:\\Users\\esther\\Desktop\\Python\\four_clean.txt"
f = open(inputPath)
o = open(fileOutput, "w")
for line in f:
    lineSegment = line.split(",")
    x = lineSegment[4]
    if x <> "Latitude":
     xformat = x[0:9]
     print xformat
     

    y = lineSegment[5]
    if y <> "Longitude":
      yformat = y[0:10]
      print yformat

      o.write(xformat + ", " + yformat + ", ")  

    ef = lineSegment[6]
    if ef <> "Elevation":
     efirst = ef[1:]
     es = lineSegment[7]
     esecond = es[:3]
     e = efirst + esecond
     print e

     o.write(e + "\n")

f.close()
o.close()
