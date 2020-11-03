from flask import Flask,render_template, request,jsonify,send_file
import pandas as pd
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode,quote_plus,unquote
import UtilityFunc
import req_code
import numpy as np
import re
import os

app = Flask(__name__, static_url_path='/static')
@app.context_processor
def DirList():
    def Portfolio(dic_name):
        list = 'main.png'
        return list
    def PortfolioTitle(dic_name):
        str_ = dic_name.split('.')[1]
        str_list = str_.split('_')
        title = ' '.join(str_list).capitalize()
        return title

    def PortfolioDesc(dic_name):
        with open(f'.\\static\\portfolio\\{dic_name}\\desc.txt','r') as f:
            desc = f.read()
            return desc

    return dict(Portfolio = Portfolio,PortfolioTitle=PortfolioTitle,PortfolioDesc=PortfolioDesc)
@app.route("/")
def index():

    return render_template('index.html',title='Home')
@app.route("/<pagename>")
def menu(pagename):
    title = pagename
    portfolio_list= []
    if title =='portfolio':
        portfolio_list = os.listdir('.\\static\\portfolio\\')
    return render_template(f'{pagename}.html',title=title,portfolio_list=portfolio_list)
@app.route("/test")
def test():
    df = pd.read_csv('C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\cyboscode.csv')
    list = df['stock_code'].tolist()
    return render_template('test.html',list = list)





if __name__ == '__main__':
    app.run(debug=True)