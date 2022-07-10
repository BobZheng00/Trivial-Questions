import json
import time
import random


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
            print("17. Miscellaneous (Random selected questions from various categories)")
        else:
            print("%i. %s (%d questions in total)" % (count, category, len(data["category"][category])))
        count += 1
        time.sleep(0.25)

    time.sleep(0.25)
    while user_category not in data["category"].keys():
        user_category = input("Please Enter the Name of Category You Want to Try: ")
    while question_count < 1 or question_count > 20:
        question_count = int(input("Please Enter the Number of Questions You Want to Try (20 at MAX): "))
    return user_category, question_count


def question_generate(user_category, question_count):
    user_score = 0
    for i in range(question_count):
        question_index = data["category"][user_category][random.randint(0, len(data["category"][user_category]))]
        user_answer = input("%i. %s\n" % (i + 1, data["questions"][question_index]["question"]))
        if user_answer == data["questions"][question_index]["correct answer"] or user_answer == data["questions"] \
                [question_index]["correct answer"].lower() or user_answer == data["questions"][question_index] \
                ["correct answer"].upper():
            user_score += 1
            if user_category != "Miscellaneous":
                data["category"][user_category].remove(question_index)
                data["category"]["Miscellaneous"].remove(question_index)
            else:
                data["category"][user_category].remove(question_index)
                data["category"][data["questions"][question_index]["category"]].remove(question_index)

    print(user_score)
    # print(len(data["category"]["Mathematics"]))
    # print(len(data["category"]["Miscellaneous"]))


if __name__ == "__main__":
    data = reload_questions()
    user_name = user_login()
    print("hello_world")
    user_category, question_count = question_request()
    question_generate(user_category, question_count)
