# Hangman Game
import random
import string
import sys
from tabulate import tabulate

WORDLIST_FILENAME = "words.txt"

responses = [
    "I am thinking of a word that is {0} letters long", #0
    "Congratulations, you won!", #1 
    "Your total score for this game is: {0}", #2
    "Sorry, you ran out of guesses. The word was: {0}",#3
    "You have {0} guesses left.", #4
    "Available letters: {0}", #5
    "Good guess: {0}", #6
    "Oops! That letter is not in my word: {0}", #7
    "Oops! You've already guessed that letter: {0}", #8
]

letters_guessed = []

cPlayer = 999999
cScore = 0

def choose_random_word(all_words):
    return random.choice(all_words)

def load_words():
    '''Loads the list of words into the variable wordlist from the "words.txt" file
    which will be accessible from anywhere in the program.'''
    print(f'Loading word list from file: {WORDLIST_FILENAME}')
    try:
        with open(WORDLIST_FILENAME, 'rt') as wordlist_file:
            wordlist = wordlist_file.read().split()

        print(f'{len(wordlist)} words loaded.\n\n')
        return wordlist
    except:
        print()
        sys.exit(f'The "{WORDLIST_FILENAME}" file does not exist or has the wrong permissions!')

# Load the list of words into the variable wordlist
# Accessible from anywhere in the program
wordlist = load_words()


def is_word_guessed(word, letters_guessed):
    for guess in letters_guessed:
        word = word.replace(guess, '')
    if word == '':
        return True
    else:
        return False

def get_guessed_word(word, letters_guessed):
    guessed_word = ""
    for letter in word:
        for guess in letters_guessed:
        
            if guess == letter:
                guessed_word += guess
                break
        else:
            guessed_word += "_ "
    return guessed_word

def get_remaining_letters(letters_guessed):
    remaining = string.ascii_lowercase
    for guess in letters_guessed:
        remaining = remaining.replace(guess, '')
    return remaining

def hangman():
    global leaderboard, cScore
    cScore = 0
    leaderboard = []
    try:
        with open("scores.txt", 'rt') as scores:
            for score in scores:
                try:
                    score = score.replace('\n', '')
                except:
                    pass
                leaderboard.append(score)
            for leader in leaderboard:
                leaderboard[leaderboard.index(leader)] = leader.split('=')
            for player in leaderboard:
                leaderboard[leaderboard.index(player)][1] = int(leaderboard[leaderboard.index(player)][1])
    except:
        with open("scores.txt", 'wt') as scores:
            scores.write("Prithvi Soma=1412")
        with open("scores.txt", 'rt') as scores:
            for score in scores:
                leaderboard.append(score)
            for leader in leaderboard:
                leaderboard[leaderboard.index(leader)] = leader.split('=')
    print("="*101)
    print("="*101)
    print("\n"+(" "*33)+"Welcome to Hangman Ultimate Edition\n")
    print("="*101)
    print("="*101)
    
def doPLQ():
    global leaderboard, cPlayer, cScore, word
    # Testing Purposes
    # testwordlist = ['hello', 'hi', 'how', 'a', 'proper']
    # word = choose_random_word(testwordlist)

    word = choose_random_word(wordlist)
    plq = input("Do you want to Play (p) view the leaderboard (l) or quit (q): ")
    if plq.lower() == "l":

        print("\n\n"+"="*33)
        print("="*33)
        print((" "*11)+"LEADERBOARD")
        print("="*33)
        print("="*33)
        leaderboard = sorted(leaderboard, key=lambda x: -x[1])
        print(tabulate(leaderboard, headers=["Name", "Score"], tablefmt='fancy_grid') + "\n")
        print("="*33)
        print("="*33+"\n\n")
        doPLQ()
                
    elif plq.lower() == "q":
        sys.exit('Thanks for playing, goodbye!')
    
    elif plq.lower() == "p":
        print("Lets Play!")
        leaderboard = sorted(leaderboard, key=lambda x: -x[1])
        print(tabulate(leaderboard, headers=["Name", "Score"], tablefmt='fancy_grid'))

        cpn = input("What is your name: ").title()
        for player in leaderboard:
            if player[0] == cpn:
                if cPlayer != 999999:
                    if leaderboard[cPlayer][0] != cpn:
                        cScore = 0
                cPlayer = leaderboard.index(player)
                break
        else:
            leaderboard.append([cpn, 0])
            with open("scores.txt", 'at') as scores:
                scores.write(f"\n{cpn}=0")
        leaderboard = sorted(leaderboard, key=lambda x: -x[1])
        for player in leaderboard:
            if player[0] == cpn:
                cPlayer = leaderboard.index(player)
                break
        print(f"Hello {leaderboard[cPlayer][0]}! Let's Go!\n")
        print("="*36)
        print(f"   Your High score so far is: {leaderboard[cPlayer][1]}\n   And your current score is: {cScore}")
        print("="*36)
        print("\n\n"+responses[0].format(len(word))+": "+("_ "*len(word)))

