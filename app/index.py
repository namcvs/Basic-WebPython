import math

from flask import render_template, request, redirect, session, jsonify, flash, url_for
import dao, utils
from app import app, login, db
from flask_login import login_user, logout_user
from app.models import NhanVien, UserRoleEnum, BenhNhan, PhieuKhamBenh, Thuoc,DonVi, User, BacSi, HuongDanSuDung,HoaDonThanhToan
from datetime import datetime
from app.admin import current_user
from sqlalchemy import func
from app.view.bacsi import bacsi_lapphieukhambenh

#VNPAY

##


@app.route("/")
def index():
    kw = request.args.get('kw')
    page = request.args.get('page')
    cates = dao.load_categories()
    products = dao.load_products(kw=kw, page=page)
    nhanviens = dao.load_nhanviens(kw=kw, page=page)

    image_data = [
        {'url': 'https://hoanmy.com/wp-content/uploads/2023/12/dai-thao-duong.png',
         'title': 'Những biến chứng nguy hiểm của đái tháo đường và cách phòng ngừa',
         'content': 'Thời gian gần đây, tỷ lệ người bệnh đái tháo đường đang gia tăng khá cao. Theo số liệu từ Hiệp hội Đái tháo đường Thế giới (International Diabetes Federation – IDF), vào năm 2019, thế giới có khoảng 463 triệu người mắc bệnh đái tháo đường. Trong số đó, ước tính hơn 4 triệu […]'},
        {'url': 'https://hoanmy.com/wp-content/uploads/2023/12/suy-gian-tinh-mach-1706-x-1080-px.png',
         'title': 'Cách phòng ngừa, điều trị suy giãn tĩnh mạch để tránh biến chứng về sau',
         'content': 'Suy giãn tĩnh mạch là căn bệnh phổ biến hiện nay, ảnh hưởng tới chất lượng cuộc sống người bệnh. Nếu không được điều trị đúng cách, bệnh có thể gây nên nhiều biến chứng nguy hiểm. Hãy cùng bệnh viện Hoàn Mỹ Sài Gòn tìm hiểu về cách phòng ngừa và điều trị suy […]'},
        # Thêm các phần tử khác nếu cần
        {'url': 'https://hoanmy.com/wp-content/uploads/2023/11/AdobeStock_455652091-scaled.jpeg',
         'title': 'Điều trị ung thư dạ dày ở đâu tốt?',
         'content': 'Theo số liệu từ Globocan 2020, ung thư dạ dày thuộc nhóm có tỷ lệ tử vong cao thứ 3 tại Việt Nam, và ngày nay loại ung thư này đang có xu hướng trẻ hóa. Chính vì thế, việc nắm được các dấu hiệu của bệnh ung thư dạ dày và tầm soát sức […]'},
        {'url': 'https://hoanmy.com/wp-content/uploads/2023/10/BCSCHU1-1.jpg',
         'title': 'Hạ đường huyết có nguy hiểm không? Nguyên nhân và cách xử trí',
         'content': 'Hạ đường huyết là tình trạng dễ gặp ở người bệnh đái tháo đường hoặc người ăn uống không khoa học. Đây là dấu hiệu cảnh báo một số vấn đề nghiêm trọng của cơ thể, cần phát hiện kịp thời và có biện pháp xử lý nhanh để tránh biến chứng nguy hiểm. Hạ […]'},
    ]
    total = dao.count_product()

    return render_template("index.html",
                           products=products, nhanviens=nhanviens,
                           image_data=image_data,
                           pages=math.ceil(total / app.config['PAGE_SIZE']))
    # role=current_user.user_role if current_user.is_authenticated else None, )


