import colander

from tikzhelper.helpers.widget import FancyCheckboxInput


class IntegralSchema(colander.Schema):
    function1 = colander.SchemaNode(colander.String())
    function2 = colander.SchemaNode(colander.String(),
                                    default='0')

    min_x = colander.SchemaNode(colander.Float(), default=-5)
    max_x = colander.SchemaNode(colander.Float(), default=5)
    min_y = colander.SchemaNode(colander.Float(), default=-5)
    max_y = colander.SchemaNode(colander.Float(), default=5)
    draw_grid = colander.SchemaNode(colander.Bool(),
                                    widget=FancyCheckboxInput(label='Draw grid'),
                                    default=False)
    draw_labels = colander.SchemaNode(colander.Bool(),
                                      widget=FancyCheckboxInput(label='Draw axis labels'),
                                      default=True)

    a = colander.SchemaNode(colander.Float())
    b = colander.SchemaNode(colander.Float())
