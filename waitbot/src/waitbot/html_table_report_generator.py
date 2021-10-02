
import os
import json

from bs4 import BeautifulSoup


class HtmlTableReportGenerator:
    @staticmethod
    def generate_report(src=os.path.expanduser('~')+"/table_report.json",
                        dst=os.path.expanduser('~')+'/table_report.html',
                        template=os.path.expanduser('~')+'/tiago_public_ws/src/ScirocEpisode1/table_report/static_report.html'):

        print('Generating HTML report...')

        print('Reading template {}...'.format(template))
        with open(template, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

        print('Reading source report {}...'.format(src))
        with open(src, 'r') as f:
            status_dict = json.load(f)

        table_status_body = soup.find(id='table-status-body')
        table_status_body.clear()
        print(status_dict['table_status'].items())

        for name, table_status in status_dict['table_status'].items():
            print(name, table_status)
            table_status_body.append(BeautifulSoup(
                '''
                <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-body">
                                    <h3 class="card-title bg-blue-600 text-white p-2">{}</h3>                
                                    <ul class="card-text list-group list-group-flush">
                                        <li class="list-group-item">
                                            <b>Status: </b>{}
                                        </li>
                                        <li class="list-group-item">
                                            <b>Number of people: </b>{}
                                        </li>
                                        <li class="list-group-item">
                                            <b>Items on table: </b>{}
                                        </li>
                                        <li class="list-group-item">
                                            <b>Order: </b>{}
                                        </li>
                                    </ul>
                                </div>
                            <div>
                        </div>
                '''.format(name, table_status['Status'], table_status['NoP'],
                           table_status['Items'], ','.join(table_status.get('Order', []))), 'html.parser'))

        with open(dst, 'w') as f:
            f.write(str(soup))
        print('HTML report generated at: {}'.format(dst))


# This part does not run if script is imported
if __name__ == '__main__':
    HtmlTableReportGenerator().generate_report()
