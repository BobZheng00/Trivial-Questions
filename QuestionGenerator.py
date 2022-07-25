import pandas as pd
import os
import json


class QuestionLoad:
    def __init__(self):
        self.questions = {"questions": [], "multiples": [], "category": {}}

    def load_questions(self):
        file_1 = pd.read_excel('Trivia-Printable.xlsx', "Trivia")
        if file_1:
            return 0
        miscellaneous = []
        for row_index, row in file_1.iterrows():
            for i in range(3):
                category = str(row[0+i*4]).replace("\u00a0", "")
                category = category.replace(" ", "")
                if category not in self.questions["category"]:
                    self.questions["category"][category] = []
                self.questions["questions"].append({})
                self.questions["questions"][row_index*3+i]["category"] = category
                self.questions["questions"][row_index*3+i]["question"] = str(row[1+i*4]).replace("\u00a0", "")
                self.questions["questions"][row_index*3+i]["correct answer"] = str(row[2+i*4]).replace("\u00a0", "")
                self.questions["category"][category].append(row_index*3+i)
                miscellaneous.append(row_index*3+i)

        self.questions["category"]["Miscellaneous"] = miscellaneous

        for key in self.questions["category"]:
            print(key)

        print(self.questions["category"])

        # Unit Test: check empty files, check correct files, check other cases
        # Use cloud storage for big files instead of uploading to github

    def load_multiples(self):
        data1, data2, data3, data4 = None, None, None, None
        with open("multiples_data/multiple_data (1).json") as json_file:
            data1 = json.load(json_file)

        with open('multiples_data/multiple_data (2).json') as json_file:
            data2 = json.load(json_file)

        with open('multiples_data/multiple_data (3).json.') as json_file:
            data3 = json.load(json_file)

        with open('multiples_data/multiple_data (4).json') as json_file:
            data4 = json.load(json_file)

        multiples = [data1, data2, data3, data4]
        for i in multiples:
            for j in range(len(i["results"])):
                if i["results"][j] not in self.questions["multiples"]:
                    self.questions["multiples"].append(i["results"][j])

        print(len(self.questions["multiples"]))
        print(self.questions)

    def load(self):
        self.load_multiples()
        self.load_questions()
        with open('questions_data.json', 'w') as outfile:
            json.dump(self.questions, outfile)

    def load_custom(self):
        custom_data = {"questions":[], "leaderboard":{}}
        path = input("Please enter the path of the .xlsx file you want to import: ")
        try:
            file = pd.read_excel(path)
            for row_index, row in file.iterrows():
                row = row.fillna("")
                if row_index > 6 and row[1] != "" and row[7] != "":
                    if row[2] == "" and row[3] == "" and row[4] == "" and row[5] == "":
                        custom_data["questions"].append({})
                        custom_data["questions"][len(custom_data["questions"]) - 1]["type"] = "question"
                        custom_data["questions"][len(custom_data["questions"]) - 1]["question"] = row[1]
                        custom_data["questions"][len(custom_data["questions"]) - 1]["correct_answer"] = row[7]
                    elif str(row[2]).lower() == "true" and str(row[3]).lower() == "false" and (row[7] == 1 or row[7] == 0):
                        custom_data["questions"].append({})
                        custom_data["questions"][len(custom_data["questions"]) - 1]["type"] = "boolean"
                        custom_data["questions"][len(custom_data["questions"]) - 1]["question"] = row[1]
                        custom_data["questions"][len(custom_data["questions"]) - 1]["correct_answer"] = str(bool(row[7]))
                    else:
                        custom_data["questions"].append({})
                        custom_data["questions"][len(custom_data["questions"]) - 1]["type"] = "multiple"
                        custom_data["questions"][len(custom_data["questions"]) - 1]["question"] = row[1]
                        custom_data["questions"][len(custom_data["questions"]) - 1]["correct_answer"] = row[7]
                        custom_data["questions"][len(custom_data["questions"]) - 1]["incorrect_answers"] = []
                        for i in range(2, 6):
                            if row[i] != "" and row[i] != row[7]:
                                custom_data["questions"][len(custom_data["questions"]) - 1]["incorrect_answers"].append(row[i])
            new_path = "custom_data/" + os.path.basename(path).replace(".xlsx", ".json")
            with open(new_path, 'w+') as outfile:
                json.dump(custom_data, outfile)

        except Exception:
            print("Invalid file. Please check.")


if __name__ == "__main__":
    question_load = QuestionLoad()
    question_load.load_custom()
