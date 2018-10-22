from math import sqrt, cos, sin, pi, acos
from tikzhelper.helpers.tikzbuilder import TikzBuilder

class Triangle:
    # construct a triangle with SAS (A,theta,B)
    # here we expect that theta is in degrees
    def __init__(self,a,b,theta):
        self.a = a
        self.b = b
        self.theta = theta * (pi/180)

        # compute the length of the remaining side
        self.c = sqrt(self.a**2 + self.b**2 - 2 * self.a * self.b * cos(self.theta))

        # what about the remaining two angles?
        self.beta = acos((self.b**2 + self.c**2 - self.a**2) / (float(2) * self.b * self.c ))
        self.alpha = pi - self.theta - self.beta

class TikzTriangle:
    def __init__(self,constructor):
        self.constructor = constructor

    def draw(self, label_a, label_b, label_c, tolerance = 0.0001,show_angle_A = False, show_angle_B = False, show_angle_C = False, label_angle_A = None, label_angle_B = None, label_angle_C = None, color_start=None, color_end = None, scale=1, align='center'):
        builder = TikzBuilder()

        # if we want to align our drawing
        if align is not None:
            builder.simple_tag('begin',align)

        # sometimes we want to change the global color
        if color_start is not None:
            builder.simple_tag('color', color_start)

        # begin our tikzpicture
        builder.simple_tag('begin','tikzpicture', {'scale' : str(scale)})

        # compute coordinates for the vertices of our triangle
        # we always assume that the base of the triangle is sitting on the x-axis
        coordinate_A = (0,0)
        coordinate_B = (self.constructor.b * cos(self.constructor.theta), self.constructor.b * sin(self.constructor.theta))
        coordinate_C = (self.constructor.a,0)


        # write out the coordinate tags
        builder.coordinate('A',coordinate_A)
        builder.coordinate('B',coordinate_B)
        builder.coordinate('C',coordinate_C)

        # draw the triangle
        v = [{'coordinate' : 'A', 'node' : {'position' : 'above left', 'label' : label_a}},
             {'coordinate' : 'B', 'node' : {'position' : 'right', 'label' : label_c}},
             {'coordinate' : 'C', 'node' : {'position' : 'below', 'label' : label_b}}]

        length = min(0.5, 0.15 * min(self.constructor.a, self.constructor.b))
        rectangle_length = min(0.3, 0.15 * min(self.constructor.a, self.constructor.b))
        label_distance = 0.5

        if show_angle_A:
            if (abs(self.constructor.alpha - pi/2) < tolerance):
                mode = 'rectangle'
                curr_length = rectangle_length
            else:
                mode = 'to[bend left]'
                curr_length = length

            start_position = (coordinate_C[0] - curr_length,coordinate_C[1])
            end_position = (coordinate_C[0]-curr_length*cos(self.constructor.alpha),coordinate_C[1]+curr_length*sin(self.constructor.alpha))

            builder.draw_angle(start_position=start_position,end_position=end_position,mode=mode,label=label_angle_A,direction='left')
            
        if show_angle_B:
            if (abs(self.constructor.beta - pi/2) < tolerance):
                mode = 'rectangle'
                curr_length = rectangle_length
            else:
                mode = 'to[bend right]'
                curr_length = length

            start_position = (coordinate_B[0]-(curr_length * cos(self.constructor.theta)),coordinate_B[1]-(curr_length *
sin(self.constructor.theta)))
            end_position = (coordinate_B[0]-curr_length*cos(self.constructor.theta+self.constructor.beta),coordinate_B[1]-curr_length*sin(self.constructor.theta+self.constructor.beta))

            builder.draw_angle(start_position=start_position,end_position=end_position,mode=mode,label=label_angle_B,direction='below')

        if show_angle_C:
            if (abs(self.constructor.theta - pi/2) < tolerance):
                mode = 'rectangle'
                curr_length = rectangle_length
            else:
                mode = 'to[bend right]'
                curr_length = length

            start_position = (coordinate_A[0]+curr_length,coordinate_A[1])
            end_position = (coordinate_A[0]+(curr_length * cos(self.constructor.theta)), coordinate_A[1]+(curr_length * sin(self.constructor.theta)))

            builder.draw_angle(start_position=start_position,end_position=end_position,mode=mode,label=label_angle_C,direction='right')
        
        builder.draw_cycle(v)

        # end all of the open tags
        builder.simple_tag('end','tikzpicture')

        if color_end is not None:
            builder.simple_tag('color', color_end)

        if align is not None:
            builder.simple_tag('end',align)

        return builder.tikz

def draw_triangle(a,b,theta,label_a='a',label_b='b',label_c='c',show_angle_A=False,show_angle_B=False,show_angle_C=False,label_angle_A=None,label_angle_B=None,label_angle_C=None,
color_start='black',color_end='red',scale=1):
    constructor = Triangle(a,b,theta)
    triangle = TikzTriangle(constructor)
    return triangle.draw(label_a,label_b,label_c,show_angle_A=show_angle_A,show_angle_B=show_angle_B,show_angle_C=show_angle_C,label_angle_A=label_angle_A,label_angle_B=label_angle_B,label_angle_C=label_angle_C,
    color_start=color_start,color_end=color_end,scale=scale)