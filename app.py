from flask import Flask, render_template, request
import pandas as pd
import gdown

app = Flask(__name__)

# ID do arquivo no Google Drive (extraído do link compartilhado)
GOOGLE_DRIVE_FILE_ID = "1mPYlc_uC3SfJnNQ_ToG6eVmn2ZYMhPCX"

def get_excel_from_google_drive():
    """Baixa a planilha do Google Drive e retorna o DataFrame."""
    url = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}"
    output_file = "patrimonio.xlsx"  # Nome temporário do arquivo baixado
    gdown.download(url, output_file, quiet=False)
    return pd.read_excel(output_file)

# Carrega a planilha na inicialização do programa
df = get_excel_from_google_drive()

@app.route("/", methods=["GET", "POST"])
def index():
    results = pd.DataFrame()  # DataFrame vazio para evitar erros na primeira carga

    if request.method == "POST":
        search_query = request.form.get("bmp_query", "").strip().lower()  # Pesquisa por BMP
        if search_query:
            # Filtra os resultados com base no BMP fornecido
            results = df[df['Nº BMP'].astype(str).str.lower().str.contains(search_query)]

    # Renderiza o template com os resultados
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
