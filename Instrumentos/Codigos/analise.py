import pandas as pd

df = pd.read_csv('responses_final.csv', index_col='index')

duplas = [
    ['loc_gpt', 'loc_stackoverflow'],
    ['comments_gpt', 'comments_stackoverflow'],
    ['comments_density_gpt', 'comments_density_stackoverflow'],
    ['cc_gpt', 'cc_stackoverflow'],
    ['npath_gpt', 'npath_stackoverflow'],
    ['cognitive_gpt', 'cognitive_stackoverflow'],
    ['var_names_gpt', 'var_names_stackoverflow'],
    ['mi_gpt', 'mi_stackoverflow'],
]

for i in duplas:
    min = df[i].min()
    max = df[i].max()
    median = df[i].median()
    sum = df[i].sum()
    print(f'\tmin:\n{min}\n\tmax:\n{max}\n\tmedian:\n{median}\n\tsoma:\n{sum}')
    count_gpt = count_stack = 0
    for j, row in df.iterrows():
        if row[i[0]] > row[i[1]]:
            count_gpt += 1
        else:
            count_stack += 1
    print()
    print(f'GPT maior: {count_gpt}, Stack maior: {count_stack}')
    diff = (df[i[0]] - df[i[1]]).sum()
    print(f'Diferença GPT - Stack: {diff}')
    print('--------------------------------------------')
    print()