import os
import json

from bs4 import BeautifulSoup


class HtmlTableReportGenerator:
    @staticmethod
    def generate_report(src='/home/paris/table_report.json', dst='/home/paris/table_report.html', template='/home/paris/tiago_public_ws/src/ScirocEpisode1/table_report/static_report.html'):

        print('Generating HTML report...')

        print(f'Reading template {template}...')
        with open(template, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

        print(f'Reading source report {src}...')
        with open(src, 'r') as f:
            status_dict = json.load(f)

        table_status_body = soup.find(id='table-status-body')
        table_status_body.clear()
        print(status_dict['table_status'].items())

        for name, table_status in status_dict['table_status'].items():
            print(name, table_status)
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
                                            <b>Items on table: </b>{table_status['Items']}
                                        </li>
                                        <li class="list-group-item">
                                            <b>Order: </b>{','.join(table_status.get('Order', []))}
                                        </li>
                                    </ul>
                                </div>
                            <div>
                        </div>
                ''', 'html.parser'))

        with open(dst, 'w') as f:
            f.write(str(soup))
        print(f'HTML report generated at: {dst}')


# This part does not run if script is imported
if __name__ == '__main__':
    HtmlTableReportGenerator().generate_report()
