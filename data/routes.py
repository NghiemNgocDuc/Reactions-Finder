

from datetime import date
from flask import render_template, request
from flask_login import current_user, login_required
from flask_security import roles_accepted
from wtforms import StringField
from apps.pu_hh import blueprint
from apps import db
from apps.pu_hh.dataTransferobjs import ChatThamGiaDTO, LichSuTimKiemCoKqDTO, LichSuTimKiemKhongCoKqDTO, PhanUngQuanTamDTO
from apps.pu_hh.forms import ChitietPhanungForm, LichSuTimKiemForm, PhanUngQuanTamForm, TaoCoSoDuLieuAdminForm, TimkiemPuHhForm, LichSuTimKiemKetQuaKhongTonTaiForm, LichSuTimKiemKetQuaTonTaiForm
from apps.pu_hh.models import ChatThamGiaPhanUng, ChiTietKetQua, DuLieuQuanTam, LichSuTimKiemKetQuaKhongTonTai, LichSuTimKiemKetQuaTonTai, PhanUngHoaHoc



@blueprint.route('/tim_kiem_pu_hh', methods=['GET', 'POST'])
@login_required
def tim_kiem_pu_hh():
    tim_kiem_form = TimkiemPuHhForm(request.form)
    if 'tim_kiem' in request.form:
    
        # lay thong tin tra cuu tu man hinh va tim kiem trong bang chat tham gia phan ung
        timkiemStr = request.form['chat_tg']     

        #tach cac chat trong noi dung tim kiem        
        ketquaStrLst = timkiemStr.split(',')
        i = 0
        for x in ketquaStrLst:
            ketquaStrLst[i] = x.strip()
            i = i +1
        print(ketquaStrLst)

        #tao chuoi tim kiem chuan

        timkiemStr  = "%".join(ketquaStrLst)
        timkiemStr = "%{}%".format(timkiemStr)
        print(timkiemStr)


        chatThamGiaPhanUngLst = ChatThamGiaPhanUng.query.filter(ChatThamGiaPhanUng.chat_tg.like(timkiemStr)).all()
         #liet ke tat ca cac ket qua tim kiem duoc tu co so du lieu o day, dung vong for va sau do tao thanh 1 list object de chuan bi dua len man hinh - begin
        chatThamGiaDTOArr = []
        
        for result in chatThamGiaPhanUngLst:
            # kiem tra neu pu_id chua co trong chatThamGiaDTOArr thi tao moi
            filter_pu_id = filter (lambda ctg: ctg.pu_id == result.pu_id, chatThamGiaDTOArr)
            if not any(filter_pu_id):
                chatThamGiaDTOArr.append(ChatThamGiaDTO(result.dv_id, result.chat_tg, result.pu_id))

        phanUngHoahocDTOArr = []
        for result in chatThamGiaDTOArr:
            # Tra cuu du lieu phan ung tu csdl 
            phanungHoahoc = PhanUngHoaHoc.query.filter_by(pu_id=result.pu_id).first()
            if phanungHoahoc:
                phanUngHoahocDTOArr.append(phanungHoahoc)

        #end             
       
        if phanUngHoahocDTOArr:
            tim_kiem_form.phanUngHoahocArr = phanUngHoahocDTOArr

            # luu vao bang lich su tim kiem co ket qua
            userIdStr = current_user.get_id()
            lichSuTimKiemKetQuaTonTai = LichSuTimKiemKetQuaTonTai(None, userIdStr, request.form['chat_tg'], phanUngHoahocDTOArr[0].pu_id, date.today())
            db.session.add(lichSuTimKiemKetQuaTonTai)
            db.session.commit()           
        else:
            userIdStr = current_user.get_id()
            lichSuTimKiemKetQuaKhongTonTai = LichSuTimKiemKetQuaKhongTonTai(None, userIdStr, request.form['chat_tg'], date.today())
            db.session.add(lichSuTimKiemKetQuaKhongTonTai)
            db.session.commit() 
        
    return render_template('pu_hh/tim_kiem.html',msg='Tìm kiếm thành công',
                               form=tim_kiem_form)
  
# Errors
@blueprint.route('/lich_su_tim_kiem', methods=['GET', 'POST'])
@login_required
def lich_su_tim_kiem():
    tim_kiem_form = LichSuTimKiemForm(request.form)
    return render_template('pu_hh/lich_su_tim_kiem.html',msg='Ket qua tim kiem',
                               form=tim_kiem_form)

