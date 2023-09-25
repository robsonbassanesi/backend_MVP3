# Use uma imagem base adequada para Python (por exemplo, python:3.8)
FROM python:3

# Defina o diretório de trabalho no contêiner
WORKDIR /backend

# Copie os requisitos de pacotes e instale-os
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie os arquivos do código-fonte para o contêiner
COPY . .

# Defina a porta em que o servidor deve ouvir
EXPOSE 4500

# Comando para iniciar o servidor quando o contêiner for iniciado
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "4500"]
