import os.path

MAX_TRIES = 6

def HANGMAN_ASCII_ART():
    return """ _   _
| | | |
| |_| | __ _ _ __   __ _ _ __ ___   __ _ _ __
|  _  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \\
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |
                   |___/
                   
For quitting the game any time - enter 0\n"""


hangman_photos = {
    6: """x-------x
.|       |
.|       
.|
.|
.|""",
    5: """x-------x
.|       |
.|       0
.|
.|
.|""",
    4: """x-------x
.|       |
.|       0
.|       |
.|      
.|""",
    3: """x-------x
.|       |
.|       0
.|      /|
.|      
.|""",
    2: """x-------x
.|       |
.|       0
.|      /|\\
.|      
.|""",
    1: """x-------x
.|       |
.|       0
.|      /|\\
.|      / 
.|""",
    0: """x-------x
|       |
|       0
|      /|\\
|      / \\
|"""
}

def checking_file_path(file_path):
    """Checking if the file exist - if not return False, if yes return True
    :file_path: a path the player enter
    :type file_path: str
    :return: True or False
    :return type: boolean
    """
    if(not(os.path.exists(file_path))):
        return False
    return True

def choose_word(file_path, index):
    """First, the function checking if the file is epmty. 
    If yes - it returns en empty string.
    If not - it builds a tuple containing the number of different words in the file, and a word selected by its position defined by the index.
    :file_path: a path to a file to choose word from
    :type file_path: str
    :index: index of a word in the file
    :type index: int
    :return: empty str or the secret word
    :return type: str
    """
    with open(file_path, "r") as file_of_words:
        file_data = file_of_words.read()
    # Checking if the file is empty
    if(file_data == ""):
        return ""
    # If the file is not empty
    else:
        list_of_words = file_data.split(" ")
        words_from_the_txt = []
        for word in list_of_words:
            if(not(word in words_from_the_txt)):
                # List of a different words
                words_from_the_txt.append(word)
        # The number of the words in the file
        number_of_words = len(list_of_words)
        index = int(index) % int(number_of_words)
        tuple_of_words = (len(words_from_the_txt), list_of_words[int(index) - 1])
        return tuple_of_words[1]

def show_hidden_word(the_secret_word, old_letters_guessed):
    """The function returns a string consisting of - 
    Letters (from the list of letters already guessed by the player)
    and Underscores (for the letters the player has not guessed yet).
    :the_secret_word: the chosen secret word
    :type the_secret_word: str
    :old_letters_guessed: list of letters the player already guessed
    :type old_letters_guessed: list
    :return: the secret word with the letters that the player guessed and underscores ('_')
    :return type: str
    """
    the_word = []
    for letter in the_secret_word:
        if(letter in old_letters_guessed):
            the_word.append(letter)
        else:
            the_word.append("_")
    the_word = " ".join(the_word)
    return the_word

def print_sorted_guessed_letter(old_letters_guessed):
    """Print sorted guessed letters.
    :old_letters_guessed: list of letters the player already guessed
    :type old_letters_guessed: list
    """
    print("The letters you already guessed: "," -> ".join(sorted(old_letters_guessed)))


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """Using the function check_valid_input to know if the letter_guessed is valid or not -
    If not - print 'X', the sorted old_letters_guessed and return False.
    If yes - adding the letter_guessed to old_letters_guessed, print the sorted old_letters_guessed and return True.
    :letter_guessed: a string (probably a letter) that the player puts in
    :type letter_guessed: str 
    :old_letters_guessed: list of letters
    :type old_letters_guessed: list
    :return: True or False
    :return type: boolean
    """
    # If the character is not valid
    if(not(check_valid_input(letter_guessed, old_letters_guessed))):
        print("X")
        if(letter_guessed in old_letters_guessed):
            print("You already guessed this letter...")
        if(len(old_letters_guessed) > 0):
            print_sorted_guessed_letter(old_letters_guessed)
        return False
    # If the character is valid
    old_letters_guessed.append(letter_guessed)
    print_sorted_guessed_letter(old_letters_guessed)
    return True

def check_valid_input(letter_guessed, old_letters_guessed):
    """A function that checks if the letter_guessed is valid - 
    If not - the letter_guessed is not a letter or already guessed or its length is different then 1 character - return False.
    If yes - return True.
    :letter_guessed: a string (probably a letter)
    :type letter_guessed: str 
    :old_letters_guessed: list of letters
    :type old_letters_guessed: list
    :return: True or False
    :return type: boolean
    """
    if(len(letter_guessed) != 1 or not (letter_guessed.isalpha()) or (letter_guessed in old_letters_guessed)):
        return False
    return True


