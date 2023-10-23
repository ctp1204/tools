import requests, os
import requests, json, time, datetime
class OOP:
    def __init__(self, TDS_token, idtiktok):
        self.TDS_token = TDS_token
        self.idtiktok = idtiktok
        self.totalXu = 0
        self.totalJobs = 0
        self.demNV = 0
        self.xuHienTai = 0
        self.STT = 0
        self.s = requests.Session()
    def layThongTinAcc(self):
        url = 'https://traodoisub.com/api/?fields=profile&access_token={0}'.format(self.TDS_token)
        response = self.s.get(url)
        dataLTT =  json.loads(response.text)
        if('error' in dataLTT):
            print('Token tds die !!!')
            exit()
        else:
            user = dataLTT['data']['user']
            xu = dataLTT['data']['xu']
            xudie = dataLTT['data']['xudie']
            self.xuHienTai += int(xu)
            print(f'[*] => Tên tài khoản: {user}')
            print(f'[*] => Xu hiện tại: {xu}')
            print(f'[*] => Xu bị phạt: {xudie}')
            print('=========================================================')

    def datCauHinh(self):
        url = 'https://traodoisub.com/api/?fields=tiktok_run&id={0}&access_token={1}'.format(self.idtiktok, self.TDS_token)
        response = self.s.get(url)
        dataDCH = json.loads(response.text)
        if('error' in dataDCH):
            print('Kiểm tra lại xem cấu hình tiktok chưa')
            exit()
        else:
            id = dataDCH['data']['id']
            user = dataDCH['data']['uniqueID']
            msg = dataDCH['data']['msg']
            print(f'Cấu hình thành công: {id} | User: {user}')
    def layNhiemVu(self):
        while(True):
            print('Đang lấy jobs, vui lòng chờ !!!', end='\r')
            time.sleep(2)
            url = 'https://traodoisub.com/api/?fields=tiktok_follow&access_token={}'.format(self.TDS_token)
            response = self.s.get(url)
            try:
                data = json.loads(response.text)
                if 'countdown' in data:
                        countdown_value = data['countdown']
                        for i in range(int(countdown_value) + 5, 0, -1):
                            print(f'Thao tác quá nhanh vui lòng chậm lại, đợi {i} giây', end='\r')
                            time.sleep(1)
                        print(" " * 50, end='\r')
                elif 'time_reset' in data:
                    print('Đổi tiktok mới, bị giới hạn nhiệm vụ rồi')
                    exit()
                else:
                    try:
                        print(f"Đã lấy được {len(data['data'])} jobs. Làm jobs nào.", end='\r')
                        time.sleep(2)
                        for item in data['data']:
                            link_value = item['link']
                            id_value = item['id']
                            now = datetime.datetime.now()
                            self.guiNhiemVu(id_value)
                            if (self.STT != 0 and self.STT % timeAntiBlock == 0 and self.demNV == 0):
                                self.nghiChongBlock(chongBlock)
                            else:
                                time.sleep(1)
                            self.demNV += 1
                            self.follow(link_value, now)
                            self.delay(seconds)
                            if self.demNV % countNV == 0:
                                self.nhanXu()

                                self.demNV = 0
                                time.sleep(5)
                                continue
                    except Exception:
                        pass
            except json.JSONDecodeError:
               pass
    def guiNhiemVu(self, id_value):
        url = 'https://traodoisub.com/api/coin/?type=TIKTOK_FOLLOW_CACHE&id={0}&access_token={1}'.format(id_value, self.TDS_token)
        response = self.s.get(url)
        dataGNV = response.json()
    def follow(self, link_value, now):
       os.system(f'termux-open-url {link_value}')
       print(f"[{self.demNV}] | CTP1204_TOOL | {now.strftime('%H:%M:%S')} | FOLLOW")
    def nhanXu(self):

            now = datetime.datetime.now()
            url = 'https://traodoisub.com/api/coin/?type=TIKTOK_FOLLOW&id=TIKTOK_FOLLOW_API&access_token={}'.format(self.TDS_token)
            response = self.s.get(url)
            dataNX = response.json()
            if response.status_code == 200:
                if 'data' in dataNX:
                    xu = dataNX['data']['xu']
                    job_success = dataNX['data']['job_success']
                    xuthem = dataNX['data']['xu_them']
                    msg = dataNX['data']['msg']
                    self.totalXu += xuthem
                    self.totalJobs += job_success

                    self.STT+= 1
                    print('=========================================================')
                    if (job_success == 0):
                        print('Tài khoản của bạn đã bị nhả jobs hoặc bị chặn Follow.')
                        print('Tool sẽ tự động dừng. Bạn vui lòng đổi nick để chạy lại.')
                        print('Chúc bạn một ngày vui và kiếm thật nhiều xu.')
                        exit()
                    else:
                        print(f"[{self.STT}] | JOBS SUCCESS : {job_success} | {msg} | TOTAL JOBS: {self.totalJobs}")
                        print(f"===> JOBS XU: {self.totalXu} XU | TOTAL XU : {xu} XU <===")
                    print('=========================================================')
                else:
                    print("Nhan xu that bai")
            else:
                print(f"Yêu cầu không thành công. Mã trạng thái: {response.status_code}")

    def delay(self, seconds):
        for i in range(seconds, 0, -1):
            print(f'[CTP1204_TOOL] ~> {str(i)} giây', end='\r')
            time.sleep(1)
    def nghiChongBlock(self, chongBlock):
        for i in range(chongBlock, 0, -1):
            print(f'Đang nghỉ chống block, vui lòng đợi sau -> {str(i)} giây', end='\r')
            time.sleep(1)
            print(f'Đã nghỉ chống block xong. Tiếp tục làm jobs.', end='\r')
