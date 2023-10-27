from flask import Flask, render_template, request, redirect, url_for , session ,jsonify
import mysql.connector
import os
import datetime
from PIL import Image
import pandas as pd
import base64
from io import BytesIO

def images_to_base64(image_paths):
    base64_images = []
    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")
            base64_images.append(base64_image)
    return base64_images

# 이미지 파일 경로 리스트
image_paths = ["./static/images/house1.jpg", "./static/images/house2.jpg", "./static/images/house3.jpg", 
                "./static/images/house3.jpg" ,"./static/images/house4.jpg" ,"./static/images/house5.jpg",
                "./static/images/house6.jpg"] 

base64_images = images_to_base64(image_paths)




# 이미지 파일 경로
image_path1 = "./static/images/milyang-arirang-festival.jpg"
image_path2 = "./static/images/sunflower.jpg"
image_path3 = "./static/images/twintunnel.jpg"
image_path4 = "./static/images/youngnamroo.jpg"


# 원하는 크기
desired_width = 200
desired_height = 150

# 이미지 열기
img1 = Image.open(image_path1)
img2 = Image.open(image_path2)
img3 = Image.open(image_path3)
img4 = Image.open(image_path4)

# 이미지 크기 조정
img_resized1 = img1.resize((desired_width, desired_height))
img_resized2 = img2.resize((desired_width, desired_height))
img_resized3 = img3.resize((desired_width, desired_height))
img_resized4 = img4.resize((desired_width, desired_height))


# 조정된 이미지 저장
img_resized1.save("./static/images2/milyang-arirang-festival_resized.jpg")
img_resized2.save("./static/images2/sunflower_resized.jpg")
img_resized3.save("./static/images2/twintunnel_resized.jpg")
img_resized4.save("./static/images2/youngnamroo_resized.jpg")

os.urandom(12)

print(os.urandom(12))

connection = mysql.connector.connect(host = 'localhost', 
                                        port = '3306',
                                        database = 'connect',
                                        user = 'root',
                                        password = 'als7946rh!')

cursor = connection.cursor()





app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.secret_key = 'H\xb0\xf0\x16\x0e\x8a\x13<\xe9E\xbd\xdc'

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    # SQL 쿼리 실행
    query = """
        SELECT a.sharehouse_img, a.name, b.city, a.avg_rating
        FROM sharehouse a, location b
        WHERE a.location_id = b.location_id
        ORDER BY avg_rating DESC
        LIMIT 4;
    """
    cursor.execute(query)
    results = cursor.fetchall()  # 모든 결과 가져오기

    # 템플릿에 전달할 데이터 준비
    sharehouse_data = []
    for i, result in enumerate(results):
         sharehouse_img, name, city, avg_rating = result
         base64_img = base64_images[i]  # 이미지를 base64로 변환한 데이터
         sharehouse_data.append({
             'img': base64_img,
             'name': name,
             'city': city,
             'avg_rating': avg_rating
         })
         
    return render_template("home.html", data=sharehouse_data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/activity")
def activity():
    return render_template("activity.html")

@app.route("/conditionSearch")
def conditionSearch():
    return render_template("conditionSearch.html")

@app.route("/review")
def review():
    return render_template("review.html")

@app.route("/listings-single")
def listings_single():
    # 데이터베이스에서 sharehouse와 comment 정보 가져오기
    query = """
        SELECT a.name, a.sharehouse_img, b.comment_text
        FROM sharehouse a
        JOIN comment b ON a.sharehouse_id = b.sharehouse_id
    """
    cursor.execute(query)
    results = cursor.fetchall()  # 모든 결과를 가져옴

    # 템플릿에 전달할 데이터 준비
    sharehouse_data = []
    for result in results:
        sharehouse_name, sharehouse_img, comment_text = result
        sharehouse_data.append({
            'name': sharehouse_name,
            'img': sharehouse_img,
            'comment': comment_text
        })

    return render_template("listings-single.html", sharehouse_data=sharehouse_data)

@app.route("/listings")
def listings():
    # Querying the necessary data from the database
    query = """
        SELECT s.name, l.address, c.comment_text, s.avg_rating
        FROM sharehouse s
        INNER JOIN location l ON s.location_id = l.location_id
        LEFT JOIN comment c ON s.sharehouse_id = c.sharehouse_id
    """
    cursor.execute(query)
    one_row = cursor.fetchone()  # Fetch the first row
    two_row = cursor.fetchone()
    three_row = cursor.fetchone()  
    four_row = cursor.fetchone()
    five_row = cursor.fetchone()
    six_row = cursor.fetchone()  
    seven_row = cursor.fetchone() 
    eight_row = cursor.fetchone()
    nine_row = cursor.fetchone()  
    ten_row = cursor.fetchone() 
    eleven_row = cursor.fetchone()
    twelve_row = cursor.fetchone()  
    thirteen_row = cursor.fetchone() 
    fourteen_row = cursor.fetchone() 

    # Rendering the listings.html template and passing the data to the template
    return render_template("listings.html", data1=one_row,data2=two_row,data3=three_row,data4=four_row,data5=five_row,
                                                data6=six_row, data7=seven_row , data8=eight_row, data9 = nine_row,
                                                data10 = ten_row, data11 = eleven_row, data12 = twelve_row,
                                                data13 = thirteen_row,data14 = fourteen_row)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # 데이터베이스에서 사용자 정보 가져오기
        cursor.execute("SELECT * FROM register WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and user[2] == password:  # user[2]는 데이터베이스에서 비밀번호가 저장된 열의 인덱스입니다. 실제로는 해싱된 비밀번호를 비교해야 합니다.
            # 로그인 성공
            session['user_id'] = user[0]  # 사용자 ID를 세션에 저장
            return redirect(url_for('home'))  # home 라우트로 리디렉션

        # 로그인 실패
        return "Invalid email or password. Please try again."

    return render_template("login.html")

# 로그아웃 처리
@app.route("/logout")
def logout():
    if 'user_id' in session:
        del session['user_id']  # 세션에서 user_id 삭제
        # return jsonify(success=True)  # 로그아웃 성공을 JSON 응답으로 반환
    return redirect(url_for('home'))  # 메인 페이지로 리디렉션

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match. Please try again."

        # 현재 시간 가져오기
        current_time = datetime.datetime.now()

        # MySQL 데이터베이스에 회원가입 정보 저장 (email, password, date_registered)
        cursor.execute("INSERT INTO register (email, password, date_registered) VALUES (%s, %s, %s)",
                       (email, password, current_time))
        connection.commit()

        return "Registration successful! You can now <a href='/login'>login</a>."

    return render_template("register.html")


@app.route("/find")
def find():
    return render_template("find.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)