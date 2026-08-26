def classFactory(iface):
    from .qgis_cpostal_tuga_plugin import CttCodigoPostalPlugin

    return CttCodigoPostalPlugin(iface)
