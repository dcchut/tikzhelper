import deform
from pyramid.view import view_config

from tikzhelper.helpers.tikz import draw_region_between_curves
from tikzhelper.models.integral import IntegralSchema
from tikzhelper.views.tabbedview import TabbedView


class IntegralView(TabbedView):
    def __init__(self, request):
        self.request = request

        # set this as the piecewise tab
        super().__init__('integral')

        self.schema = IntegralSchema()

    def get_view(self):
        view = super().get_view()

        # load the files necessary for prism
        view['req_js'].append('tikzhelper:static/prism.js')
        view['req_css'].append('tikzhelper:static/prism.css')

        return view

    @view_config(route_name='integral', renderer='../templates/integral.pt')
    def integral(self):
        view = self.get_view()
        view['tikz'] = None
        view['e'] = None

        form = deform.Form(self.schema, buttons=('submit',))

        if self.request.method == 'POST' and 'submit' in self.request.POST:
            try:
                appstruct = form.validate(self.request.POST.items())
                form.set_appstruct(appstruct)

                view['tikz'] = draw_region_between_curves(a=appstruct['a'],
                                                  b=appstruct['b'],
                                                  f=appstruct['function1'],
                                                  g=appstruct['function2'],
                                                  min_x=appstruct['min_x'],
                                                  max_x=appstruct['max_x'],
                                                  min_y=appstruct['min_y'],
                                                  max_y=appstruct['max_y'],
                                                  draw_grid=appstruct['draw_grid'],
                                                  draw_labels=appstruct['draw_labels'])

            except deform.exception.ValidationFailure as e:
                view['e'] = e

        view['form'] = form
        return view