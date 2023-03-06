"""
Pseudolocalisation based on https://github.com/Shopify/pseudolocalization
"""

# The original included Y, which doesn't make sense. Y isn't a vowel.
VOWELS = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}

LETTERS = {
    'a': 'α',
    'b': 'ḅ',
    'c': 'ͼ',
    'd': 'ḍ',
    'e': 'ḛ',
    'f': 'ϝ',
    'g': 'ḡ',
    'h': 'ḥ',
    'i': 'ḭ',
    'j': 'ĵ',
    'k': 'ḳ',
    'l': 'ḽ',
    'm': 'ṃ',
    'n': 'ṇ',
    'o': 'ṓ',
    'p': 'ṗ',
    'q': 'ʠ',
    'r': 'ṛ',
    's': 'ṡ',
    't': 'ṭ',
    'u': 'ṵ',
    'v': 'ṽ',
    'w': 'ẁ',
    'x': 'ẋ',
    'y': 'ẏ',
    'z': 'ẓ',
    'A': 'Ḁ',
    'B': 'Ḃ',
    'C': 'Ḉ',
    'D': 'Ḍ',
    'E': 'Ḛ',
    'F': 'Ḟ',
    'G': 'Ḡ',
    'H': 'Ḥ',
    'I': 'Ḭ',
    'J': 'Ĵ',
    'K': 'Ḱ',
    'L': 'Ḻ',
    'M': 'Ṁ',
    'N': 'Ṅ',
    'O': 'Ṏ',
    'P': 'Ṕ',
    'Q': 'Ǫ',
    'R': 'Ṛ',
    'S': 'Ṣ',
    'T': 'Ṫ',
    'U': 'Ṳ',
    'V': 'Ṿ',
    'W': 'Ŵ',
    'X': 'Ẋ',
    'Y': 'Ŷ',
    'Z': 'Ż'
}

def pseudolocalise(string):
    pseudolocalisedString = ""
    for character in string:
        if character in LETTERS:
            pseudolocalisedString += LETTERS[character]
            if character in VOWELS:
                pseudolocalisedString += LETTERS[character]
        else:
            pseudolocalisedString += character
    return pseudolocalisedString

import os
import json

TRANSLATABLE_KEYS = {
    'name',
    'displayName',
    'desc',
    'plural',
    'text'
}

thisModuleRoot = os.path.dirname(__file__)

def pseudolocaliseJson(moduleName, moduleAssetsRoot, jsonFilePath):
    print(os.path.realpath(jsonFilePath))
    jsonContents = None
    with open(jsonFilePath, "r", encoding='utf-8') as jsonFile:
        jsonContents = json.load(jsonFile)
    localisedJsonDelta = {}
    localisedJsonOverride = pseudolocaliseDict(jsonContents, localisedJsonDelta)
    relativeFilePath = os.path.relpath(jsonFilePath, start=moduleAssetsRoot)

    useOverride = (jsonFilePath.endswith(".ui"))
    if len(localisedJsonDelta) == 0 and not useOverride:
        return
    
    destinationPath = os.path.join(thisModuleRoot, "deltas" if not useOverride else "overrides", moduleName, relativeFilePath)
    os.makedirs(os.path.dirname(destinationPath), exist_ok=True)
    print(localisedJsonDelta)
    print(destinationPath)
    with open(destinationPath, "w", encoding='utf-8') as localisedFile:
        json.dump(localisedJsonDelta if not useOverride else localisedJsonOverride, localisedFile, ensure_ascii=False, indent=4)

def pseudolocaliseDict(data, deltasDict):
    for key in data:
        if key in TRANSLATABLE_KEYS:
            if type(data[key]) == str:
                data[key] = pseudolocalise(data[key])
                deltasDict[key] = data[key]
        if type(data[key]) == dict:
            deltasDict[key] = {}
            pseudolocaliseDict(data[key], deltasDict[key])
            if len(deltasDict[key]) == 0:
                del deltasDict[key]
        if type(data[key]) == list:
            deltasDict[key] = {}
            for item in data[key]:
                if type(item) == dict:
                    pseudolocaliseDict(item, deltasDict[key])
            if len(deltasDict[key]) == 0:
                del deltasDict[key]
    return data

ALLOWED_DIRECTORIES = {'items', 'ships', 'ui'}

def scanModule(moduleRoot, moduleRootPath):
    assetsRoot = os.path.join(moduleRootPath, "assets")
    for root, directories, files in os.walk(assetsRoot):
        if root == assetsRoot:
            for directory in set(directories):
                if directory not in ALLOWED_DIRECTORIES:
                    directories.remove(directory)
        for file in files:
            if file.endswith(".json") or file.endswith(".ui"):
                pseudolocaliseJson(moduleRoot, assetsRoot, os.path.join(root, file))
if __name__ == "__main__":
    modulesRoot = ".."
    engineModuleRoot = "../../engine/src/main/resources/org/destinationsol/"
    for moduleRoot in os.listdir(modulesRoot):
        moduleRootPath = os.path.join(modulesRoot, moduleRoot)
        if not os.path.isdir(moduleRootPath):
            continue
        scanModule(moduleRoot, moduleRootPath)
    scanModule("engine", engineModuleRoot)
