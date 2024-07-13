
from flask_login import UserMixin

from apps import db

class PhanUngHoaHoc(db.Model, UserMixin):

    __tablename__ = 'phan_ung_hoa_hoc'

    pu_id = db.Column(db.Integer, primary_key=True)
    chat_nhap_vao = db.Column(db.String(1000))
    ket_qua_pu = db.Column(db.String(1000))
    pu_trung_gian = db.Column(db.String(1000))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():

            if hasattr(value, '__iter__') and not isinstance(value, str):
                
                value = value[0]
            setattr(self, property, value)

    def __init__(self, chatTg, puHh):
        self.chat_nhap_vao = chatTg
        self.ket_qua_pu = puHh

    def __repr__(self):
        return str(self.ket_qua_pu)


class ChatThamGiaPhanUng(db.Model, UserMixin):

    __tablename__ = 'chat_tg_phan_ung'

    dv_id = db.Column(db.Integer, primary_key=True)
    chat_tg = db.Column(db.String(1000))
    chiso_tg = db.Column(db.Integer)
    pu_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            
            if hasattr(value, '__iter__') and not isinstance(value, str):
                
                value = value[0]
            setattr(self, property, value)

    def __init__(self, chatTg, chisoTg, puId):
        self.chat_tg = chatTg
        self.chiso_tg = chisoTg
        self.pu_id = puId

    def __repr__(self):
        return str(self.chat_tg)
    

    
    


class LichSuTimKiemKetQuaTonTai(db.Model, UserMixin):

    __tablename__ = 'lich_su_tra_cuu'

    ls_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    tt_tra_cuu = db.Column(db.Text)
    id_kq_pu = db.Column(db.Integer)
    thoi_gian_tra_cuu = db.Column(db.Date)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            
            if hasattr(value, '__iter__') and not isinstance(value, str):
                
                value = value[0]
            setattr(self, property, value)

    def __init__(self, id, userId, ttTraCuu, idKq, tgTraCuu):
        self.ls_id = id
        self.user_id = userId
        self.tt_tra_cuu = ttTraCuu
        self.id_kq_pu = idKq       
        self.thoi_gian_tra_cuu = tgTraCuu

    def __repr__(self):
        return str(self.tt_tra_cuu)
  
class LichSuTimKiemKetQuaKhongTonTai(db.Model, UserMixin):

    __tablename__ = 'tra_cuu_chua_co_kq'

    tc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    tt_tra_cuu = db.Column(db.Text)
    thoi_gian_tra_cuu = db.Column(db.Date)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            
            if hasattr(value, '__iter__') and not isinstance(value, str):
                
                value = value[0]
            setattr(self, property, value)

    def __init__(self, id, userId, ttTraCuu, tgTraCuu):
        self.tc_id = id
        self.user_id = userId
        self.tt_tra_cuu = ttTraCuu    
        self.thoi_gian_tra_cuu = tgTraCuu

    def __repr__(self):
        return str(self.tt_tra_cuu)
    



class ChiTietKetQua(db.Model, UserMixin):

    __tablename__ = 'chi_tiet_kq_phan_ung'

    ct_id = db.Column(db.Integer, primary_key=True)
    pu_id = db.Column(db.Integer)
    hinh_anh = db.Column(db.Text)
    dieu_kien= db.Column(db.Text)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():

            if hasattr(value, '__iter__') and not isinstance(value, str):
                
                value = value[0]
            setattr(self, property, value)

    def __init__(self, ctId, puId, HinhAnh, dieuKien):
        self.ct_id = ctId
        self.pu_id = puId
        self.hinh_anh = HinhAnh    
        self.dieu_kien = dieuKien

    def __repr__(self):
        return str(self.ct_id)
    def __init__(self, puId, HinhAnh, dieuKien):
        self.pu_id = puId
        self.Hinh_anh = HinhAnh
        self.dieu_kien = dieuKien


class DuLieuQuanTam(db.Model, UserMixin):

    __tablename__ = 'dulieu_quan_tam'

    qt_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    pu_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            
            if hasattr(value, '__iter__') and not isinstance(value, str):
                
                value = value[0]
            setattr(self, property, value)

    def __init__(self, userId, puId):
        self.user_id = userId
        self.pu_id = puId

    def __repr__(self):
        return str(self.qt_id)