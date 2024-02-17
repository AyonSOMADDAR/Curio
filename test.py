import streamlit as st

# Define the set of questions and their corresponding options
questions = [
    "What is the capital of France?\n Who wrote 'To Kill a Mockingbird'?\n What is the chemical symbol for water? \nWhat is the largest planet in our solar system? \nWho painted the Mona Lisa?"
]

options = [
    ["Paris", "London", "Berlin", "Rome"],
    ["Harper Lee", "J.K. Rowling", "Charles Dickens", "Ernest Hemingway"],
    ["H2O", "CO2", "NaCl", "O2"],
    ["Jupiter", "Saturn", "Mars", "Earth"],
    ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Michelangelo"]
]

# Display the questions and collect user answers
def main():
    st.title("Multiple Choice Quiz")
    user_answers = {}
    for i, question in enumerate(questions):
        st.subheader(f"Question {i+1}: {question}")
        for j, option in enumerate(options[i]):
            user_answer = st.radio(f"Option {j+1}", options=options[i], key=f"{i}_{j}")
            if user_answer:
                user_answers[f"Question {i+1}"] = user_answer

    st.write("Your answers:")
    for question, answer in user_answers.items():
        st.write(f"{question}: {answer}")

if __name__ == "__main__":
    main()
