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

questions = {}

for i in range(0, len(df), 100):
    df_subset = df.iloc[i:i + 100]
    ids = df_subset['question_id'].tolist()
    ids = map(str, ids)
    questions.update(stack_overflow.get_question_data(';'.join(ids)))

for i, row in df.iterrows():
   df.loc[i, 'up_votes'] = questions[row['question_id']]['up_vote_count']
   df.loc[i, 'comment_count'] = questions[row['question_id']]['comment_count']
   df.loc[i, 'answer_count'] = questions[row['question_id']]['answer_count']
   df.loc[i, 'score'] = questions[row['question_id']]['score']
   df.loc[i, 'favorite_count'] = questions[row['question_id']]['favorite_count']

print(df[['title', 'question_id', 'up_votes']])

df.to_csv('responses_up_votes.csv')
