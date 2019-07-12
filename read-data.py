# Import pandas
import pandas as pd
import matplotlib.pyplot as plt

# Assign spreadsheet filename to `file`
file = './data/reservas-pendentes.xlsx'

# Load spreadsheet
df = pd.read_excel(file, index_col=0)

df['DT_Necessidade'] = pd.to_datetime(df['DT_Necessidade'])
graph = df['NU_QTde_atend'].groupby(
    df['DT_Necessidade'].dt.to_period('M')).sum().reset_index()

print(graph.DT_Necessidade)

# graph.plot()
# plt.show()
