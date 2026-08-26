from qgis.core import QgsApplication

from .processing_provider import CttCodigoPostalProvider


class CttCodigoPostalPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.provider = None

    def initGui(self):
        self.provider = CttCodigoPostalProvider(self.iface)
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        if self.provider is not None:
            QgsApplication.processingRegistry().removeProvider(self.provider)
            self.provider = None
