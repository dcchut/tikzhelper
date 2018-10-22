from tikzhelper.helpers.triangle import TikzBuilder
from math import floor, ceil

colors = ['blue', 'red', 'orange', 'purple', 'olive', 'violet']

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

def draw_piecewise_fn_definition(domains, labels, fn_name='f', fn_variable='x'):
    builder = TikzBuilder()

    builder.tikz += f"{fn_name}({fn_variable})="
    builder.simple_tag('begin', 'cases')

    length = len(domains)

    for k in range(0,length):
        curr_color = colors[k % len(colors)]
        builder.simple_tag('color', curr_color,newline=False)
        builder.tikz += labels[k]
        builder.tikz += ' & \\text{if }'
        builder.simple_tag('color', curr_color,newline=False)
        builder.tikz += f'{domains[k][0]}'
        if k == length - 1:
            builder.tikz += '.'
        else:
            builder.tikz += ','
        builder.tikz += '\\\\\n'

    builder.simple_tag('end','cases')

    return builder.tikz

def draw_piecewise_fn_graph(domains, functions, min_x, max_x, min_y, max_y, fn_name='f', fn_variable='x'):
    builder = TikzBuilder()

    builder.simple_tag('begin', 'center')
    # makes a \filledcirc tex command to create a filled circle
    builder.tikz += '\\newcommand\\filledcirc{{\\color{white}\\bullet}\\mathllap{\\circ}}\n'

    builder.simple_tag('begin', 'tikzpicture', {'scale' : 1})

    # draw the coordinate axes
    builder.tikz += f'\\draw[help lines] ({min_x},{min_y}) grid ({max_x},{max_y});\n'
    builder.tikz += f'\\draw[<->] ({min_x},0)--({max_x},0) node[right]' + '{$' + fn_variable + '$};\n'
    builder.tikz += f'\\draw[<->] (0,{min_y})--(0,{max_y}) node[above]' + '{$y$};\n'

    # we want our axis labels to be integers, so we truncate min/max x/y
    # in the appropriate direction
    min_x = ceil(min_x)
    max_x = floor(max_x)

    min_y = ceil(min_y)
    max_y = floor(max_y)

    # draw x-axis labels
    builder.tikz += '\\foreach \\x in {' + ','.join([str(x) for x in range(min_x,max_x+1)]) + '} {\\draw (\\x, 0)'
    builder.tikz += ' node[below]{\\small{$\\x$}};}\n'

    # draw y-axis labels
    # we have to be careful here to not draw another label at 0, if we already did that
    if 0 in range(min_x, max_x+1):
        y_points = [str(y) for y in range(min_y, max_y+1) if y != 0]
    else:
        y_points = [str(y) for y in range(min_y, max_y+1)]

    builder.tikz += '\\foreach \\y in {' + ','.join(y_points) + '} {\\draw (0,\\y)'
    builder.tikz += ' node[left]{\\small{$\\y$}};}\n'

    # now draw each section of the graph
    length = len(domains)

    for k in range(0,length):
        # cycle through our defined colors
        curr_color = colors[k % len(colors)]
        builder.simple_tag('color', curr_color)

        builder.tikz += '\\draw[ultra thick'

        # draw arrows as appropriate
        if k == 0 and length == 1:
            builder.tikz += ',<->'
        elif k == 0:
            builder.tikz += ',<-'
        elif k == length - 1:
            builder.tikz += ',->'
        else:
            builder.tikz += ',-'

        builder.tikz += '] plot [domain = '
        builder.tikz += str(domains[k][1]) + ':' + str(domains[k][2]) + ', samples=100]'
        builder.tikz += ' (\\x,{' + str(functions[k]) + '});\n'

        # add a right endpoint
        if k < length - 1:
            # dirty hack
            builder.tikz += '\\foreach \\x in {' + str(domains[k][2]) + '}'
            builder.tikz += ' {\\draw (\\x,{' + str(functions[k]) + '}) node{{$\\'
            if domains[k][4]:
                builder.tikz += 'bullet'
            else:
                builder.tikz += 'filledcirc'
            builder.tikz += '$}};};\n'

        # add a left endpoint
        if k > 0:
            # dirty hack
            builder.tikz += '\\foreach \\x in {' + str(domains[k][1]) + '}'
            builder.tikz += ' {\\draw (\\x,{' + str(functions[k]) + '}) node{{$\\'
            if domains[k][3]:
                builder.tikz += 'bullet'
            else:
                builder.tikz += 'filledcirc'
            builder.tikz += '$}};};\n'

    builder.simple_tag('end', 'tikzpicture')
    builder.simple_tag('end', 'center')

    return builder.tikz
