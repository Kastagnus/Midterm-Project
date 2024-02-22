import random

word_list = ["shipment", "battleship", "cargo", "flower", "accounting", "heartless", "batmobile", "blackboard",
             "shoulder"]

# გამოაქვს ეკრანზე მისალმება და ბეჭდავს არჩეული სიტყვის შესაბამისი ასოების რაოდენობის ქვედა ტირეს
def welcome_and_display(limit, word):
    print(f"Welcome to the game hangman, you have {limit} tries to guess the hidden word !")
    num_letters = len(word)
    print("_" * num_letters)

# ფუნქცია რომელიც მომხმაებელს ასოს შეყვანას სთხოვს და ამოწმებს რომ შეყვანილი მონაცემი ნამდვილად ასოა
def ask_input():

        letter = input("Enter a letter: ")
        if letter.isalpha():
            return letter.lower()
        else:
            return None

#
def start_game():
    word = random.choice(word_list)
    limit = 7
    welcome_and_display(limit, word)

    #ამოწმებს რამდენი მცდელობა აქვს დარჩენილი მომხმაებელს და აწვდის შესაბამის გაფრთხილებას
    def check_limit(limit):

        if limit == 4:
            print(f"\nCareful! you have to guess it quickly! only {4} attempts remaining")
        elif limit == 1:
            print("\nThe last attempt!")
        elif limit == 0:
            print("\nout of attempts!")
        else:
            print(f"\nYou have {limit} attempts left")
    # სია რომელშიც ინახება დაშიფრული სიტყვა ქვედა ტირეებით და იცვლება ასოებად თუ მომხმარებელი სწორად გამოიცნობს
    charlist = []
    # მომხმარებლის მიერ შეყვანილი ასოების სრული სიმრავლე
    used_letters = []
    for _ in word:
        charlist.append("_")

    # თამაშოს პროცესი, გრძელდება მანამ, სანამ არ ამოიწურება მცდელობები
    while limit > 0:
        letter = ask_input()
        # თუ მონაცემი სწორად არის შეყვანილი, მონაცემი ერთ სიმბოლოიანია, ეს სიმბოლო მოიძებნა დამალულ სიტყვაში და არ იძებნება
        #უკვე შეყვანილ სიმბოლოებში
        if letter is not None and len(letter) == 1 and letter in word and letter not in used_letters:
            indicies = lambda word, letter: [i for i, char in enumerate(word) if char == letter]
            # ქვედა ტირეების სიაში, შესაბამისი ტირეები იცვლება სწორად გამოცნობილი სიმბოლოთი
            for i in indicies(word, letter):
                charlist[i] = letter
            # თუ სიაში ქვედა ტირე აღარ დარჩა ე.ი სიტყვა გამოცნობილია და მომხმარებელს ვულოცათ მოგებას
            if "_" not in charlist:
                print(f"Congratulations! You won!, correct word is {word}")
                limit -= limit
                return True
            print("Wow! You have guessed the letter correctly")
            check_limit(limit)
            print("".join(charlist))
            used_letters.append(letter)
        # თუ მომხმარებლის მიერ შეყვანილი სიტყვა ჩაფიქრებული სიტყვის შესაბამისია, მომხმარებელს ვულოცავთ მოგებას
        elif letter == word:
            limit -= limit
            print(f"Congratulations! You won, correct word is {word}")
            return True
        # თუ მომხმარებლის მიერ შეყვანილი სიმბოლო მან ერთხელ უკვე გამოიყენა, ვაძლევთ შეტყობინებას ამის შესახებ
        elif letter in used_letters:
            print(f"You already used letter: {letter}, please choose another one")
            print(f"used characters are: {used_letters}")
        # თუ მომხმარებელმა არასწორი სიმბოლო შეიყვანა, ვატყობინებთ ამის შესახებ
        elif letter is None:
            print(f"Wrong input! please provide only alphabet characters")
            check_limit(limit)
        # თუ მომხმარებელმა შეცდომით (გაუფრთხილებლობით) შეიყვანა სიმბოლოები, ვაფრთხილებთ და არ ვართმევთ მცდელობას
        elif len(letter) > 1 and len(letter) != len(word):
            print("\nYou can only write 1 letter or the full word, try again !")
            print("".join(charlist))
        else:
            used_letters.append(letter)
            limit -= 1
            #ვაფრთხილებთ მომხმარებელს რომ შეყვანილ სიმბოლოს არ შეიცავს ჩაფიქრებულ სიტყვა და ვაკლებთ მცდელობას
            if limit > 0:
                print("Wrong Shot! try again <3")
                print("\n" +"".join(charlist), end="")
            # თუ მცდელობების რაოდენობა ნულის ტოლია, ვატყობინებთ მომხმარებელს რომ ვერ გაიმარჯვა
            else:
                print("Sorry, game is over!")
                return True

            check_limit(limit)

#პროგრამის გამშვები
def run():

    while True:
        #თამაშის დასრულების შემთხვევაში start_game() აბრუნებს True მნიშვნელობას, თუ თამაში დასრულდა ვეკითხებით მოთამაშეს
        #სურს თუ არა გაგრძელება
        finished = start_game()
        if finished:
            while True:
                ask_again = input("\nDo you want to play again? yes or no: ")
                if ask_again.isalpha() and ask_again.lower() == "yes":
                    break
                elif ask_again.isalpha() and ask_again.lower() == "no":
                    print("\nThank you for playing! Goodbye ! ")
                    return
                else:
                    print("\nPlease enter yes or no")

run()