@blueprint.route('/danh_sach_phan_ung_quan_tam', methods=['GET', 'POST'])
@login_required
def danh_sach_phan_ung_quan_tam():
    tim_kiem_form = LichSuTimKiemForm(request.form)
    return render_template('pu_hh/danh_sach_phan_ung_quan_tam.html',msg='Kết quả quan tâm',
                               form=tim_kiem_form)


@blueprint.route('/lich_su_tim_kiem_ket_qua_khong_ton_tai', methods=['GET', 'POST'])
@login_required
def lich_su_tim_kiem_ket_qua_khong_ton_tai():
    tim_kiem_form = LichSuTimKiemKetQuaKhongTonTaiForm(request.form)
    userIdStr=current_user.get_id()

    lichSuTimkiemKhongCoKqLst = LichSuTimKiemKetQuaKhongTonTai.query.filter_by(user_id=userIdStr).all()
     #liet ke tat ca cac ket qua tim kiem duoc tu co so du lieu o day, dung vong for va sau do tao thanh 1 list object de chuan bi dua len man hinh - begin
    print(lichSuTimkiemKhongCoKqLst)
    lichSuTimkiemKhongCoKqDTOArr = []
        
    for result in lichSuTimkiemKhongCoKqLst:
            # kiem tra neu pu_id chua co trong chatThamGiaDTOArr thi tao moi
            filter_pu_id = filter (lambda ctg: ctg.tt_tra_cuu == result.tt_tra_cuu, lichSuTimkiemKhongCoKqDTOArr)
            if not any(filter_pu_id):
                lichSuTimkiemKhongCoKqDTOArr.append(LichSuTimKiemKhongCoKqDTO(result.tc_id, result.tt_tra_cuu, result.thoi_gian_tra_cuu))

    

    tim_kiem_form.lichSuTimKiemKetQuaKhongTonTai = lichSuTimkiemKhongCoKqDTOArr

    return render_template('pu_hh/lich_su_tim_kiem_ket_qua_khong_ton_tai.html',msg='Kết quả phản ứng không tồn tại',
                               form=tim_kiem_form)


    


@blueprint.route('/lich_su_tim_kiem_ket_qua_ton_tai', methods=['GET', 'POST'])
@login_required
def lich_su_tim_kiem_ket_qua_ton_tai():
    tim_kiem_form = LichSuTimKiemKetQuaTonTaiForm(request.form)
    userIdStr=current_user.get_id()
    lichSuTimkiemCoKqLst = LichSuTimKiemKetQuaTonTai.query.filter_by(user_id=userIdStr).all()
     #liet ke tat ca cac ket qua tim kiem duoc tu co so du lieu o day, dung vong for va sau do tao thanh 1 list object de chuan bi dua len man hinh - begin
    print(lichSuTimkiemCoKqLst)
    lichSuTimkiemCoKqDTOArr = []
        
    for result in lichSuTimkiemCoKqLst:
            # kiem tra neu pu_id chua co trong chatThamGiaDTOArr thi tao moi
            filter_pu_id = filter (lambda ctg: ctg.id_kq_pu == result.id_kq_pu, lichSuTimkiemCoKqDTOArr)
            if not any(filter_pu_id):
                lichSuTimkiemCoKqDTOArr.append(LichSuTimKiemCoKqDTO(result.ls_id, result.tt_tra_cuu, result.id_kq_pu, '', result.thoi_gian_tra_cuu))

    
    for result in lichSuTimkiemCoKqDTOArr:
        # Tra cuu du lieu phan ung tu csdl 
            phanungHoahoc = PhanUngHoaHoc.query.filter_by(pu_id=result.id_kq_pu).first()
            if phanungHoahoc:
                result.ct_kq_pu=phanungHoahoc.ket_qua_pu

    tim_kiem_form.lichSuTimKiemKetQuaTonTai = lichSuTimkiemCoKqDTOArr
    return render_template('pu_hh/lich_su_tim_kiem_ket_qua_ton_tai.html',msg='Kết quả phản ứng tồn tại',
                               form=tim_kiem_form)

@blueprint.route('/chi_tiet_pu_hh', methods=['GET', 'POST'])
@login_required
def chi_tiet_pu_hh():
    chitietPhanungForm = ChitietPhanungForm(request.form)
    pu_id = request.args['pu_id']
