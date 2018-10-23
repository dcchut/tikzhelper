import colander


def Positive(node, value, **kwargs):
    if value <= 0:
        raise colander.Invalid(node, "Must be a positive integer")


class RiemannSchema(colander.Schema):
    function = colander.SchemaNode(colander.String())
    label = colander.SchemaNode(colander.String())

    min_x = colander.SchemaNode(colander.Float(), default=-5)
    max_x = colander.SchemaNode(colander.Float(), default=5)
    min_y = colander.SchemaNode(colander.Float(), default=-5)
    max_y = colander.SchemaNode(colander.Float(), default=5)

    n = colander.SchemaNode(colander.Integer(), default=4, validator=Positive)
    a = colander.SchemaNode(colander.Float())
    b = colander.SchemaNode(colander.Float())
