from math import cos, sin, ceil, floor

class MagicTikzBuilder:
    def __init__(self):
        self.tikz = ''
        self._tmp = ''
        self._indent = 0
        self._indentpredelta = 0
        self._indentpostdelta = 0

    def _nl(self):
        self._tmp += '\n'
        return self

    def _free(self, txt):
        self._tmp += ' {} '.format(txt)
        return self

    def _raw(self, txt):
        self._tmp += str(txt)
        return self

    def _xy(self, x, y):
        return self._pr('axis cs:{},{}'.format(x, y))

    def _pr(self, txt):
        self._tmp += '({})'.format(txt)
        return self

    def _sq(self, options, bracket=True, newline=False):
        unpacked = []
        for k in options:
            if options[k] is None:
                unpacked.append(k)
            else:
                if isinstance(options[k],dict):
                    unpacked.append('{}={{{}}}'.format(k, self._sq(options[k], False)))
                else:
                    unpacked.append('{}={}'.format(k,str(options[k])))

        if not bracket:
                return ','.join(unpacked)

        else:
            if newline and len(unpacked) > 0:
                tmp = ''
                for k, line in enumerate(unpacked):
                    if k == 0:
                        tmp += '{},\n'.format(line)
                    else:
                        tmp += ('    ' * self._indent) + (' ' * (len(self._tmp) + 1)) + '{},\n'.format(line)
                tmp = tmp[:-2]
                self._tmp += '[{}]'.format(tmp)
            else:
                self._tmp += '[{}]'.format(','.join(unpacked))

            return self

    def __getitem__(self, item):
        self._tmp += '{' + '{}'.format(item) + '}'
        return self

    def __getattr__(self, name):
        # increase indent level by 1 after we begin a tag
        if name == 'begin':
            self._indentpostdelta += 1
        # decrease indent level by 1 whenever we end a tag
        if name == 'end':
            self._indentpredelta -= 1

        self._tmp += '\\{}'.format(name)
        return self

    def __call__(self, line_sep=''):
        # end the line, concat to overall tikz
        self._tmp += line_sep
        self._nl()

        # update the indent with the pre delta
        self._indent = max(0, self._indent + self._indentpredelta)

        # indent the line
        self.tikz += '    ' * self._indent + self._tmp

        # update the indent with the post delta for the next line
        self._indent = max(0, self._indent + self._indentpostdelta)

        # reset buffers
        self._indentpredelta = 0
        self._indentpostdelta = 0
        self._tmp = ''


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


def draw_axes(builder, min_x, max_x, min_y, max_y, draw_grid=False, draw_labels=False):
    xticks = '{' + ','.join([str(x) for x in range(ceil(min_x), floor(max_x)) if x != 0]) + '}'
    yticks = '{' + ','.join([str(y) for y in range(ceil(min_y), floor(max_y)) if y != 0]) + '}'

    options = {'axis lines': 'middle',
                              'xlabel': '$x$',
                              'ylabel': '$y$',
                              'xticklabel style' : {'font' : '\\tiny', 'yshift' : '0.5ex'},
                              'yticklabel style' : {'font' : '\\tiny', 'xshift' : '0.5ex'},
                              'xmin': min_x,
                              'xmax': max_x,
                              'ymin': min_y,
                              'ymax': max_y,
                              'xtick' : xticks,
                              'ytick' : yticks}

    # optionally add a grid to our axes
    # drawing a grid overrides any x/y tick settings
    if draw_grid:
        options['grid'] = 'both'
        options['minor tick num'] = 1

    # optionally draw axis labels
    if not draw_labels:
        options['xticklabels'] = {}
        options['yticklabels'] = {}

    builder.begin['axis']._sq(options, newline=True)()


