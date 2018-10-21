from pyramid.view import view_config
from tikzhelper.views.tabbedview import TabbedView

class RiemannView(TabbedView):
    def __init__(self, request):
        self.request = request

        # set this as the piecewise tab
        super().__init__('riemann')

    def get_view(self):
        view = super().get_view()

        return view

    @view_config(route_name='riemann', renderer='../templates/riemann.pt')
    def piecewise(self):
        view = self.get_view()

        return view