import os, json5, json, argparse, random, string, shutil
import glob as _glob
from glob import glob
from distutils.dir_util import copy_tree

from src.Logger import logger
from src.util import *

DIR = os.path.dirname(__file__)

if not os.path.exists('input/'):
    logger.error('Please place your input mods in the input folder!')
    os.makedirs('input')
    exit()

if os.path.exists('output/'):
    shutil.rmtree('output/')
    
if not os.path.exists('output/'):
    os.mkdir('output/')

def main():
    input_mods = os.listdir('input')
    parser = argparse.ArgumentParser(
        prog='cp-merger',
        description='A tool to merge Content Patcher mods.')
    parser.add_argument('-i', '--modid', '--id')
    args = parser.parse_args()
    
    outputID = args.modid
    if outputID == None:
        outputID = f'merged_cp_mod.of{len(input_mods)}_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        logger.warn(f'No mod ID specified. Will use "{outputID}"')

    logger.info(f'Output mod will have ID {outputID}')

    outputManifest = {
        "Name": "Merged: ",
        "Author": "CP Merger, ",
        "Version": "1.0.0",
        "Description": "A merged version of: ",
        "UniqueID": outputID,
        "UpdateKeys": [],
        "ContentPackFor": {
            "UniqueID": "Pathoschild.ContentPatcher"
        }
    }
    
    outputContent = {}

    for folder in os.listdir('input'):
        moddir = os.path.join(DIR, 'input', folder)
        manifest = json5.load(open(os.path.join(moddir, 'manifest.json')))

        subfolders = glob(_glob.escape(moddir.replace("\\", "/")) + '/*/')
        print(subfolders)
        print(moddir.replace("\\", "/") + '/*/')
        
        if manifest.get('ContentPackFor') \
            and manifest['ContentPackFor']['UniqueID'].lower() != 'pathoschild.contentpatcher':
            logger.error(f'Skipping {manifest["Name"]} (Not Content Patcher)')
            continue
        else:
            logger.success(f'Found {manifest["Name"]}')
        
        content = json5.load(open(os.path.join(moddir, 'content.json')))

        outputManifest["Name"] += manifest["Name"] + ', '
        outputManifest["Description"] += manifest["Name"]  + ', '
        outputManifest["Author"] += manifest["Author"]  + ', '
        

        for configKey in default(content, "ConfigSchema", {}):
            config = content['ConfigSchema'][configKey]
            if "ConfigSchema" not in outputContent:
                outputContent["ConfigSchema"] = {}

            config["$sourcemod"] = manifest["UniqueID"]

            outputContent["ConfigSchema"][configKey] = config
        
        for token in default(content, "DynamicTokens", []):
            if "DynamicTokens" not in outputContent:
                outputContent["DynamicTokens"] = []

            token["$sourcemod"] = manifest["UniqueID"]
            outputContent["DynamicTokens"].append(token)

        for location in default(content, "CustomLocations", []):
            if "CustomLocations" not in outputContent:
                outputContent["CustomLocations"] = []

            location["$sourcemod"] = manifest["UniqueID"]
            outputContent["CustomLocations"].append(location)

        for change in default(content, "Changes", []):
            if "Changes" not in outputContent:
                outputContent["Changes"] = []

            if 'LogName' not in change:
                change['LogName'] = ''
            change['LogName'] += f' - {manifest["UniqueID"]}'

            if 'FromFile' in change:
                change['FromFile'] = manifest["UniqueID"] + '/' + change['FromFile']

            change["$sourcemod"] = manifest["UniqueID"]
            outputContent["Changes"].append(change)

        if subfolders != []:
            os.makedirs(f'output/{manifest["UniqueID"]}')

        for subfolder in subfolders:
            copy_tree(
                os.path.join(moddir, subfolder),
                f'output/{manifest["UniqueID"]}'
            )
        


    json.dump(
        outputManifest,
        open('output/manifest.json', 'w'),
        indent=4
    )
    json.dump(
        outputContent,
        open('output/content.json', 'w'),
        indent=4
    )

    logger.success('Complete.')


if __name__ == '__main__':
    main()