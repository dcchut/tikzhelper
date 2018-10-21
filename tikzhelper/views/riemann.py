from pyramid.view import view_config
from tikzhelper.views.tabbedview import TabbedView

class RiemannView(TabbedView):
    def __init__(self, request):
        self.request = request

        # set this as the piecewise tab
        super().__init__('riemann')

    @view_config(route_name='riemann', renderer='../templates/riemann.pt')
    def piecewise(self):
        return self.render_view()