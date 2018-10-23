from pyramid.view import view_config

from tikzhelper.views.tabbedview import TabbedView
from tikzhelper.helpers.tikz import draw_region_between_curves

class IntegralView(TabbedView):
    def __init__(self, request):
        self.request = request

        # set this as the piecewise tab
        super().__init__('integral')

    def get_view(self):
        view = super().get_view()

        return view

    @view_config(route_name='integral', renderer='../templates/integral.pt')
    def integral(self):
        view = self.get_view()
        view['tikz'] = draw_region_between_curves()


        return view