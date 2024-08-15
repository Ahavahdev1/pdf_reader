import requests
import fitz  # PyMuPDF

# Função para extrair texto de um PDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        return text
    except Exception as e:
        return f"Erro ao ler o PDF: {str(e)}"

# Função para interagir com a API do Groq
def ask_groq(question, context):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",  # Substitua pelo modelo desejado
        "messages": [
            {"role": "system", "content": "Você é a Eleonora AI da StudioWeb, especialista em extração de dados de PDFs."},
            {"role": "user", "content": f"Contexto: {context}"},
            {"role": "user", "content": f"Responda a seguinte pergunta em português: {question}"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as http_err:
        return f"Erro HTTP: {http_err}"
    except Exception as err:
        return f"Erro: {err}"

# Caminho do PDF e extração do texto
pdf_path = r'C:\pdf\pdf.pdf'
pdf_text = extract_text_from_pdf(pdf_path)

if "Erro" in pdf_text:
    print(pdf_text)
else:
    # Loop de perguntas e respostas
    while True:
        user_question = input("Faça uma pergunta sobre o PDF: ")
        if user_question.lower() in ['sair', 'exit']:
            break
        answer = ask_groq(user_question, pdf_text)
        print(f"Resposta do PDF Ninja: {answer}")
