import pandas as pd
import calculate_metrics as cl
import markdown
from bs4 import BeautifulSoup

df = pd.read_csv('responses_final.csv', index_col='index')
df_answer = pd.read_csv('responses.csv', index_col='index')

metrics = [
    'loc_gpt',  #0
    'loc_stackoverflow',  #1
    'comments_gpt',  #2
    'comments_stackoverflow',  #3
    'comments_density_gpt',  #4
    'comments_density_stackoverflow',  #5
    'cc_gpt',  #6
    'cc_stackoverflow',  #7
    'npath_gpt',  #8
    'npath_stackoverflow',  #9
    'cognitive_gpt',  #10
    'cognitive_stackoverflow',  #11
    'var_names_gpt',  #12
    'var_names_stackoverflow',  #13
    'mi_gpt',  #14
    'mi_stackoverflow',  #16
]

index = df.loc[df[metrics[9]] == 82.0]
row = df_answer.loc[index.index]

print(row[['title', 'question_id']])
for i in metrics:
    print(f'{i}: {index[i].values[0]}')

html = markdown.markdown(row['answer_chatgpt'].values[0],
                         extensions=["fenced_code"])
soup = BeautifulSoup(html, "html.parser")
code_blocks = soup.find_all("code")
cl.create_java(name='RespostaGPT', dir='files', code_blocks=code_blocks)
html = row['answer_stackoverflow'].values[0]
soup = BeautifulSoup(html, "html.parser")
code_blocks = soup.find_all("code")
cl.create_java(name='RespostaStackOverflow',
               dir='files',
               code_blocks=code_blocks)
