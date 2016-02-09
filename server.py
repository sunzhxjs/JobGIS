from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from pandas import DataFrame, read_csv
import numpy as np
import pandas as pd
app = Flask(__name__,static_folder="static",static_url_path='')
##url_for('static', filename='style.css')

df = pd.read_csv('./amount.csv',index_col="state")
df['total_in_state']=df.sum(axis=1) #sum all columns and ingnore non-numeric columns
df.loc['total_in_language']=df.sum(axis=0)
header_list = df.columns.values.tolist()
print header_list

#row = df.loc['Texas'].values.tolist();

@app.route('/')
def index():
    return render_template('main.html')



@app.route('/language/<string:lan_id>',methods=['GET'])
def get_language_count(lan_id):
	state_ls = df[header_list[int(lan_id)-1]].values.tolist()
	# lan.decode(encoding='UTF-8')
	# print lan
	#state_ls=df[lan].values.tolist()
	return jsonify({'count':state_ls})




if __name__ == '__main__':
    app.run(debug=True)