# lay thong tin tu bang Phan ung hoa hoc
    phanungHoahoc = PhanUngHoaHoc.query.filter_by(pu_id=pu_id).first()
    chitietPhanungForm.ket_qua_pu=phanungHoahoc.chat_nhap_vao + "-->" +phanungHoahoc.ket_qua_pu


    #lay thong tin chi tiet cua ket qua phan ung va hinh anh
    chitietPuhhModel = ChiTietKetQua.query.filter_by(pu_id=pu_id).first()

    chitietPhanungForm.pu_id.data = pu_id
    hinh_anh_id= chitietPuhhModel.hinh_anh

    #duong dan youtobe co videId sau dau =, vi vay can tach de lay gia tri videoId cho viec hien thi embedded tren trang cua minh
    if hinh_anh_id.find("=") >= 0:
        HinhAnhStrLst = hinh_anh_id.split('=')
        hinh_anh_id = HinhAnhStrLst[1].strip()
   
    chitietPhanungForm.hinh_anh = hinh_anh_id
    return render_template('pu_hh/chi_tiet_pu_hh.html',msg='',
                               form=chitietPhanungForm)






@blueprint.route('/tao_co_so_du_lieu_admin', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'Normal')
def tao_co_so_du_lieu_admin():
    tao_csdl_admin = TaoCoSoDuLieuAdminForm(request.form)
    msgStr = ""
    actionStr = request.args.get('action')

    #thuc hien hien thi man hinh sua phan ung hoa hoc
    if actionStr=='sua_pu':
        msgStr = "Thức hiện sửa dữ liệu phản ứng"
        puIdStr = request.args.get('pu_id')
        phanungHoahoc = PhanUngHoaHoc.query.filter_by(pu_id=puIdStr).first()

        if phanungHoahoc:
           tao_csdl_admin.ct_puhh.data = phanungHoahoc.chat_nhap_vao + '=' + phanungHoahoc.ket_qua_pu
           tao_csdl_admin.update_pu_id.data = phanungHoahoc.pu_id

        
        chitietPuhhModel = ChiTietKetQua.query.filter_by(pu_id=puIdStr).first()
        if chitietPuhhModel:
            tao_csdl_admin.dkpu.data = chitietPuhhModel.dieu_kien
            tao_csdl_admin.dd_hinhanh.data = chitietPuhhModel.hinh_anh
       

    elif 'Luu' in request.form:
    
        # lay thong tin tra cuu tu man hinh va tim kiem trong bang chat tham gia phan ung
        ctpuhhStr = request.form['ct_puhh']     
        dkpuStr = request.form['dkpu'] 
        ddhinhanhStr = request.form['dd_hinhanh'] 
        updatePuId = request.form['update_pu_id'] 
        #tach cac chat trong noi dung tim kiem    HCl+NaOH =  NaCl + H2O can cu dau =hoac ->
        chatTg= None
        chatTgcsdl = None
        kqPu = None
        if ctpuhhStr.find("=") >= 0:
            ketquaStrLst = ctpuhhStr.split('=')
            chatTg = ketquaStrLst[0].strip()  
            chatTgcsdl = chatTg.replace('+',',')      
            kqPu = ketquaStrLst[1].strip() 
            print(ketquaStrLst)
        elif ctpuhhStr.find("->") >= 0:
            ketquaStrLst = ctpuhhStr.split('->')
            chatTg = ketquaStrLst[0].strip()   
            chatTgcsdl = chatTg.replace('+',',')        
            kqPu = ketquaStrLst[1].strip() 
            print(ketquaStrLst)
        elif ctpuhhStr.find("→") >= 0:
            ketquaStrLst = ctpuhhStr.split('→')
            chatTg = ketquaStrLst[0].strip()   
            chatTgcsdl = chatTg.replace('+',',')        
            kqPu = ketquaStrLst[1].strip() 
            print(ketquaStrLst)
        
        #kiem tra neu phan ung hoa hoc da co trong csdl thi khong thuc hien luu thong tin
        phanungHoahoc = PhanUngHoaHoc.query.filter_by(ket_qua_pu=kqPu).first()
        
        if phanungHoahoc == None:
            # Tao du lieu trong bang phan_ung_hoa_hoc
            puHHModel = PhanUngHoaHoc(chatTg, kqPu)
            db.session.add(puHHModel)
            db.session.commit()
            db.session.refresh(puHHModel)

            # tao du lieu bang chat_tham_gia
            pu_id = puHHModel.pu_id
            chatTgModel = ChatThamGiaPhanUng(chatTgcsdl, None, pu_id)
            db.session.add(chatTgModel)
            db.session.commit()

            # tao du lieu bang chi tiet ket qua pha ung
            pu_id = puHHModel.pu_id
            chiTietketquaModel = ChiTietKetQua(pu_id, ddhinhanhStr, dkpuStr)
            db.session.add(chiTietketquaModel)
            db.session.commit()
            msgStr = "Lưu thông tinh phản ứng hóa học thành công"
        elif updatePuId != None and updatePuId != "":
            #cap nhat phan ung da co trong csdl
            puHHModel = PhanUngHoaHoc.query.filter_by(pu_id=updatePuId).first()
            puHHModel.chat_nhap_vao = chatTg
            puHHModel.ket_qua_pu = kqPu
            

            chiTietketquaModel = ChiTietKetQua.query.filter_by(pu_id=updatePuId).first()
            chiTietketquaModel.hinh_anh = ddhinhanhStr
            chiTietketquaModel.dieu_kien = dkpuStr

            chatTgModel = ChatThamGiaPhanUng.query.filter_by(pu_id=updatePuId).first()
            chatTgModel.chat_tg = chatTgcsdl

            db.session.commit()
            msgStr = "Cập nhật thông tin phản ứng " + chatTg + " thành công!"

        else:
            msgStr = "Phản ứng đã tồn tại, không lưu cơ sở dữ liệu nhiều lần."

    return render_template('pu_hh/tao_csdl_admin.html',msg=msgStr,
                               form=tao_csdl_admin)

