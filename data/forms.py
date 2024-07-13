
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField
from wtforms.validators import DataRequired


# login and registration


class TimkiemPuHhForm(FlaskForm):
    chat_tg = StringField('chat_tg',
                         id='chat_tg',
                         validators=[DataRequired()])
    phanUngHoahocArr = []

class LichSuTimKiemForm(FlaskForm):
    lich_su_tim_kiem = StringField('lich_su_tim_kiem',
                         id='lich_su_tim_kiem',
                         validators=[DataRequired()])
    
class LichSuTimKiemKetQuaKhongTonTaiForm(FlaskForm):
    lichSuTimKiemKetQuaKhongTonTai = []
    

class LichSuTimKiemKetQuaTonTaiForm(FlaskForm):
    lichSuTimKiemKetQuaTonTai = []



class ChitietPhanungForm(FlaskForm):       
    ket_qua_pu = None
    hinh_anh = None
    pu_id = HiddenField("pu_id")

class TaoCoSoDuLieuAdminForm(FlaskForm):
    ct_puhh = StringField('ct_puhh',
                         id='ct_puhh',
                         validators=[DataRequired()])
    dd_hinhanh = StringField('dd_hinhanh',
                         id='dd_hinhanh',
                         validators=[DataRequired()])
    dkpu = StringField('dkpu',
                         id='dkpu',
                         validators=[DataRequired()])
    
    update_pu_id = HiddenField('update_pu_id',
                         id='update_pu_id',
                         validators=None)
    


class PhanUngQuanTamForm(FlaskForm):
    phanUngQuanTam = []