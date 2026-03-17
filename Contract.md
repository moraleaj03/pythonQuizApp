# Prompt Contract: Create a python quiz app using flask and ollama qwen3-vl:235b-cloud model. 

## Goal
Produce an app that quizzes user and gives feedback and scores the users quiz.

## Inputs
User will answer questions on the app that are basic python problems, for beginners. 

## Output format
Structure:
     - Give user there grade in percentage & and also show what they got in right/total questions format. 
    - Also give user feedback on each question on how the code can be improved. 

## Must
User can leave questions unanswered. The qwen3-vl:235b-cloud model has to give feedback. Write a README.md, requirements.txt, write this prompt contract into a Contract.md file, and a .gitignore file.

## Quality checklist 
- Quiz of about 8 questions
- Feedback and scoring
- The app must use the qwen3-vl:235b-cloud model

