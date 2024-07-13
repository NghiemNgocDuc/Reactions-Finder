


# doi tuong chat tham gia khi tim kiem
class ChatThamGiaDTO:
    id = None
    chat_tg = None
    pu_id = None
    def __init__(self, id, chatTg, puHh):
        self.id = id
        self.chat_tg = chatTg
        self.pu_id = puHh

#doi tuong phan ung hoa hoa
class PhanUngHoaHocDTO:    
    pu_id = None
    chat_nhap_vao = None
    ket_qua_pu = None

    def __init__(self, id, chatTg, puHh):
        self.pu_id = id
        self.chat_nhap_vao = chatTg
        self.ket_qua_pu = puHh

#doi tuong phan ung hoa hoa
class LichSuTimKiemCoKqDTO:    
    ls_id = None    
    tt_tra_cuu = None
    ct_kq_pu = None
    id_kq_pu = None
    thoi_gian_tra_cuu = None

    def __init__(self, id, ttTraCuu, idKq, ctKqPu, tgTraCuu):
        self.ls_id = id
        self.tt_tra_cuu = ttTraCuu
        self.id_kq_pu = idKq
        self.ct_kq_pu = ctKqPu
        self.thoi_gian_tra_cuu = tgTraCuu


class LichSuTimKiemKhongCoKqDTO:    
    tc_id = None    
    tt_tra_cuu = None
    thoi_gian_tra_cuu = None

    def __init__(self, id, ttTraCuu, tgTraCuu):
        self.tc_id = id
        self.tt_tra_cuu = ttTraCuu
        self.thoi_gian_tra_cuu = tgTraCuu


class TaoCoSoDuLieuAdminDTO:
    ct_puhh = None
    dd_hinhanh = None
    dkpu = None
    def __init__(self, ctPuhh, ddHinhanh, dkPu):
        self.ct_puhh = ctPuhh
        self.dd_hinhanh = ddHinhanh
        self.dkpu = dkPu



class PhanUngQuanTamDTO:
    tt_tra_cuu = None
    ct_kq_pu = None
    pu_id = None
    def __init__(self, id, ttTraCuu, ctKqPu):
        self.tt_tra_cuu = ttTraCuu
        self.ct_kq_pu = ctKqPu
        self.pu_id = id
