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