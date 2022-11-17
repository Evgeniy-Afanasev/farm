from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os


app = Flask(__name__, static_folder=rf'{os.path.dirname(os.path.abspath(__file__))}\templates')

msa_drivers = [x for x in pyodbc.drivers() if 'ACCESS' in x.upper()]
print(f'MS-Access Drivers : {msa_drivers}')

#Попытка установки соединения с БД
try:
    con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'+rf'DBQ={os.path.dirname(os.path.abspath(__file__))}\farm.accdb;'
    conn = pyodbc.connect(con_string)
    print("Connected To Database")

except pyodbc.Error as e:
    print("Error in Connection", e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('action1') == 'Информация о ферме':
            return redirect(url_for('data'))
        elif request.form.get('action2') == 'VALUE2':
            return 'Тык1'
        else:
            return 'Тык2'
    elif request.method == 'GET':
        return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    title = 'Ваша Ферма'
    header = 'Информация о состоянии вашей фермы'

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM situation")

    data = [string for string in cursor.fetchall()]

    print(data)

    x = range(0, len(data))
    y = [i[1] for i in data[::]]

    plt.plot(x, y)

    status_plot = 'templates/img/status_plot.png'
    plt.savefig('templates/img/status_plot.png')
    plt.switch_backend('agg')
    return render_template('data.html', title=title, header=header, data=data, status_plot=status_plot)

if __name__ == '__main__':
    app.debug = True
    app.run()



