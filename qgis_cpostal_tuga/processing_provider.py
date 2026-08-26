from qgis.core import QgsProcessingProvider

from .qgis_cpostal_tuga_algorithm import CttCodigoPostalAlgorithm


class CttCodigoPostalProvider(QgsProcessingProvider):
    def __init__(self, iface=None):
        super().__init__()
        self.iface = iface

    def id(self):
        return "qgis_cpostal_tuga"

    def name(self):
        return "QGIS CPostal Tuga"

    def longName(self):
        return "QGIS CPostal Tuga"

    def loadAlgorithms(self):
        self.addAlgorithm(CttCodigoPostalAlgorithm(self.iface))
