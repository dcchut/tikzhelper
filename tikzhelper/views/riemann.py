import deform
from pyramid.view import view_config

from tikzhelper.helpers.tikz import draw_riemann_graph
from tikzhelper.models.riemann import RiemannSchema
from tikzhelper.views.tabbedview import TabbedView


class RiemannView(TabbedView):
    def __init__(self, request):
        self.request = request

        # set this as the piecewise tab
        super().__init__('riemann')

        self.schema = RiemannSchema()

    def get_view(self):
        view = super().get_view()

        # load the files necessary for prism
        view['req_js'].append('tikzhelper:static/prism.js')
        view['req_css'].append('tikzhelper:static/prism.css')

        return view

    @view_config(route_name='riemann', renderer='../templates/riemann.pt')
    def riemann(self):
        view = self.get_view()
        form = deform.Form(self.schema, buttons=('submit',))

        view['form'] = form
        view['e'] = None
        view['tikz'] = None

        if self.request.method == 'POST' and 'submit' in self.request.POST:
            try:
                appstruct = form.validate(self.request.POST.items())
                form.set_appstruct(appstruct)

                view['tikz'] = draw_riemann_graph(a=appstruct['a'],
                                                  b=appstruct['b'],
                                                  n=appstruct['n'],
                                                  sample_pos=appstruct['sample_pos'],
                                                  function=appstruct['function'],
                                                  min_x=appstruct['min_x'],
                                                  max_x=appstruct['max_x'],
                                                  min_y=appstruct['min_y'],
                                                  max_y=appstruct['max_y'],
                                                  draw_grid=appstruct['draw_grid'],
                                                  draw_labels=appstruct['draw_labels'])

            except deform.exception.ValidationFailure as e:
                view['e'] = e

        return view