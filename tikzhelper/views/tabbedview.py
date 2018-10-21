from tikzhelper.helpers.tabbednavigation import Tab, TabbedNavigation

tabs = [Tab('triangle', 'Triangles'),
        Tab('piecewise', 'Piecewise functions'),
        Tab('riemann', 'Riemann sums'),
        Tab('integral', 'Integrals')]

class TabbedView(object):
    def __init__(self, current):
        self.current = current

    def navigation(self):
        nav = TabbedNavigation(self.current, tabs)

        return nav

    def render_view(self):
        # prepare the tabbed navigation object
        nav = TabbedNavigation(self.current, tabs)

        return {'nav' : nav}