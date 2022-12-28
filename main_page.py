import streamlit as st
import streamlit as st
import pandas as pd
import psycopg2
import time
import random
from PIL import Image

img=Image.open('sin.PNG')
st.set_page_config(page_title="Sina-Apps", page_icon=img)

st.markdown("# Who I am 🎈")
st.sidebar.markdown("# Welcome 🎈")

st.markdown(':blue[For every need please contact with **_sina.kian@mail.polimi.it_** \n I will develope applications to ease the work]🚧🚧🚧')
st.markdown('Here I attach some demo apps as examples. I develope specific applications for daily, boring or complex duties.')
st.markdown(f"###### :blue[Your problems are like a piece of cake!] 🍰 \n"
            f"###### :blue[You announce your problem, I eat it.] 😉") 


st.markdown("To see other 2 interesting apps (Exam, Timesheet) please contact me")
