# 📚 Tutoriais de QGIS

Bem-vindo ao repositório de Tutoriais de QGIS!

Este é um espaço para compartilhar tutoriais, documentos e exemplos. Mergulhe e melhore as suas habilidades no QGIS! 🚀

## Plugins

* 🌐 [Plugin_QGIS2Web.pdf](Plugin_QGIS2Web.pdf) - Aprenda a usar o plugin **QGIS2Web** para criar mapas web a partir de projetos QGIS.
* 🛤️ [plugin_LRS.pdf](plugin_LRS.pdf) - Um guia sobre como utilizar o plugin de **Sistema de Referência Linear (LRS)** no QGIS para gerenciar e analisar dados lineares.

## Análise de Redes

* 🔗 [QGIS_Redes.pdf](QGIS_Redes.pdf) - Tutorial cobrindo a análise e visualização de redes usando o QGIS.

## Plugin Processing: CTT Código Postal

A pasta `ctt_codigo_postal/` contém um plugin QGIS simples que adiciona um
algoritmo ao Processing para consultar a API de códigos postais dos CTT:
`https://www.cttcodigopostal.pt/api`.

### Instalação local

1. Copie a pasta `ctt_codigo_postal/` para a pasta de perfis/plugins do QGIS.
2. Reinicie o QGIS ou recarregue os plugins.
3. Ative o plugin **CTT Código Postal** no Gestor de Plugins.

### Utilização

1. Abra a Caixa de Ferramentas Processing.
2. Execute **CTT Código Postal → Códigos postais → Pesquisar código postal CTT**.
3. Introduza a sua API KEY da plataforma `cttcodigopostal.pt`.
4. Introduza o código postal no formato `0000-000`.
5. O algoritmo cria uma camada de pontos em `EPSG:4326` com uma feição por rua
   devolvida pela API, incluindo atributos como morada, localidade, freguesia,
   concelho, distrito, latitude e longitude.

Quando a opção **Aproximar o mapa à camada criada** estiver ativa, o plugin tenta
aproximar a vista do mapa à camada de resultados criada.

## 🌟 Contributos

Sinta-se à vontade para contribuir fazendo um fork deste repositório e criando pull requests.

Vamos tornar o aprendizado de GIS acessível para todos! 🌍
