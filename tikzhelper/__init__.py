from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pkg_resources import resource_filename
from deform import Form

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.set_session_factory(SignedCookieSessionFactory('itsasecrsdasdet'))
    config.add_static_view(name='static', path='tikzhelper:static')
    config.add_static_view(name='deform_static', path='deform:static')
    config.add_route('home', '/')
    config.add_route('piecewise', '/piecewise')
    config.add_route('riemann', '/riemann')
    config.add_route('riemann_view', '/riemann/view')
    config.add_route('integral', '/integrals')
    config.add_route('triangle', '/triangles')
    config.scan()
    return config.make_wsgi_app()
