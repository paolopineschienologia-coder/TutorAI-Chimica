from google import genai

client = genai.Client(
	api_key="AQ.Ab8RN6KG1LFVJK63MmJxqxk8CApmhnHEgQHt8DXgeeP5WU3_xA"
)

for model in client.models.list():
	print(model.name)
