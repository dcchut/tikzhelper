class TabbedNavigation:
    def __init__(self, current, tabs):
        self.current = current
        self.tabs = tabs

class Tab:
    def __init__(self,name,label, route_name = None):
        self.name = name
        self.label = label

        # if no route name is provided, we assume the name is the same
        if route_name is None:
            self.route_name = name
        else:
            self.route_name = route_name

    def label(self):
        return self.label