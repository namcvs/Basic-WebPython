import datetime
import json

from flask_login import current_user
from sqlalchemy.sql.elements import and_
from sqlalchemy.orm import joinedload
from app.models import  BenhNhan,Thuoc,BacSi,DanhSachKhamBenh,LichKhamBenh
from flask import session


from app import db







# def search_patient_information(name, cccd):
#     # Assuming you have access to the current logged-in doctor's ID (bacsi_id)
#     bacsi_id = 1  # Replace with the actual ID of the logged-in doctor
#
#     # Search for the patient based on name and ID card number
#     patient = BenhNhan.query.filter_by(hoTen=name, maCCCD=cccd).first()
#
#     if patient:
#         # Kiểm tra xem bệnh nhân có hồ sơ y tế liên quan không
#         medical_record = LichKhamBenh.query\
#             .join(DanhSachKhamBenh, DanhSachKhamBenh.id == LichKhamBenh.dsKhamBenh_id)\
#             .filter(DanhSachKhamBenh.YTa_ID == bacsi_id, LichKhamBenh.maBN == patient.maBN)\
#             .options(joinedload(LichKhamBenh.bieumau))\
#             .first()
#
#         if medical_record:
#             return patient, medical_record
#         else:
#             return None, None  # Patient has no medical record
#     else:
#         return None, None  # Patient not found

# def get_medicine_unit(medicine_name=None):
#     return db.session.query(MedicineUnitModel.name) \
#         .join(MedicineModel) \
#         .filter(and_(MedicineUnitModel.medicine_unit_id.__eq__(MedicineModel.medicine_unit_id),
#                      MedicineModel.name.__eq__(str(medicine_name).strip()))) \
#         .first()


