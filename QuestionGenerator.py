import pandas as pd
import json


def load_questions():
    file_1 = pd.read_excel('Trivia-Printable.xlsx', "Trivia")
    questions = {"questions":[], "category":{}}
    miscellaneous = []
    # category = {}
    for row_index, row in file_1.iterrows():
        for i in range(3):
            category = str(row[0+i*4]).replace("\u00a0", "")
            category = category.replace(" ", "")
            if category not in questions["category"]:
                questions["category"][category] = []
            questions["questions"].append({})
            questions["questions"][row_index*3+i]["category"] = category
            questions["questions"][row_index*3+i]["question"] = str(row[1+i*4]).replace("\u00a0", "")
            questions["questions"][row_index*3+i]["correct answer"] = str(row[2+i*4]).replace("\u00a0", "")
            questions["category"][category].append(row_index*3+i)
            miscellaneous.append(row_index*3+i)

    questions["category"]["Miscellaneous"] = miscellaneous

    with open('questions_data.json', 'w') as outfile:
        json.dump(questions, outfile)

    for key in questions["category"]:
        print(key)

    print(questions["category"])


if __name__ == "__main__":
    load_questions()
