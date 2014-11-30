import arcpy

arcpy.env.workspace = "C:\\Users\\esther\\Desktop\\EBowlin_Final"

arcpy.env.overwriteOutput = True


# define variables 
outFolder = "C:\\Users\\esther\\Desktop\\EBowlin_Final"
fClass = "anomalies.shp"
inputPath = "C:\\Users\\esther\\Desktop\\EBowlin_Final\\anomalies.txt"

try:
    
# open text file for reading
    inputFile = open(inputPath)

# create point shapefile
    arcpy.CreateFeatureclass_management(outFolder, fClass, "POINT")
    print "Created point shapefile."

# add name field to point shapefile
    arcpy.AddField_management(fClass, "anom_ID", "SHORT")
    print "Added 'name' field to point shapefile."

# create insert cursor to add names to name field and x,y coordinates
    cursor = arcpy.da.InsertCursor(fClass, ["anom_ID", "SHAPE@"])
    print "Opened point shapefile for editing."

except:
    print "Feature Class creation failed."


try:
    
# loop through the anomalies text file to add each anomaly name and its coordinates to the point shapefile
    for line in inputFile:
        lineSegment = line.split(",")

        name = lineSegment[0]
        point = arcpy.Point((lineSegment[1]), (lineSegment[2]))
        cursor.insertRow((name, point))
   
    print "Anomalies shapefile created."

# unlock shapefile    
    del cursor

except:
    print "Anomalies shapefile creation failed."


try:
# create for loop that will iterate over the "Grid_ID" column and create grid layer
    gridsPath = "C:\\Users\esther\\Desktop\\EBowlin_Final\\survey_grids.shp"
    fieldList = ["Anom_densi", "Anom_count", "Grid_Area", "Grid_ID"]

    with arcpy.da.UpdateCursor(gridsPath, fieldList) as cursor:
        for row in cursor:
            whereClause = "Grid_ID = '{0}' ".format(row[3])
            print whereClause

# create grids layer utilizing whereClause       
            arcpy.MakeFeatureLayer_management(gridsPath , "grids_lyr", whereClause)

# create anomalies layer
            anomaliesPath = "C:\\Users\\esther\\Desktop\\EBowlin_Final\\anomalies.shp"
            arcpy.MakeFeatureLayer_management(anomaliesPath , "anomalies_lyr")


# use selected grids layer to select anomalies
            arcpy.SelectLayerByLocation_management("anomalies_lyr", "WITHIN", "grids_lyr", "", "NEW_SELECTION")


# count number of anomalies in each grid
            anomaliesCount = int(arcpy.GetCount_management("anomalies_lyr").getOutput(0))
        

# add anomaly count for each grid to grid table           
            row[1] = anomaliesCount
            cursor.updateRow(row)   
            print "There are " + str(row[1]) + " anomalies in this grid."

            
# calculate number of acres per anomaly and add to grid attribute table                
            row[0] = ((row [2]) / (row[1]))
            cursor.updateRow (row)
            print "There are " + str(row[0]) + " square meters per every one anomaly."

    print "File processing complete."

except:
    print "File processing failed."


# unlock shapefile
del cursor

try:
    
# assign a spatial reference to the anomalies shapefile post-processing
    infc = r"C:\\Users\\esther\\Desktop\\EBowlin_Final\\anomalies.shp"
    sr = arcpy.SpatialReference("NAD 1983 UTM Zone 13N")
    arcpy.DefineProjection_management(infc, sr)
    print "Anomalies shapefile projection complete."
    
except:
    print "Anomalies shapefile projection unsuccessful."
