#Khởi tạo
from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
app=Flask(__name__)

app.secret_key="Admin@123456789"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/clinicdb' % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"]=6


db = SQLAlchemy(app)
login = LoginManager(app=app)

import cloudinary

cloudinary.config(
    cloud_name="dx5nqi4ll",
    api_key="362937263322676",
    api_secret="w339Gv4z_NcM7gvOPmiq5QloAB0"
)

#############INIT VALUES DATABASE###########

# from models import QuyDinh
#
# def initValuesForTable():
#     try:
#         #ADD QUY DINH
#         quydinh1 = QuyDinh(tenQD='Quy định về người đại diện của người bệnh',
#                            noiDung='Một người bệnh chỉ có một người đại diện tại một thời điểm.')
#         quydinh2 = QuyDinh(tenQD='Nguyên tắc trong khám bệnh, chữa bệnh',
#                            noiDung='Tôn trọng, bảo vệ, đối xử bình đẳng và không kỳ thị, phân biệt đối xử đối với người bệnh.')
#         db.session.add_all([quydinh1,quydinh2])
#         db.session.commit()
#     except:
#         db.session.rollback()




