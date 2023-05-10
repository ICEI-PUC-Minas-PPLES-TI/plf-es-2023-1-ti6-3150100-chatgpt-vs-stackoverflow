import gpt_utils as gpt
import stack_overflow_utils as stack_overflow
import calculate_metrics as calc
import time
import pandas as pd

# questions = stack_overflow.get_questions(1500, 5)
# responses = []
# for question in questions:
#     gpt_question = "Generate a Java code to answer the following question: " + question[
#         'title']
#     print(gpt_question)
#     try:
#         response = gpt.ask_gpt(gpt_question)
#         question['answer_chatgpt'] = response
#         responses.append(question)
#     except:
#         time.sleep(360)

#     time.sleep(15)

# df = pd.DataFrame(data=responses)
# print(df)
# df.to_csv('responses.csv')

# # Rodar só depois de minerar todos os dados
# calc.calculate_all()

#pegar os upvotes
df = pd.read_csv('responses_final.csv', index_col='index')

up_votes = {}

for i in range(0, len(df), 100):
    df_subset = df.iloc[i:i + 100]
    ids = df_subset['question_id'].tolist()
    ids = map(str, ids)
    up_votes.update(stack_overflow.get_up_votes(';'.join(ids)))

for i, row in df.iterrows():
    df.loc[i, 'up_votes'] = up_votes[row['question_id']]

print(df[['title', 'question_id', 'up_votes']])

df.to_csv('responses_up_votes.csv')
