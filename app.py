from flask import Flask, render_template, request
import random
import requests
from bs4 import BeautifulSoup
import csv
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('main.html')
    
@app.route('/welcome')
def welcome():
    return 'Welcome flask!'
    
@app.route('/html_tag')
def html_tag():
    return '<h1>안녕하세요!!</h1>'
    
@app.route('/html_line')
def html_line():
    return """
    <h1>여러줄을 보내봅시다.</h1>
    <ul>
        <li>1번</li>
        <li>2번</li>
    </ul>
    """

@app.route('/html_file')
def html_file():
    return render_template('file.html')
    
@app.route('/hello_p/<string:name>')
def hello_p(name):
    return render_template('hello.html', people_name=name)
    
@app.route('/cube/<int:number>')
def cube(number):
    result = number ** 3
    return render_template('cube.html', number = number, result = result)   # 백엔드에서 연산을 다 해서 html로 보내는것이 좋음.
    
@app.route('/lunch')
def lunch():
    menu_name = {'튀김우동': 'https://post-phinf.pstatic.net/MjAxNzA4MTRfMTIy/MDAxNTAyNjczMTU4MzA3.9YGZFc60Jgqpk0Eou-5UC98i-fa0w5J7Mt-NOFFvsHcg.6GL6-42a49WWR6TDp22OxkRyj7oLutrydTwiu4zHFfgg.JPEG/m_noodle01.jpg?type=w1200',
                 '제육덮밥': 'http://recipe1.ezmember.co.kr/cache/recipe/2017/07/05/7d7c90b00f0b25d2df545e694a2647741.jpg',
                 '콩나물밥': 'http://imagescdn.gettyimagesbank.com/500/201708/jv10933074.jpg',
                 '부대찌개': 'https://cdn.shopify.com/s/files/1/1071/7482/products/10_1.jpeg?v=1460714334'}
    choiced_menu = random.choice(list(menu_name.keys()))
    menu_image = menu_name[choiced_menu]
    return render_template('lunch.html', lunch_menu=choiced_menu, lunch_image=menu_image)
    
@app.route('/lotto')
def lotto():
    lotto_nums = [num for num in range(1, 46, 1)]
    normal_picked = random.sample(lotto_nums, 6)
    return render_template('lotto.html', normal_picked=sorted(normal_picked[:-1]), bonus_picked=normal_picked[-1])
    
@app.route('/naver')
def naver():
    return render_template('naver.html')
    
@app.route('/google')
def google():
    return render_template('google.html')
    
@app.route('/hello')
def hell():
    return render_template('hell.html')
    
@app.route('/hi')
def hi():
    user_name = request.args.get('name')
    return render_template('hi.html', user_name=user_name)
    
@app.route('/user')
def user():
    return render_template('user.html')
    
@app.route('/user/value')
def value():
    name = request.args.get('name')
    first = ord(name[0]) * 100
    second = ord(name[1]) * 1000
    third = ord(name[2]) * 10000
    return render_template('value.html', name=name, values=first+second+third)
    
@app.route('/opgg')
def opgg():
    return render_template('opgg.html')
    
@app.route('/opgg/summoner')
def summoner():
    summoner = request.args.get('summoner')
    url = 'http://www.op.gg/summoner/userName='
    html = requests.get(url+summoner).text
    soup = BeautifulSoup(html, 'html.parser')
    winloss = soup.find('span', class_='WinLose')

    if winloss == None:
        win = 0
        loss = 0
        total = 0
        winratio = '0%'
        # f = open('list.csv', 'a+', encoding='utf-8', newline='\n')
        # csvfile = csv.writer(f)
        # data = [datetime.datetime.now(), summoner, total, win, loss, winratio]
        # csvfile.writerow(data)
        # f.close()
        # return '<h1>솔랭 안돌림?</h1>'
    else:
        win = int(winloss.find('span', class_='wins').text[:-1])
        loss = int(winloss.find('span', class_='losses').text[:-1])
        total = win + loss
        winratio = winloss.find('span', class_='winratio').text.split()[-1]
        
    f = open('list.csv', 'a+', encoding='utf-8', newline='\n')
    csvfile = csv.writer(f)
    data = [datetime.datetime.now(), summoner, total, win, loss, winratio]
    csvfile.writerow(data)
    f.close()
    
    return render_template('summoner.html', win=win, loss=loss, winratio=winratio, summoner=summoner)
    
@app.route('/log')
def log():
    f = open('list.csv', 'r', encoding='utf-8')
    logs = csv.reader(f)
    return render_template('log.html', logs=logs)