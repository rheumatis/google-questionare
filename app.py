import gspread
from flask import Flask, render_template, jsonify
from oauth2client.service_account import ServiceAccountCredentials

# http://hleecaster.com/python-google-drive-spreadsheet-api/
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
json_file_name = 'absolute-water-275404-2c5754f0926c.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
# 공유 링크
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/16XeeQXR4bMLEhT_rN74EQsXLONbGo4RPs_MMbb6eS40/edit?usp=sharing'
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('Form Responses 1')

app = Flask(__name__)


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/records', methods=['GET'])
def records():
    return jsonify(worksheet.get_all_records())


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
