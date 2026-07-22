from automation.asset_library import AssetLibrarySite
from automation.masw import MASWSite
from automation.pd_cloud import PDCloudSite
from automation.vertiv import VertivSite

SITE_CLASSES = (
    VertivSite,
    AssetLibrarySite,
    PDCloudSite,
    MASWSite,
)
