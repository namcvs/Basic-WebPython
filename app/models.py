# Tác động tới CSDL
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db
from flask_login import UserMixin
import enum
from datetime import datetime


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    BACSI = 3
    YTA = 4
    THUNGAN = 5


class Sex(enum.Enum):
    MALE = 0,
    FEMALE = 1


# UserMixin để nó hiều đây là model dùng để chứng thực-> vì Python da kế thừa
class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://th.bing.com/th/id/OIP.48Pj-NVeziMTgdX6rHGpKAHaI1?w=162&h=194&c=7&r=0&o=5&dpr=1.1&pid=1.7')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    nhanvien = relationship('NhanVien', backref='user', lazy=True)

    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    image = Column(String(100))
    Category_ID = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


# -----------------------------------------------------------------------


class PersonModel(object):
    # attributes
    hoTen = Column(String(50), default='')
    ngaySinh = Column(DateTime, default=datetime.now())
    maCCCD = Column(String(12), unique=True, default='')
    diaChi = Column(String(150), default='')
    email = Column(String(50), default='')
    soDienThoai = Column(String(10), default='')
    sex = Column(Enum(Sex), default=Sex.MALE)


class NhanVien(PersonModel, db.Model):
    __tablename__ = 'nhanvien'

    # primary keys
    maNV = Column(Integer, primary_key=True, autoincrement=True)
    # attributes
    ngayVaoLam = Column(DateTime, default=datetime.now())
    # ChuyenNganh = Column(String(50))
    avatar = Column(String(250),
                    default='https://th.bing.com/th/id/OIP.48Pj-NVeziMTgdX6rHGpKAHaI1?w=162&h=194&c=7&r=0&o=5&dpr=1.1&pid=1.7')
    user_id = Column(Integer, ForeignKey(User.id))

    def __str__(self):
        return self.name


class YTa(NhanVien):
    __tablename__ = 'yta'
    # primary key
    maYT = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)
    # relationship
    danhsachkhamBenh_id = relationship('DanhSachKhamBenh', backref='yta', lazy=True)

    def __str__(self):
        return self.name


class BacSi(NhanVien):
    __tablename__ = 'bacsi'

    # primary keys
    maBS = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)
    # foreign key

    # relationships
    phieuKhamBenh = relationship('PhieuKhamBenh', backref='bacsi', lazy=True)

    def __str__(self):
        return self.name


class ThuNgan(NhanVien):
    __tablename__ = 'thungan'
    # primary key
    thuNgan_id = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)

    hoadonthanhtoan = relationship('HoaDonThanhToan', backref='thungan', lazy=True)

    def __str__(self):
        return self.name


class BenhNhan(PersonModel, db.Model):
    __tablename__ = 'BenhNhan'

    # attribute
    maBN = Column(Integer, primary_key=True, autoincrement=True)
    tienSuBenh = Column(String(200), default='Không')
    danhsachkhambenh_id = relationship('DanhSachKhamBenh', backref='benhnhan', lazy=True)

    def __str__(self):
        return self.name


class DanhSachKhamBenh(db.Model):
    __tablename__ = 'danhsachkhambenh'
    id = Column(Integer, primary_key=True, autoincrement=True)

    YTa_ID = Column(Integer, ForeignKey(YTa.maYT))
    maBN_ID = Column(Integer, ForeignKey(BenhNhan.maBN))
    ngayKham = Column(DateTime, default=datetime.now())

    phieukhambenh_id = relationship('PhieuKhamBenh', backref='danhsachkhambenh', lazy=True)

    quanly = relationship('QuanLy', backref='danhsachkhambenh', lazy=True)

    def __str__(self):
        return self.name


# class LichKhamBenh(db.Model):
#     __tablename__ = 'lichkhambenh'
#
#     # attribute
#     id = Column(Integer, primary_key=True, autoincrement=True)
#
#     maBN = Column(Integer, ForeignKey(BenhNhan.maBN))
#     dsKhamBenh_id = Column(Integer, ForeignKey(DanhSachKhamBenh.id))
#
#     bieumau = relationship('BieuMau', backref='lichkhambenh', lazy=True)
#
#     def __str__(self):
#         return self.name


class QuyDinh(db.Model):
    __tablename__ = 'quydinh'
    maQD = Column(Integer, primary_key=True, autoincrement=True)
    tenQD = Column(String(50), nullable=False)
    noiDung = Column(String(200), nullable=False)

    quanly = relationship('QuanLy', backref='quydinh', lazy=True)

    def __str__(self):
        return self.name


