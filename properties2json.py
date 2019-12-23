import os;
import json;
import shutil
import re;
import sys;

#given a valid <your file>.properties, produces <your file>.json in the same folder
def prop2json(inputPath):
    if(".properties"!=inputPath[-11:]): raise NameError("invalid filename");
    
    inputText = open(inputPath).read();
    output = open(inputPath.replace(".properties", ".json"), "w+");
    lines = inputText.split("\n");
    objects = {}; #we store every entry as key-value pair within objects

    output.write("{");
    for line in lines:
        if(len(line)==0 or line[0]=='#' or line[0]=='!'): continue; #skipping comments
        equalIndex = line.find("=");
        if(equalIndex==-1): raise NameError(line);
        
        match = re.split(r'\[|\.|\]\=', line[0: equalIndex+1], 1);
        level = objects;
        oName = line[0:equalIndex];
        subName = line[0:equalIndex];
        while(len(match)==2 and match[1]!=""): #reads nested objects, split on " [ ] . = " symbols
            oName = match[0];
            subName = match[1];
            if(oName not in level): level[oName] = {};
            match = re.split(r'\[|\.|\]\=', subName, 1);
            level = level[oName];
        level[subName.strip("[].=")] = line[equalIndex+1:];

    output.write(json.dumps(objects, indent=4)[1:-1]);    
    output.write("}");
    output.close();
    return;

#recursively produces clone of .properties directories as .json 
def convert(folderPath, outputPath):
    shutil.rmtree(outputPath, True);
    shutil.copytree(folderPath, outputPath);
    for (dirName, subdirList, fileList) in os.walk(outputPath):
        for fname in fileList:
            if(".properties"==fname[-11:]): 
                prop2json(dirName+"/"+fname);
                os.remove(dirName+"/"+fname);
    return;

def main():
    usage = "\nTo convert a file: python properties2json.py <FILE NAME>.properties \nTo convert folder: python properties2json.py <SRC> <DEST>\n"

    if(len(sys.argv)<2 or len(sys.argv)>3):
        print(usage);
        raise EnvironmentError("Incorrect number of arguments");

    if(len(sys.argv)==2 and os.path.isdir(sys.argv[1])):
        print(usage);
        raise EnvironmentError("Expected a file where folder was provided");

    if(len(sys.argv)==3 and os.path.isfile(sys.argv[1])):
        print(usage);
        raise EnvironmentError("Expected a folder where file was provided");

    if(len(sys.argv)==3 and os.path.isfile(sys.argv[2])):
        print(usage);
        raise EnvironmentError("Destination must be a folder");

    if(os.path.isdir(sys.argv[1])): convert(sys.argv[1], sys.argv[2]);
    if(os.path.isfile(sys.argv[1])): prop2json(sys.argv[1]);
    return;

main();
