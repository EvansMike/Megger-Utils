from setuptools import setup

setup(name='megger',
      version='0.1',
      description='Megger utility',
      #url='http://github.com/storborg/funniest',
      author='Mike Evans',
      author_email='mikee@saxicola.co.uk',
      license='MIT',
      packages=['megger'],
      entry_points = {'console_scripts': ['megger_cap=megger.megger_cap:main',\
            'mk_merge=megger.mk_merge:main'],},
      zip_safe=False
      )