class DonVi(db.Model):
    __tablename__ = 'donvi'
    maDV = Column(Integer, primary_key=True, autoincrement=True)
    tenDV = Column(String(50), nullable=False)

    thuoc = relationship('Thuoc', backref='donvi', lazy=True)

    def __str__(self):
        return self.name


class Thuoc(db.Model):
    __tablename__ = 'thuoc'
    maThuoc = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50), nullable=False)
    moTa = Column(String(250), nullable=True)
    ngaySX = Column(DateTime, default=datetime.now(), nullable=False)
    nhaSX = Column(String(250), nullable=False)
    soLuong = Column(Integer, nullable=False)
    giaTien = Column(Float, default=0)
    image = Column(String(250),
                   default='https://data-service.pharmacity.io/pmc-upload-media/production/pmc-ecm-core/__sized__/products/P00222_11-thumbnail-510x510-70.jpg')

    # foreign key
    maDV_id = Column(Integer, ForeignKey(DonVi.maDV))

    # relationships
    danhsachthuoc = relationship('DanhSachThuoc', backref='thuoc', lazy=True)
    huongdansudung = relationship('HuongDanSuDung', backref='thuoc', lazy=True)

    def __str__(self):
        return self.name


class PhieuKhamBenh(db.Model):
    __tablename__ = 'phieukhambenh'
    maPhieuKham = Column(Integer, primary_key=True, autoincrement=True)
    trieuChung = Column(String(250), default="Không có")
    duDoanBenh = Column(String(100), default="Không có")

    bacsi_ID = Column(Integer, ForeignKey(BacSi.maBS))
    ngayLap = Column(DateTime, default=datetime.now())
    maBN = Column(Integer, ForeignKey(DanhSachKhamBenh.maBN_ID))
    huongdansudung = relationship('HuongDanSuDung', backref='phieukhambenh', lazy=True)
    hoadonthanhtoan = relationship('HoaDonThanhToan', backref='phieukhambenh', lazy=True)
    quanly = relationship('QuanLy', backref='phieukhambenh', lazy=True)

    def __str__(self):
        return self.name


class HuongDanSuDung(db.Model):
    __tablename__ = 'huongdansudung'
    maThuoc_id = Column(Integer, ForeignKey(Thuoc.maThuoc), primary_key=True)
    maPhieuKham_id = Column(Integer, ForeignKey(PhieuKhamBenh.maPhieuKham), primary_key=True)
    lieuDung = Column(Integer, default=0)
    cachDung = Column(String(250), nullable=True)

    def __str__(self):
        return self.name


class DanhSachThuoc(db.Model):
    __tablename__ = 'danhsachthuoc'
    maDS = Column(Integer, primary_key=True, autoincrement=True)
    maThuoc_id = Column(Integer, ForeignKey(Thuoc.maThuoc))

    quanly = relationship('QuanLy', backref='danhsachthuoc', lazy=True)

    def __str__(self):
        return self.name


class HoaDonThanhToan(db.Model):
    __tablename__ = 'hoadonthanhtoan'
    maHD = Column(Integer, primary_key=True, autoincrement=True)
    tienKham = Column(Float, default=0)
    tienThuoc = Column(Float, default=0)
    trangThai = Column(String(100), default='Chưa Thanh Toán')

    thuNgan_id = Column(Integer, ForeignKey(ThuNgan.thuNgan_id))
    maPhieuKham = Column(Integer, ForeignKey(PhieuKhamBenh.maPhieuKham))

    quanly = relationship('QuanLy', backref='hoadonthanhtoan', lazy=True)

    def __str__(self):
        return self.name


class Admin(NhanVien):
    __tablename__ = 'admin'
    # primary key
    admin_id = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)
    quanly_id = relationship('QuanLy', backref='admin', lazy=True)

    def __str__(self):
        return self.name


