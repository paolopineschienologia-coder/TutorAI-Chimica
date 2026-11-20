import streamlit as st
from google import genai

st.title("Test Gemini")

if st.button("Contatta Gemini"):

	try:

		client = genai.Client(
		api_key="AQ.Ab8RN6KG1LFVJK63MmJxqxk8CApmhnHEgQHt8DXgeeP5WU3_xA"
		)

		response = client.models.generate_content(
			model="gemini-3.5-flash-lite",
			contents="Rispondi esclusivamente con la parola OK"
		)

		st.success("Risposta ricevuta")
		st.write(response.text)

	except Exception as e:
		st.error(str(e))
