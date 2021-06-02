import re
import os
import string

# Add entries to specify lines to remove if the keyword is present
keywords = ('#')


def main():
    # Get file contents
    file = open("text.txt", "r")
    lines = file.readlines()
    file.close()

    # Remove keywords markers
    new_lines = []
    for line in lines:
        if any(keyword in line for keyword in keywords):
            print(f"IGNORE: {line}")
        else:
            new_lines.append(line)

    # Split by question
    full_document = "".join(new_lines)
    questions = re.split(r"[0-9]+\.\s", full_document)
    questions_and_answers: list[list[str]] = []

    # Split by answer
    for question in questions:
        questions_and_answers.append(re.split(r"\n[a-z]\.\s", question))
    del questions_and_answers[0]

    for i in range(len(questions_and_answers)):
        questions_and_answers[i][0] = questions_and_answers[i][0].replace("\n", " ")

    # Get start number for questions
    start = int(input("start number? "))

    # Mix questions and answers into format
    output = ""
    i = 0
    letters = string.ascii_lowercase
    for question in questions_and_answers:
        output += f"{start + i}. {question[0]}\n"
        for ans in range(1, len(question)):
            output += f"{letters[ans-1]}. {question[ans]}\n"
        i += 1

    # Write to file
    file = open("new_text.txt", "w")
    file.write(output)
    file.close()


if __name__ == "__main__":
    if os.path.exists("text.txt"):
        main()

    else:
        print("Create a text.txt file containing the text to rip from!")
        input("...")
