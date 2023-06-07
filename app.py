from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import certifi

app = Flask(__name__)

client = MongoClient('mongodb+srv://sparta:test@cluster0.qtbduoj.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta

# URL = "https://movie.daum.net/ranking/reservation"
# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(URL, headers=headers)
# soup = BeautifulSoup(data.text, 'html.parser')

# lis = soup.select("#mainContent > div > div.box_ranking > ol > li")
# print(lis)

# # 기존 데이터 삭제
# db.movie.delete_many({})

# for li in lis:
#     title = li.select_one('.link_txt').text
#     rate = li.select_one('.txt_num').text
#     poster = li.select_one('.poster_movie>img')['src']
#     rank = li.select_one('.rank_num').text

#     if title is not None:
#         doc = {
#             'title': title,
#             'poster': poster,
#             'rank': rank,
#             'rate': rate,
#         }
#         print(doc)
#         db.movie.insert_one(doc)
#     print(rank, title, rate, poster)


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    URL = "https://movie.daum.net/ranking/reservation"
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(URL, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    lis = soup.select("#mainContent > div > div.box_ranking > ol > li")
    print(lis)

    # 기존 데이터 삭제
    db.movie.delete_many({})

    for li in lis:
        title = li.select_one('.link_txt').text
        rate = li.select_one('.txt_num').text
        poster = li.select_one('.poster_movie>img')['src']
        rank = li.select_one('.rank_num').text

        if title is not None:
            doc = {
                'title': title,
                'poster': poster,
                'rank': rank,
                'rate': rate,
            }
            print(doc)
            db.movie.insert_one(doc)
        print(rank, title, rate, poster)
    
    return jsonify({'msg': 'POST 연결 완료!'})
    
@app.route("/movie", methods=["GET"])
def movie_get():
    all_movie = list(db.movie.find({},{'_id':False}))
    return jsonify({'result': all_movie})

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
