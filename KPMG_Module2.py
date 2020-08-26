#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import timedelta


# In[2]:


xl_file = pd.ExcelFile('KPMG_RawData.xlsx')


# In[3]:


transaction = pd.read_excel(xl_file, sheet_name = "Transactions")


# In[4]:


transaction.head()


# In[5]:


transaction["Profit"] = transaction["list_price"] - transaction["standard_cost"]


# In[6]:


transaction["transaction_date"] = pd.to_datetime(transaction["transaction_date"])


# In[7]:


snapshot_date = transaction["transaction_date"].max() + timedelta(days = 1)
print(snapshot_date)


# In[8]:


data_process = transaction.groupby(['customer_id']).agg({'transaction_date': lambda x: (snapshot_date - x.max()).days,
                                                        'transaction_id': 'count',
                                                        'list_price': 'sum'})
display(data_process.head())


# In[9]:


data_process.rename(columns = {'transaction_date': 'Recency',
                              'transaction_id': 'Frequency',
                              'list_price': 'MonetaryValue'}, inplace = True)


# In[10]:


r_labels = range(4,0,-1)
f_labels = range(1,5)
m_labels = range(1,5)


# In[11]:


r_groups = pd.qcut(data_process['Recency'], q = 4, labels = r_labels)
f_groups = pd.qcut(data_process['Frequency'], q=4, labels = f_labels)
m_groups = pd.qcut(data_process['MonetaryValue'], q=4, labels = m_labels)


# In[12]:


data_process = data_process.assign(R = r_groups.values, F = f_groups.values, M = m_groups.values)


# In[13]:


data_process.head()


# In[14]:


print(data_process['Recency'].max())
print(data_process['Frequency'].max())
print(data_process['MonetaryValue'].max())


# In[15]:


data_process['rfm_score'] = data_process[['R','F','M']].sum(axis =1)


# In[16]:


data_process.head()


# In[17]:


def rfm_level(df):
    if df['rfm_score'] >= 10:
        return 'Platinum'
    elif ((df['rfm_score'] >= 8) and (df['rfm_score'] < 10)):
        return 'Gold'
    elif ((df['rfm_score'] >= 6) and (df['rfm_score'] < 8)):
        return 'Silver'
    elif ((df['rfm_score'] >= 4) and (df['rfm_score'] < 6)):
        return 'Bronze'
    else:
        return 'Basic'


# In[18]:


data_process['RFM_Level'] = data_process.apply(rfm_level, axis=1)


# In[19]:


data_process.head()


# In[20]:


rfm = data_process.groupby('RFM_Level').agg({'Recency': 'mean',
                                            'Frequency': 'mean',
                                            'MonetaryValue': ['mean', 'count']})
display(rfm)


# In[21]:


Final_Draft = rfm.sort_values([('MonetaryValue', 'mean')], ascending = False)


# In[22]:


Final_Draft


# In[23]:


Final_Draft = Final_Draft.reset_index()
display(Final_Draft)


# In[24]:


Final_Draft.rename(columns = {'RFM_Level': 'Customer Type'}, inplace = True)
display(Final_Draft)


# In[25]:


Final_Draft = Final_Draft.set_index('Customer Type')


# In[26]:


Final_Draft


# In[29]:


from pandas import ExcelWriter
from openpyxl import load_workbook
writer = ExcelWriter('hi.xlsx', engine = 'openpyxl')
writer.book = load_workbook('hi.xlsx')
data_process.to_excel(writer, 'RFM_gen_model')
writer.save()


# In[ ]:




