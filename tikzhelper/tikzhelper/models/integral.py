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

    def validator(self, form, values):
        # todo: find out how to pass a form node to colander.Invalid
        # currently it seems like I can't force the error on the domains node
        if values['min_x'] > values['max_x']:
            e = colander.Invalid(form)
            e['min_x'] = 'Minimum x-value must be smaller than the maximum x-value'

            raise e

        if values['min_y'] > values['max_y']:
            e = colander.Invalid(form)
            e['min_y'] = 'Minimum y-value must be smaller than the maximum y-value'

            raise e