# -------------------------------Bác Sĩ--------------------------
#
# --------------------------------DAT LICH KHAM------------------------------
@app.route("/datlichkham", methods=['post', 'get'])
def add_benh_nhan():
    err_msg = ""
    success_message = ""

    if request.method == 'POST':
        hoTen = request.form.get('hoTen')
        ngaySinh = request.form.get('ngaySinh')
        maCCCD = request.form.get('maCCCD')
        diaChi = request.form.get('diaChi')
        email = request.form.get('email')
        soDienThoai = request.form.get('soDienThoai')
        tienSuBenh = request.form.get('tienSuBenh')
        sex = request.form.get('sex')

        if not all([hoTen, ngaySinh, maCCCD, diaChi, email, soDienThoai, tienSuBenh, sex]):
            err_msg = "Please fill in all required fields."
            return render_template("yta.html", err_msg=err_msg)

        try:
            isTrungCCCD = dao.save_benhnhan_data_to_session(hoTen=hoTen, ngaySinh=ngaySinh, maCCCD=maCCCD,
                                                            diaChi=diaChi, email=email,
                                                            soDienThoai=soDienThoai, tienSuBenh=tienSuBenh, sex=sex)
            if isTrungCCCD:
                dao.confirm_benhnhan_and_insert_to_database()
                success_message = "BenhNhan added successfully!"
                err_msg = ""
            else:
                success_message = ""
                err_msg = "Mã CCCD Trùng rồi"
                return render_template("BenhNhan.html", err_msg=err_msg, success_message=success_message)
        except Exception as e:
            print(f"An error occurred: {e}")
            success_message = ""
            err_msg = "Hệ thống đang gặp lỗi!"
        return render_template("BenhNhan.html", err_msg=err_msg, success_message=success_message)

    return render_template("BenhNhan.html", err_msg=err_msg, success_message=success_message)


@app.route('/thanhtoan', methods=['get'])
def thanhtoan():

    maPK = request.args.get('maPK')
    if maPK:
        phieukhambenh = dao.get_maphieukham_by_id(maPK)
    else:
        phieukhambenh = dao.get_maphieukham_by_id(1)
    benhnhan= BenhNhan.query.get(phieukhambenh.maBN)
    bacsi=BacSi.query.get(phieukhambenh.bacsi_ID)
    hoadon=HoaDonThanhToan.query.get(phieukhambenh.maPhieuKham)
    # huongdansudung = HuongDanSuDung.query.get(phieukhambenh.maPhieuKham)

    # thuocs = db.session.query(Thuoc).join(HuongDanSuDung, Thuoc.maThuoc == HuongDanSuDung.maThuoc_id) \
    #     .filter(HuongDanSuDung.maPhieuKham_id == phieukhambenh.maPhieuKham).all()

    lieuDung_total = (
            db.session.query(func.sum(HuongDanSuDung.lieuDung))
            .filter(HuongDanSuDung.maPhieuKham_id == phieukhambenh.maPhieuKham)
            .scalar() or 0  # Nếu không có dữ liệu, trả về 0
    )
    # Tính tổng tiền khám
    tien_kham = db.session.query(func.sum(HoaDonThanhToan.tienKham)) \
                    .filter(HoaDonThanhToan.maPhieuKham == phieukhambenh.maPhieuKham).scalar() or 0

    # Tính tổng tiền thuốc
    tien_thuoc = db.session.query(func.sum(Thuoc.giaTien * HuongDanSuDung.lieuDung)) \
                     .join(HuongDanSuDung, Thuoc.maThuoc == HuongDanSuDung.maThuoc_id) \
                     .filter(HuongDanSuDung.maPhieuKham_id == phieukhambenh.maPhieuKham).scalar() or 0

    thuocs = db.session.query(Thuoc, DonVi).join(DonVi, Thuoc.maDV_id == DonVi.maDV) \
        .join(HuongDanSuDung, Thuoc.maThuoc == HuongDanSuDung.maThuoc_id) \
        .filter(HuongDanSuDung.maPhieuKham_id == phieukhambenh.maPhieuKham).all()

    thuoc_va_lieu_dung = db.session.query(Thuoc, HuongDanSuDung) \
        .join(HuongDanSuDung, Thuoc.maThuoc == HuongDanSuDung.maThuoc_id) \
        .filter(HuongDanSuDung.maPhieuKham_id == phieukhambenh.maPhieuKham) \
        .all()

    for thuoc, donvi in thuocs:
        print(f"Tên thuốc:{thuoc.maThuoc} ,{thuoc.tenThuoc}, Đơn vị: {donvi.tenDV}")
    for thuoc, huong_dan in thuoc_va_lieu_dung:
        print(f"Tên thuốc:{thuoc.maThuoc} ,{thuoc.tenThuoc}, Liều dùng: {huong_dan.lieuDung}, Cách dùng: {huong_dan.cachDung}")



    # for thuoc in thuocs:
    #     print(thuoc.tenThuoc,thuoc.maThuoc)
    return render_template("thungan.html",phieukhambenh=phieukhambenh,benhnhan=benhnhan,
                           bacsi=bacsi,thuocs=thuocs,lieuDung_total=lieuDung_total,
                           tien_thuoc=tien_thuoc,tien_kham=tien_kham,
                           thuoc_va_lieu_dung=thuoc_va_lieu_dung,
                           hoadon=hoadon)


