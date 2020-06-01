# Embeddings-leis

## Executando os scripts

### Criando ambiente virtual

Para evitar conflitos entre as versões das bibliotecas Python utilizadas e as instaladas globalmente em uma máquina, utilize um ambiente virtual isolado para executar os scripts deste repositório.

Para isso, execute os comandos abaixo.

```
python -m venv environment
source environment/bin/activate
```

### Instalando dependências

Criado o ambiente virtual, instale as dependências necessárias para executar os scripts.

```
pip install -r requirements.txt
```

### Extraindo justificativas 

Após o download dos arquivos das proposições, execute o seguinte comando para extrair as justificativas.

```
python scripts/extrator_justificativas.py --files <path>/*.pdf > justificativas.csv
```

Certifique-se de mudar `<path>` para o caminho do diretório que contém os arquivos das proposições. Caso não queira que o arquivo com as justificativas tenha o nome das colunas, utilize a flag `--no-header`.

```
python scripts/extrator_justificativas.py --files <path>/*.pdf --no-header > justificativas.csv
```

Nos comandos acima o nome do arquivo `justificativas.csv` pode ser modificado para qualquer outro. Se preferir que o arquivo resultante seja salvo em um diretório, adicione o caminho deste diretório antes do nome do arquivo e certifique-se de que ele já exista antes da execução do comando.

O arquivo resultante conterá as seguintes colunas:
* `arquivo`: Nome do arquivo pdf cujo conteúdo foi extraído
* `texto_anterior`: Texto anterior à justificativa
* `justificativa`: A justificativa extraída.
