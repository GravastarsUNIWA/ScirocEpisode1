import os
import json

table_report = {
    'table_status':
        {'Table1': {
            'items': False,
            'NoP': 2,
            'Status': 'Serving',
            'Order': []
        },
        'Table2': {
            'items': False,
            'NoP': 1,
            'Status': 'Serving',
            'Order': []
        },
        'Table3': {
            'items': False,
            'NoP': 3,
            'Status': 'Served',
            'Order': ['beer', 'fanta', 'cocacola']
        },
        'Table4': {
            'items': True,
            'NoP': 0,
            'Status': 'Cleaning',
            'Order': []
        }
    },
    'total_number_of_customes': 6
}

PARENT_DIR = os.path.abspath(os.path.dirname(__file__))
save_path = os.path.join(PARENT_DIR, 'table_report.json')

with open(save_path, 'w') as f:
    f.write(json.dumps(table_report, indent=4))
