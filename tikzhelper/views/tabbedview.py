from tikzhelper.helpers.tabbednavigation import Tab, TabbedNavigation

tabs = [Tab('triangle', 'Triangles'),
        Tab('piecewise', 'Piecewise functions'),
        Tab('riemann', 'Riemann sums'),
        Tab('integral', 'Integrals')]

class TabbedView(object):
    def __init__(self, current):
        self.current = current

    def get_view(self):
        view = {}
        view['nav'] = self.navigation()
        view['req_css'] = []
        view['req_js'] = []

        return view

    def navigation(self):
        nav = TabbedNavigation(self.current, tabs)
        return nav