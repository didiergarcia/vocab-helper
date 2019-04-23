#
#
#
#
#
#

import random
import time
import os
import curses

questionsAsked = 0
correctAnswers = 0

# Empty Dictionary and Word List
wordDefs = {}
wordList = []

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


def main(stdscr):

  global questionsAsked
  global correctAnswers

  # Colors
  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

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

  stdscr.clear()
  
  start_time = time.time()
  # Start the Game loop
  while True:
      # Pick the words for this challenge
      currentWordDefs = getRandomWordDefs()

      # Choose the correct word/definition
      correctChoice = random.randint(0, 3)

      # Print the words

      line_num = 0
      # Show the correct definition
      stdscr.addstr(line_num,0, "> {}".format(currentWordDefs[correctChoice][2]))
      
      line_num += 5
      stdscr.move(line_num,0)

      # Show each word with a number choice
      for i in range(4):
          stdscr.addstr(line_num, 0, "{}. {}".format(i+1, currentWordDefs[i][1]))
          line_num += 1

      stdscr.move(line_num, 0)
      line_num += 1

      questionsAsked += 1

      # Get User's selection
      stdscr.addstr(line_num, 0, '"quit" to exit!', curses.color_pair(3))
      line_num += 1
      stdscr.addstr(line_num, 0, '? ')
      selection = stdscr.getkey()

      # Clear screen
      stdscr.clear()
      stdscr.refresh()

      # Handle User's selection
      if selection == "quit" or selection == "q":
          questionsAsked -= 1
          break
      elif selection not in ["1", "2", "3", "4"]:
          # Ignore bad input
          line_num += 2
          stdscr.addstr(line_num, 0, "Wrong :(", curses.color_pair(2))
          line_num +=1
          stdscr.addstr(line_num, 0 ,"{} - {}".format(currentWordDefs[correctChoice][1], currentWordDefs[correctChoice][2]))
      elif (int(selection) - 1) == correctChoice:
          line_num += 2
          stdscr.addstr(line_num, 0 , "Correct!!", curses.color_pair(1))
          line_num += 1
          stdscr.addstr(line_num, 0 ,"{} - {}".format(currentWordDefs[correctChoice][1], currentWordDefs[correctChoice][2]))
          correctAnswers += 1
      else:
          line_num += 2
          stdscr.addstr(line_num, 0, "Wrong :(", curses.color_pair(2))
          line_num += 1
          stdscr.addstr(line_num, 0, "{} - {}".format(currentWordDefs[correctChoice][1], currentWordDefs[correctChoice][2]))

      line_num += 1
      stdscr.move(line_num, 0)

  # Finally print session stats
  line_num = 0
  elapsed_time = time.time() -start_time
  line_num += 1
  stdscr.addstr(line_num, 0, "=" * 25 + " Session Results " + "=" * 25)
  if questionsAsked > 0:
      line_num += 1
      stdscr.addstr(line_num, 0, "Score: {}/{} - {:3.1f}%".format(correctAnswers, questionsAsked, correctAnswers/questionsAsked * 100))

      # calculate time
      # Hours?
      hours = elapsed_time // 3600
      minutes = (elapsed_time - (hours * 3600)) // 60
      seconds = (elapsed_time - (hours * 3600) - (minutes * 60)) // 1

      line_num += 1
      stdscr.addstr(line_num, 0, "Time: {:2.0f} Hrs {:2.0f} Mins {:2.0f} Secs".format(hours, minutes, seconds))
  else:
      line_num += 1
      stdscr.addstr(line_num, 0, "Nothing to see here")

  line_num += 1
  stdscr.addstr(line_num, 0, "=" * 67)
  line_num += 1
  stdscr.addstr(line_num, 0, "Press any key...")

  # Wait for the user to press any key
  stdscr.getkey()

# Start a curses wrapped session.
if __name__ == '__main__':
  curses.wrapper(main)
