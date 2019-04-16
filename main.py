#
#
#
#
#
#

import random
import time
import os

questionsAsked = 0
correctAnswers = 0

# Empty Dictionary and Word List
wordDefs = {}
wordList = []

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def getRandomWordDefs():
    tupleList = []
    wordCount = len(wordList)

    # Get 4 random numbers between 0 and wordCount (exclusive)
    randomIndexList = getDistinctRandoms(wordCount, 4)

    # Build tuples and return
    for i in randomIndexList:
        word = wordList[i]
        definition = wordDefs.get(word)

        #print("Choosing: {}: {} - {}".format(i, word, definition))
        tupleList.append((i, word, definition))

    return tupleList

def getDistinctRandoms( limit, numberOfRandoms ):

    distinctRandoms = []
    currentIndex = 0;

    for i in range(numberOfRandoms):
        newRandom = random.randint(0, limit-1)

        # Make sure that newRandom is distinct
        while newRandom in distinctRandoms:
            newRandom = random.randint(0, limit-1)

        # By now newRandom is assured to be distinct
        distinctRandoms.append(newRandom)

    return distinctRandoms

def getColorCode( color ):
    colorCode = None

    if color == "green":
        colorCode = "\033[92m"
    elif color == "red":
        colorCode = "\033[91m"
    elif color == "blue":
        colorCode = "\033[94m"
    elif color == "yellow":
        colorCode = "\033[93m"

    return colorCode

def getColorCodeEnd():
    return "\033[0m"

def printColor( msg, color ):

    start_color = getColorCode(color)

    if start_color:
        print(start_color + msg + getColorCodeEnd())
    else:
        print(msg)

# Load the definitions file and populate the dictionary
defsFilePointer = open("defs.txt", "r")
wordCounter = 0

for line in defsFilePointer:

    word, definition = line.rstrip().split(":", 2)
    # print("#{} word: {}, definition: {}".format(wordCounter, word, definition))

    wordDefs[word] = definition
    wordList.append(word)

    wordCounter += 1

defsFilePointer.close()

clearScreen()
print("\n\n")

start_time = time.time()
# Start the Game loop
while True:
    # Pick the words for this challenge
    currentWordDefs = getRandomWordDefs()

    # Choose the correct word/definition
    correctChoice = random.randint(0, 3)

    # Print the words

    # Show the correct definition
    print("> {}".format(currentWordDefs[correctChoice][2]))
    print()

    # Show each word with a number choice
    for i in range(4):
        print("{}. {}".format(i+1, currentWordDefs[i][1]))

    print()
    questionsAsked += 1

    # Get User's selection
    printColor('"quit" to exit', "blue")
    selection = input("? ")

    # Clear screen
    clearScreen()

    # Handle User's selection
    if selection == "quit":
        questionsAsked -= 1
        break
    elif selection not in ["1", "2", "3", "4"]:
        # Ignore bad input
        printColor("Wrong :(", "red")
        print("{} - {}".format(currentWordDefs[correctChoice][1], currentWordDefs[correctChoice][2]))
    elif (int(selection) - 1) == correctChoice:
        printColor("Correct!!", "green")
        print()
        correctAnswers += 1
    else:
        printColor("Wrong :(", "red")
        print("{} - {}".format(currentWordDefs[correctChoice][1], currentWordDefs[correctChoice][2]))

    print()

# Finally print session stats
elapsed_time = time.time() -start_time
print("=" * 25 + " Session Results " + "=" * 25)
if questionsAsked > 0:
    print("Score: {}/{} - {:3.1f}%".format(correctAnswers, questionsAsked, correctAnswers/questionsAsked * 100))

    # calculate time
    # Hours?
    hours = elapsed_time // 3600
    minutes = (elapsed_time - (hours * 3600)) // 60
    seconds = (elapsed_time - (hours * 3600) - (minutes * 60)) // 1
    print("Time: {:2.0f} Hrs {:2.0f} Mins {:2.0f} Secs".format(hours, minutes, seconds))
else:
    print("Nothing to see here")
print("=" * 67)
print("\n")

