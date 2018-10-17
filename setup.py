from setuptools import setup

requires = [
	'pyramid',
	'pyramid_chameleon',
	'waitress',
]

setup(name='tikzhelper',
	install_requires=requires,
	entry_points="""\
	[paste.app_factory]
	main = tikzhelper:main
	""",
)