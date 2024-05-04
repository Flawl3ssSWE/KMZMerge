# KMZMerge
A simple Python script that merges multiple KMZ (Keyhole Markup Language Zipped) files into a single one. Through simply extracting all the JPGs from them one by one and adding them to a single folder, then it does the same thing for the KML files. Before zipping all of the files up to a single KMZ file.

## Usage
1. Clone/Download the repository;
2. Place all your KMZ files in the `input` folder (it is possible to have them within subfolders in the input folder);
3. Run the script by running the following command `python KMZMerge.py`
4. Follow the simple prompts the script gives
5. You will very shortly have your combined KMZ file, in the same folder as the KMZMerge.py file.

## Requirements
- Python 3.x

## Notes
There are no guarantees that this will work for your specific use case, as it was developed for my particular needs. I used it to merge numerous small KMZ files covering the Swedish parts of the Scandinavian Mountains for use in my Garmin handheld GPS. These merged files can be opened in Garmin Basecamp, Garmin GPSMAP 66i, and Google Earth Pro. However, I have not tested the resulting KMZ files in any other programs.

I have tested it on KMZ files that include multiple JPGs, and it works for those as well. However, it's important to note that the program expects all the JPGs to have unique names; otherwise, it does not handle the files correctly. If file names clash, it will keep one of them. This means that as long as the JPG files with the same names cover the same area, it will not cause any trouble, as one of them will be kept.