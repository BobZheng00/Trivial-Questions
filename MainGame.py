import json
import time
import random
from inputimeout import inputimeout, TimeoutOccurred
import inflect
import QuestionGenerator
import os
import glob

inflector = inflect.engine()


class Gameplay:
    def __init__(self):
        self.user_name = self.user_login()
        self.data = self.reload_questions()
        self.leader_board = self.reload_leaderboard()

    def reload_questions(self):
        while True:
            if_custom = input("Do You Want to Try LOCAL Questions or Custom Questions: (ENTER LOCAL or CUSTOM) ")
            if if_custom.lower() == "local" or if_custom.lower() == "custom":
                break
        if if_custom.lower() == "local":
            with open('questions_data.json') as json_file:
                data = json.load(json_file)
            return data
        else:
            while True:
                custom_files = glob.glob("custom_data/*.json")
                print(custom_files)
                for i in range(len(custom_files)):
                    print("%i. %s" % (i + 1, os.path.basename(custom_files[i])))
                while True:
                    custom_choice = input("Please select the questions you want to try: (Type IMPORT to load your own "
                                          "questions)")
                    if custom_choice.lower() == "import":
                        QuestionGenerator.QuestionLoad.load_custom(self)
                        break
                    elif 0 < int(custom_choice) <= len(custom_files):
                        with open(custom_files[int(custom_choice)-1]) as json_file:
                            data = json.load(json_file)
                        return data

    def user_login(self):
        print("WELCOME TO TRIVIAL QUESTIONS")
        time.sleep(0.5)
        user_name = input("Please Enter Your Name: ")
        return user_name

    def reload_leaderboard(self):
        with open('leaderboard.json') as json_file:
            leader_board = json.load(json_file)
        return leader_board

    def select_type(self):
        if "category" not in self.data:
            return 3
        else:
            user_type = -1
            print("Hi %s, Select the Type of Questions You May Want to Try:" % self.user_name)
            time.sleep(0.25)
            print("1. Trivia Questions")
            time.sleep(0.25)
            print("2. Multiple Choice and True & False")
            time.sleep(0.25)
            while int(user_type) not in [1, 2]:
                user_type = int(input("Please Enter the INDEX of Type You Want: "))
        return user_type

    def update_leaderboard(self):
        leader_board = dict(sorted(self.leader_board.items(), key=lambda item: item[1], reverse=True))
        with open('leaderboard.json', 'w') as outfile:
            json.dump(leader_board, outfile)
        return leader_board

    def display_leaderboard(self):
        count = 1
        print("################ LEADERBOARD ################")
        for key in self.leader_board:
            print("%s     %s      %s      %i" % (
                inflector.ordinal(count), key, self.leader_board[key][1], self.leader_board[key][0]))
            count += 1

    def question_request(self):
        user_category = -1
        question_count = -1
        print("Hi %s, Here are Some Categories of Questions You may Want to Try:" % self.user_name)
        time.sleep(0.5)
        count = 1
        for category in self.data["category"]:
            if category == "Miscellaneous":
                print("17. Miscellaneous (Random selected questions from various categories) (%d questions in total)" \
                      % len(self.data["category"][category]))
            else:
                print("%i. %s (%d questions in total)" % (count, category, len(self.data["category"][category])))
            count += 1
            time.sleep(0.25)

        time.sleep(0.25)

        while user_category not in self.data["category"].keys():
            user_category = input("Please Enter the Name of Category You Want to Try: ")
            if user_category in self.data["category"].keys() and not self.data["category"][user_category]:
                print("You Have Finished All Questions in %s. Please Try Another" % user_category)
                user_category = -1

        while question_count < 1:
            question_count = int(input("Please Enter the Number of Questions You Want to Try: "))
            if question_count > len(self.data["category"][user_category]):
                print("Your Request is INVALID. Maximum Number of Questions You Can Try in This Category is %i" % \
                      len(self.data["category"][user_category]))
                question_count = -1

        return user_category, question_count

    def question_generate(self, user_category, question_count):
        user_score = 0
        for i in range(question_count):
            question_index = self.data["category"][user_category][
                random.randint(0, len(self.data["category"][user_category]) - 1)]

            try:
                user_answer = inputimeout(
                    prompt="%i. %s\n" % (i + 1, self.data["questions"][question_index]["question"]), timeout=30)
            except TimeoutOccurred:
                print('Sorry, times up')
                user_answer = ""

            if user_answer == self.data["questions"][question_index]["correct answer"] or user_answer == \
                    self.data["questions"] \
                            [question_index]["correct answer"].lower() or user_answer == \
                    self.data["questions"][question_index] \
                            ["correct answer"].upper():
                user_score += 1
                if user_category != "Miscellaneous":
                    # swap and pop the last
                    self.data["category"][user_category].remove(question_index)
                    self.data["category"]["Miscellaneous"].remove(question_index)
                else:
                    self.data["category"][user_category].remove(question_index)
                    self.data["category"][self.data["questions"][question_index]["category"]].remove(
                        question_index)

        print("You Score is %i out of %d questions" % (user_score, question_count))
        if self.user_name not in self.leader_board:
            self.leader_board[self.user_name] = [user_score, user_category]
        elif self.user_name in self.leader_board and self.leader_board[self.user_name][0] < user_score:
            self.leader_board[self.user_name] = [user_score, user_category]
            print("Your New Record has been Updated on Leaderboard!")
        else:
            print("Your Record on Leaderboard was %i. Keep Trying!" % self.leader_board[self.user_name][0])

        self.leader_board = self.update_leaderboard()

    def multiple_generate(self):
        multiple_count = -1
        user_score = 0
        user_answer = ""
        while multiple_count < 1:
            multiple_count = int(input("Please Enter the Number of Questions You Want to Try: "))
            if multiple_count > len(self.data["multiples"]):
                print("Your Request is INVALID. Maximum Number of Questions You Can Try is %i" % len(
                    self.data["multiples"]))
                multiple_count = -1

        for i in range(multiple_count):
            multiple_index = random.randint(0, len(self.data["multiples"]) - 1)
            if self.data["multiples"][multiple_index]["type"] == "multiple":
                selections = [self.data["multiples"][multiple_index]["correct_answer"]] + \
                             self.data["multiples"][multiple_index]["incorrect_answers"]
                print("\n%i. %s" % (i + 1, self.data["multiples"][multiple_index]["question"]))
                for j in range(4):
                    single_selection = selections.pop(random.randint(0, len(selections) - 1))
                    if single_selection == self.data["multiples"][multiple_index]["correct_answer"]:
                        correct_answer = chr(ord('@') + j + 1)
                    print("%s. %s" % (chr(ord('@') + j + 1), single_selection))
                try:
                    user_answer = inputimeout(prompt="Select the best possible answer: ", timeout=30)
                except TimeoutOccurred:
                    print('Sorry, times up')
                    user_answer = ""

            elif self.data["multiples"][multiple_index]["type"] == "boolean":
                print("\n%i. %s" % (i + 1, self.data["multiples"][multiple_index]["question"]))
                print("True or False")
                correct_answer = self.data["multiples"][multiple_index]["correct_answer"]
                try:
                    user_answer = inputimeout(prompt="Choose either True or False: ", timeout=30)
                except TimeoutOccurred:
                    print('Sorry, times up')
                    user_answer = ""

            if user_answer == correct_answer:
                user_score += 1
                self.data["multiples"].pop(multiple_index)

    def run(self):
        while True:
            user_type = self.select_type()
            if user_type == 1:
                user_category, question_count = self.question_request()
                self.question_generate(user_category, question_count)
            elif user_type == 2:
                self.multiple_generate()
            elif user_type == 3:
                print("CUSTOM QUESTION SET")
            self.display_leaderboard()
            should_continue = input("Do you wish to continue playing? Y/N\n")
            if should_continue.lower() == 'n' or should_continue == "N":
                break


if __name__ == "__main__":
    question_load = QuestionGenerator.QuestionLoad()
    gameplay = Gameplay()
    gameplay.run()
