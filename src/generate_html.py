import os
import json
import datetime
from collections import defaultdict
from vessel_flags import vessel_flags

VESSEL_DATA_DIR = 'thames-london'
OUTPUT_HTML_FILE = 'vessel-report.html'

# Function to read all vessel files and collect their data
def read_vessel_data(directory):
    vessel_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            mmsi = filename.split('.')[0]
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                data['mmsi'] = mmsi  # Store the MMSI in the data
                vessel_data.append(data)
    return vessel_data

# Function to generate the HTML table
def generate_html(vessel_data):
    # Sort vessels by the last seen date (more recent on top)
    vessel_data.sort(key=lambda x: x['last_seen'], reverse=True)

    # Find the earliest and latest dates seen across all vessels
    all_dates_seen = set()
    for data in vessel_data:
        all_dates_seen.update(data['dates_seen'])
    all_dates_seen = sorted(all_dates_seen)
    start_date = datetime.datetime.strptime(all_dates_seen[0], "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(all_dates_seen[-1], "%Y-%m-%d").date()

    # Create a list of all dates from start_date to end_date
    date_range = [start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    
    # Generate HTML
    html = '''
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                text-align: center;
                padding: 8px;
            }
            th {
                position: sticky;
                top: 0;
                background: #f2f2f2;
                z-index: 2;
            }
            td:first-child, th:first-child {
                position: sticky;
                left: 0;
                background: #f2f2f2;
                z-index: 1;
                text-align: left;  /* Left align the first column */
            }
            .green {
                background-color: green;
                color: white;
            }
            .gray {
                background-color: gray;
                color: white;
            }
            .scrollable-table {
                overflow: auto;
                white-space: nowrap;
            }
        </style>
    </head>
    <body>
        <div class="scrollable-table">
            <table>
                <tr>
                    <th>Vessel Name</th>'''

    for date in date_range:
        html += f'<th>{date.strftime("%Y-%m-%d")}</th>'
    
    html += '</tr>'
    
    for data in vessel_data:
        mmsi = data['mmsi']
        vessel_name = data['last_full_data'].get('NAME', mmsi)
        vessel_mid = int(str(mmsi)[:3])
        flag = vessel_flags.get(vessel_mid, '')
        vessel_name_with_flag = f"{flag} {vessel_name}"
        vessel_link = f"https://www.vesselfinder.com/?mmsi={mmsi}"
        html += f'<tr><td><a href="{vessel_link}">{vessel_name_with_flag}</a></td>'
        
        earliest_seen_date = datetime.datetime.strptime(data['dates_seen'][0], "%Y-%m-%d").date()
        for date in date_range:
            if date < earliest_seen_date:
                html += '<td class="gray"></td>'
            elif date.strftime("%Y-%m-%d") in data['dates_seen']:
                html += '<td class="green"></td>'
            else:
                html += '<td></td>'
        
        html += '</tr>'
    
    html += '''
            </table>
        </div>
    </body>
    </html>
    '''
    
    return html

# Read the vessel data
vessel_data = read_vessel_data(VESSEL_DATA_DIR)

# Generate the HTML content
html_content = generate_html(vessel_data)

# Write the HTML content to a file
with open(OUTPUT_HTML_FILE, 'w', encoding='utf-8') as file:
    file.write(html_content)

print(f"HTML report generated: {OUTPUT_HTML_FILE}")