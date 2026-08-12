class Permissions:

    ALL_PAGES = [
        "Test Settings",
        "Configuration",
        "Endurance-Live Monitoring",
        "Parameter Settings",
        "Line Regulation",
        "Load Regulation",
        "Historical Trend",
        "Alarm Settings",
        "Report"
    ]

    OPERATOR_PAGES = [
        page for page in ALL_PAGES
        if page != "Configuration"
    ]

    ROLE_PAGES = {
        "root": ALL_PAGES,
        "admin": ALL_PAGES,
        "operator": OPERATOR_PAGES
    }

    @classmethod
    def can_access(cls, role, page):
        role = (role or "").lower()
        return page in cls.ROLE_PAGES.get(role, [])