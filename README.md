![ferret-logo](https://cloud.githubusercontent.com/assets/4680755/24068678/e7aedea0-0b73-11e7-9dd3-3775f959e46f.png)

## Quick Start
The library is pretty straightforward to be used:

```python
from ferret.main import Ferret

ferret = Ferret(url='http://g1.globo.com/politica/blog/cristiana-lobo/post/setor-de-propina-da-odebrecht-movimentou-us-33-bi-diz-delator.html')

ferret.get_article()
```

Ferret also takes two optional arguments: HTML and/or language.

```python
from ferret.main import Ferret

ferret = Ferret(url='http://g1.globo.com/politica/blog/cristiana-lobo/post/setor-de-propina-da-odebrecht-movimentou-us-33-bi-diz-delator.html', html='<html><head></head><body><h1>Título da página de notcias</h1></body></html>', lang='pt')

ferret.get_article()
```


## Contribute

## Licensing

## Credits to Logo
The image contains copyright to skaterjob at [Vecteezy](https://www.vecteezy.com/vector-art/128860-chinchilla-vector-set).