def add_score():
    global cScore
    cScore += 1


def save_score(cPlayer, cScore):
    global leaderboard
    if cScore > leaderboard[cPlayer][1]:
        leaderboard[cPlayer][1] = cScore
    scoreList = ""
    for leader in leaderboard:
        scoreList += f"{leader[0]}={leader[1]}\n"
    else:
        with open("scores.txt", 'wt') as scores:
            scores.write(scoreList)

def gameLoop():
    doPLQ()
    global guesses
    while guesses > 0 and is_word_guessed(word, letters_guessed) == False:
        print(responses[4].format(guesses))
        print(responses[5].format(get_remaining_letters(letters_guessed)))
        user_guess = input('Please guess a letter: ').lower()

        # User types in more than one letter
        if len(user_guess) > 1:
            for char in user_guess:
                if not char.isalpha():
                    print(f"Your guess '{char}' was invalid! : {get_guessed_word(word, letters_guessed)}")
                    print('---------------------------------\n')
                    guesses -= 1
                    if guesses != 0:
                        continue
                    else:
                        break

                if any(char in s for s in letters_guessed):
                    print(f'As for letter "{char}"...')
                    print("You already guessed it: {0}".format(get_guessed_word(word, letters_guessed)))
                    print('---------------------------------\n')
                    if guesses != 0:
                        continue
                    else:
                        break


                # User guessed letter correctly
                if word.find(char) != -1:
                    # good guess
                    letters_guessed.append(char)
                    print(f'Letter "{char}" is a correct guess!')
                    print(responses[6].format(get_guessed_word(word, letters_guessed)))
                    print('---------------------------------\n')
                    if guesses != 0:
                        continue
                    else:
                        break
                else:
                    # wrong guess
                    letters_guessed.append(char)
                    print(f'Letter "{char}" is a wrong guess..')
                    print("Its not in my word: {0}".format(get_guessed_word(word, letters_guessed)))
                    print('---------------------------------\n')
                    guesses -= 1
                    if any(char in s for s in "aeiou"):
                        guesses -= 1
                    if guesses != 0:
                        continue
                    else:
                        break
            continue

        if not user_guess.isalpha():
            print("Your guess was invalid!")
            print('---------------------------------\n')
            guesses -= 1
            continue

        # User already guessed it
        if any(user_guess in s for s in letters_guessed):
            print(responses[8].format(get_guessed_word(word, letters_guessed)))
            print('---------------------------------\n')
            continue


        # User guessed letter correctly
        if word.find(user_guess) != -1:
            # good guess
            letters_guessed.append(user_guess)
            print(responses[6].format(get_guessed_word(word, letters_guessed)))
            print('---------------------------------\n')
            continue
        else:
            # wrong guess
            letters_guessed.append(user_guess)
            print(responses[7].format(get_guessed_word(word, letters_guessed)))
            print('---------------------------------\n')
            guesses -= 1
            if any(user_guess in s for s in "aeiou"):
                guesses -= 1
            continue
    else:
        if is_word_guessed(word, letters_guessed):
            print(responses[1])
            add_score()
            print(responses[2].format(cScore))
            continueGameFunc()

        else:
            print(responses[3].format(word))
            continueGameFunc()

def continueGameFunc():
    global guesses, cPlayer, cScore, letters_guessed, leaderboard
    continueGame = input("\n\nWould you like to continue the game? [y/n]: ")
    save_score(cPlayer, cScore)
    guesses = 6
    letters_guessed = []
    if continueGame == "y":
        # reset guesses and start the loop
        gameLoop()

    elif continueGame == "n":
        print("Here are the final score list!")
        leaderboard = sorted(leaderboard, key=lambda x: -x[1])
        print(tabulate(leaderboard, headers=["Name", "Score"], tablefmt='fancy_grid'))
        sys.exit('\n\nThanks for playing, goodbye!')

        
    else:
        print("Invalid input! Please Try again...")
        continueGameFunc()

def main():
    global guesses, word
    guesses = 6
    hangman()
    gameLoop()
    
# Driver function for the program
if __name__ == "__main__":
    main()
