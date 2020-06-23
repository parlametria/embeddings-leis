# Embeddings-leis

Usamos word embeddings para analisar as proposições legislativas do Congresso Nacional. 

## Executando os scripts

### Criando ambiente virtual

Para evitar conflitos entre as versões das bibliotecas Python:

```
python -m venv environment
source environment/bin/activate
```

### Instalando dependências

```
pip install -r requirements.txt
```

### Baixando os csv's com as proposições

```
python scripts/concatenate_datasets.py --start=<starting_year> --end=<ending_year>
```

Importante notar que, por algum motivo, a leitura do dataset baixado por esse script funciona somente se for usado os parâmetros sep='|' e lineterminator='\n', como demonstrado abaixo. 

```
import pandas as pd
df = pd.read_csv("data/propositions.csv", sep='|', lineterminator="\n")
```

### Extraindo justificativas 

Após o download dos arquivos das proposições:

```
python scripts/extrator_justificativas.py --source <path> > justificativas.csv
```

Caso não queira o nome das colunas no resultado, use a flag `--no-header`.

O arquivo resultante conterá as seguintes colunas:
* `arquivo`: Nome do arquivo pdf cujo conteúdo foi extraído
* `id`: Identificador da proposição
* `numero`: Número da proposição
* `tipo`: Tipo da proposição
* `texto_anterior`: Texto anterior à justificativa
* `justificativa`: A justificativa extraída.
