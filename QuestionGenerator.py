import pandas as pd
import json


def load_questions():
    global questions
    file_1 = pd.read_excel('Trivia-Printable.xlsx', "Trivia")
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

    for key in questions["category"]:
        print(key)

    print(questions["category"])


def load_multiples():
    with open('multiple_data (1).json') as json_file:
        data1 = json.load(json_file)

    with open('multiple_data (2).json') as json_file:
        data2 = json.load(json_file)

    with open('multiple_data (3).json.') as json_file:
        data3 = json.load(json_file)

    with open('multiple_data (4).json') as json_file:
        data4 = json.load(json_file)

    multiples = [data1, data2, data3, data4]
    for i in multiples:
        for j in range(len(i["results"])):
            if i["results"][j] not in questions["multiples"]:
                questions["multiples"].append(i["results"][j])

    print(len(questions["multiples"]))
    print(questions)


if __name__ == "__main__":
    questions = {"questions": [], "multiples": [], "category": {}}
    load_multiples()
    load_questions()
    with open('questions_data.json', 'w') as outfile:
        json.dump(questions, outfile)
