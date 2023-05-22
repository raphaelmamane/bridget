# import collections 
# import sys

# if sys.version_info.major == 3 and sys.version_info.minor >= 10:
#     from collections.abc import MutableSet
#     collections.MutableSet = collections.abc.MutableSet
# else: 
#     from collections import MutableSet

import sys, os
sys.path.append('/Users/raphael/bridget')

import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
from components.sidebar import sidebar

from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

from openai.error import OpenAIError



def clear_submit():
    st.session_state["submit"] = False


st.set_page_config(page_title="Ask Bridget!", page_icon="📖", layout="wide")
st.header("Ask Bridget!")

sidebar()

api_key_file = os.pardir + '/secrets/openai_key.txt'
with open(api_key_file, 'r') as f:
    OPENAI_API_KEY = f.read()
    f.close()
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
                            When I say ‘city’, it is reffering to the column CITY_NAME_OF_THE_INCIDENT.
                            When I say ‘region’, it is reffering to the column REGION_OF_THE_INCIDENT.
                              """

option = st.selectbox(
    'Which datset would you like Bridget to Analyze?',
    ('Marketing Stats', 'Fleets CRM', 'Incidents'))



query = st.text_area("Ask a Bridget:")

button = st.button("Submit")

if button or st.session_state.get("submit"):
    if not query:
        st.error("Please enter a question")
    elif not option:
        st.error('Please choose a dataset')
    else:
        st.session_state["submit"] = True

        try:
            df = datasets[ds_converter[option]].copy()
            pandas_ai.run(df, prompt=query, preamble=general_preamble+ preambles_dict[ds_converter[option]])

        except OpenAIError as e:
            st.error(e._message)