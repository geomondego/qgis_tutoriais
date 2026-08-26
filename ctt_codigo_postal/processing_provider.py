from qgis.core import QgsProcessingProvider

from .ctt_codigo_postal_algorithm import CttCodigoPostalAlgorithm


class CttCodigoPostalProvider(QgsProcessingProvider):
    def __init__(self, iface=None):
        super().__init__()
        self.iface = iface

    def id(self):
        return "ctt_codigo_postal"

    def name(self):
        return "CTT Código Postal"

    def longName(self):
        return "CTT Código Postal"

    def loadAlgorithms(self):
        self.addAlgorithm(CttCodigoPostalAlgorithm(self.iface))