# --------------------------------DANG KI TRUC TIEP------------------------------
@app.route('/dangkikhamtructiep', methods=['post', 'get'])
def dangkitructiep():
    err_msg = ""
    success_message = ""

    if request.method == 'POST':
        hoTen = request.form.get('hoTen')
        ngaySinh = request.form.get('ngaySinh')
        maCCCD = request.form.get('maCCCD')
        diaChi = request.form.get('diaChi')
        email = request.form.get('email')
        soDienThoai = request.form.get('soDienThoai')
        tienSuBenh = request.form.get('tienSuBenh')
        sex = request.form.get('sex')

        if not all([hoTen, ngaySinh, maCCCD, diaChi, email, soDienThoai, tienSuBenh, sex]):
            err_msg = "Please fill in all required fields."
            return render_template("yta.html", err_msg=err_msg)

        try:
            isTrungCCCD = dao.save_benhnhan_data_to_session(hoTen=hoTen, ngaySinh=ngaySinh, maCCCD=maCCCD,
                                                            diaChi=diaChi, email=email,
                                                            soDienThoai=soDienThoai, tienSuBenh=tienSuBenh, sex=sex)
            if isTrungCCCD:
                dao.confirm_benhnhan_and_insert_to_database()
                success_message = "BenhNhan added successfully!"
                err_msg = ""
            else:
                success_message = ""
                err_msg = "Mã CCCD Trùng rồi"
                return render_template("yta.html", err_msg=err_msg, success_message=success_message)
        except Exception as e:
            print(f"An error occurred: {e}")
            success_message = ""
            err_msg = "Hệ thống đang gặp lỗi!"
        return render_template("yta.html", err_msg=err_msg, success_message=success_message)

    return render_template("yta.html", err_msg=err_msg, success_message=success_message)


##################################################

# --------------------------Bác Sĩ---------------------------------
@app.route('/lapphieukham', methods=['post', 'get'])
def lapphieukham():
    err_msg = ""
    success_message = ""

    thuocs = dao.load_thuocs()
    if not current_user.is_authenticated:
        # Redirect to the login page or handle unauthorized access
        return redirect('/login')  # Adjust the URL accordingly


    query = (
        db.session.query(User, NhanVien)
        .join(NhanVien, User.id == NhanVien.user_id)
        .join(BacSi, BacSi.maNV == NhanVien.maNV)
        .filter(User.id == current_user.id)
        .first()
    )
    if query:
        user_instance, nhanvien_instance = query
        maNV_value = nhanvien_instance.maNV
        print(user_instance)
        print(nhanvien_instance.email)
        print(maNV_value)

    if request.method == "POST":
        maCCCD = request.form.get('maCCCD')
        patient = BenhNhan.query.filter_by(maCCCD=maCCCD).first()
        # Check if the current user is logged in and is an instance of User
        # Perform a join to get the maNV attribute

        if patient:
            ###
            trieuChung = request.form.get('trieuChung')
            duDoanBenh = request.form.get('duDoanBenh')
            bacsi_ID = maNV_value
            maBN=patient.maBN
            phieu_kham = PhieuKhamBenh(trieuChung=trieuChung, duDoanBenh=duDoanBenh, bacsi_ID=bacsi_ID,maBN=maBN)
            db.session.add(phieu_kham)
            db.session.commit()
            ####
            maThuoc_id = request.form.get('maThuoc_id')
            maPhieuKham_id = phieu_kham.maPhieuKham
            lieuDung = request.form.get('lieuDung')
            cachDung = ""

            huongdansudung = HuongDanSuDung(maThuoc_id=maThuoc_id, maPhieuKham_id=maPhieuKham_id, lieuDung=lieuDung,
                                            cachDung=cachDung)
            db.session.add(huongdansudung)
            db.session.commit()


        return render_template("bacsi.html", thuocs=thuocs)
    return render_template("bacsi.html", thuocs=thuocs)


