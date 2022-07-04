import pandas as pd
import json


def load_questions():
    file_1 = pd.read_excel('Trivia-Printable.xlsx', "Trivia")
    questions = []
    category = {}
    for row_index, row in file_1.iterrows():
        if file_1.iloc[row_index, 0] not in category:
            category[file_1.iloc[row_index, 0]] = []
        questions.append({})
        questions[row_index]["category"] = file_1.iloc[row_index, 0]
        questions[row_index]["question"] = file_1.iloc[row_index, 1]
        questions[row_index]["correct answer"] = file_1.iloc[row_index, 2]
        questions[row_index]["incorrect answer"] = []
        category[file_1.iloc[row_index, 0]].append(file_1.iloc[row_index, 2])

    print(questions)
    print(category)


if __name__ == "__main__":
    load_questions()