def save_account_info(TDS_token, idtiktok):
    with open("tds_token.txt", "w") as tds_file:
        tds_file.write(TDS_token)
    with open("idtiktok.txt", "w") as idtiktok_file:
        idtiktok_file.write(idtiktok)

def load_account_info():
    try:
        with open("tds_token.txt", "r") as tds_file:
            TDS_token = tds_file.read()
        with open("idtiktok.txt", "r") as idtiktok_file:
            idtiktok = idtiktok_file.read()
        return TDS_token, idtiktok
    except FileNotFoundError:
        return None, None
TDS_token, idtiktok = load_account_info()

def getInfoAccount():
        s = requests.Session()
        url = 'https://traodoisub.com/api/?fields=profile&access_token={0}'.format(TDS_token)
        response = s.get(url)
        dataLTT =  json.loads(response.text)
        if('error' in dataLTT):
            print('Token tds die. Vui lòng xóa đi file tds_token.txt. Và khởi động lại tools !!!')
            exit()
        else:
            user = dataLTT['data']['user']
        return user

print('=========================================================')
print('= [*] =>             Tên tool: CTP1204_TOOL             =')
print('= [*] =>              Admin: Lê Quốc Cường              =')
print('= [*] =>              Zalo:  0935 53 53 25              =')
print('= [*] =>             Facebook: Cường TânPhú             =')
print('= [*] => Mua/bán Xu TDS liên hệ Admin qua Zalo hoặc FB. =')
print('=========================================================')
print('========> Admin chúc bạn cày thật nhiều xu !!!! <========')
print('=========================================================')

if TDS_token is None or idtiktok is None:
    TDS_token = input('[*] => Nhập token TDS : ')
    idtiktok = input('[*] => Nhập id tiktok cần cấu hình : ')
    save_account_info(TDS_token, idtiktok)
else:
    user = getInfoAccount()
    print(f'[*] => Nhập [1] Giữ tài khoản TDS: ({user}).')
    print(f'[*] => Nhập [2] Đổi Access_Token TDS mới.')
    keep_old_or_new_token_tds = input(f'[*] => Nhập số : ')
    if keep_old_or_new_token_tds.lower() == '2':
        TDS_token = input('[*] => Nhập Access_Token TDS mới: ')

    print(f'[*] => Nhập [1] Giữ tài khoản Tiktok: ({idtiktok}).')
    print(f'[*] => Nhập [2] Đối tài khoản Tiktok mới.')
    keep_or_new_idtiktok = input(f'[*] => Nhập số : ')
    if keep_or_new_idtiktok.lower() == '2':
        idtiktok = input('[*] => Nhập id tiktok mới: ')
    save_account_info(TDS_token, idtiktok)
seconds = int(input('[*] => Nhập delay (s) : '))
countNV = int(input('[*] => Sau bao nhiêu nhiệm vụ thì nhận xu : '))
print('=========================================================')
print('[*] => Nhiệm vụ chống block (lớn hơn 1 nhỏ hơn 10.)')
print('[*] => Khuyến khích trong khoảng từ 2-5 là hợp lý nhất.')
print(f'[*] => Nhập [2] hoàn thành {countNV*2} nv dừng chống block.')
print(f'[*] => Nhập [3] hoàn thành {countNV*3} nv dừng chống block.')
print(f'[*] => Nhập [4] hoàn thành {countNV*4} nv dừng chống block.')
print(f'[*] => Nhập [5] hoàn thành {countNV*5} nv dừng chống block.')
print('=========================================================')
timeAntiBlock = int(input('[*] => Nhập số : '))
chongBlock = int(input('[*] => Nhập delay chống block (s) : '))
# os.system('termux-open-url https:\/\/tiktok.com\/@nguyenngocquang004')
# TDS_token = 'TDSQfikjclZXZzJiOiIXZ2V2ciwiIxETMxgmbhhGdpFGZiojIyV2c1Jye'
# idtiktok = '7170579645727867931'
api = OOP(TDS_token, idtiktok)
api.datCauHinh()
api.layThongTinAcc()
api.layNhiemVu()
