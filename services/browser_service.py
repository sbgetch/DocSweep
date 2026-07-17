from automation.browser import Browser

from automation.vertiv import VertivSite
from automation.asset_library import AssetLibrarySite
from automation.pd_cloud import PDCloudSite
from automation.masw import MASWSite


class BrowserService:

    def __init__(self):

        self.browser = Browser()

    @property
    def driver(self):

        return self.browser.driver

    def launch(self):

        self.browser.start()

        self.browser.open_startup_tabs()

    def verify_sites(self):

        sites = [
            ("Vertiv", VertivSite),
            ("Asset Library", AssetLibrarySite),
            ("PD Cloud", PDCloudSite),
            ("MASW", MASWSite),
        ]

        results = []

        for name, site_class in sites:

            try:

                site = site_class(self.driver)

                site.attach()

                results.append((name, "Ready"))

            except Exception as ex:

                results.append((name, str(ex)))

        return results
