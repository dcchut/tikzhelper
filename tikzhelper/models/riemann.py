import colander

from tikzhelper.helpers.widget import FancyCheckboxInput

def validate_positive(node, value, **kwargs):
    if value <= 0:
        raise colander.Invalid(node, "Must be a positive integer")


class RiemannSchema(colander.Schema):
    function = colander.SchemaNode(colander.String())
    label = colander.SchemaNode(colander.String())

    min_x = colander.SchemaNode(colander.Float(), default=-5)
    max_x = colander.SchemaNode(colander.Float(), default=5)
    min_y = colander.SchemaNode(colander.Float(), default=-5)
    max_y = colander.SchemaNode(colander.Float(), default=5)
    draw_grid = colander.SchemaNode(colander.Bool(),
                                    widget=FancyCheckboxInput(label='Draw grid'),
                                    default=False)
    draw_labels = colander.SchemaNode(colander.Bool(),
                                      widget=FancyCheckboxInput(label='Draw axis labels'),
                                      default=False)

    sample_pos = colander.SchemaNode(colander.Float(),
                              default=0.5,
                              validator=colander.Range(0,1))

    n = colander.SchemaNode(colander.Integer(), default=4, validator=validate_positive)
    a = colander.SchemaNode(colander.Float())
    b = colander.SchemaNode(colander.Float())
