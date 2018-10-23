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

    def draw_axes(self,min_x,max_x,min_y,max_y, fn_variable):
        tmp = f'\\draw[<->,thick] ({min_x},0) -- ({max_x},0) coordinate (x axis) node[right] ' + '{$' + fn_variable + '$};\n'
        tmp += f'\\draw[<->,thick] (0,{min_y}) -- (0, {max_y}) coordinate (y axis) node[above] ' + '{$y$};\n'

        self.tikz += tmp

def draw_riemann_graph(a,b,n, sample_pos, label, function, min_x, max_x,min_y, max_y, fn_variable='x'):
    builder = TikzBuilder()

    builder.simple_tag('usepackage', 'tikz')
    builder.simple_tag('usetikzlibrary', 'backgrounds')
    builder.tikz += '\n'

    builder.simple_tag('begin', 'center')
    builder.simple_tag('begin','tikzpicture')

    # draw our coordinate axes
    builder.draw_axes(min_x=min_x,max_x=max_x,min_y=min_y,max_y=max_y, fn_variable=fn_variable)

    # compute our sample points
    delta = (b - a) / n

    delta_l = delta * sample_pos
    delta_r = delta - delta_l

    sample_points = [str(a + (delta * (i + delta_l))) for i in range(0,n)]

    builder.tikz += '\\begin{scope}[on background layer]\n'

    # draw the rectangles
    builder.tikz += '\\foreach \\x in {' + ','.join(sample_points) + '} {\\pgfmathparse{' + function + '} \\pgfmathresult\n';
    builder.tikz += f'\\draw[fill=blue!20] (\\x-{delta_l},\\pgfmathresult |- x axis) -- \n'
    builder.tikz += f'(\\x-{delta_l},\\pgfmathresult) -- (\\x+{delta_r},\\pgfmathresult) -- '
    builder.tikz += f'(\\x+{delta_r},\\pgfmathresult |- x axis) -- cycle;' + '}\n'

    # label a and b on the graph
    builder.tikz += f'\\node at ({a},-5pt) ' + '{\\footnotesize{$a$}};\n'
    builder.tikz += f'\\node at ({b},-5pt) ' + '{\\footnotesize{$b$}};\n'

    builder.tikz += f'\\draw[<->,blue,ultra thick,smooth,samples=100,domain={a}:{b}] plot(\\x,' + '{' + function + '});\n'

    builder.tikz += '\\end{scope}\n'

    # close open tags
    builder.simple_tag('end', 'tikzpicture')
    builder.simple_tag('end', 'center')

    return builder.tikz

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

    # required libraries
    builder.simple_tag('usepackage', 'tikz')
    builder.simple_tag('usepackage', 'mathtools')
    builder.tikz += '\n'

    builder.simple_tag('begin', 'center')
    # makes a \filledcirc tex command to create a filled circle
    builder.tikz += '\\newcommand\\filledcirc{{\\color{white}\\bullet}\\mathllap{\\circ}}\n'

    builder.simple_tag('begin', 'tikzpicture', {'scale' : 1})

    # craw the coordinate axes
    builder.draw_axes(min_x=min_x,max_x=max_x,min_y=min_y,max_y=max_y, fn_variable=fn_variable)

    # draw a handy-dandy grid
    builder.tikz += f'\\draw[help lines] ({min_x},{min_y}) grid ({max_x},{max_y});\n'

    # we want our axis labels to be integers, so we truncate min/max x/y
    # in the appropriate direction
    min_x = ceil(min_x)
    max_x = floor(max_x)

    min_y = ceil(min_y)
    max_y = floor(max_y)

    # draw x-axis labels
    builder.tikz += '\\foreach \\x in {' + ','.join([str(x) for x in range(min_x,max_x+1) if x != 0]) + '} {\\draw (\\x, 0)'
    builder.tikz += ' node[below]{\\small{$\\x$}};}\n'

    # draw y-axis labels
    builder.tikz += '\\foreach \\y in {' + ','.join([str(y) for y in range(min_y,max_y+1) if y != 0]) + '} {\\draw (0,\\y)'
    builder.tikz += ' node[left]{\\small{$\\y$}};}\n'

    # now draw each section of the graph
    length = len(domains)

    for k in range(0,length):
        # cycle through our defined colors
        curr_color = colors[k % len(colors)]
        builder.simple_tag('color', curr_color)

        builder.tikz += '\\draw['

        # draw arrows as appropriate
        if k == 0 and length == 1:
            builder.tikz += '<->'
        elif k == 0:
            builder.tikz += '<-'
        elif k == length - 1:
            builder.tikz += '->'
        else:
            builder.tikz += '-'

        builder.tikz += ',ultra thick,smooth,samples=100,domain='
        builder.tikz += str(domains[k][1]) + ':' + str(domains[k][2]) + '] plot'
        builder.tikz += '(\\x,{' + str(functions[k]) + '});\n'

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