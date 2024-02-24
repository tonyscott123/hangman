
# Hangman console game
# @author: TScott
# How to run: pasted the code below into an online python compiler,
# https://www.programiz.com/python-programming/online-compiler/


import random

# ++++++ Game Vars ++++++ #
# Pool of words from where a hangman word is selected at random
word_collection = {
    "test": "Before buying a device, you should do this", 
    "cars": "What you see on roads", 
    "bell": "This is a typical curve in statistics", 
    "bear": "This eats salmons going up rivers", 
    "tree": "You will find this in forests"
}

# Select a word at random from the word collection
random_word = random.choice(list(word_collection.keys()))

# Clue for the selected random/hidden word
hidden_word_clue = word_collection[random_word]

# Convert random word into hangman display format
hidden_word = list("_" * len(random_word))

# game format of solved random word
solved_hidden_word = [str(l).upper() for l in random_word]

# List to store failed letter matches
failed_letter_matches = []

# List to store failed word matches
failed_word_matches = []

# Number of guesses allowed (minimum 7 or length of the word)
guess_nums = 7 if len(random_word) <=7 else len(random_word)


# ++++++ Functions ++++++ #
def is_match(input: str, guess_type: str) -> bool:
    '''Check if validated input matches the target word.

    Parameters:
        input (str): User input (letter or word).
        guess_type (str): Type of guess ('letter_guess' or 'word_guess').
    Returns:
        bool: True if input matches target word or letter in word; 
              False otherwise.
    '''
    
    if guess_type == "word_guess":
        return input == random_word
        
    elif guess_type == "letter_guess":
        return input in random_word
    
    return False
    
    
def is_valid(input: str, guess_type :str) -> bool:
    '''Validates user input for the Hangman game.
    
    Parameters:
        input (str): The user's input to be validated.
        guess_type (str): Type of guess ('letter_guess' or 'word_guess').
    Returns:
        bool: True if input is valid; False otherwise.
    Checks input for:
    1. Numeric characters.
    2. Length matching.
    Prints relevant error messages on failure.
    '''
    
    input_size = len(input)
    word_size = len(random_word)
    vars = {
        "type_err": "input",
        "err_msg": {
            "has_numbers":   "should not be/contain any numbers",
            "is_duplicate":  "has already beeen used",
            "is_off_length": f"is {input_size} "+ "letters long vs {}"},
        "input": input, 
        "guess_type": guess_type 
    }
    
    if input.isnumeric():
        
        display_error(vars, msg = vars['err_msg']['has_numbers'])
        return False
            
    if guess_type == "letter_guess":
        
        if input_size != 1:
            display_error(vars, msg = vars['err_msg']['is_off_length'].format(1))
            return False

        if input in failed_letter_matches or input in hidden_word:
            display_error(vars, msg =vars['err_msg']['is_duplicate'])
            return False
            
    if guess_type == "word_guess":
        
        if input_size != word_size:
            display_error(vars, msg = vars['err_msg']['is_off_length'].format(word_size))
            return False

        if input in failed_word_matches:
            display_error(vars, msg = vars['err_msg']['is_duplicate'])
            return False
            
    return True
    
    
def display_error(vars_coll: dict, msg: str) -> None:
    ''' outputs select error messages'''
    
    if vars_coll["type_err"] == 'input':
        
        print(f"[Input Error]: your {vars_coll['guess_type']}, [{vars_coll['input']}], {msg}. Try again...\n")
        
        
def update_random_word(letter_guess: str) -> None:
    ''' updates the random word with matching letter'''
 
    for idx,letter in enumerate(random_word):
        
        if letter != letter_guess: continue
    
        else: hidden_word[idx] = letter_guess
        
        
def draw_hangman_ascii() -> None:
    ''' draws the hangman incrementally'''
    
    fail_num= len(failed_letter_matches) + len(failed_word_matches)
    
    input_formatted = ""
    if fail_num >0:
        for i in "hangman".upper()[:fail_num]:
            input_formatted +=i.upper()+"  "
        
    return (input_formatted + "__  "* (len("hangman")-fail_num))
    
    
