from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from tikzhelper.views.tabbedview import TabbedView
from tikzhelper.models.riemann import RiemannSchema
from tikzhelper.helpers.tikz import draw_riemann_graph
import deform
import json
from peppercorn import parse

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

    @view_config(route_name='riemann_view', renderer='../templates/riemann_view.pt')
    def riemann_view(self):
        view = self.get_view()
        form = deform.Form(self.schema, buttons=('submit',))

        if 'json' in self.request.GET:
            try:
                struct = json.loads(self.request.GET['json'])
            except ValueError as e:
                raise HTTPBadRequest()

            # we have to convert our json to a nicer format
            tmp = []

            # the value here needs to be a string or nothing works
            for k in struct:
                tmp.append((k, str(struct[k])),)

            try:
                appstruct = form.validate(tmp)
                view['tikz'] = draw_riemann_graph(**appstruct)

            except ValueError as e:
                raise HTTPBadRequest()
            except deform.exception.ValidationFailure as e:
                raise HTTPBadRequest()
        else:
            return HTTPFound(self.request.route_url('riemann'))

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

                view['tikz'] = draw_riemann_graph(**appstruct)
                view['json'] = json.dumps(appstruct)

            except deform.exception.ValidationFailure as e:
                view['e'] = e

        return view