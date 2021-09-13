import os
import json

from bs4 import BeautifulSoup

with open('static_report.html', 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')

with open('table_report.json', 'r') as f:
    status_dict = json.load(f)

table_status_body = soup.find(id='table-status-body')
table_status_body.clear()

for name, table_status in status_dict['table_status'].items():
    table_status_body.append(BeautifulSoup(
    f'''
    <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h3 class="card-title bg-blue-600 text-white p-2">{name}</h3>                
                        <ul class="card-text list-group list-group-flush">
                            <li class="list-group-item">
                                <b>Status: </b>{table_status['Status']}
                            </li>
                            <li class="list-group-item">
                                <b>Number of people: </b>{table_status['NoP']}
                            </li>
                            <li class="list-group-item">
                                <b>Items on table: </b>{table_status['items']}
                            </li>
                            <li class="list-group-item">
                                <b>Order: </b>{','.join(table_status['Order'])}
                            </li>
                        </ul>
                    </div>
                <div>
            </div>
    ''', 'html.parser'))

with open('table_report.html', 'w') as f:
    f.write(str(soup))