def display_options_menu() -> None:
    ''' return game menu options '''
    
    options ={
        "intro_prompt": "Choose a number from the following 3 options:",
            1: "1. Guess a letter",
            2: "2. Guess the full word",
            3: "3. Quit the game"
    }
        
    for key, value in options.items():
        print(value)
    

def get_game_board() -> str:
    ''' dsplays game board options'''
    sep ='='*50
    return(
        f"{sep}\n\nWORD TO SOLVE: \n\t{hidden_word}"
        f"\n\t-> Hint: {hidden_word_clue}"
        f"\n\n\tGuesses left: {guess_nums} "
        f" \n\tFailed Letter Matches:{failed_letter_matches}\n\tFailed Word Matches:{failed_word_matches}"
        f"\n\nHANG STATUS: {draw_hangman_ascii()}"
        f" \n\n {sep}\n" 
    )
    
    
def get_intro():
    ''' returns game intro text '''
    
    return ("Welcome to the tscott Hangman© console game\n" \
           "This game consists in guessing each letter of a random word " \
           "\n\nHow To Play" \
           "\nA. Read the '-> Hint' then try guessing one letter or the entire word" \
           "\nB. Any letter or word guess that is not a match is recorded in 'failed letter matches' or 'failed letter words' boxes." \
           "\nC. For each mismatch, 'HANG STATUS' will display one letter from the word 'Hangman'.\n" \
                 "\t\tWhen all letters in 'Hangman' are displayed, you loose the game" \
           "\nD. Note, a mistmatch or match only applies to letters or words not already used. \n" \
                 "\t\tIf a letter or word was already used, then the game prompts for another guess without any penalty\n"  
           "\nGame Board elements:" \
           "\n1. [Word To Solve][_, _, ..., _]: the random word to guess" \
           "\n2. [Hint]: a clue relating to the word" \
           "\n3. [guesses left]: number of guess attempts possible/left" \
           "\n4. [failed letter matches]: letter guesses that were not a match " \
           "\n5. [failed word matches]: word guesses that were not a match " \
           "\n6. [HANG STATUS]: draws one letter from the word 'HANGMAN' for every failed guesses")


# ++++++ Game start ++++++ #
print(get_intro())

while True:
    
    print(get_game_board())
    display_options_menu()
    
    # prompt user/validate user selected menu option 
    invalid_option_msg = '[Invalid Input!]. Please enter a valid number [1-3].\n'
    try:
        option_select=(int(input("--> Your choice? ")))
        if option_select >9 or option_select <0:
            print (invalid_option_msg)
            continue
         
    except ValueError:
       print (invalid_option_msg)
       continue
 
    # process user input when validated option1(letter guess) is chosen
    if option_select == 1:
        
        letter_guess = str(input(f"\tGuess a letter >: "))
        match_msg =f"Your guess '{letter_guess}',"+" was{}a match! Next guess...\n"
        
        if (is_valid(letter_guess, "letter_guess")):
            
            if (is_match(letter_guess, "letter_guess")):
                print(match_msg.format(" "))
                update_random_word(letter_guess)
                
            else:
                print(match_msg.format(" NOT "))
                failed_letter_matches.append(letter_guess)
            
        else:
            continue
    
    # validate/process user input when option2 (word guess) is chosen
    if option_select == 2:
        
        word_guess = str(input("\tGuess the full word: "))
        match_msg =f"Your guess '{word_guess}',"+" was{} a match! Next guess...\n"
        
        if (is_valid(word_guess, "word_guess")):
            
            if (is_match(word_guess, "word_guess")):
                print(f"You won!!! Word solved: {solved_hidden_word}")
                break
            
            else:
                print(match_msg.format(" NOT "))
                failed_word_matches.append(word_guess)

    # validate/process user input when option3 (quit game) is chosen
    if option_select == 3:
        print("You chose to quit the game. Until next time. Goodbye.")
        break
    
    # decrement number of guesses
    guess_nums -=1
    
    # eval game: when no more guesses avail, determine win/loose
    if guess_nums == 0:
        if ''.join(map(str,hidden_word)) == random_word: 
            print(f"You won!!! Word solved: {solved_hidden_word}")
        else:
            print(f"There are no guesses are left. The word was {solved_hidden_word}. Thanks for playing")
        break
        


      
