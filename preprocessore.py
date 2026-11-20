import fitz
from google import genai
from pathlib import Path

# =======================
# CONFIGURAZIONE
# =======================

API_KEY = "AQ.Ab8RN6KG1LFVJK63MmJxqxk8CApmhnHEgQHt8DXgeeP5WU3_xA"


# ========================================
# LETTURA PDF
# =======================================

def leggi_pdf(percorso):

	testo = ""

	documento = fitz.open(percorso)

	for pagina in documento:
		testo += pagina.get_text()

	documento.close()

	return testo

# =============================
# ELABORAZIONE GEMINI
# ============================

def genera_materiale(testo):

	client = genai.Client(
		api_key=API_KEY
	)

	prompt = f"""
Sei un docente esperto di Chimica.

Riorganizza il materiale seguente.

## Titolo

## Riassunto

## Concetti chiave

## Definizioni importanti

## Relazioni tra i concetti

## Descrizione delle immagini citate nel testo
(se presenti)

## Esempi significativi

## Errori concettuali da evitare

## Prerequisiti

## Obiettivi di apprendimento

## Concetti che lo studente deve padroneggiare

## Errori tipici degli studenti

## Collegamenti con altri argomenti

## Utilizza un linguaggio rigoroso ma adatto a studenti
di scuola secondaria di secondo grado.

## Evita ripetizioni inutili.

## Mantieni le definizioni concise.

## Quando presenti relazioni tra concetti, 
usa elenchi puntati.
Materiale:

{testo}
"""

	response = client.models.generate_content(
		model="gemini-3.1-flash-lite",
		contents=prompt
	)

	return response.text

## ==========================
## SALVATAGGIO FILE
# ==========================

def salva_markdown(contenuto, file_output):

	with open(file_output, "w", encoding="utf-8") as f:
		f.write(contenuto)

# ===============================
# PROGRAMMA PRINCIPALE
# ==============================

cartella_input = Path("materiali_originali")
cartella_output = Path("materiali_tutor")

pdf_files = cartella_input.glob("*.pdf")

for pdf in pdf_files:

	print(f"\nElaboro: {pdf.name}")

	testo_pdf = leggi_pdf(pdf)

	print("Caratteri estratti:", len(testo_pdf))

	try:

		materiale = genera_materiale(testo_pdf)

		output_file = cartella_output / (pdf.stem + ".md")

		salva_markdown(
			materiale,
			output_file
		)

		print(f"Creato:  {output_file.name}")

	except Exception as errore:

		print("ERRORE:")
		print(errore)

print("\nElaborazione conmpletata.")

