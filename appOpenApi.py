from flask import Flask,render_template, request,jsonify,send_file
import pandas as pd
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode,quote_plus,unquote
import UtilityFunc
import req_code
import numpy as np
import os
app = Flask(__name__, static_url_path='/static')
@app.route("/")
def index():
    df = pd.read_csv('C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\cyboscode.csv')
    list = df['stock_code'].tolist()
    return render_template('test.html',list = list)


@app.route("/publicapi",methods=['POST'])
def publicapi():
    url = request.form['url']
    key = request.form['key']
    req_data = request.form.getlist('req_data[]')
    rep_data = 0
    filename=''
    print(len(req_data))
    if len(url)!=0 and len(key) != 0 and "" not in req_data:
        key = unquote(key)
        #queryParams = '?' + urlencode({ quote_plus('ServiceKey'):key})
        query = {quote_plus('ServiceKey'):key}
        for i in range(len(req_data)):
            if i%2 == 1:
                query[quote_plus(req_data[i-1])] = req_data[i]


        queryParams = '?' + urlencode(query)
        df = UtilityFunc.get_data(url,queryParams)
        print(df)
        print(req_code.req_code.keys())
        if str(type(df)) == "<class 'str'>":
            if df in req_code.req_code.keys():
                rep_data = req_code.req_code[df]
            elif df == '00':
                rep_data = 00
        else:
            df_cut = df.iloc[:,:6]
            df_result = df_cut.to_html()

            df_T = df.T
            rep_data = df_T.to_html()
            filename = np.random.randint(100,987654321)
            down_path = f'.\\DB\\Download\\{filename}.csv'
            df_T.to_csv(down_path,encoding='utf-8-sig')
    if "" in req_data:
        rep_data =1

    return jsonify({'rep_data':rep_data,'path':filename})
@app.route("/download",methods=['POST'])
def SendData():
    file = request.form['filename'] +'.csv'
    path = '.\\DB\\download\\'
    return send_file(path+file,mimetype="text/csv",attachment_filename=file,as_attachment=True)
@app.route("/deletedata",methods=['POST'])
def DeleteData():
    file = request.form['filename'] + '.csv'
    path = '.\\DB\\download\\'
    print(path+file)
    if os.path.isfile(path+file):
        os.remove(path+file)
    return jsonify('DeleteData')


if __name__ == '__main__':
    app.run(debug=True)