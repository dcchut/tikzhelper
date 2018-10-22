from pyramid.view import view_config
from tikzhelper.views.tabbedview import TabbedView
from tikzhelper.helpers.piecewise import draw_piecewise_fn_definition, draw_piecewise_fn_graph, format_domain

import json
import colander
import deform
import re

def validate_json(node, value, **kwargs):
    try:
        js = json.loads(value)
    except ValueError as e:
        raise colander.Invalid(node,"Not in JSON format")

def validate_domains(node, value, **kwargs):
    try:
        js = json.loads(value)

        # now verify each entry in value against our regex
        for d in js:
            if re.match('[\(\[][-]?(?:(?:\d*\.\d+)|(?:\d+\.?)|∞),[-]?(?:(?:\d*\.\d+)|(?:\d+\.?)|∞)[\)\]]',
                        d) is None:
                raise colander.Invalid(node,"TF")

    except ValueError as e:
        raise colander.Invalid(node, "TT")


class PiecewiseSchema(colander.MappingSchema):
    domains = colander.SchemaNode(colander.String(),
                                  validator=validate_domains)
    functions = colander.SchemaNode(colander.String(),
                                    validator=validate_json)
    labels = colander.SchemaNode(colander.String(),
                                 validator=validate_json)

    min_x = colander.SchemaNode(colander.Float(),
                                default=-5.0)
    max_x = colander.SchemaNode(colander.Float(),
                                default=5.0)
    min_y = colander.SchemaNode(colander.Float(),
                                default=-5.0)
    max_y = colander.SchemaNode(colander.Float(),
                                default=5.0)

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
        view['e'] = ''

        form = deform.Form(self.schema, buttons=('submit',))

        if self.request.method == 'GET' and 'submit' in self.request.GET:
            try:
                appstruct = form.validate(self.request.GET.items())

                # load in our three variables
                domains = [format_domain(d, appstruct['min_x'], appstruct['max_x']) for d in json.loads(appstruct['domains'])]
                functions = json.loads(appstruct['functions'])
                labels = json.loads(appstruct['labels'])

                # we have to reorder our lists to ensure that the domains are in order

                # we have valid data - generate our tikz code
                view['tikz'] = draw_piecewise_fn_definition(domains=domains,
                                                            labels=labels)

                view['tikz2'] = draw_piecewise_fn_graph(domains=domains,
                                                        functions=functions,
                                                        min_x=appstruct['min_x'],
                                                        max_x=appstruct['max_x'],
                                                        min_y=appstruct['min_y'],
                                                        max_y=appstruct['max_y'])

                form.set_appstruct(appstruct)

            except deform.exception.ValidationFailure as e:
                # this seems like an ugly hack, but I don't know a way around it for now
                view['e'] = e
                view['form'] = e.field

        view['form'] = form

        return view