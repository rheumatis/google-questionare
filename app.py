import gspread
from flask import Flask, render_template, jsonify
from oauth2client.service_account import ServiceAccountCredentials

# http://hleecaster.com/python-google-drive-spreadsheet-api/
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
json_file_name = 'C:\\app\\absolute-water-275404-2c5754f0926c.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
# 공유 링크
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/16XeeQXR4bMLEhT_rN74EQsXLONbGo4RPs_MMbb6eS40/edit#gid=1012218114'
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('Form Responses 1')

app = Flask(__name__, template_folder='C:\\app\\templates')

worksheet.update_acell('Z1', '')

cell_list = worksheet.range('A1:Z1')
cell_values = ['A. Timestamp','B. 이름','C. 방문경로','D. 확인사항','q. Positive ROS','a. MHx','c. Drug SE/allergy','d. Op Hx','f. Health Exam in 2 yrs','h. Smoking','i. Alcohol','j. Exercise','k. Occupation','l. Marriage','m. Offsprings','n. Spont Abortion','o. Menopause', 'E. 실비서류', 'r. Comment', 'e. FHx','b. Current med', 'F. ---------------------', 'G. S>', 's. O>', 'g. -------', 'p. -------']

for i, val in enumerate(cell_values):
        cell_list[i].value = val

worksheet.update_cells(cell_list)
## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/records', methods=['GET'])
def records():
    record_list = worksheet.get_all_records()
    return jsonify(record_list[-10:])


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
