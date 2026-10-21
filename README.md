# QC Minicurso

Projeto Jupyter Notebook com exemplos de computação quântica usando Qiskit, Ket e PennyLane.

## SVM: MNIST 3 ou 6

O notebook [`qml/svm.ipynb`](qml/svm.ipynb) contém os blocos **Margem rígida**
e **Margem suave**, com dígitos, tabelas de confusão e gráficos dos dados e da
solução do SVM. O MNIST é carregado com `fetch_openml("mnist_784", version=1)`.
O exemplo usa os mesmos 300 dígitos no treino dos dois modelos e todos os 1.968
dígitos 3 e 6 do teste oficial. Os gráficos dos dois modelos usam a mesma projeção dos dados e os mesmos
limites de eixo.

### Executar com Docker

```bash
docker compose up --build
```

Abra `http://localhost:8888` com o token exibido no terminal.
O contêiner contém todo o projeto: `fundamentos/`, `qml/`, `animacoes/` e os
outros arquivos. A pasta do projeto é montada em `/workspace`, preservando as
edições e os resultados no computador.

Todas as dependências Python vêm do `requirements.txt`, incluindo o Manim.
O Dockerfile instala os pacotes de sistema necessários ao Manim e às fórmulas
LaTeX usadas nas animações. O MNIST é baixado pelo próprio notebook com OpenML.

Para executar comandos no contêiner:

```bash
docker compose exec minicurso bash
```

Para renderizar a animação de Grover:

```bash
docker compose run --rm minicurso manim -ql animacoes/grover.py GroverAlgorithm --media_dir resultados/manim
```

Os vídeos ficam em `resultados/manim/`. Para encerrar:

```bash
docker compose down
```

## Como executar

```bash
source .env/bin/activate
jupyter notebook exemplo_bloch.ipynb
```

Para abrir o exemplo em Ket:

```bash
source .env/bin/activate
jupyter notebook exemplo_ket.ipynb
```

Para abrir o exemplo em PennyLane:

```bash
source .env/bin/activate
jupyter notebook exemplo_pennylane.ipynb
```
