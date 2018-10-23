from math import cos, sin, ceil, floor


class TikzBuilder:
    def __init__(self):
        self.tikz = ''

    def simple_tag(self,op,v,options=None,newline=True):
        tmp = '\\' + op + '{' + v + '}'
        if options is not None:
            tmp += '['
            for k in options:
                tmp += k + '=' + str(options[k])
            tmp += ']'
        self.tikz += tmp
        if newline:
            self.tikz += '\n'

    def coordinate(self, label, coordinates):
        self.tikz += '\\coordinate (' + label + ') at (' + str(coordinates[0]) + 'cm,' + str(coordinates[1]) + 'cm);\n'

    def draw_cycle(self,v):
        tmp = '\\draw '

        for dt in v:
            tmp += '(' + dt['coordinate'] + ') -- '
            if 'node' in dt:
                tmp += 'node[' + dt['node']['position'] + '] {' + dt['node']['label'] + '} '

        # draw back to our initial entry
        tmp += '(' + v[0]['coordinate'] + ');\n'

        self.tikz += tmp

    def draw_angle(self,start_position, end_position, mode, label=None, direction=None):
        tmp = '\\draw (' + str(start_position[0]) + ',' + str(start_position[1]) + ') ' + mode
        if label is not None and label  != '':
            tmp += ' node[midway'
            if direction is not None:
                tmp += ',' + direction
            tmp += '] {' + label + '}'
        tmp += ' (' + str(end_position[0]) + ',' + str(end_position[1]) + ');\n'
        self.tikz += tmp


def draw_piecewise_fn_definition(domains, labels, fn_name='f', fn_variable='x',
                                 colors=['blue', 'red', 'orange', 'purple', 'olive', 'violet']):
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

def draw_piecewise_fn_graph(domains, functions, min_x, max_x, min_y, max_y, fn_name='f', fn_variable='x',
                            colors=['blue', 'red', 'orange', 'purple', 'olive', 'violet']):
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