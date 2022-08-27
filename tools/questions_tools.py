import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    """Question model"""
    question: str
    answer: str


def fetch_data(folder: str, file: str) -> str:
    """Fetch data from a file."""
    questions_file_path = os.path.join(folder, file)
    with open(questions_file_path, "r", encoding="KOI8-R") as file:
        data = file.read()
    return data


def extract_questions(file: str) -> list[Question]:
    """Fetch questions from a file."""
    questions = []
    processed_questions, answers = [], []

    for line in file.split("\n\n"):
        if line.strip().startswith("Вопрос"):
            _, question_text = line.split(sep=":", maxsplit=1)
            processed_questions.append(
                question_text.replace("\n", " ").strip())
        elif line.strip().startswith("Ответ"):
            _, answer_text = line.split(sep=":", maxsplit=1)
            answers.append(answer_text.replace("\n", " ").strip())

    for index in range(0, len(processed_questions)):
        questions.append(
            Question(
                processed_questions[index],
                answers[index]
            )
        )

    return questions


def get_questions() -> list[Question]:
    questions_folder = 'questions'
    questions_files = os.listdir(questions_folder)
    questions = []
    for questions_file in questions_files:
        file = fetch_data(questions_folder, questions_file)
        questions.append(extract_questions(file))

    # TODO: Я не знаю как исправить нейминг.
    questions = [question for questions in questions for question in questions]
    return questions


def main() -> None:
    print(get_questions())


if __name__ == "__main__":
    main()
