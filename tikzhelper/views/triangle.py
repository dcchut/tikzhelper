from pyramid.view import view_config
from tikzhelper.views.tabbedview import TabbedView
import colander
import deform
from tikzhelper.helpers.widget import FancyCheckboxInput
from tikzhelper.helpers.triangle import draw_triangle

class TriangleSchema(colander.MappingSchema):
    a = colander.SchemaNode(colander.Float(),
                            validator=colander.Range(min=0,
                                                     min_err='Side length must be positive'),
                            default=5)
    b = colander.SchemaNode(colander.Float(),
                            validator=colander.Range(min=0,
                                                     min_err='Side length must be positive'),
                            default=5)
    theta = colander.SchemaNode(colander.Float(),
                                validator=colander.Range(min=0,
                                                         max=180,
                                                         min_err='Angle must be positive',
                                                         max_err='Angle must be less than 180 degrees'),
                                default=45)
    label_a = colander.SchemaNode(colander.String(),
                                  missing='')
    label_b = colander.SchemaNode(colander.String(),
                                  missing='')
    label_c = colander.SchemaNode(colander.String(),
                                  missing='')
    label_angle_A = colander.SchemaNode(colander.String(),
                                        missing='')
    label_angle_B = colander.SchemaNode(colander.String(),
                                        missing='')
    label_angle_C = colander.SchemaNode(colander.String(),
                                        missing='')
    show_angle_A = colander.SchemaNode(colander.Bool(),
                                       widget=FancyCheckboxInput(label='Render Angle (A)'),
                                       default=True)
    show_angle_B = colander.SchemaNode(colander.Bool(),
                                       widget=FancyCheckboxInput(label='Render Angle (B)'),
                                       default=True)
    show_angle_C = colander.SchemaNode(colander.Bool(),
                                       widget=FancyCheckboxInput(label='Render Angle (C)'),
                                       default=True)


class TriangleView(TabbedView):
    def __init__(self, request):
        self.request = request

        # set this as the triangle tab
        super().__init__('triangle')

        # set up the triangle schema
        self.schema = TriangleSchema()

    def get_view(self):
        view = super().get_view()

        # load the files necessary for prism
        view['req_js'].append('tikzhelper:static/prism.js')
        view['req_css'].append('tikzhelper:static/prism.css')

        # load the javascript for deform
        view['req_js'].append('deform:static/scripts/deform.js')

        return view

    @view_config(route_name='home', renderer='../templates/triangle.pt')
    @view_config(route_name='triangle', renderer='../templates/triangle.pt')
    def triangle(self):
        form = deform.Form(self.schema, buttons=('submit',))

        view = self.get_view()

        # define local variables
        view['tikz'] = ''
        view['e'] = ''

        # try to validate their submission
        if self.request.method == 'POST' and 'submit' in self.request.POST:
            try:
                appstruct = form.validate(self.request.POST.items())

                view['tikz'] = draw_triangle(a=appstruct['a'],
                                             b=appstruct['b'],
                                             theta=appstruct['theta'],
                                             label_a=appstruct['label_a'],
                                             label_b=appstruct['label_b'],
                                             label_c=appstruct['label_c'],
                                             show_angle_A=appstruct['show_angle_A'],
                                             show_angle_B=appstruct['show_angle_B'],
                                             show_angle_C=appstruct['show_angle_C'],
                                             label_angle_A=appstruct['label_angle_A'],
                                             label_angle_B=appstruct['label_angle_B'],
                                             label_angle_C=appstruct['label_angle_C'])

                form.set_appstruct(appstruct)
            except deform.exception.ValidationFailure as e:
                view['e'] = e

        view['form'] = form
        return view