from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from tikzhelper.triangle import draw_triangle

@view_defaults(route_name='home')
class TikzhelperViews:
	def __init__(self, request):
		self.request = request
	
	@view_config(route_name='home', renderer='home.pt')
	def home(self):
		return {}
		
	@view_config(route_name='generate', request_method='POST')
	def generate(self):
		a = self.request.params['a']
		b = self.request.params['b']
		theta = self.request.params['theta']
		
		url = self.request.route_url('result',a=a,b=b,theta=theta)
		return HTTPFound(location=url)
		
	@view_config(route_name='result', renderer='result.pt')
	def result(self):
		a = float(self.request.matchdict['a'])
		b = float(self.request.matchdict['b'])
		theta = float(self.request.matchdict['theta'])

		tikz_code = draw_triangle(a,b,theta,
															label_a='a',label_b='b',label_c='c',
															label_angle_C='$\\theta$',label_angle_A='').strip()
		
		return {'page_title': 'Edit View', 'a' : a, 'b' : b, 'theta' : theta, 'tikz_code' : tikz_code, 'rows' : 15}