@blueprint.route('/tim_kiem_admin', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin')
def tim_kiem_admin():
    tim_kiem_form = TimkiemPuHhForm(request.form)
    if 'tim_kiem' in request.form:
    
        # lay thong tin tra cuu tu man hinh va tim kiem trong bang chat tham gia phan ung
        timkiemStr = request.form['chat_tg']     

        #tach cac chat trong noi dung tim kiem        
        ketquaStrLst = timkiemStr.split(',')
        i = 0
        for x in ketquaStrLst:
            ketquaStrLst[i] = x.strip()
            i = i +1
        print(ketquaStrLst)

        #tao chuoi tim kiem chuan

        timkiemStr  = "%".join(ketquaStrLst)
        timkiemStr = "%{}%".format(timkiemStr)
        print(timkiemStr)


        chatThamGiaPhanUngLst = ChatThamGiaPhanUng.query.filter(ChatThamGiaPhanUng.chat_tg.like(timkiemStr)).all()
         #liet ke tat ca cac ket qua tim kiem duoc tu co so du lieu o day, dung vong for va sau do tao thanh 1 list object de chuan bi dua len man hinh - begin
        chatThamGiaDTOArr = []
        
        for result in chatThamGiaPhanUngLst:
            # kiem tra neu pu_id chua co trong chatThamGiaDTOArr thi tao moi
            filter_pu_id = filter (lambda ctg: ctg.pu_id == result.pu_id, chatThamGiaDTOArr)
            if not any(filter_pu_id):
                chatThamGiaDTOArr.append(ChatThamGiaDTO(result.dv_id, result.chat_tg, result.pu_id))

        phanUngHoahocDTOArr = []
        for result in chatThamGiaDTOArr:
            # Tra cuu du lieu phan ung tu csdl 
            phanungHoahoc = PhanUngHoaHoc.query.filter_by(pu_id=result.pu_id).first()
            if phanungHoahoc:
                phanUngHoahocDTOArr.append(phanungHoahoc)

        #end             
       
        if phanUngHoahocDTOArr:
            tim_kiem_form.phanUngHoahocArr = phanUngHoahocDTOArr
        
    return render_template('pu_hh/tim_kiem_admin.html',msg='Tìm kiếm thành công',
                               form=tim_kiem_form)
  
@blueprint.route('/xoa_phan_ung', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin')
def xoa_phan_ung():
    tim_kiem_form = TimkiemPuHhForm(request.form)
    # lay thong tin tra cuu tu man hinh va tim kiem trong bang chat tham gia phan ung
    timkiemStr = request.args.get('pu_id')
    #request.form['pu_id'] 
    # thu thap pu_id roi xoa o cac bang chi_tiet_kq_phan_ung, chat_tg_phan_ung, phan_ung_hoa_hoc
    ChatThamGiaPhanUng.query.filter(ChatThamGiaPhanUng.pu_id == timkiemStr).delete() 
    PhanUngHoaHoc.query.filter(PhanUngHoaHoc.pu_id == timkiemStr).delete() 
    ChiTietKetQua.query.filter(ChiTietKetQua.pu_id == timkiemStr).delete()
  
    db.session.commit()

    return render_template('pu_hh/tim_kiem_admin.html',msg='',
                               form=tim_kiem_form)


@blueprint.route('/dulieu_quan_tam', methods=['GET', 'POST'])
def dulieu_quan_tam():
    chitietPhanungForm = ChitietPhanungForm(request.form)
    
    if 'quantam' in request.form:
        pu_id_str = chitietPhanungForm.pu_id.data
        #luu thong tin quan tam
        userIdStr = current_user.get_id()
        dulieuQuanTam = DuLieuQuanTam(userIdStr, pu_id_str)

        #kiem tra neu du lieu quan tam da ton tai thi khong luu 
        dulieuQuanTam2 = DuLieuQuanTam.query.filter_by(pu_id=pu_id_str).first()

        msgStr = ''

        if not dulieuQuanTam2:

            try:
                db.session.add(dulieuQuanTam)
                db.session.commit()        
                msgStr = 'Hoàn thành lưu dữ liệu quan tâm'            
            except Exception as expt:
                print (expt)
                return render_template('home/page-500.html'), 500
        else:
            msgStr = 'Dữ liệu quan tam đã tồn tại'

# lay thong tin tu bang Phan ung hoa hoc
    phanungHoahoc = PhanUngHoaHoc.query.filter_by(pu_id=pu_id_str).first()
    chitietPhanungForm.ket_qua_pu=phanungHoahoc.chat_nhap_vao + "-->" +phanungHoahoc.ket_qua_pu


    #lay thong tin chi tiet cua ket qua phan ung va hinh anh
    chitietPuhhModel = ChiTietKetQua.query.filter_by(pu_id=pu_id_str).first()

    chitietPhanungForm.pu_id.data = pu_id_str
    hinh_anh_id= chitietPuhhModel.hinh_anh

    #duong dan youtobe co videId sau dau =, vi vay can tach de lay gia tri videoId cho viec hien thi embedded tren trang cua minh
    if hinh_anh_id.find("=") >= 0:
        HinhAnhStrLst = hinh_anh_id.split('=')
        hinh_anh_id = HinhAnhStrLst[1].strip()
   
    chitietPhanungForm.hinh_anh = hinh_anh_id
    return render_template('pu_hh/chi_tiet_pu_hh.html',msg=msgStr,
                               form=chitietPhanungForm)





@blueprint.route('/danh_sach_quan_tam', methods=['GET', 'POST'])
@login_required
def danh_sach_quan_tam():
    danh_sach_quan_tam_form = PhanUngQuanTamForm(request.form)

    userIdStr = current_user.get_id()

    lichSuTimkiemCoKqLst = DuLieuQuanTam.query.filter_by(user_id=userIdStr).all()
     #liet ke tat ca cac ket qua tim kiem duoc tu co so du lieu o day, dung vong for va sau do tao thanh 1 list object de chuan bi dua len man hinh - begin
    print(lichSuTimkiemCoKqLst)
    lichSuTimkiemCoKqDTOArr = []
        
    for result in lichSuTimkiemCoKqLst:
            lichSuTimkiemCoKqDTOArr.append(PhanUngQuanTamDTO(result.pu_id,'',''))

    
    for result in lichSuTimkiemCoKqDTOArr:
        # Tra cuu du lieu phan ung tu csdl 
            phanungHoahoc = PhanUngHoaHoc.query.filter_by(pu_id=result.pu_id).first()
            if phanungHoahoc:
                result.ct_kq_pu=phanungHoahoc.ket_qua_pu
                result.tt_tra_cuu=phanungHoahoc.chat_nhap_vao

    danh_sach_quan_tam_form.danhSachPhanUngQuanTam = lichSuTimkiemCoKqDTOArr
    return render_template('pu_hh/danh_sach_phan_ung_quan_tam.html',msg='Kết quả phản ứng tồn tại',
                               form=danh_sach_quan_tam_form)