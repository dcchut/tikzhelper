import colander
from tikzhelper.helpers.widget import FancyCheckboxInput

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