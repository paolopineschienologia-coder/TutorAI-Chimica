from google import genai

client = genai.Client(
	api_key="AQ.Ab8RN6KG1LFVJK63MmJxqxk8CApmhnHEgQHt8DXgeeP5WU3_xA"
)

try:

	response = client.models.generate_content(
		model="models/gemini-3.5-flash-lite",
		contents="Rispondi soltanto con la parola OK."
	)

	print(response.text)

except Exception as e:
	print("ERRORE:")
	print(e)