# @app.route('/api/lapphieukham', methods=['post'])
# def add_thuoc_to_list():
#     thuocs = session.get('thuocs')
#     if thuocs is None:
#         thuocs = {}
#     data = request.json()
#     maThuoc=str(data.get("maThuoc"))
#
#     if maThuoc in thuocs:
#         thuocs[maThuoc]['soLuong'] = thuocs[maThuoc]['soLuong'] + 1
#     else:
#         thuocs[maThuoc] = {
#             "maThuoc": maThuoc,
#             "tenThuoc": data.get("tenThuoc"),
#             "giaTien": data.get("giaTien"),
#             "quantity": data.get("quantity"),
#         }
#
#     session['thuocs'] = thuocs
#     return jsonify({
#         'tienKham': 100,
#         "tongTien": 100
#     })


@app.route('/aboutus')
def aboutus():
    return render_template("about_us.html")


@app.route('/doingu')
def doingu():
    return render_template("client_doingu.html")


@app.route("/nhanvien/<id>")
def details(id):
    nhanvien = NhanVien.query.get(id)
    return render_template('details.html', nhanvien=nhanvien, datetime=datetime)


@app.route('/login', methods=['post', 'get'])
def login_user_process():
    isCorrect = True;
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
        else:
            isCorrect = False;
            return render_template('login.html', isCorrect=isCorrect)
        next = request.args.get('next')
        return redirect('/' if next is None else next)
    return render_template('login.html', isCorrect=isCorrect)


@app.route('/logout')
def logout_user_process():
    logout_user()
    return redirect("/login")


@app.route('/register', methods=['post', 'get'])
def register_user():
    err_msg = ""
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password,
                             avatar=request.files.get('avatar'))
            except:
                err_msg = 'he thong dang bi loi!!!'
            else:
                return redirect('/login')
            # avatar là lấy từ trường name trong register.html
            # request.files['avatar']
        else:
            err_msg = "Mật khẩu ko khớp!!!!!"

    return render_template('register.html', err_msg=err_msg)


@app.route("/admin/login", methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


#-------------------------------------------
@app.route('/api/cart', methods=['post'])
def add_cart():
    cart = session.get('cart')
    if cart is None:
        cart = {}
    data = request.json
    id = str(data.get("id"))

    if id in cart:  # san pham da co trong gio
        cart[id]["quantity"] = cart[id]["quantity"]+1
    else:  # san pham chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }
    session['cart'] = cart

    return jsonify(utils.count_cart(cart))



@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        quantity = request.json.get('quantity')
        cart[product_id]['quantity'] = int(quantity)

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/pay', methods=['post'])
def pay():
    try:
        dao.add_receipt(session.get('cart'))
    except:
        return jsonify({'status': 500, 'err_msg': 'he thong dang co loi'})
    else:
        del session['cart']
        return jsonify({'status': 200})

#-------------------------------------------
@app.route('/cart')
def cart_list():
    return render_template('cart.html')


@app.route("/testhtml")
def index1():
    return render_template("testhtml.html")

# ---------------------------------------------------------------------

@app.route('/VNPAY')


# ---------------------------------------------------------------------
@app.context_processor  # trang nao cung se co du lieu nay`
def common_resp():
    role = current_user.user_role if current_user.is_authenticated else None
    return {
        'caregories': dao.load_categories(),
        'cart': utils.count_cart(session.get('cart')),
        'UserRoleEnum': UserRoleEnum,
        'role': role,
        'benhnhans': dao.load_benhnhans(),
        'bacsis': dao.load_bacsis()
        # 'numberOfVicTimInDay':
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin

    bacsi_lapphieukhambenh

    app.run(debug=True)
