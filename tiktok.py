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
            print(f'User : {user} | Xu : {xu} | Xu die : {xudie}')
            print('======================================================')

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
            print(f'{id} | {user} | {msg}')
    def layNhiemVu(self):
        while(True):
            print('Đang lấy jobs, vui lòng chờ !!!', end='\r')
            time.sleep(10)
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
                            # if (self.STT == answer):
                            #     self.nghiChongBlock(chongBlock)
                            # else:
                            time.sleep(2)
                            self.demNV += 1
                            self.follow(link_value, now)
                            self.delay(seconds)
                            if self.demNV % countNV == 0:
                                self.nhanXu()

                                self.demNV = 0
                                time.sleep(10)
                                continue
                            # if self.demNV == 9:
                            #     self.nhanXu()
                        
                            #     self.demNV = 0
                            #     time.sleep(10)
                            #     continue
                    except Exception:
                        pass
                        # for i in range(len(arr_link_value)):
                        #     link_value = arr_link_value[i]
                        #     print(link_value)
                            # id_value = arr_id_value[i]
                            # self.guiNhiemVu(id_value)
                            # time.sleep(5)
                            # self.follow(link_value)

            except json.JSONDecodeError:
               pass
    def guiNhiemVu(self, id_value):
        url = 'https://traodoisub.com/api/coin/?type=TIKTOK_FOLLOW_CACHE&id={0}&access_token={1}'.format(id_value, self.TDS_token)
        response = self.s.get(url)
        dataGNV = response.json()
        
        # for i in range(1, dataGNV['cache'] + 1):
        #     self.demNV += 1
        #     if self.demNV == 9:
        #         self.nhanXu()
        #         self.demNV = 0
        #         continue
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
                    print(f"[{self.STT}] | JOBS : {job_success} | {msg} | TOTAL JOBS: {self.totalJobs} | JOBS XU: {self.totalXu} XU | TOTAL XU : {xu} XU")
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
            print('Token tds die !!!')
            exit()
        else:
            user = dataLTT['data']['user']
        
        return user
            # print(f'User : {user} | Xu : {xu} | Xu die : {xudie}')


print('======================================================')
print('[*] => Tên Tool: CTP1204_TOOL')
print('[*] => Admin: Cường TânPhú')
print('[*] => Zalo: 0935 53 53 25')
print('======================================================')
print('Chúc bạn cày thật nhiều xu !!!')
print('======================================================')

if TDS_token is None or idtiktok is None:
    TDS_token = input('Nhập token TDS : ')
    idtiktok = input('Nhập id tiktok cần cấu hình : ')
    save_account_info(TDS_token, idtiktok)
else:
    user = getInfoAccount()
    print(f'1. Giữ tài khoản TDS củ: ({user})')
    print(f'2. Bạn có muốn đổi tài khoản TDS mới không ?')
    keep_old_or_new_token_tds = input(f'Nhập số : ')
    if keep_old_or_new_token_tds.lower() == '2':
        TDS_token = input('1.1 Nhập token TDS mới: ')

    print(f'1. Giữ tài khoản Tiktok củ: ({idtiktok})')
    print(f'2. Bạn có muôn đối tài khoản Tiktok mới không ?')
    keep_or_new_idtiktok = input(f'Nhập số : ')
    if keep_or_new_idtiktok.lower() == '2':
        idtiktok = input('2.1 Nhập id Tiktok mới: ')
    save_account_info(TDS_token, idtiktok)
seconds = int(input('Nhập delay : '))
# answer = int(input('Sau bao nhiêu nhiệm vụ thì nghỉ chống block : '))
# chongBlock = int(input('Nghỉ chống block bao nhiêu giây : '))
countNV = int(input('Bạn muốn chạy bao nhiêu nhiệm vụ thì nhận xu : '))
# os.system('termux-open-url https:\/\/tiktok.com\/@nguyenngocquang004')
# TDS_token = 'TDSQfikjclZXZzJiOiIXZ2V2ciwiIxETMxgmbhhGdpFGZiojIyV2c1Jye'
# idtiktok = '7170579645727867931'
api = OOP(TDS_token, idtiktok)
api.datCauHinh()
api.layThongTinAcc()
api.layNhiemVu()
