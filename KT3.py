import pandas as pd
import streamlit as st
import io
import matplotlib.pyplot as plt

uploaded_file = st.sidebar.file_uploader("Требуется загрузка CSV", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.warning("Нужно загрузить файл CSV")

if 'df' in locals():
    invers = st.toggle('Инвертировать')
    df['year'] = df['month'].str.split('-').str[0]
    selected_year = st.sidebar.selectbox('Выберите год', df['year'].unique())

    filtered_df = df[df['year'] == selected_year]

    st.subheader(f"Топ штатов по количеству оружия за {selected_year}")
    if invers:
        top_states = filtered_df.groupby('state')['totals'].sum().nlargest(10)
    else:
        top_states = filtered_df.groupby('state')['totals'].sum().nsmallest(10)

    fig, ax = plt.subplots(figsize=(10, 8))
    top_states.plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)

    selected_state = st.selectbox("Выберите штат", df['state'].unique())
    filtered_state = df[(df['state'] == selected_state) & (df['year'] == selected_year)]

    st.download_button("Скачать CSV",
                       data=filtered_state.to_csv(index=False),
                       file_name="data.csv",
                       mime="text/csv")
