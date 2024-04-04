'''

პროგრამა გაშვების მომენტში ქმნის ფაილს სახელად bank_customers და კონსოლში გამოაქვს მენიუ
კონსოლ მენიუში გამოაქვს მენიუ სადაც ვრეგისტრირდებით და გვენიჭება უნიკალური პინ კოდი
პინ კოდის საშუალებით შევდივართ სისტემაში სადაც: 1. ვამოწმებთ ბალანსს, 2. ვაკეთებთ დეპოზიტს 3. გაგვაქვს თანხა

'''

import os
import csv
import random


# ქმნის ფაილს, თუ შექმნილია გვატყობინებს რომ შექმნილია
def create_file(file_name):
    file_path = os.path.join(f"{file_name}.csv")
    try:
        file = open(f"{file_name}.csv", "x", encoding="utf-8")
        file.close()
    except FileExistsError as ex:
        print(f"File already exists")
        print("You can work on that file")
    return file_path


path = create_file("bank_customers")


# ხსნის მიწოდებულ ფაილს წაკითხვის რეჟიმში და აბრუნებს ლექსიკონების სიას
def file_reader(path):
    with open(path, "r", encoding="utf-8", newline='') as file:
        reader = list(csv.DictReader(file))
    return reader


# ფაილში მონაცემის ჩამწერი, თუ ფაილია ცარიელია ჯერ დაამატებს ველებს, შემდგომ გადაცემულ ინფორმაციას
def write_file(path, customer):
    fields = ["id", "name", "surname", "PIN", "balance"]
    file_exists = os.path.isfile(path) and os.path.getsize(path) > 0
    with open(path, "a", encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        if not file_exists:
            writer.writeheader()
        writer.writerow(customer)


# აგენერირებს შემთხვევით შერჩეულ 4 ნიშნა ციფრს რომელიც უკვე რეგისტრირებულ ოთხნიშნა ციფრებში არ შედის
def generate_pin_code():
    data = file_reader(path)
    pins = [x["PIN"] for x in data]
    pin = random.randint(1000, 9999)
    while pin in pins:
        pin = random.randint(1000, 9999)
    return pin


# მომხმარებლის ფაილში შენახვის წინ აგენერირებს ID-ს რომელიც ერთი ბიჯით მეტია ბოლო ID-ზე და ანიჭებს მას ახალ მომხმარებელს
def incremented_id():
    try:
        reader = file_reader(path)
        highest_id = 0
        for row in reader:
            row_id = int(row["id"])
            if row_id > highest_id:
                highest_id = row_id
    except FileNotFoundError:
        highest_id = 0
    new_id = highest_id + 1
    return new_id


# ამოწმებს გადაცემული სიტყვები შეიცავს თუ არა მხოლოდ ანბანის ასოებს და სფეისებს
def is_name_valid(name):
    return all(char.isalpha() or char.isspace() for char in name)


# პროგრამის გამშვები რომელიც მუშაობს მანამ სანამ მომხმარებელი ღილაკი 9-is დაჭერით არ გათიშავს მას
def display_screen():
    atm_on = True

    while atm_on:
        print("\nwelcome to ATM of Bank of Georgia")
        digit = input(
            "1 - Login to bank of Georgia\n2 - Register with bank of Georgia\n9 - Turn off ATM\nPlease enter your choice (1, 2 or 9): ")
        if digit == "1":
            ask_login = True
            logged_in = False
            data = file_reader(path)
            customer = {

            }
            while ask_login:
                pin = input("Please provide PIN: ")
                for row in data:
                    if row["PIN"] == pin:
                        for key, value in row.items():
                            customer[key] = value
                        ask_login = False
                        logged_in = True
                        break
                else:
                    print("Wrong input!")
                    print(f"\nPIN {pin} does not exist")
                    break

            while logged_in:
                print(f"\nDear {customer['name'].capitalize()}, check the operations below...")
                decision = input(
                    "1 - Check Balance\n2 - Make a Deposit\n3 - Withdraw\n9 - Log Out\nChoose the operation (1,2,3, or 9): ")
                if decision == "1":
                    print("\nYour current balance is: ", customer["balance"], "GEL")
                elif decision == "2" or decision == "3":

                    word = "Successfull Deposit" if decision == "2" else "Successfull Withdraw"
                    amount = input(f"How much do you want to {word[12:]}?: ")
                    updated_account = []
                    try:
                        amount.isdigit()
                        if decision == "2":
                            customer["balance"] = float(customer["balance"]) + float(amount)
                        else:
                            if float(customer["balance"]) < float(amount):
                                word = "Insufficient funds"
                            else:
                                customer["balance"] = float(customer["balance"]) - float(amount)
                        for row in data:
                            if row["PIN"] == customer["PIN"]:
                                row["balance"] = customer["balance"]
                            updated_account.append(row)
                        with open(path, 'r', newline='') as file:
                            reader = csv.DictReader(file)
                            fieldnames = reader.fieldnames
                        with open(path, "w", encoding="utf-8", newline='') as file:
                            writer = csv.DictWriter(file, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(updated_account)
                            print(f"\n{word}!, your current balance is {customer['balance']} GEL")
                    except ValueError:
                        print("\nAmount has to be a number, try again !")
                elif decision == "9":
                    break

        elif digit == "2":
            print("Provide your credentials, we will Provide PIN code, save it and do NOT share it to anyone")
            id = incremented_id()
            while True:
                name = input("Please enter your name: ")
                surname = input("Please enter your surname: ")
                if is_name_valid(name) and is_name_valid(surname):
                    break
                else:
                    print("Please enter only alphabet letters")
            pin = generate_pin_code()
            balance = 0
            new_customer = {"id": id, "name": name, "surname": surname, "PIN": pin, "balance": balance}
            write_file(path, new_customer)
            print(f"\nThank you {name.capitalize()} for choosing our Bank, your PIN code is {pin}, Save it !")
        elif digit == "9":
            print("Thanks for using ATM")
            atm_on = False
        else:
            print("Invalid input!")


display_screen()
