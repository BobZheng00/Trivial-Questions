import json
import time
import random
from threading import Timer


def reload_questions():
    with open('questions_data.json') as json_file:
        data = json.load(json_file)
    return data


def user_login():
    print("WELCOME TO TRIVIAL QUESTIONS")
    time.sleep(0.5)
    user_name = input("Please Enter Your Name: ")
    return user_name


def question_request():
    user_category = -1
    question_count = -1
    print("Hi %s, Here are Some Categories of Questions You may Want to Try:" % user_name)
    time.sleep(0.5)
    count = 1
    for category in data["category"]:
        if category == "Miscellaneous":
            print("17. Miscellaneous (Random selected questions from various categories) (%d questions in total)" \
                  % len(data["category"][category]))
        else:
            print("%i. %s (%d questions in total)" % (count, category, len(data["category"][category])))
        count += 1
        time.sleep(0.25)

    time.sleep(0.25)

    while user_category not in data["category"].keys():
        user_category = input("Please Enter the Name of Category You Want to Try: ")
        if not data["category"][user_category]:
            print("You Have Finished All Questions in %s. Please Try Another" % user_category)
            user_category = -1

    while question_count < 1:
        question_count = int(input("Please Enter the Number of Questions You Want to Try: "))
        if question_count > len(data["category"][user_category]):
            print("Your Request is INVALID. Maximum Number of Questions You Can Try in This Category is %i" % \
                  len(data["category"][user_category]))
            question_count = -1

    return user_category, question_count


def question_generate(user_category, question_count):
    user_score = 0
    for i in range(question_count):
        question_index = data["category"][user_category][random.randint(0, len(data["category"][user_category]) - 1)]

        timeout = 10
        t = Timer(timeout, print, ['Sorry, times up'])
        t.start()
        user_answer = input("%i. %s\n" % (i + 1, data["questions"][question_index]["question"]))
        t.cancel()

        if user_answer == data["questions"][question_index]["correct answer"] or user_answer == data["questions"] \
                [question_index]["correct answer"].lower() or user_answer == data["questions"][question_index] \
                ["correct answer"].upper():
            user_score += 1
            if user_category != "Miscellaneous":
                # swap and pop the last
                data["category"][user_category].remove(question_index)
                data["category"]["Miscellaneous"].remove(question_index)
            else:
                data["category"][user_category].remove(question_index)
                data["category"][data["questions"][question_index]["category"]].remove(question_index)

    print("You Score is %i out of %d questions" % (user_score, question_count))
    # print(len(data["category"]["Mathematics"]))
    # print(len(data["category"]["Miscellaneous"]))


if __name__ == "__main__":
    data = reload_questions()
    user_name = user_login()
    while True:
        user_category, question_count = question_request()
        question_generate(user_category, question_count)
        should_continue = input("Do you wish to continue playing? Y/N\n")
        if should_continue.lower() == 'n' or should_continue == "N":
            break
    # leaderboard
