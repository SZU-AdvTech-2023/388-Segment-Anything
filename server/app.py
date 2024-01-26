from flask import Flask, send_file,request
from io import BytesIO
import cv2 as cv
from flask_cors import CORS
from algo import image_fuse
import webbrowser
webbrowser.open("index.html")

def serve_cv_image(cv_img1,cv_img2):
    # 格式/图片/压缩比
    if(cv_img1 is None):
        return 'false'

    #调整大小
    h1, w1, _ = cv_img1.shape
    img2 =  cv.resize(cv_img2, (w1, h1))
    # 图像融合
    img3 = cv.addWeighted(img2, 0.5, cv_img1, 0.5, 0)
    # gray = cv.cvtColor(cv_img1, cv.COLOR_BGR2GRAY)

    _, encoded_img = cv.imencode('.jpg', img3, [int(cv.IMWRITE_JPEG_QUALITY), 100])

    # # 编码后的图像存储在内存
    img_io = BytesIO(encoded_img)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpg')
app = Flask(__name__)
CORS(app, supports_credentials=True)
@app.route("/")
def index():
    return 'hello '

@app.route("/cv", methods=['POST'])
def cvimg():
    ori_img1 =request.files['ct']
    ori_img2 =request.files['xray']

    img_name1 ='ct.jpg'
    img_name2 = 'xray.jpg'

    path = "./static/img/"
    file_path1 = path+img_name1
    file_path2 = path+img_name2


    ori_img1.save(file_path1)
    ori_img2.save(file_path2)

    res1 = cv.imread(file_path1)
    res2 = cv.imread(file_path2)

    return image_fuse(res2,res1)


app.run()