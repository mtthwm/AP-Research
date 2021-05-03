from utils.CommandLineArgs import CommandLineArgs
import sys


args = CommandLineArgs(sys.argv, 'file:str:!', 'readFile:str:!')

with open(args.get('readFile'), 'r') as file:
    lineCount = 0
    wordCount = 0
    characterCount = 0
    for line in file:
        lineCount += 1
        for word in line.split():
            wordCount += 1
            characterCount += len(word)

    print(f"Lines: {lineCount}\nWords: {wordCount}\nCharacters: {characterCount}")