def draw_riemann_graph(a,b,n, sample_pos, function, min_x, max_x,min_y, max_y, draw_grid, draw_labels):
    builder = MagicTikzBuilder()

    builder.begin['center']()
    builder.begin['tikzpicture']()

    # draw axes
    draw_axes(builder=builder,
              min_x=min_x,
              max_x=max_x,
              min_y=min_y,
              max_y=max_y,
              draw_grid=draw_grid,
              draw_labels=draw_labels)

    # compute our sample points
    delta = (b-a)/n
    delta_l = delta * sample_pos
    delta_r = delta - delta_l

    sample_points = '{' + ','.join([str(a + (delta * i) + delta_l) for i in range(0,n)]) + '}'

    # we have to change from x to #1 to satisfy pgfplots needs
    pgfplots_function = function.replace('x','#1')

    # draw the rectangles
    builder.pgfplotsinvokeforeach._raw(sample_points)._raw(' {')()
    builder.draw._sq({'fill' : 'blue!20'})._xy('#1-{}'.format(delta_l),0)._free('--')
    builder._xy('#1+{}'.format(delta_r),0)._free('--')._xy('#1+{}'.format(delta_r),'{{{}}}'.format(pgfplots_function))._free('--')
    builder._xy('#1-{}'.format(delta_l),'{{{}}}'.format(pgfplots_function))._raw(' -- cycle')(';')
    builder._raw('}')()

    # label a and b on the graph if we don't already have axis labels
    if not draw_labels:
        builder.node._sq({'below' : None})._free('at')._xy(a,0)._raw('{\\footnotesize{$a$}}')(';')
        builder.node._sq({'below' : None})._free('at')._xy(b,0)._raw('{\\footnotesize{$b$}}')(';')

    # now plot our function
    builder.addplot._sq({'<->' : None,
                         'blue' : None,
                         'thick' : None,
                         'smooth' : None,
                         'samples' : 100,
                         'domain' : '{}:{}'.format(a,b)})[function](';')

    builder.end['axis']()
    builder.end['tikzpicture']()
    builder.end['center']()

    return builder.tikz

def draw_piecewise_fn_definition(domains, labels,
                                 colors=['blue', 'red', 'orange', 'purple', 'olive', 'violet']):
    builder = MagicTikzBuilder()

    # begin our function definition
    builder._raw('f(x)=').begin['cases']()

    length = len(domains)
    for k in range(0,length):
        curr_color = colors[k % len(colors)]

        # add the function definition
        builder.color[curr_color]._raw(labels[k])._free('&').text['if '].color[curr_color]._raw(domains[k][0])
        builder._raw('.' if k == length - 1 else ',')._raw('\\\\')()

    builder.end['cases']()

    return builder.tikz

def draw_piecewise_fn_graph(domains, functions, min_x, max_x, min_y, max_y, draw_grid, draw_labels,
                            colors=['blue', 'red', 'orange', 'purple', 'olive', 'violet']):
    builder = MagicTikzBuilder()

    builder.begin['center']()
    builder.begin['tikzpicture']()

    draw_axes(builder=builder,
              min_x=min_x,
              max_x=max_x,
              min_y=min_y,
              max_y=max_y,
              draw_grid=draw_grid,
              draw_labels=draw_labels)

    # now draw each section of the graph
    length = len(domains)

    for k in range(0, length):
        # draw arrows as appropriate
        plot_decoration = '-'
        if k == 0 and length == 1:
            plot_decoration = '<->'
        elif k == 0:
            plot_decoration = '<-'
        elif k == length - 1:
            plot_decoration = '->'

        # cycle through our defined colors
        curr_color = colors[k % len(colors)]

        builder.addplot._sq({plot_decoration: None,
                             curr_color: None,
                             'thick': None,
                             'smooth': None,
                             'samples': 100,
                             'domain': '{}:{}'.format(domains[k][1],domains[k][2])})[functions[k]](';')
        # we have to change from x to #1 to satisfy pgfplots needs
        pgfplots_function = '{' + functions[k].replace('x', '#1') + '}'

        #add a right endpoint
        if k < length - 1:
            builder.pgfplotsinvokeforeach._raw('{{{}}}'.format(domains[k][2]))._raw(' {')()
            builder.draw._xy('#1',pgfplots_function)._raw(' node{').color[curr_color]._raw('{$')
            if domains[k][4]:
                builder._raw('\\bullet')
            else:
                builder._raw('{\\color{white}\\bullet}\\mathllap{\\circ}')
            builder._raw('$}};}')()

        # add a left endpoint
        if k > 0:
            builder.pgfplotsinvokeforeach._raw('{{{}}}'.format(domains[k][1]))._raw(' {')()
            builder.draw._xy('#1',pgfplots_function)._raw(' node{').color[curr_color]._raw('{$')
            if domains[k][3]:
                builder._raw('\\bullet')
            else:
                builder._raw('{\\color{white}\\bullet}\\mathllap{\\circ}')
            builder._raw('$}};}')()

    builder.end['axis']()
    builder.end['tikzpicture']()
    builder.end['center']()

    return builder.tikz

