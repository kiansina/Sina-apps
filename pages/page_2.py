import streamlit as st
import pandas as pd
import math
from functools import partial
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from PIL import Image
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import datetime
from datetime import date
import time

st.sidebar.markdown("# Coordinates ❄️")

# Function to check if a value is NaN
def isnan(value):
    try:
        return math.isnan(float(value))
    except:
        return False

today = date.today()

# Function to convert DataFrame to Excel
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1', startrow=1, header=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    cell_format = workbook.add_format()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    worksheet.set_column('A:ZZ', 25, cell_format)
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'vdistributed',
        'align': 'center',
        'fg_color': '#A5F5B0'
    })
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    worksheet.set_column('A:ZZ', 25)
    writer.close()
    processed_data = output.getvalue()
    return processed_data

if 'df' not in st.session_state:
    st.session_state["df"] = pd.DataFrame()

geolocator = Nominatim(user_agent="googleearth")
geocode = partial(geolocator.geocode, language="en")

cons = st.empty()
var = cons.container()
cons1 = st.empty()
var1 = cons1.container()

if 's' not in st.session_state:
    st.session_state['s'] = 0

def cha():
    st.session_state['s'] = 0

# Load sample data
dsample = pd.read_excel("sample.xlsx", sheet_name='Sheet1')
dsample2 = pd.read_excel("sample.xlsx", sheet_name='Sheet2')
sample = to_excel(dsample)
sample2 = to_excel(dsample2)

with var:
    st.markdown("# Coordinates app 🎈")
    st.markdown(f"#### You can upload your excel file including :blue[Addresses], and then download the same excel with the :blue[coordinates] added.")
    st.markdown(':blue[For every need please contact with **_sina.kian@mail.polimi.it_** \n I will develop applications to ease your work]🚧🚧🚧')
    st.info("Your excel can be structured in one of the two ways:")
    st.markdown(f"1. You have 4 columns exactly named as: :blue[”Country” , ”City” , ”Address” , ”Number”] \n"
                f"2. You have 1 column which combines all the above, exactly named as: :blue[”Completed_Address”] \n"
                f"You can leave 1 or more columns empty, but to have precise values, you need to insert all \n"
                f" \n :blue[Download the sample excel. Sheet 1 as an example of first mode, Sheet 2 as an example of second mode.]")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download sample1 input", sample, "sample_input.xlsx", "text/csv", key='download-sample')
    with col2:
        st.download_button("Download sample2 input", sample2, "sample2_input.xlsx", "text/csv", key='download-sample2')
    uploaded_file = st.file_uploader("Upload your file", type="xlsx", on_change=cha)
    if st.session_state['s'] == 1:
        st.download_button("Press to Download", st.session_state['final_file'], "Output_{}.xlsx".format(today.strftime("%m_%d_%y")), "text/csv", key='download-excel')
        st.session_state['s'] = 2

def geocode_with_retry(query, retries=3, delay=2):
    for attempt in range(retries):
        try:
            location = geolocator.ge ocode (query, timeout=10)
            return location
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                raise  # Reraise the last exception if all retries fail

def batch_geocode(addresses, batch_size=100):
    """Geocode a list of addresses in batches."""
    results = []
    for i in range(0, len(addresses), batch_size):
        batch = addresses[i:i+batch_size]
        batch_results = []
        for address in batch:
            location = geocode_with_retry(address)
            if location:
                batch_results.append((location.latitude, location.longitude))
            else:
                batch_results.append((None, None))
        results.extend(batch_results)
    return results

def coor():
    st.session_state["df"] = pd.DataFrame(pd.read_excel(uploaded_file))  # , dtype={'data_update': datetime.datetime})
    st.session_state["df"] = st.session_state["df"].fillna(" ")
    st.session_state["df"]['Longitude'] = [''] * len(st.session_state["df"])
    st.session_state["df"]['Latitude'] = [''] * len(st.session_state["df"])
    st.session_state["df"]['precision'] = [''] * len(st.session_state["df"])
    st.session_state["df"]['Length'] = [''] * len(st.session_state["df"])
    st.session_state["df"]['number of tries'] = [''] * len(st.session_state["df"])
    if 'Completed_Address' not in st.session_state["df"].columns:
        st.session_state["df"]['Completed_Address'] = [''] * len(st.session_state["df"])
        if 'Country' not in st.session_state["df"].columns:
            st.session_state["df"]['Country'] = [''] * len(st.session_state["df"])
        if 'City' not in st.session_state["df"].columns:
            st.session_state["df"]['City'] = [''] * len(st.session_state["df"])
        if 'Address' not in st.session_state["df"].columns:
            st.session_state["df"]['Address'] = [''] * len(st.session_state["df"])
        if 'Number' not in st.session_state["df"].columns:
            st.session_state["df"]['Number'] = [''] * len(st.session_state["df"])
        Ad = []
        for i in st.session_state["df"].index:
            if not isnan(st.session_state["df"]['Country'][i]):
                A = str(st.session_state["df"]['Country'][i])
            if not isnan(st.session_state["df"]['City'][i]):
                A = A + ', ' + str(st.session_state["df"]['City'][i])
            if not isnan(st.session_state["df"]['Address'][i]):
                A = A + ', ' + str(st.session_state["df"]['Address'][i])
            if not isnan(st.session_state["df"]['Number'][i]):
                A = A + ' ' + str(st.session_state["df"]['Number'][i])
            Ad.append(A)
        st.session_state["df"]['Completed_Address'] = Ad
    else:
        Ad = st.session_state["df"]['Completed_Address']
    results = batch_geocode(Ad)
    st.session_state["df"]["Longitude"] = [r[0] for r in results]
    st.session_state["df"]["Latitude"] = [r[1] for r in results]
    st.session_state["df"]["precision"] = [''] * len(st.session_state["df"])
    st.session_state["df"]["Length"] = [''] * len(st.session_state["df"])
    st.session_state["df"]["number of tries"] = [''] * len(st.session_state["df"])
    st.session_state['final_file'] = to_excel(st.session_state["df"])
    st.session_state['s'] = 1

if (uploaded_file is not None) and (st.session_state['s'] == 0):
    with var1:
        st.success(f"### File is successfully uploaded!")
        st.button('search for coordinates', on_click=coor)
