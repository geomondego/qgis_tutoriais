# qgis_cpostal_tuga

Plugin QGIS que adiciona uma ferramenta Processing para pesquisar códigos
postais portugueses através da API `https://www.cttcodigopostal.pt/api`.

## Instalação local

1. Copie a pasta `qgis_cpostal_tuga/` para a pasta de perfis/plugins do QGIS.
2. Reinicie o QGIS ou recarregue os plugins.
3. Ative o plugin **QGIS CPostal Tuga** no Gestor de Plugins.

## Utilização

1. Abra a Caixa de Ferramentas Processing.
2. Execute **QGIS CPostal Tuga → Códigos postais → Pesquisar código postal CTT**.
3. Introduza a sua API KEY da plataforma `cttcodigopostal.pt`.
4. Introduza o código postal no formato `0000-000`.
5. O algoritmo cria uma camada de pontos em `EPSG:4326` com uma feição por rua
   devolvida pela API, incluindo atributos como morada, localidade, freguesia,
   concelho, distrito, latitude e longitude.

Quando a opção **Aproximar o mapa à camada criada** estiver ativa, o plugin tenta
aproximar a vista do mapa à camada de resultados criada.


## Publicação no GitHub

Para criar um novo repositório GitHub chamado `qgis_cpostal_tuga` e copiar/publicar
para lá os ficheiros deste plugin, autentique primeiro o GitHub CLI e execute:

```bash
gh auth login
./publish_to_github.sh qgis_cpostal_tuga --public
```

O script usa `gh repo create qgis_cpostal_tuga --source . --push` a partir desta pasta.
