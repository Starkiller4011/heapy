from __future__ import division, print_function
def Initialize():
    import sys
    import importlib
    import subprocess
    dependencies = ['sys', 'concurrent.futures', 'numpy', 'matplotlib', 'pandas', 'sklearn', 'astropy']
    def install(package):
        subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', package])
    for dep in dependencies:
        try:
            importlib.import_module(dep)
        except:
            print('%s not installed, installing...' % dep, file=sys.stderr)
            try:
                install(dep)
            except:
                print('Error installing %s' % dep, file=sys.stderr)
            else:
                print('%s successfuly installed' % dep, file=sys.stderr)
    del dependencies, install
Initialize()
del Initialize
from .structure_function import StructureFunction
from .time_series import TimeSeries
def ExampleData():
    import os
    import pandas as pd
    ex_data = {}
    df = pd.read_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/example_lc.csv'))
    ex_data['time'] = df['time'].tolist()
    ex_data['value'] = df['value'].tolist()
    ex_data['error'] = df['error'].tolist()
    del df
    return ex_data
