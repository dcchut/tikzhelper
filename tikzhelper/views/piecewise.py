import json

import deform
from pyramid.view import view_config

from tikzhelper.helpers.tikz import draw_piecewise_fn_definition, draw_piecewise_fn_graph
from tikzhelper.models.piecewise import PiecewiseSchema, order_by_domains, format_domain
from tikzhelper.views.tabbedview import TabbedView


class PiecewiseView(TabbedView):
    def __init__(self, request):
        self.request = request

        # set this as the piecewise tab
        super().__init__('piecewise')

        self.schema = PiecewiseSchema()

    def get_view(self):
        view = super().get_view()

        # load the files necessary for prism
        view['req_js'].append('tikzhelper:static/prism.js')
        view['req_css'].append('tikzhelper:static/prism.css')

        # load up our custom js
        view['req_js'].append('tikzhelper:static/piecewise.js')

        return view

    @view_config(route_name='piecewise', renderer='../templates/piecewise.pt')
    def piecewise(self):
        view = self.get_view()

        view['tikz'] = ''
        view['tikz2'] = ''
        view['e'] = None

        form = deform.Form(self.schema, buttons=('submit',))

        if self.request.method == 'GET' and 'submit' in self.request.GET:
            try:
                appstruct = form.validate(self.request.GET.items())

                # load in our three variables
                domains = [format_domain(d, appstruct['min_x'], appstruct['max_x']) for d in json.loads(appstruct['domains'])]
                functions = json.loads(appstruct['functions'])
                labels = json.loads(appstruct['labels'])

                # we should reorder our lists so that the domains are in order
                domains, functions, labels = order_by_domains(domains,functions,labels)

                # we have valid data - generate our tikz code
                view['tikz'] = draw_piecewise_fn_definition(domains=domains,
                                                            labels=labels)

                view['tikz2'] = draw_piecewise_fn_graph(domains=domains,
                                                        functions=functions,
                                                        min_x=appstruct['min_x'],
                                                        max_x=appstruct['max_x'],
                                                        min_y=appstruct['min_y'],
                                                        max_y=appstruct['max_y'],
                                                        draw_grid=appstruct['draw_grid'],
                                                        draw_labels=appstruct['draw_labels'])

                form.set_appstruct(appstruct)

            except deform.exception.ValidationFailure as e:
                # place the exception into view
                view['e'] = e

        view['form'] = form

        return view