def check_win(the_secret_word, old_letters_guessed):
    """ If one of the letters in the_secret_word is not included in old_letters_guessed - the function will return False.
    Otherwise - return True.
    :the_secret_word: the chosen secret word
    :type the_secret_word: str
    :old_letters_guessed: list of letters
    :type old_letters_guessed: list
    :return: True or False
    :return type: boolean
    """
    for letter in the_secret_word:
        if(not(letter in old_letters_guessed)): 
            return False
    return True

def get_the_secret_word():
    """Function that returns the secret word - 
    At first, the function asks the player to enter a file path.
    Then checkes if the path exist (using the function checking_file_path).
    If not - asks for another file path until the user enter a path that exist.
    If the path exists - asks for a number, and then using the function choose_word to get a random word.
    If the file is epmty - starting all again.
    If not - returns the random word.
    Also, the player have an exit points - if the player enters '0'.
    :return: the secret/random word
    :return type: str
    """
    the_secret_word = ""
    while(the_secret_word == ""):
        file_path = input("Enter a file path: ").lower()
        # Exit point
        if(file_path == "0"):
            return file_path
        while(not(checking_file_path(file_path))):
            file_path = input("The file in this path does not exist. Enter another file path: ").lower()
            if(file_path == "0"):
                return file_path
        index = input("Enter a number: ")
        # Exit point
        if(index == "0"):
            return index
        # Checking if the number is a int
        while(not(index.isnumeric())):
            index = input("Try again - enter a number: ")
        the_secret_word = choose_word(file_path, index)
        # Checking if the file is empty
        if(the_secret_word == ""):
            print("Your file is empty. Try another file.")
    return the_secret_word

def print_quitting_message():
    """The message the player get if he wants to quit the game
    """
    print("You decided to quit this game...\nSee you next time!")

def play_game(the_secret_word):
    """Implements the game - the function gets the_secret_word - 
    The player starting to guess letters. The function checks if the letters are in the secret word. 
    If the user guess all the letters in the secret word - he wins.
    If not and he reaches the maximum errors allowed - he loses.
    Also, the player have an exit point every round - if the player enters '0'.
    :the_secret_word: the chosen secret word
    :type the_secret_word: str
    :return: none
    """
    num_of_tries = MAX_TRIES
    old_letters_guessed = []
    # Starting the game
    while(not(check_win(the_secret_word, old_letters_guessed))):
        print("Number of left tries: ",num_of_tries,"\nRemember - for quitting enter 0\n",
            hangman_photos[num_of_tries],
            "\nHidden word: ",show_hidden_word(the_secret_word, old_letters_guessed))
        letter_guessed = input("Guess a letter: ").lower()
        # Exit point
        if(letter_guessed == "0"):
            print_quitting_message()
            return
        # Cchecking if the letter is valid or not
        while(not(try_update_letter_guessed(letter_guessed, old_letters_guessed))):
            letter_guessed = input("Invalid guessing, try again: ")
        # Checking if the letter is in the secret word
        if(not(letter_guessed in the_secret_word)):
            num_of_tries = num_of_tries - 1
            print(":(")
        # Checking if the player reaches the maximum errors allowed
        if(num_of_tries == 0):
            print(hangman_photos[num_of_tries],"\nThe word was: ",the_secret_word.upper())
            print("YOU LOST - the game is over!\nByeBye")
            return        
    # If the player won
    print("The word was:",the_secret_word.upper(),"\nYou discovered the word!\nYOU WON!")

def main():
    """The main function - print the headline, getting the secret word with the function get_the_Secret_word 
    and give it to the function play_game to start the hangman game.
    Also, the player have a exit point - if the player enters '0'.
    :return: none
    """
    print(HANGMAN_ASCII_ART())
    the_secret_word = get_the_secret_word()
    # Exit point
    if(the_secret_word == "0"):
            print_quitting_message()
            return
    play_game(the_secret_word)


# כשמייבאים ספרייה חיצונית, אם לא נשתמש בתנאי הזה, אז הספרייה תייבא את כל מה שנמצא בה (ולא רק ספצפית את מה שנרצה ממנה)
# וגם כל מה שבקובץ הזה ירוץ
if __name__ == "__main__":
    main()