# QuanLy
class QuanLy(db.Model):
    __tablename__ = 'quanly'
    quanLy_id = Column(Integer, primary_key=True, autoincrement=True)
    dsThuoc_id = Column(Integer, ForeignKey(DanhSachThuoc.maDS))
    quyDinh_id = Column(Integer, ForeignKey(QuyDinh.maQD))
    maPhieuKham_id = Column(Integer, ForeignKey(PhieuKhamBenh.maPhieuKham))
    hoaDon_id = Column(Integer, ForeignKey(HoaDonThanhToan.maHD))
    danhSachKhamBenh_id = Column(Integer, ForeignKey(DanhSachKhamBenh.id))

    admin_id = Column(Integer, ForeignKey(Admin.admin_id), primary_key=True)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()

        # # ---------------------ADD BENHNHAN------------------------
        # benhnhan1 = BenhNhan(
        #     hoTen='Nguyễn Văn A',
        #     ngaySinh=datetime(1990, 1, 1),
        #     maCCCD='56565658',
        #     diaChi='123 Đường ABC, Quận XYZ',
        #     email='nguyenvana@example.com',
        #     soDienThoai='012366789',
        #     sex=Sex.MALE,
        #     tienSuBenh='Tiền sử bệnh của bệnh nhân 1'
        # )
        # benhnhan2 = BenhNhan(
        #     hoTen='Trần Thị B',
        #     ngaySinh=datetime(1985, 5, 5),
        #     maCCCD='98724661012',
        #     diaChi='456 Đường XYZ, Quận ABC',
        #     email='tranthib@example.com',
        #     soDienThoai='0987274321',
        #     sex=Sex.FEMALE,
        #     tienSuBenh='Tiền sử bệnh của bệnh nhân 2'
        # )
        # benhnhan3 = BenhNhan(
        #     hoTen='Trần Thị C',
        #     ngaySinh=datetime(2004, 5, 5),
        #     maCCCD='26724661012',
        #     diaChi='472 Đường Bình Thạnh, Quận ABC',
        #     email='tranthic@example.com',
        #     soDienThoai='0987274321',
        #     sex=Sex.FEMALE,
        #     tienSuBenh='Tiền sử bệnh của bệnh nhân 3'
        # )
        # benhnhan4 = BenhNhan(
        #     hoTen='Đông Văn Nam',
        #     ngaySinh=datetime(2004, 5, 5),
        #     maCCCD='1211159902',
        #     diaChi='472 Đường Bình Chánh, Quận ABC',
        #     email='tranthiNam@example.com',
        #     soDienThoai='0982224321',
        #     sex=Sex.MALE,
        #     tienSuBenh='Tiền sử bệnh của bệnh nhân 4'
        # )
        # benhnhan5 = BenhNhan(
        #     hoTen='Đông Văn Nhan',
        #     ngaySinh=datetime(2004, 5, 5),
        #     maCCCD='1217759922',
        #     diaChi='472 Đường Bình Chánh, Quận ABC',
        #     email='tranthiNam@example.com',
        #     soDienThoai='0982222221',
        #     sex=Sex.MALE,
        #     tienSuBenh='Tiền sử bệnh của bệnh nhân 5'
        # )
        # db.session.add_all([benhnhan1,benhnhan2,benhnhan3,benhnhan4,benhnhan5])
        # db.session.commit()
        # # ---------------------ADD USER------------------------
        # import hashlib
        #
        # u1 = User(name='Admin',
        #           username='admin',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           avatar='https://mdbcdn.b-cdn.net/img/new/avatars/2.webp',
        #           user_role=UserRoleEnum.ADMIN)
        #
        # u2 = User(name='BacSi',
        #           username='bacsi',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           avatar='https://hoanmy.com/wp-content/uploads/2023/05/HMSG-BS-NGUYEN-THI-THU-MAI.jpg',
        #           user_role=UserRoleEnum.BACSI)
        #
        # u3 = User(name='User',
        #           username='user',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           avatar='https://mdbcdn.b-cdn.net/img/new/avatars/1.webp',
        #           user_role=UserRoleEnum.USER)
        # u4 = User(name='YTa',
        #           username='yta',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           avatar='https://th.bing.com/th/id/OIP.rdALIqgMwrEqQjUn0ZfJpwHaHR?w=768&h=754&rs=1&pid=ImgDetMain',
        #           user_role=UserRoleEnum.YTA)
        # u5 = User(name='ThuNgan',
        #           username='thungan',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           avatar='https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(10).webp',
        #           user_role=UserRoleEnum.THUNGAN)
        #
        # db.session.add_all([u1, u2, u3, u4, u5])
        # db.session.commit()
        # # ---------------------ADD ADMIN------------------------
        # admin1 = Admin(
        #     hoTen="Võ Duy Khôi",
        #     ngaySinh=datetime(2003, 4, 15),
        #     maCCCD="032122026",
        #     diaChi="Thới Lai, Bình Đại, Bến Tre",
        #     email="voduykhoi1504@example.com",
        #     soDienThoai="0362728158",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2016, 4, 20),
        #     avatar="https://mdbcdn.b-cdn.net/img/new/avatars/1.webp",
        #     user_id=1
        # )
        #
        # db.session.add(admin1)
        # db.session.commit()
        # # ---------------------Bác sĩ------------------------
        # d1 = BacSi(
        #     hoTen="Nguyễn Thị Thu Hồng",
        #     ngaySinh=datetime(1990, 1, 1),
        #     maCCCD="123456789012",
        #     diaChi="123 Main St",
        #     email="john.doe@example.com",
        #     soDienThoai="1234567890",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime.now(),
        #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMDN-XET-NGHIEM-PHAM-THI-THANH-HUYEN-9628.jpg",
        #     user_id=2
        #
        # )
        # d2 = BacSi(
        #     hoTen="Phan Thanh Tươi",
        #     ngaySinh=datetime(2003, 1, 1),
        #     maCCCD="123456789013",
        #     diaChi="127 Main St",
        #     email="ThanhDat@example.com",
        #     soDienThoai="1234567891",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2020, 2, 1),
        #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMSGC-Bs-Phan-Thanh-Tuoi.jpg"
        #
        # )
        # d3 = BacSi(
        #     hoTen="Đặng Thị Thu Bé",
        #     ngaySinh=datetime(2003, 1, 1),
        #     maCCCD="123456789014",
        #     diaChi="127 Main St",
        #     email="ThanhDat@example.com",
        #     soDienThoai="1234567891",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2020, 2, 1),
        #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMSGC-THAY-THUOC-UU-TU.-DANG-THI-BE-THU.jpg"
        #
        # )
        # d4 = BacSi(
        #     hoTen="Thạch Minh Huy",
        #     ngaySinh=datetime(2003, 1, 1),
        #     maCCCD="123456789015",
        #     diaChi="127 Main St",
        #     email="ThanhDat@example.com",
        #     soDienThoai="1234567891",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2020, 2, 1),
        #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMSGC-Bs-Thach-Minh-Huy.jpg"
        # )
        # d5 = BacSi(
        #     hoTen="Thạch Minh Vũ",
        #     ngaySinh=datetime(2003, 1, 1),
        #     maCCCD="1234525015",
        #     diaChi="Bến tre",
        #     email="ThanhDat@example.com",
        #     soDienThoai="1234567891",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2020, 2, 1),
        #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMDN-NOI-NGUYEN-ANH-TUYEN.jpg"
        # )
        # d6 = BacSi(
        #     hoTen="Thạch Anh Tuyền",
        #     ngaySinh=datetime(2003, 1, 1),
        #     maCCCD="1223015",
        #     diaChi="Bến tre",
        #     email="ThanhDat@example.com",
        #     soDienThoai="12312391",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2020, 2, 1),
        #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMDN-CMO-Tran-Minh-Nghia.jpg"
        # )
        # d7 = BacSi(
        #     hoTen="Thạch Anh Tuyền",
        #     ngaySinh=datetime(2003, 1, 1),
        #     maCCCD="232751315",
        #     diaChi="Bến Bình Đại",
        #     email="ThanhDat@example.com",
        #     soDienThoai="1233891",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2021, 2, 1),
        #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/DNIH-BSCKII.-Tran-Van-Thuan-Truong-khoa-noi-kiem-Pho-giam-doc-chuyen-mon-BV.jpg"
        # )
        # d8 = BacSi(
        #     hoTen="Thạch Anh Tuyền",
        #     ngaySinh=datetime(2003, 1, 1),
        #     maCCCD="233220065",
        #     diaChi="Bến Bình Đại",
        #     email="ThanhDat@example.com",
        #     soDienThoai="123267891",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2021, 2, 1),
        #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMMH-Phan-Van-Hung.jpg"
        # )
        # db.session.add_all([d1, d2, d3, d4,d5, d6, d7, d8])
        # db.session.commit()
        # # ---------------------ADD YTA------------------------
        # yta1 = YTa(
        #     hoTen="Nguyễn Văn Y ",
        #     ngaySinh=datetime(2003, 1, 1),
        #     maCCCD="123456789016",
        #     diaChi="123 Đường Chính",
        #     email="yta1@example.com",
        #     soDienThoai="1234567890",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2017, 4, 20),
        #     avatar="https://res.cloudinary.com/dx9eo8pyh/image/upload/v1704361418/yta_qwimqb.png",
        #     user_id=4
        #
        # )
        #
        # yta2 = YTa(
        #     hoTen="Trần Thị Mỹ",
        #     ngaySinh=datetime(2002, 2, 1),
        #     maCCCD="987654321017",
        #     diaChi="456 Đường Sồi",
        #     email="yta2@example.com",
        #     soDienThoai="0987654321",
        #     sex=Sex.FEMALE,
        #     ngayVaoLam=datetime(2018, 5, 25),
        #     avatar="https://res.cloudinary.com/dx9eo8pyh/image/upload/v1704361418/yta_qwimqb.png",
        # )
        # db.session.add_all([yta1,yta2])
        # db.session.commit()
        # # ---------------------ADD THU NGAN------------------------
        # thungan1 = ThuNgan(
        #     hoTen="Nguyễn Trọng Phúc",
        #     ngaySinh=datetime(2002, 9, 12),
        #     maCCCD="987654325",
        #     diaChi="DS19 Hiep Binh Chanhn",
        #     email="thungan1@example.com",
        #     soDienThoai="036897456",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2016, 4, 20),
        #     avatar="https://res.cloudinary.com/dx9eo8pyh/image/upload/v1704361418/yta_qwimqb.png",
        #     user_id=5
        # )
        # thungan2 = ThuNgan(
        #     hoTen="Võ Thị Mẫn Nghi",
        #     ngaySinh=datetime(2001, 9, 12),
        #     maCCCD="987654666",
        #     diaChi="239 Phan Văn Trị",
        #     email="thungan2@example.com",
        #     soDienThoai="036889456",
        #     sex=Sex.FEMALE,
        #     ngayVaoLam=datetime(2019, 4, 20),
        #     avatar="https://res.cloudinary.com/dx9eo8pyh/image/upload/v1704361418/yta_qwimqb.png",
        # )
        #
        # db.session.add_all([thungan1,thungan2])
        # db.session.commit()
        #
        # # ---------------------DON VI------------------------
        #
        # donvi1 = DonVi(tenDV='viên')
        # donvi2 = DonVi(tenDV='chay')
        # donvi3 = DonVi(tenDV='vĩ')
        #
        # db.session.add_all([donvi1, donvi2,donvi3])
        # db.session.commit()
        # # ---------------------ADD QUY DINH------------------------
        # quydinh1 = QuyDinh(tenQD='Số lượt khám trong ngày',
        #                    noiDung='Mỗi ngày khám tối đa 40 bệnh nhân.')
        # quydinh2 = QuyDinh(tenQD='Quy định về loại và đơn vị thuốc',
        #                    noiDung='Có 30 loại thuốc, 3 loại đơn vị (viên, chai, vỹ).')
        # quydinh3 = QuyDinh(tenQD='Tiền Khám',
        #                    noiDung='Tiền khám 100.000 VNĐ')
        # db.session.add_all([quydinh1, quydinh2,quydinh3])
        # db.session.commit()
        #
        # # ---------------------THUOC-----------------------
        # thuoc1 = Thuoc(tenThuoc='Acetylcystein',moTa='Thuốc Acetylcystein 200mg Khapharco tiêu nhầy trong bệnh viêm phế quản, bệnh nhầy nhớt (190 viên)',
        #                ngaySX=datetime(2023, 1, 1),nhaSX='Khánh Hòa',
        #                soLuong=190,giaTien='147000',
        #                image='https://cdn.nhathuoclongchau.com.vn/unsafe/373x0/filters:quality(90)/https://cms-prod.s3-sgn09.fptcloud.com/00033640_acetylcystein_200mg_khapharco_190v_4715_6239_large_c0df9dbf99.jpg',
        #                 maDV_id=1)
        # thuoc2 = Thuoc(tenThuoc='Panadol', moTa='Hoạt chất: Paracetamol 500mg/viên',
        #                ngaySX=datetime(2023, 2, 12), nhaSX='GlaxoSmithKline',
        #                soLuong=84, giaTien='60000',
        #                image='https://cdn.nhathuoclongchau.com.vn/unsafe/373x0/filters:quality(90)/https://cms-prod.s3-sgn09.fptcloud.com/00005708_panadol_500mg_vien_sui_9558_5c06_large_1e05052a61.JPG',
        #                maDV_id=3)
        # thuoc3 = Thuoc(tenThuoc='Frigofast Spray ', moTa='Chai xịt lạnh Frigofast Spray giảm đau bong gân, căng cơ, giãn dây chằng (200ml)',
        #                ngaySX=datetime(2022, 5, 22), nhaSX='FARMAC - ZABBAN S.P.A',
        #                soLuong=21, giaTien='175000',
        #                image='https://cdn.nhathuoclongchau.com.vn/unsafe/373x0/filters:quality(90)/https://cms-prod.s3-sgn09.fptcloud.com/00502251_chai_xit_lanh_giam_dau_frigofast_spray_italia_200ml_8660_63d7_large_aa0c229207.jpg',
        #                maDV_id=2)
        # thuoc4 = Thuoc(tenThuoc='Clorpheniramin',
        #                moTa='điều trị dị ứng da & dị ứng đường hô hấp (200 viên)',
        #                ngaySX=datetime(2022, 5, 22), nhaSX='CÔNG TY CP DƯỢC PHẨM KHÁNH HÒA',
        #                soLuong=56, giaTien='64000',
        #                image='https://www.domesco.com/pictures/catalog/products/san-pham-2019/03-10-2019/Clorpheniramin-maleat-4-mg-nang.jpg',
        #                maDV_id=3)
        # thuoc5 = Thuoc(tenThuoc='Acetylcystein',
        #                moTa='Thuốc Acetylcystein 200mg Khapharco tiêu nhầy trong bệnh viêm phế quản, bệnh nhầy nhớt (190 viên)',
        #                ngaySX=datetime(2023, 1, 1), nhaSX='Khánh Hòa',
        #                soLuong=190, giaTien='87650',
        #                image='https://cdn.nhathuoclongchau.com.vn/unsafe/373x0/filters:quality(90)/https://cms-prod.s3-sgn09.fptcloud.com/00033640_acetylcystein_200mg_khapharco_190v_4715_6239_large_c0df9dbf99.jpg',
        #                maDV_id=1)
        # thuoc6 = Thuoc(tenThuoc='Panadol', moTa='Hoạt chất: Paracetamol 500mg/viên',
        #                ngaySX=datetime(2023, 2, 12), nhaSX='GlaxoSmithKline',
        #                soLuong=5, giaTien='212578',
        #                image='https://cdn.nhathuoclongchau.com.vn/unsafe/373x0/filters:quality(90)/https://cms-prod.s3-sgn09.fptcloud.com/00005708_panadol_500mg_vien_sui_9558_5c06_large_1e05052a61.JPG',
        #                maDV_id=3)
        # thuoc7 = Thuoc(tenThuoc='Frigofast Spray ',
        #                moTa='Uống Frigofast Spray giúp ổn định dần và cân đối lượng đường lại (200ml)',
        #                ngaySX=datetime(2022, 5, 22), nhaSX='FARMAC - ZABBAN S.P.A',
        #                soLuong=80, giaTien='145556',
        #                image='https://cdn.nhathuoclongchau.com.vn/unsafe/373x0/filters:quality(90)/https://cms-prod.s3-sgn09.fptcloud.com/00502251_chai_xit_lanh_giam_dau_frigofast_spray_italia_200ml_8660_63d7_large_aa0c229207.jpg',
        #                maDV_id='2')
        # thuoc8 = Thuoc(tenThuoc='Revitalize Capsules',
        #                moTa='Revitalize Capsules giúp tăng cường năng lượng và sự tỉnh táo (45 viên)',
        #                ngaySX=datetime(2022, 10, 12),
        #                nhaSX='Energize Pharma',
        #                soLuong=40,
        #                giaTien='74985',
        #                image='https://example.com/revitalize_capsules.jpg',
        #                maDV_id='3')
        # thuoc9 = Thuoc(tenThuoc='MintyFresh Drops',
        #                moTa='MintyFresh Drops	 giúp đường huyết trong cơ thể điều hòa lại (15ml)',
        #                ngaySX=datetime(2022, 7, 10),
        #                nhaSX='Natures Wellness',
        #                soLuong=30,
        #                giaTien='112566',
        #                image='https://example.com/mintyfresh_drops.jpg',
        #                maDV_id='3')
        # thuoc10 = Thuoc(tenThuoc='MintyFresh Drops',
        #                moTa='MintyFresh Drops mang lại hương thơm tự nhiên, giảm cảm giác khó chịu trong họng (15ml)',
        #                ngaySX=datetime(2022, 7, 10),
        #                nhaSX="Thanh long",
        #                soLuong=70,
        #                giaTien='224125',
        #                image='https://example.com/mintyfresh_drops.jpg',
        #                maDV_id='3')
        #
        # db.session.add_all([thuoc1,thuoc2,thuoc3,thuoc4,thuoc5,thuoc6,thuoc7,thuoc8,thuoc8,thuoc9,thuoc10])
        # db.session.commit()
        # # ---------------------DANH SACH THUOC------------------------
        #
        # dsthuoc1 = DanhSachThuoc(maThuoc_id=1)
        # dsthuoc2 = DanhSachThuoc(maThuoc_id=2)
        # dsthuoc3 = DanhSachThuoc(maThuoc_id=3)
        # dsthuoc4 = DanhSachThuoc(maThuoc_id=4)
        # dsthuoc5 = DanhSachThuoc(maThuoc_id=5)
        # dsthuoc6 = DanhSachThuoc(maThuoc_id=6)
        # dsthuoc7 = DanhSachThuoc(maThuoc_id=7)
        # dsthuoc8 = DanhSachThuoc(maThuoc_id=8)
        # dsthuoc9 = DanhSachThuoc(maThuoc_id=9)
        # dsthuoc10 = DanhSachThuoc(maThuoc_id=10)
        # db.session.add_all([dsthuoc1, dsthuoc2,dsthuoc3,dsthuoc4,dsthuoc5, dsthuoc6,dsthuoc7,dsthuoc8,dsthuoc9,dsthuoc10])
        #
        # db.session.commit()
        #
        #
        # #---------------------DANHSACHKHAMBENH------------------------
        # dskhambenh1 = DanhSachKhamBenh( YTa_ID=10,ngayKham=datetime(2023, 11, 1),maBN_ID=1)
        # dskhambenh2 = DanhSachKhamBenh( YTa_ID=10,ngayKham=datetime(2023, 12, 2),maBN_ID=2)
        # dskhambenh3 = DanhSachKhamBenh(YTa_ID=10, ngayKham=datetime(2023, 12, 3), maBN_ID=3)
        # dskhambenh4 = DanhSachKhamBenh(YTa_ID=11, ngayKham=datetime(2023, 12, 4), maBN_ID=4)
        # dskhambenh5 = DanhSachKhamBenh(YTa_ID=11, ngayKham=datetime(2023, 11, 5), maBN_ID=5)
        # db.session.add_all([dskhambenh1, dskhambenh2,dskhambenh3,dskhambenh4,dskhambenh5])
        # db.session.commit()
        # #---------------------ADD PHIEUKHAMBENH------------------------
        # phieukhambenh1 = PhieuKhamBenh(trieuChung='Triệu chứng của bệnh nhân 1',
        #                    duDoanBenh='Dự đoán bệnh cho bệnh nhân 1',
        #                          bacsi_ID=2,ngayLap=datetime(2023, 12, 1),maBN=1)
        # phieukhambenh2 = PhieuKhamBenh(trieuChung='Triệu chứng của bệnh nhân 2',
        #                          duDoanBenh='Dự đoán bệnh cho bệnh nhân 2',
        #                          bacsi_ID=3,ngayLap=datetime(2023, 12, 2),maBN=2)
        # phieukhambenh3 = PhieuKhamBenh(trieuChung='Triệu chứng của bệnh nhân 3',
        #                                duDoanBenh='Dự đoán bệnh cho bệnh nhân 3',
        #                                bacsi_ID=2, ngayLap=datetime(2023, 12, 3), maBN=3)
        # phieukhambenh4 = PhieuKhamBenh(trieuChung='Triệu chứng của bệnh nhân 4',
        #                                duDoanBenh='Dự đoán bệnh cho bệnh nhân 4',
        #                                bacsi_ID=4, ngayLap=datetime(2023, 12, 1), maBN=4)
        # phieukhambenh5 = PhieuKhamBenh(trieuChung='Triệu chứng của bệnh nhân 5',
        #                                duDoanBenh='Dự đoán bệnh cho bệnh nhân 5',
        #                                bacsi_ID=2, ngayLap=datetime(2023, 12, 2), maBN=5)
        # db.session.add_all([phieukhambenh1, phieukhambenh2,phieukhambenh3,phieukhambenh4,phieukhambenh5])
        # db.session.commit()
        # # ---------------------HUONG DAN SU DUNG------------------------
        # huongdansudung1 = HuongDanSuDung(maThuoc_id=2,
        #                                  maPhieuKham_id=1,
        #                                  lieuDung=21,
        #                                  cachDung='Uống thuốc với nước. Không nhai hoặc nghiền thuốc khi sử dụng.')
        # huongdansudung2 = HuongDanSuDung(maThuoc_id=1,
        #                                  maPhieuKham_id=2,
        #                                  lieuDung=12,
        #                                  cachDung='Không được dùng đồng thời với các thuốc ho khác hoặc bất cứ thuốc nào làm giảm bài tiết đờm.')
        # huongdansudung3 = HuongDanSuDung(maThuoc_id=1,
        #                                  maPhieuKham_id=3,
        #                                  lieuDung=10,
        #                                  cachDung='Uống thuốc bằng một cốc nước lớn. Tránh uống cùng với các đồ uống có caffeine.')
        # huongdansudung4 = HuongDanSuDung(maThuoc_id=4,
        #                                  maPhieuKham_id=4,
        #                                  lieuDung=9,
        #                                  cachDung='Uống thuốc trước hoặc sau khi ăn, tùy thuộc vào hướng dẫn của bác sĩ. Hạn chế uống cùng với chất có thể tạo tác dụng phụ.')
        #
        # huongdansudung5 = HuongDanSuDung(maThuoc_id=9,
        #                                  maPhieuKham_id=5,
        #                                  lieuDung=5,
        #                                  cachDung='Nên uống thuốc cùng một thời điểm mỗi ngày để duy trì liều lượng ổn định trong cơ thể.')
        # db.session.add_all([huongdansudung1, huongdansudung2,huongdansudung3, huongdansudung4,huongdansudung5])
        # db.session.commit()
        # # ---------------------HOADONTHANHTOAN------------------------
        # hoadonthanhtoan1 = HoaDonThanhToan(tienKham=100000,tienThuoc=120000,thuNgan_id=12,maPhieuKham=1)
        # hoadonthanhtoan2 = HoaDonThanhToan(tienKham=100000, tienThuoc=100000, thuNgan_id=12, maPhieuKham=2)
        # hoadonthanhtoan3 = HoaDonThanhToan(tienKham=100000, tienThuoc=87650, thuNgan_id=12,maPhieuKham=3)
        # hoadonthanhtoan4 = HoaDonThanhToan(tienKham=100000, tienThuoc=212578,  thuNgan_id=12,maPhieuKham=4)
        # hoadonthanhtoan5 = HoaDonThanhToan(tienKham=100000, tienThuoc=145556,  thuNgan_id=13, maPhieuKham=5)
        #
        #
        # db.session.add_all([hoadonthanhtoan1, hoadonthanhtoan2,hoadonthanhtoan3,hoadonthanhtoan4,hoadonthanhtoan5])
        # db.session.commit()
        #
        #
        #
        # # ---------------------QUANLY------------------------
        # quanly1 = QuanLy(
        #     dsThuoc_id=1,  # Thay 1 bằng ID thực tế của Danh Sách Thuốc
        #     quyDinh_id=1,  # Thay 3 bằng ID thực tế của Quy Định
        #     maPhieuKham_id=1,  # Thay 4 bằng ID thực tế của Phiếu Khám Bệnh
        #     hoaDon_id=1,  # Thay 5 bằng ID thực tế của Hóa Đơn Thanh Toán
        #     danhSachKhamBenh_id=1,  # Thay 6 bằng ID thực tế của Danh Sách Khám Bệnh
        #     admin_id=1
        # )
        # quanly2 = QuanLy(
        #     dsThuoc_id=2,  # Thay 1 bằng ID thực tế của Danh Sách Thuốc
        #     quyDinh_id=2,  # Thay 3 bằng ID thực tế của Quy Định
        #     maPhieuKham_id=2,  # Thay 4 bằng ID thực tế của Phiếu Khám Bệnh
        #     hoaDon_id=2,  # Thay 5 bằng ID thực tế của Hóa Đơn Thanh Toán
        #     danhSachKhamBenh_id=2,  # Thay 6 bằng ID thực tế của Danh Sách Khám Bệnh
        #     admin_id=1
        # )
        #
        # db.session.add_all([quanly1, quanly2])
        # db.session.commit()


#########################
# c1 = Category(name="Iphone")
# c2 = Category(name="tablet")
#
# db.session.add(c1)
# db.session.add(c2)
# db.session.commit()
# # ########################
#     p1 = Product(name="IPhone15 Pro Max", price=10000000, Category_ID=2, image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
#     p2 = Product(name="IPhone12 Pro Max", price=20000000, Category_ID=2, image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
#     p3 = Product(name="IPhone13 Pro Max", price=30000000, Category_ID=2,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
#     p4 = Product(name="IPhone16 Pro Max", price=40000000, Category_ID=1,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
#     p5 = Product(name="IPhone19 Pro Max", price=90000000, Category_ID=1,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
#     p6 = Product(name="Samsung", price=10000000, Category_ID=2, image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
#     p7 = Product(name="Oppo Pro Max", price=20000000, Category_ID=2, image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
#     p8 = Product(name="realme Pro Max", price=30000000, Category_ID=2,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
#     p9 = Product(name="Oppo 2", price=40000000, Category_ID=1,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
#     p10 = Product(name="Samsung2 Pro Max", price=90000000, Category_ID=1,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
#     db.session.add_all([p1, p2, p3, p4, p5,p6, p7, p8, p9, p10])
#     db.session.commit()
# # #####