def draw_region_between_curves(min_x,max_x,min_y,max_y,a,b,f,g,draw_grid,draw_labels,delta=0.0001):
    builder = MagicTikzBuilder()
    builder.begin['center']()
    builder.begin['tikzpicture']()

    draw_axes(builder=builder,
              min_x=min_x,
              max_x=max_x,
              min_y=min_y,
              max_y=max_y,
              draw_grid=draw_grid,
              draw_labels=draw_labels)

    # by default we give our functions arrows at the end of their domain
    # except if we're taking our integral to the same place
    plot_decoration = '<->'

    if a == min_x:
        plot_decoration = '-' if b == max_x else '->'
    elif b == max_x:
        plot_decoration = '<-'

    f_options = {plot_decoration: None,
                        'blue': None,
                        'thick': None,
                        'smooth': None,
                        'samples': 100,
                        'domain': '{}:{}'.format(min_x,max_x),
                        'name path': 'f'}

    # we don't draw the function if it's zero
    if f == '0':
        f_options['draw'] = 'none'

    builder.addplot._sq(f_options)[f](';')

    g_options = {plot_decoration: None,
                        'red': None,
                        'thick': None,
                        'smooth': None,
                        'samples': 100,
                        'domain': '{}:{}'.format(min_x,max_x),
                        'name path': 'g'}

    # we don't draw the function if it's zero
    if g == '0':
        g_options['draw'] = 'none'

    builder.addplot._sq(g_options)[g](';')

    # draw the region between f and g
    builder.addplot._sq({'blue': None, 'opacity': 0.1})._free('fill between')._sq(
        {'of': 'f and g', 'soft clip': {'domain' : '{}:{}'.format(a,b)}})(';')

    # compute path intersections
    builder.path._sq({'name path': 'v_st'})._xy(a + delta, min_y)._free('--')._xy(a + delta, max_y)(';')
    builder.path._sq({'name path': 'v_end'})._xy(b - delta, min_y)._free('--')._xy(b - delta, max_y)(';')
    builder.path._sq({'name intersections': {'of': 'f and v_st', 'by': 'f_st'}})(';')
    builder.path._sq({'name intersections': {'of': 'g and v_st', 'by': 'g_st'}})(';')
    builder.path._sq({'name intersections': {'of': 'f and v_end', 'by': 'f_end'}})(';')
    builder.path._sq({'name intersections': {'of': 'g and v_end', 'by': 'g_end'}})(';')

    # draw the dashed left and right borderse
    builder.draw._sq({'dashed': None})._pr('f_st')._free('--')._pr('g_st')(';')
    builder.draw._sq({'dashed': None})._pr('f_end')._free('--')._pr('g_end')(';')

    builder.end['axis']()
    builder.end['tikzpicture']()
    builder.end['center']()

    return builder.tikz