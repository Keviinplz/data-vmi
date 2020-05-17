import re
from os import listdir
from os.path import isfile, join
import pandas as pd

DATA_PATH = "Datos/"

txt_files = [f.replace('.txt', '') for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f))]

data = {}

for txt in txt_files:
    with open(f'{DATA_PATH}{txt}.txt', 'r') as file:
        file_to_string = file.read()

    data_day = re.findall(r'(\d+) (\d+) \d+,\d% (\d+) (\d+) \d+,\d+%$', file_to_string, re.MULTILINE)[:-1]
    if len(data_day) != 0:
        data_list = []
        for i in range(len(data_day)):
            for j in range(len(data_day[0])):
                data_list.append(int(data_day[i][j]))
        data[txt] = data_list

header = list(data.keys())
centros = ['CENTRAL', 'NORTE', 'OCCIDENTE', 'ORIENTE', 'SUR', 'SUR ORIENTE']
vmi_info = ['VMI TOTALES', 'PACIENTES VMI', 'COVID VMI', 'SOSPECHA VMI']

tuples = []

for i in range(len(centros)):
    for j in range(len(vmi_info)):
        tuples.append((centros[i], vmi_info[j]))

indexs = pd.MultiIndex.from_tuples(tuples, names=['Ubicacion Centro', 'Informacion']) 

df = pd.DataFrame(data, index=indexs)


# Excel
df.to_excel('output.xls', header=header, merge_cells=False)

# CSV
excel = pd.read_excel(r'output.xls')
excel.to_csv(r'output.csv', index=None, header=True)
