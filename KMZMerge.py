### KMZMerge ###

import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

# Extract the JPG files from the KMZ files and put them in the tmp folder
def extractJPG(kmzFile):
    jpgFiles = []
    with zipfile.ZipFile(kmzFile, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.jpg'):
                filename = os.path.basename(file)
                jpgFiles.append(filename)
                with zip_ref.open(file) as source, open(os.path.join('tmp', filename), 'wb') as target:
                    shutil.copyfileobj(source, target)
    return jpgFiles

# Merge KML files
def mergeKMLFiles(kmzFiles, folderName):
    # Some weird KML stuff, do not ask me about it please as I do not understand any of it
    namespaces = {
        "": "http://www.opengis.net/kml/2.2",
        "gx": "http://www.google.com/kml/ext/2.2",
        "kml": "http://www.opengis.net/kml/2.2",
        "atom": "http://www.w3.org/2005/Atom"
    }
    kmlFilesCombinedEncoded = ET.Element('{http://www.opengis.net/kml/2.2}kml', nsmap=namespaces)
    folder = ET.SubElement(kmlFilesCombinedEncoded, '{http://www.opengis.net/kml/2.2}Folder')
    folderNameElement = ET.SubElement(folder, '{http://www.opengis.net/kml/2.2}name')
    folderNameElement.text = folderName
    
    for kmzFile in kmzFiles:
        with zipfile.ZipFile(kmzFile, 'r') as zip_ref:
            docKML = zip_ref.extract('doc.kml')
            tree = ET.parse(docKML)
            root_element = tree.getroot()
            for child in root_element.findall('.//{http://www.opengis.net/kml/2.2}GroundOverlay'):
                folder.append(child)
    
    # Remove stray KML file that is left when program has been run            
    os.remove(docKML)                
    
    return kmlFilesCombinedEncoded

# Create KMZ file
def createKMZ(kmlFilesCombinedEncoded, jpgFiles, outputKMZ):
    # Create KML content as a string
    kmlContent = ET.tostring(kmlFilesCombinedEncoded, encoding="utf-8", xml_declaration=True)
    kmlString = kmlContent.decode()

    # Fixes some stuff in the KML file, someone more knowledgeable about this could probably fix these tags within the mergeKML function
    kmlString = kmlString.replace('ns0:', '')
    kmlString = kmlString.replace(
        f'<kml xmlns:ns0="http://www.opengis.net/kml/2.2" nsmap="{{\'\': \'http://www.opengis.net/kml/2.2\', \'gx\': \'http://www.google.com/kml/ext/2.2\', \'kml\': \'http://www.opengis.net/kml/2.2\', \'atom\': \'http://www.w3.org/2005/Atom\'}}"><Folder><name>{userInputtedName}</name><GroundOverlay>', 
        f'<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom"><Folder><name>{userInputtedName}</name><GroundOverlay>'
    )

    with zipfile.ZipFile(outputKMZ, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Write the appended KML content to the file
        with zipf.open('doc.kml', 'w') as kml_file:
            kml_file.write(kmlString.encode())

        # Add the JPG files to the KMZ file
        for jpgFile in jpgFiles:
            zipf.write(os.path.join('tmp', jpgFile), os.path.join('files', jpgFile))

############
### Main ###
############
os.makedirs('tmp', exist_ok=True)  

# Get KMZ files from input directory recursively
kmzFiles = []
for root, dirs, files in os.walk('input'):
    for file in files:
        if file.endswith('.kmz'):
            kmzFiles.append(os.path.join(root, file))

# Extract JPG files from KMZ files
jpgFiles = []
for kmzFile in kmzFiles:
    jpgFiles.extend(extractJPG(kmzFile))

userInputtedName = input("Please enter the desired name of the merged KMZ file: ")

kmlFilesCombinedEncoded = mergeKMLFiles(kmzFiles, userInputtedName)

createKMZ(kmlFilesCombinedEncoded, jpgFiles, f"{userInputtedName}.kmz")

shutil.rmtree('tmp')

print("Successfully merged the KMZ files")
