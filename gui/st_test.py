
#%%
import sys
sys.path.append('/Users/raphael/bridget')

import pandas as pd
import matplotlib.pyplot as plt


from pandasai import PandasAI
from pandasai.llm.openai import OpenAI



OPENAI_API_KEY = "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"
llm = OpenAI(api_token=OPENAI_API_KEY)


pandas_ai = PandasAI(llm)

ds_converter = {'Marketing Stats':'marketing', 
                'Fleets CRM':'fleets', 
                'Incidents':'incidents'}
datasets = dict()
datasets['marketing'] = pd.read_parquet('/Users/raphael/bridget/data/marketing.parquet')
datasets['fleets'] = pd.read_parquet('/Users/raphael/bridget/data/fleets.parquet')
datasets['incidents'] = pd.read_parquet('/Users/raphael/bridget/data/incidents.parquet')

general_preamble = """
                    You are a professional Data Scientist and Analyst tasked with providing insights into datassets for the various stakeholders.
                    You're job us perform these analyes on pandas dataframes and provide the code for this anlaysis.
                    The pandas dataframe you are provided with is named df and is already in your code environment. It is not necessary to load any data from an external file.
                    Pay attention to the names of the columns in the provided dataframe and use those names precisely in the code you provide when querying those columns.
                    Make sure to print any numerical results you have using python print function.
                    Do not ask follow up questions. Make the best effort to answer on the first attempt. 
                    If you are missing information or can not answer accurately, please be honest.
                   """
preambles_dict = dict()
preambles_dict['marketing'] = """
                              """
preambles_dict['fleets'] = """
                            When asked for source the intention is to the column utm_source.
                            When asked for mql or marketing qualified leads, the intention is when 'Lifecycle Stage' column is set to 'Marketing Qualified Lead'
                            When asked for sql or sales qualified leads, the intention is when 'Lifecycle Stage' columns is set to 'Sales Qualified Lead'
                            When asked for customers, the intention is when 'Lifecycle Stage' is set to 'Customer'
                              """
preambles_dict['incidents'] = """
                              """

#%%
option = 'Fleets CRM'

query = """
identify the sources that are driving  the most customers with a fleet size of over 10 vehicles and understand their most common challenges or pain points that these leads are facing.
"""
query = "identify the sources that are driving  the most sqls with a fleet size of over 20 vehicles and understand their most common challenges or pain points that these leads are facing."

df = datasets[ds_converter[option]].copy()

pandas_ai._verbose =True

pandas_ai.run(df, prompt=query, preamble=general_preamble + preambles_dict[ds_converter[option]])


# %%
