from pyramid.view import view_config
from tikzhelper.views.tabbedview import TabbedView
from tikzhelper.models.riemann import RiemannSchema
import deform


class RiemannView(TabbedView):
    def __init__(self, request):
        self.request = request

        # set this as the piecewise tab
        super().__init__('riemann')

        self.schema = RiemannSchema()

    def get_view(self):
        view = super().get_view()

        return view

    @view_config(route_name='riemann', renderer='../templates/riemann.pt')
    def riemann(self):
        view = self.get_view()
        form = deform.Form(self.schema, buttons=('submit',))

        view['form'] = form
        view['e'] = None

        if self.request.method == 'POST' and 'submit' in self.request.POST:
            try:
                appstruct = form.validate(self.request.POST.items())
                form.set_appstruct(appstruct)
            except deform.exception.ValidationFailure as e:
                view['e'] = e

        return view