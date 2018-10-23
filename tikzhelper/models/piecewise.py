import json
import colander
import re


class ExtendedNumber(object):
    def __init__(self, n):
        if n == '∞':
            self.infinite = 1
        elif n == '-∞':
            self.infinite = -1
        else:
            self.infinite = 0
            self.n = float(n)

    def __lt__(self, other):
        if self.infinite == -1:
            if other.infinite >= 0:
                return True
            else:
                return False

        if self.infinite == 0:
            if other.infinite == -1:
                return False
            elif other.infinite == 0:
                return self.n < other.n
            else:
                return True

        if self.infinite == 1:
            return False

    def __le__(self, other):
        if self.infinite == -1:
            return True

        if self.infinite == 0:
            if other.infinite == -1:
                return False
            elif other.infinite == 0:
                return self.n <= other.n
            else:
                return True

        if self.infinite == 1:
            if other.infinite <= 0:
                return False
            else:
                return True

# take the user submitted domain and parse it to a neater format
def format_domain(domain, min_x, max_x, variable='x'):
    l_sep = '<' if domain[0] == '(' else '\leq'
    r_sep = '<' if domain[-1] == ')' else '\leq'

    inner = domain[1:-1].split(',')

    l_endpoint = inner[0]
    r_endpoint = inner[1]
    l_filled = False if l_sep == '<' else True
    r_filled = False if r_sep == '<' else True

    if l_endpoint == '-∞' and r_endpoint == '∞':
        r = f'-\infty < {variable} < \infty'
    elif l_endpoint == '-∞':
        r = f'{variable} {r_sep} {r_endpoint}'
    elif r_endpoint == '∞':
        sep = '>' if domain[0] == '(' else '\geq'
        r = f'{variable} {sep} {l_endpoint}'
    else:
        r = f'{l_endpoint} {l_sep} {variable} {r_sep} {r_endpoint}'

    # if we have infinite endpoints, truncate them at min/max x/y
    if l_endpoint == '-∞' or l_endpoint == '∞':
        l_endpoint = min_x
    if r_endpoint == '-∞' or r_endpoint == '∞':
        r_endpoint = max_x

    return (r, l_endpoint, r_endpoint, l_filled, r_filled)


# reorder domains according to the left endpoint
def order_by_domains(domains,functions,labels):
    packed = [[domains[k], functions[k], labels[k]] for k in range(0,len(domains))]

    packed.sort(key = lambda x: ExtendedNumber(x[0][1]))

    new_domains = []
    new_functions = []
    new_labels = []

    for row in packed:
        new_domains.append(row[0])
        new_functions.append(row[1])
        new_labels.append(row[2])

    return (new_domains, new_functions, new_labels)

def validate_json(node, value, **kwargs):
    try:
        js = json.loads(value)
    except ValueError as e:
        raise colander.Invalid(node, "Not in JSON format")

def validate_domains(node, value, **kwargs):
    try:
        js = json.loads(value)
        # now verify each entry in value against our regex
        for d in js:
            if re.match('[\(\[][-]?(?:(?:\d*\.\d+)|(?:\d+\.?)|∞),[-]?(?:(?:\d*\.\d+)|(?:\d+\.?)|∞)[\)\]]',
                        d) is None:
                raise colander.Invalid(node,"TF")

            # for each domain, determine whether the left endpoint is less than the right endpoint
            dom = d[1:-1].split(',')
            if not ExtendedNumber(dom[0]) <= ExtendedNumber(dom[1]):
                raise colander.Invalid(node,"Invalid domain specification")

    except ValueError as e:
        raise colander.Invalid(node, "TT")

class PiecewiseSchema(colander.Schema):
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

    def validator(self, form, values):
        # we want all three lists to have the same length
        # and for them to be nonempty
        a = len(json.loads(values['domains']))
        b = len(json.loads(values['functions']))
        c = len(json.loads(values['labels']))

        # todo: find out how to pass a form node to colander.Invalid
        # currently it seems like I can't force the error on the domains node
        if a != b or a != c or b != c or a == 0:
            raise colander.Invalid(form, "Invalid piecewise function definition.")

        if values['min_x'] > values['max_x']:
            e = colander.Invalid(form)
            e['min_x'] = 'Minimum x-value must be smaller than the maximum x-value'

            raise e

        if values['min_y'] > values['max_y']:
            e = colander.Invalid(form)
            e['min_y'] = 'Minimum y-value must be smaller than the maximum y-value'

            raise e
