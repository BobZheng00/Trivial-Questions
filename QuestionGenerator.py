import pandas as pd
import json


def load_questions():
    file_1 = pd.read_excel('Trivia-Printable.xlsx', "Trivia")
    questions = {"questions":[]}
    # category = {}
    for row_index, row in file_1.iterrows():
        for i in range(3):
            # if file_1.iloc[row_index, 0+i*4] not in category:
            #     category[file_1.iloc[row_index, 0+i*4]] = []
            questions["questions"].append({})
            questions["questions"][row_index*3+i]["category"] = str(row[0+i*4]).replace("\u00a0", "")
            questions["questions"][row_index*3+i]["question"] = str(row[1+i*4]).replace("\u00a0", "")
            questions["questions"][row_index*3+i]["correct answer"] = str(row[2+i*4]).replace("\u00a0", "")
            # questions[row_index*3+i]["incorrect answer"] = []
            # category[file_1.iloc[row_index, 0+i*4]].append(file_1.iloc[row_index, 2+i*4])

    json_string = json.dumps(questions)
    print(json_string)
    with open('questions_data.json', 'w') as outfile:
        json.dump(json_string, outfile)
    # print(category)


if __name__ == "__main__":
    load_questions()