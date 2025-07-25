# python_ml_api

Wrapper não oficial da API do Mercado Livre com funcionalidades completas de visitas.

## Funcionalidades

- ✅ Autenticação e gerenciamento de tokens
- ✅ Gestão completa de anúncios
- ✅ Informações de vendas e pedidos
- ✅ **API completa de Visitas** (Nova!)
- ✅ Consultas de usuários e vendedores
- ✅ Categorias e produtos
- ✅ Envios e logística

## 🆕 Nova API de Visitas

A partir da versão atual, o wrapper inclui suporte completo para todas as funcionalidades de visitas da API do Mercado Livre:

### Funcionalidades Disponíveis:

1. **Total de visitas por anúncio** - Visitas dos últimos 2 anos
2. **Total de visitas por usuário** - Entre datas específicas
3. **Visitas por anúncios em período** - Consulta detalhada com intervalos
4. **Visitas por janela de tempo** - Tanto para anúncios quanto usuários
5. **Compatibilidade com métodos legados** - Sem quebrar código existente

### Exemplo Rápido:

```python
from py_ml.wrapper import visitas

# Criar instância
visits_api = visitas(access_token="seu_token")

# Total de visitas de um anúncio
total = visits_api.total_por_anuncio("MLB123456789")

# Visitas dos últimos 7 dias
tendencia = visits_api.por_anuncio_janela(
    item_id="MLB123456789",
    last=7,
    unit="day"
)
```

📖 **Documentação completa**: [VISITS_API.md](VISITS_API.md)  
🚀 **Exemplos práticos**: [exemplo_visitas.py](exemplo_visitas.py)

## Instalação

```bash
pip install py_ml
```

## Uso Básico

```python
from py_ml.wrapper import anuncio, visitas, vendedor

# Autenticação
api = anuncio.get(access_token="seu_token")

# Nova API de visitas
visits = visitas(access_token="seu_token")
```

# Material de apoio

O primeiro passo é ter o código de sua biblioteca separado em uma pasta



*   meu\_pacote/ # Pasta do projeto
    *   codigos\_da\_biblioteca/ # Diretório onde deve ficar os códigos de sua biblioteca
    *   LICENCE # Um arquivo com a licença da sua lib
    *   [README.MD](http://README.MD) # Uma descrição do projeto
    *   [setup.py](http://setup.py) # Código Python responsável pelo empacotamento



Adicione uma licença

```plain
The MIT License (MIT)

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```



Adicione um readme

```markdown
# Sua descrição aqui
```



Instale a lib setuptools

```plain
pip install setuptools
```



Crie o [setup.py](http://setup.py)

```plain
from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='wrapper-panda-video',
    version='0.0.1',
    license='MIT License',
    author='Caio Sampaio',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='caio@pythonando.com.br',
    keywords='panda video',
    description=u'Wrapper não oficial do Panda Video',
    packages=['panda_video'],
    install_requires=['requests'],)
```



Execute o comando

```plain
python3 setup.py sdist
```



Instale o twine para fazer o upload para o pypi

```plain
pip install twine
```



Crie uma conta no pypi



Execute o comando para criar um repositório de teste

```plain
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```



Ou para criar um repositório oficial:

```plain
twine upload dist/*
```
