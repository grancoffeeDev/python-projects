import pandas as pd
from pack.util import util as u
import datetime

df = pd.read_json("175419170-1.json") #,orient="columns",lines=True
df2 = pd.DataFrame(df)

data = datetime.datetime.now()

df2['dt_get'] = data

print (df2)

#dups = df2.pivot_table(index = ['id'], aggfunc ='size')
#dup_filter = dups
#dups.columns()

#print(dups)

#df_mask=df2['id']==175324119

#print(df2[df_mask])
