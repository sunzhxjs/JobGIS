from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from pandas import DataFrame, read_csv
import numpy as np
import pandas as pd
import os
app = Flask(__name__,static_folder="static",static_url_path='')
##url_for('static', filename='style.css')

df = pd.read_csv('./amount.csv',index_col="state")
df_city = pd.read_csv('./amount_city.csv',index_col='city')
df_city=df_city.fillna(0)
df_city=df_city.astype(int)
#print df.get_dtype_counts()
df_city['total_in_city']=df_city.sum(axis=1)
#print df_city
df['total_in_state']=df.sum(axis=1) #sum all columns and ingnore non-numeric columns
df.loc['total_in_language']=df.sum(axis=0)

state_header_list = df.columns.values.tolist()
city_header_list = df.columns.values.tolist()
#print header_list

#row = df.loc['Texas'].values.tolist();

@app.route('/')
def index():
    return render_template('main.html')



@app.route('/language/<string:lan_id>',methods=['GET'])
def get_language_count(lan_id):
	if int(lan_id)==0:
		print 'total'
		state_ls = df['total_in_state'].values.tolist()
		city_ls = df_city['total_in_city'].values.tolist()
		state_rank= df['total_in_state'][0:-1].rank(ascending=False).values.tolist()
		city_rank= df_city['total_in_city'][0:-1].rank(ascending=False).values.tolist()
		print state_rank
	else:
		print 'not_total'
		state_ls = df[state_header_list[int(lan_id)-1]].values.tolist()
		city_ls = df_city[city_header_list[int(lan_id)-1]].values.tolist()
		state_rank = df[state_header_list[int(lan_id)-1]][0:-1].rank(ascending=False).values.tolist()
		city_rank = df_city[city_header_list[int(lan_id)-1]][0:-1].rank(ascending=False).values.tolist()

	
	# lan.decode(encoding='UTF-8')
	# print lan
	#state_ls=df[lan].values.tolist()
	return jsonify({'state_count':state_ls,'city_count':city_ls,'state_rank':state_rank,'city_rank':city_rank})




if __name__ == '__main__':
	hostport=int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0',port=hostport)
	#app.run(debug=True)