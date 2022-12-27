import streamlit as st

st.markdown("# Update Your Excel DataBase 🎉")
st.sidebar.markdown("# Update Your Excel DataBase 🎉")


import pandas as pd
import streamlit as st
import datetime
from datetime import date
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb


st.markdown("Please, take the steps with the order. \n 1. Upload your main database \n 2. Select the column(s) that gives a unique key (id) \n 3. Upload your update excel")
st.info("The selected columns as key must be in both of the excels with the same column name")

uploaded_file = st.file_uploader("Choose the mother file",type="xlsx")
if uploaded_file is not None:
    st.session_state["df"]=pd.DataFrame(pd.read_excel(uploaded_file))
    options = st.multiselect(
        'Select the columns that you want to keep as unique key',
        st.session_state["df"].columns,
        )
uploaded_file2 = st.file_uploader("Choose the update file",type="xlsx")
if uploaded_file is None:
    uploaded_file2=None
    #st.legacy_caching.caching.clear_cache()

today=date.today()
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1', startrow=1, header=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    #
    cell_format = workbook.add_format()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    worksheet.set_column('A:ZZ', 25,cell_format)
    #
    formatdict = {'num_format':'yyyy-mm-dd', 'align':'center', 'valign':'center'}
    fmt = workbook.add_format(formatdict)
    #fmt.set_num_format('yyyy-mm-dd')
    #fmt.set_align('center')
    #fmt.set_align('vcenter')
    worksheet.set_column('I:I', 25, fmt)
    worksheet.set_column('J:J', 25, fmt)
    worksheet.set_column('O:O', 25, fmt)
    worksheet.set_column('T:T', 25, fmt)
    #worksheet.set_column('W:W', 25, fmt)
    #worksheet.set_column('Z:Z', 25, fmt)
        #
    formatdict2 = {'num_format':'###0', 'align':'center', 'valign':'center'}
    stndg = workbook.add_format(formatdict2)
    worksheet.set_column('A:A', 25, stndg)
    #format1 = workbook.add_format({'num_format': '0.00'})
    #worksheet.set_column('A:A', None, format1)
    #####
    #####
    # Add a header format.
    header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'vdistributed',
    'align' : 'center',
    'fg_color': '#00B050'})#,
    #'border': 1})
    ##
    ##
    # Write the column headers with the defined format.
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    ##
    #data_format1 = workbook.add_format({'bg_color': '#00B050'})
    #worksheet.set_row(1, cell_format=data_format1)
    worksheet.set_column('A:ZZ', 25)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


if uploaded_file is not None:
    st.session_state["df"]=pd.DataFrame(pd.read_excel(uploaded_file))#, dtype={'data_update': datetime.datetime})
    st.session_state["df"]['updated']=[0]*len(st.session_state["df"])
    st.session_state["df"]['data_update']=[0]*len(st.session_state["df"])
    #st.session_state["df"]=st.session_state["df"].fillna(" ")
    #st.session_state["df"] = st.session_state["df"].astype(str)


if uploaded_file2 is not None:
    st.session_state["dg"]=pd.DataFrame(pd.read_excel(uploaded_file2))#, dtype={'data_update': datetime.datetime})
    st.session_state["dg"]['updated']=[1]*len(st.session_state["dg"])
    st.session_state["dg"]['data_update']=[today.strftime("%m_%d_%y")]*len(st.session_state["dg"])
    #st.session_state["dg"]=st.session_state["dg"].fillna(" ")
    #st.session_state["dg"] = st.session_state["dg"].astype(str)
    ##st.session_state["dg"].columns=st.session_state["df"].columns
    st.session_state["dg"].set_index(options,inplace=True)
    st.session_state["df"].set_index(options, inplace=True)
    df=st.session_state["df"]
    dg=st.session_state["dg"]
    df.update(dg)
    #st.session_state["df"] = df.astype(str)
    df=df.reset_index()
    #df[' Data Apertura '] = pd.to_datetime(df[' Data Apertura '], format='yyyy-mm-dd')
    #df[' Data Chiusura '] = pd.to_datetime(df[' Data Chiusura '], format='yyyy-mm-dd')
    #df['Data Presa in carico'] = pd.to_datetime(df['Data Presa in carico'], format='yyyy-mm-dd')
    #df['DATA PREVISTA PER INCASSO'] = pd.to_datetime(df['DATA PREVISTA PER INCASSO'], format='yyyy-mm-dd')
    #df['DATA INCASSO'] = pd.to_datetime(df['DATA INCASSO'], format='yyyy-mm-dd')
    st.session_state["dF"]=df
    final_file = to_excel(st.session_state["dF"])
    st.download_button(
       "Press to Download",
       final_file,
       "Output_{}.xlsx".format(today.strftime("%m_%d_%y")),
       "text/csv",
       key='download-excel'
    )
