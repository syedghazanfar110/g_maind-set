import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="data sweeper", layout="wide")
#custum css
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5f5;
        color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# tital and discription
st.title("Datasweeper sterling integrator by ghazazfar")
st.write("Transform your files between csv and excel")

#file uploder
uploaded_files =st.file_uploader("upload your files (accepts csv or Excel)", type=["cvs","excel"], accept_multiple_files=(True))

if uploaded_files: 
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue
            #file details       

            st.write ("preview the head of the Dataframe")
            st.dataframe(df.head())

            #data cleaning option

            st.subheader("data cleaning option")
            if st.chat_message(f"clean data for {file.name}"):
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"Remove duplicates from the file :{file.name}"):
                        df.drop_duplicates(input=True)
                        st.write("Duplicates removed")

                with col2:
                    if st.button(f"file missing values for {file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("missing values have been filled")
        st.subheader("select colums to keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #data visualization 
        st.subheader("Data visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        #Conversion Options 

        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["cvs" , "Excel"],key=file.name)
    if st.button(f"Convert{file.name}"):
        buffer = BytesIO()    
    if conversion_type == "csv":
        df.to.csv(buffer,index=False)
        file_name = file.name.replace(file_ext, "csv")
        mime_type = "text/csv"

    elif conversion_type == "Exel":
        df.to_excel(buffer, index=False)        
        file_name = file.name.replace(file_ext, "xlsx")
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    buffer.seek(0)

    st.download_button(
        label=f"Download{file.name} as {conversion_type}",
        data=buffer,
        file_name=file_name,
        mime=mime_type
    )       
st.success("All files processed successfully")
