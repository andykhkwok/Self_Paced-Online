#!/usr/bin/env python3
""" Automate a script to send a thank you mail, print a report of donor or quit the program."""
from operator import itemgetter
import os
import datetime

table_dictionary = {
    'Toni Orlando': [150.00, 200.00, 100.00],
    'Amanda Clark': [1800.00],
    'Robin Hood': [1234.56, 4500.34, 765.28],
    'Gina Travis': [523.10, 75.00],
    'Mark Johnson': [850.00, 20.14]
}
actions_dictionary = {'1': 'Send a Thank You', '2': 'Create a Report', '3': 'Send letters to everyone', '4': 'Quit'}


def select_action_dictionary(prompt, switch_func_dict):
    """User selects an action by its corresponding order number."""
    while True:
        choice_actions = input(prompt)
        try:
            if switch_func_dict[choice_actions]() == "quit":
                print("Before quitting.")
                break
        except KeyError:
            print("Please enter only one of the listed options.")




def print_menu():
    """Prints the action list to the console"""
    str_result = ''
    for i in actions_dictionary:
        str_result += ("{}) {}".format(i, actions_dictionary[i]))
        str_result += '\n'
    str_result += 'Select the corresponding number for the action you want to take action: '
    return str_result


# action_prompt = (print_menu() + 'Select the corresponding number for the action you want to take action: ')


def sending_thank_you():
    """Lists all the donors or prompts for a name and donation amount to compile the thank you email."""
    send_to_name = input("First: Who do you want to send the email to? Type 'list' for a list of all the donors. ")
    if send_to_name == 'list':
        display_donor_dictionary()
        send_to_name = input("Second: Who do you want to send the email to? Type 'list' for a list of all the donors. ")
    if send_to_name not in table_dictionary:
        table_dictionary[send_to_name] = []
    # donation_amount = input("What donation amount do you want to thank them for? ")
    while True:
        try:
            donation_amount = float(input('What donation amount do you want to thank them for? '))
            if donation_amount > 0:
                break
            else:
                print("Number has to be positive.")
        except ValueError:
            print("Input must be a number.")
    table_dictionary[send_to_name].append(donation_amount)
    print("Dear {}, Thank you for your generous contribution of ${:.2f} to our program.".format(send_to_name,
                                                                                                donation_amount))


def display_donor_dictionary():
    """Prints the full list of donors and corresponding donation history."""
    for key, item in table_dictionary.items():
        print("{:<20}: {}".format(key, item))
    pass


def print_report():
    """Prints the donor table in equally amount of column width with each donor, total amount, number of gifts and average donation."""
    table_header = ['Donor Name', 'Total Given', 'Num Gifts', 'Average Gifts']
    len_header = len(table_header)
    print("|".join(["{:<20}"] * len_header).format(*table_header))
    print("-" * (20 * len_header + (len_header - 1)))
    new_list = []
    for k in table_dictionary:
        sum_donations = sum(table_dictionary[k])
        total_gifts = len(table_dictionary[k])
        average_gift = sum_donations / total_gifts
        new_list.append([k, sum_donations, total_gifts, average_gift])
    sorted_new_list = sorted(new_list, key=itemgetter(1), reverse=True)
    for row in sorted_new_list:
        print("{0:<20} ${1:>19.2f} {2:>20} ${3:>19.2f}".format(*row))
    return new_list


def send_everyone_letters(
        target_directory=os.getcwd()):
    """Sends a letter to everyone in the table for their first donation in the list."""
    file_name_extension = '.txt'
    today_date_short = calculate_date()
    for file_name in table_dictionary:
        target_file_path = os.path.join(target_directory,
                                        str(file_name).replace(' ', '_') + today_date_short + file_name_extension)
        try:
            with open(str(target_file_path), 'w') as tf:
                letter_content = ("Dear {},\n"
                                  "\tThank you for your kind donation of $ {:.2f}.\n"
                                  "\tIt will be put to very good use.\n"
                                  "\t\tSincerely,\n"
                                  "\t\t\t-The Team").format(file_name, table_dictionary[file_name].pop())
                tf.write(letter_content)
        except FileNotFoundError as err:
            print("File path is not correct.")
            print(err)
    print("Done")


def calculate_date():
    today_date = datetime.datetime.now()
    result_today_date = "_" + str(today_date.year) + "_" + str(today_date.month) + "_" + str(today_date.day)
    return result_today_date


def quit_program():
    """Quits the program."""
    return "quit"


switch_func_dict = {
    '1': sending_thank_you,
    '2': print_report,
    '3': send_everyone_letters,
    '4': quit_program
}

if __name__ == '__main__':
    select_action_dictionary(print_menu(), switch_func_dict)
