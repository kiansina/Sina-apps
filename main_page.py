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

st.markdown(':blue[For every need please contact with **_sina.kian@mail.polimi.it_** \n I will develope applications to ease your work]🚧🚧🚧')
st.markdown('Here I attach some demo apps as examples. I can develope specific applications for your daily boring or complex duties.')
st.markdown(f"###### :blue[Your problems are like a piece of cake!] 🍰 \n"
            f"###### :blue[You announce your problem, we eat it.] 😉") 


st.markdown("To see other 2 interesting apps (Exam, Timesheet) please contact me")
