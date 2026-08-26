import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPointXY,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterString,
    QgsWkbTypes,
)


class CttCodigoPostalAlgorithm(QgsProcessingAlgorithm):
    API_KEY = "API_KEY"
    CODIGO_POSTAL = "CODIGO_POSTAL"
    APROXIMAR = "APROXIMAR"
    OUTPUT = "OUTPUT"

    API_URL = "https://www.cttcodigopostal.pt/api/v1/{api_key}/{codigo_postal}"

    def __init__(self, iface=None):
        super().__init__()
        self.iface = iface

    def tr(self, string):
        return QCoreApplication.translate("CttCodigoPostalAlgorithm", string)

    def createInstance(self):
        return CttCodigoPostalAlgorithm(self.iface)

    def name(self):
        return "pesquisar_codigo_postal_ctt"

    def displayName(self):
        return self.tr("Pesquisar código postal CTT")

    def group(self):
        return self.tr("Códigos postais")

    def groupId(self):
        return "codigos_postais"

    def shortHelpString(self):
        return self.tr(
            "Pesquisa a API cttcodigopostal.pt por um código postal no formato "
            "0000-000 e cria uma camada de pontos em EPSG:4326 com as ruas "
            "devolvidas pela API. É necessário introduzir uma API KEY válida."
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterString(
                self.API_KEY,
                self.tr("API KEY cttcodigopostal.pt"),
                defaultValue="",
                optional=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.CODIGO_POSTAL,
                self.tr("Código postal (0000-000)"),
                defaultValue="",
                optional=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.APROXIMAR,
                self.tr("Aproximar o mapa à camada criada"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr("Ruas do código postal"),
                QgsProcessing.TypeVectorPoint,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        api_key = self.parameterAsString(parameters, self.API_KEY, context).strip()
        codigo_postal = self._normalizar_codigo_postal(
            self.parameterAsString(parameters, self.CODIGO_POSTAL, context)
        )
        aproximar = self.parameterAsBool(parameters, self.APROXIMAR, context)

        if not api_key:
            raise QgsProcessingException(self.tr("Introduza uma API KEY válida."))

        resultados = self._consultar_api(api_key, codigo_postal, feedback)
        if not resultados:
            raise QgsProcessingException(
                self.tr("A API não devolveu ruas para o código postal indicado.")
            )

        fields = self._fields()
        crs = QgsCoordinateReferenceSystem("EPSG:4326")
        sink, dest_id = self.parameterAsSink(
            parameters, self.OUTPUT, context, fields, QgsWkbTypes.Point, crs
        )
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        total = len(resultados)
        criados = 0
        for current, item in enumerate(resultados):
            if feedback.isCanceled():
                break
            feature = self._feature_from_item(item, fields)
            if feature is not None:
                sink.addFeature(feature)
                criados += 1
            feedback.setProgress(int((current + 1) * 100 / total))

        if criados == 0:
            raise QgsProcessingException(
                self.tr("Nenhum resultado tinha coordenadas válidas para criar pontos.")
            )

        feedback.pushInfo(
            self.tr(f"Criados {criados} ponto(s) para o código postal {codigo_postal}.")
        )
        self._aproximar_camada(context, dest_id, aproximar)
        return {self.OUTPUT: dest_id}

    def _normalizar_codigo_postal(self, codigo_postal):
        digits = re.sub(r"\D", "", (codigo_postal or ""))
        if len(digits) != 7:
            raise QgsProcessingException(
                self.tr("O código postal deve ter 7 dígitos, por exemplo 2520-193.")
            )
        return f"{digits[:4]}-{digits[4:]}"

    def _consultar_api(self, api_key, codigo_postal, feedback):
        url = self.API_URL.format(api_key=quote(api_key), codigo_postal=codigo_postal)
        request = Request(url, headers={"User-Agent": "QGIS CTT Codigo Postal Plugin"})
        feedback.pushInfo(self.tr(f"A consultar {url}"))
        try:
            with urlopen(request, timeout=30) as response:
                payload = response.read().decode("utf-8")
        except HTTPError as err:
            body = err.read().decode("utf-8", errors="replace")
            raise QgsProcessingException(
                self.tr(f"Erro HTTP {err.code} ao consultar a API: {body}")
            )
        except URLError as err:
            raise QgsProcessingException(self.tr(f"Não foi possível consultar a API: {err}"))

        try:
            data = json.loads(payload)
        except json.JSONDecodeError as err:
            raise QgsProcessingException(self.tr(f"Resposta JSON inválida: {err}"))

        if isinstance(data, dict) and "error" in data:
            raise QgsProcessingException(self.tr(f"Erro devolvido pela API: {data['error']}"))
        if not isinstance(data, list):
            raise QgsProcessingException(self.tr("A resposta da API não é uma lista."))
        return data

    def _fields(self):
        fields = QgsFields()
        for name in (
            "morada",
            "porta",
            "localidade",
            "freguesia",
            "concelho",
            "distrito",
            "codigo_postal",
            "info_local",
            "codigo_arteria",
            "concelho_codigo",
            "distrito_codigo",
            "latitude",
            "longitude",
        ):
            fields.append(QgsField(name, QVariant.String))
        return fields

    def _feature_from_item(self, item, fields):
        try:
            latitude = float(item.get("latitude", ""))
            longitude = float(item.get("longitude", ""))
        except (TypeError, ValueError):
            return None

        feature = QgsFeature(fields)
        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(longitude, latitude)))
        feature.setAttributes(
            [
                item.get("morada", ""),
                item.get("porta", ""),
                item.get("localidade", ""),
                item.get("freguesia", ""),
                item.get("concelho", ""),
                item.get("distrito", ""),
                item.get("codigo-postal", ""),
                item.get("info-local", ""),
                item.get("codigo-arteria", ""),
                str(item.get("concelho-codigo", "")),
                str(item.get("distrito-codigo", "")),
                str(item.get("latitude", "")),
                str(item.get("longitude", "")),
            ]
        )
        return feature

    def _aproximar_camada(self, context, layer_id, aproximar):
        if not aproximar or self.iface is None:
            return
        layer = context.getMapLayer(layer_id)
        if layer is None or layer.extent().isEmpty():
            return
        canvas = self.iface.mapCanvas()
        canvas.setExtent(layer.extent())
        canvas.zoomScale(max(canvas.scale() * 0.5, 1000))
        canvas.refresh()
