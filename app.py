##########已更新 2##########
#主選單
#打擊特效
#暫停畫面
#前置建構優化
#結束選單
#音效調整
#重複(保存)
#新局
#don chan
##########已更新 3##########
#setting (button, input box, img, text)
#bpm, play time
#auto, ez, hr
#1/4, 1/4+1/6, 1/6
#(1/4 : 1/6), (4notes : 7notes)
#notes density 
#don-chan (menu & playing & icon, quality lol, hope this is not the end version.)
#clock
#font
#info text and position
##########待更新##########
#hit判定物件 (不裝在note上而是另外開一個物件收集所有須hit的位置?時間?),300 100 miss,結束評價,acc
#設定存檔
#圖譜匯出
#遊玩匯入的圖譜(初始時更新,可按按鈕更新)
#menu, 暫停, 結束畫面滑鼠按鈕
from ast import Pass
from colorsys import TWO_THIRD
from pickle import GLOBAL
from turtle import color
import pygame
import random
import os
from datetime import datetime

USE_FPS = 1
WIDTH = 1280 #寬
HEIGHT = 720 #高
IS_END = 0 #目前只有是否顯示end info的功能
IS_BUILD = 0
IS_STOP = 0
IS_RETRY = 0
IS_PAUSE = 0
MAPID_SEED = 0

WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

VOLUME=30 #音量,介於1~0之間 (/100)

#note座標(中心點座標)
NOTE_X = 1100
NOTE_Y = 300

#combo的顯示位置座標(中心點座標)
COMBO_X = 85
COMBO_Y = NOTE_Y

#遊戲資訊顯示位置座標(左上角座標)
GAME_INFO_X = 325
GAME_INFO_Y = 15

#結束資訊顯示位置座標(左上角座標)
END_INFO_X = 900
END_INFO_Y = 425

FPS_SV_BALANCE = 1
FPS = 60*FPS_SV_BALANCE#60 120 240 480 越高build速度越快,但要看每台電腦效能有沒有辦法承受 (已改為固定)
MODS = [10*FPS_SV_BALANCE,15*FPS_SV_BALANCE,5*FPS_SV_BALANCE] #(NM,EZ,HR)
MODS_INDEX = 0 #default nm

IS_AUTO = 0 #auto模式
AT_STATUS = 0
#if IS_AUTO == 1:
#    AT_STATUS = 1
EZ_STATUS = 0
HR_STATUS = 0

ori_BPM = 180
SPEED = ori_BPM / MODS[MODS_INDEX] #流速sv 1s移動 SPEED像素*FPS(60), 60s => SPEED*3600 #5=hr,10=nm,15=ez
#speed=2.5, 1min, 9000格
#speed=10, 1min, 36000格
#TYPE=["1/4","1/4 + 1/6","1/6"]

IS_ONE_FOURTH = 0 #1/4
IS_ONE_FOURTH_AND_ONE_SIXTH = 1 #1/4 + 1/6
IS_ONE_SIXTH = 0 #1/6
#1/4 : 1/6
ONE_FOURTH_PROPORTION = 7
ONE_SIXTH_PROPORTION = 10 - ONE_FOURTH_PROPORTION
#depends on 1/4 : 1/6
ONE_SIXTH_NEED_NUM = 0
#two types of 1/6
FOUR_NOTES_PROPORTION = 8
SEVEN_NOTES_PROPORTION = 10 - FOUR_NOTES_PROPORTION

multi = 4 #[4] = 1/4,
BPM = ori_BPM *multi #原始為1/1(四分音符)
BARLINE = 4 *multi #原始為1/1(四拍四分音符(全音音符)), bpm*多少BARLINE就*多少
CENTER = 230 #判定圓x(橫)座標(中心點座標)

PLAYTIME = 60 #seconds
DISTANCE = SPEED*FPS*PLAYTIME #pre_construct跑的總距離 (生成區總長) #每次移動距離*每秒更新次數*總遊玩秒數 = 總遊玩時間的移動距離
PRE_SPEED = DISTANCE/(BPM/(60/PLAYTIME)) #生成點間距
PRE_END_CENTER = 1500 #生成區左邊線
PRE_CENTER = PRE_END_CENTER + DISTANCE #生成區右邊線

#TIME=(60/BPM)*1000

GREAT_RANGE = 25 #300,良
COMBO = 0 #combo

#音符密度 10%, 20%, 30%, ..., 100%
POSSIBILITY_LIST = [10,20,30,40,50,60,70,80,90,100]
POSSIBILITY_INDEX = 6
POSSIBILITY = POSSIBILITY_LIST[POSSIBILITY_INDEX]
POSSIBILITY_RED_RIGHT = POSSIBILITY/2
POSSIBILITY_BLUE_LEFT = POSSIBILITY_RED_RIGHT+1
POSSIBILITY_BLUE_RIGHT = POSSIBILITY

lb_TAP_IS_USE = 0#按一下只能消一顆
lr_TAP_IS_USE = 0
rr_TAP_IS_USE = 0
rb_TAP_IS_USE = 0

menu_init = True #首頁首次執行的初始化
game_init = True #遊戲區首次執行的初始化
setting_init = True #設定區首次執行的初始化
running = True
pause_init = True

TOTAL_PLAY_TIME_start=0
TOTAL_PLAY_TIME_finish=0

#end text
POSSIBLE_NOTE =""
TOTAL_NOTE=""
RED_NOTE=""
BLUE_NOTE=""
BUILD_TIME_COST =""
TOTAL_PLAYTIME=""
##########存檔函式
def setting_sav():
    #print("save")
    f=open("./data\\setting_sav","w")
    f.write(f"ori_BPM={ori_BPM}"+"\n")
    f.write(f"PLAYTIME={PLAYTIME}"+"\n")
    f.write(f"MODS_INDEX={MODS_INDEX}"+"\n")
    f.write(f"IS_AUTO={IS_AUTO}"+"\n")
    f.write(f"AT_STATUS={AT_STATUS}"+"\n")
    f.write(f"EZ_STATUS={EZ_STATUS}"+"\n")
    f.write(f"HR_STATUS={HR_STATUS}"+"\n")
    f.write(f"IS_ONE_FOURTH={IS_ONE_FOURTH}"+"\n")
    f.write(f"IS_ONE_FOURTH_AND_ONE_SIXTH={IS_ONE_FOURTH_AND_ONE_SIXTH}"+"\n")
    f.write(f"IS_ONE_SIXTH={IS_ONE_SIXTH}"+"\n")
    f.write(f"ONE_FOURTH_PROPORTION={ONE_FOURTH_PROPORTION}"+"\n")
    f.write(f"ONE_SIXTH_PROPORTION={ONE_SIXTH_PROPORTION}"+"\n")
    f.write(f"FOUR_NOTES_PROPORTION={FOUR_NOTES_PROPORTION}"+"\n")
    f.write(f"SEVEN_NOTES_PROPORTION={SEVEN_NOTES_PROPORTION}"+"\n")
    f.write(f"POSSIBILITY_INDEX={POSSIBILITY_INDEX}"+"\n")
    f.write(f"VOLUME={VOLUME}"+"\n")
    f.write(f"MAPID_SEED={MAPID_SEED}"+"\n")
    #f.write(f"={}"+"\n")
    f.close()
##########圖譜匯出函式
def map_save():
    map = Map(RETRY_BARLINE_LIST,RETRY_NOTE_LIST,ori_BPM,PLAYTIME,True,0)
    f=open(f"./data/map\\{map.id}.tkz","w")
    f.write(f"mapid={map.id}\n")
    f.write(f"BPM={map.bpm}\n")
    f.write(f"TIME={map.time}\n")
    f.write(f"barlinenum={len(RETRY_BARLINE_LIST)}\n")
    f.write(f"notenum={len(RETRY_NOTE_LIST)}\n")
    i=0
    while i<len(RETRY_BARLINE_LIST):
        f.write(f"{RETRY_BARLINE_LIST[i][0]},{RETRY_BARLINE_LIST[i][1]}\n")
        i+=1
    i=0
    while i<len(RETRY_NOTE_LIST):
        f.write(f"{RETRY_NOTE_LIST[i][0]},{RETRY_NOTE_LIST[i][1]},{RETRY_NOTE_LIST[i][2]}\n")
        i+=1
    f.close()
##########圖譜讀取函式
MAP_LIST=[]
#ALL_RETRY_BARLINE_LIST = []
#ALL_RETRY_NOTE_LIST = []
#retry_barline_list=[]
#retry_note_list=[]
def map_load():
    global MAP_LIST
    map_name_list = os.listdir("data\\map")
    j=0
    count =0 
    while j<len(map_name_list):
        if map_name_list[j].find('.tkz',len(map_name_list[j])-4) != -1:
            count += 1
            f=open(f"./data/map\\{map_name_list[j]}","r")
            id=int(f.readline().strip().split('=')[1])
            bpm = int(f.readline().strip().split('=')[1])
            time = int(f.readline().strip().split('=')[1])
            barlinenum = int(f.readline().strip().split('=')[1])
            notenum = int(f.readline().strip().split('=')[1])
            i=0
            retry_barline_list = []
            retry_note_list = []
            while i<barlinenum:
                s = f.readline().strip()
                barline_x = float(s.split(',')[0])
                barline_y = int(s.split(',')[1])
                retry_barline_list.append([barline_x,barline_y])
                i+=1
            i=0
            while i<notenum:
                s = f.readline().strip()
                note_color = s.split(',')[0]
                note_x = float(s.split(',')[1])
                note_y = int(s.split(',')[2])
                retry_note_list.append([note_color,note_x,note_y])
                i+=1
            MAP_LIST.append(Map(retry_barline_list,retry_note_list,bpm,time,False,id))
            f.close()
        j+=1
        
##########讀檔
if not os.path.exists("./data"):
    os.mkdir("./data")
if not os.path.exists("./map"):
    os.mkdir("./map")
if os.path.isfile("./data\\setting_sav"):
    f = open("./data\\setting_sav","r")
    ori_BPM = int(f.readline().strip().split('=')[1])
    PLAYTIME = int(f.readline().strip().split('=')[1])
    MODS_INDEX = int(f.readline().strip().split('=')[1])
    IS_AUTO = int(f.readline().strip().split('=')[1])
    AT_STATUS = int(f.readline().strip().split('=')[1])
    EZ_STATUS = int(f.readline().strip().split('=')[1])
    HR_STATUS = int(f.readline().strip().split('=')[1])
    IS_ONE_FOURTH = int(f.readline().strip().split('=')[1])
    IS_ONE_FOURTH_AND_ONE_SIXTH = int(f.readline().strip().split('=')[1])
    IS_ONE_SIXTH = int(f.readline().strip().split('=')[1])
    ONE_FOURTH_PROPORTION = int(f.readline().strip().split('=')[1])
    ONE_SIXTH_PROPORTION = int(f.readline().strip().split('=')[1])
    FOUR_NOTES_PROPORTION = int(f.readline().strip().split('=')[1])
    SEVEN_NOTES_PROPORTION = int(f.readline().strip().split('=')[1])
    POSSIBILITY_INDEX = int(f.readline().strip().split('=')[1])
    VOLUME = int(f.readline().strip().split('=')[1])
    MAPID_SEED = int(f.readline().strip().split('=')[1])
    f.close()
    #重算
    SPEED = ori_BPM / MODS[MODS_INDEX] #流速sv 1s移動 SPEED像素*FPS(60), 60s => SPEED*3600 #5=hr,10=nm,15=ez
    DISTANCE = SPEED*FPS*PLAYTIME #pre_construct跑的總距離 (生成區總長) #每次移動距離*每秒更新次數*總遊玩秒數 = 總遊玩時間的移動距離
    PRE_SPEED = DISTANCE/(BPM/(60/PLAYTIME)) #生成點間距
    PRE_CENTER = PRE_END_CENTER + DISTANCE #生成區右邊線
    POSSIBILITY = POSSIBILITY_LIST[POSSIBILITY_INDEX]
    POSSIBILITY_RED_RIGHT = POSSIBILITY/2
    POSSIBILITY_BLUE_LEFT = POSSIBILITY_RED_RIGHT+1
    POSSIBILITY_BLUE_RIGHT = POSSIBILITY

else:
    setting_sav()
##########

#遊戲初始化 and 創建視窗
pygame.init()#初始化
pygame.mixer.init()#初始化音效模組
screen = pygame.display.set_mode((WIDTH,HEIGHT))#傳入元組,表示畫面高度跟寬度
pygame.display.set_caption("Taiko Simulator v2.0")#設定視窗名稱
clock = pygame.time.Clock()

#載入圖片,!載入前需先做pygame.init()初始化,否則會發生錯誤
#統一路徑寫法
#.convert()將圖片轉換成pygame較好讀取的模式,可加快讀取速度
background_img = pygame.image.load(os.path.join("data","img","bg.png")).convert()
pause_img = pygame.image.load(os.path.join("data","img","pause.png")).convert()
pause_img.set_colorkey(BLACK)
circle_img = pygame.image.load(os.path.join("data","img","circle.png")).convert()
icon_img = pygame.image.load(os.path.join("data","img","icon.ico")).convert()
icon_img.set_colorkey(BLACK)
pygame.display.set_icon(icon_img)#設定視窗icon
red_img = pygame.image.load(os.path.join("data","img","red.png")).convert()
blue_img = pygame.image.load(os.path.join("data","img","blue.png")).convert()
pre_dot_img = pygame.image.load(os.path.join("data","img","pre_dot.png")).convert()
end_barline_img = pygame.image.load(os.path.join("data","img","end_barline.png")).convert()
barline_img = pygame.image.load(os.path.join("data","img","barline.png")).convert()
red_hit_left_img = pygame.image.load(os.path.join("data","img","red_hit_left.png")).convert()
red_hit_right_img = pygame.image.load(os.path.join("data","img","red_hit_right.png")).convert()
blue_hit_right_img = pygame.image.load(os.path.join("data","img","blue_hit_right.png")).convert()
blue_hit_left_img = pygame.image.load(os.path.join("data","img","blue_hit_left.png")).convert()
arrow_img = pygame.image.load(os.path.join("data","img","arrow.png")).convert()
option_img = pygame.image.load(os.path.join("data","img","option.png")).convert()
donchan_img = pygame.image.load(os.path.join("data","img","gray_donchan.png")).convert()
#donchan_img.set_colorkey(BLACK)
shortcut_img = pygame.image.load(os.path.join("data","img","shortcut.png")).convert()
sound_img = pygame.image.load(os.path.join("data","img","sound.png")).convert()
left_arrow_img = pygame.image.load(os.path.join("data","img","left_arrow.png")).convert()
left_arrow_img.set_colorkey(BLACK)
right_arrow_img = pygame.image.load(os.path.join("data","img","right_arrow.png")).convert()
right_arrow_img.set_colorkey(BLACK)
input_box_img = pygame.image.load(os.path.join("data","img","input_box.png")).convert()
input_box_img.set_colorkey(BLACK)

at_inactive_img = pygame.image.load(os.path.join("data","img","at_inactive.png")).convert()
at_active_img = pygame.image.load(os.path.join("data","img","at_active.png")).convert()
at_active_img.set_colorkey(BLACK)
at_imgs = [at_inactive_img,at_active_img]

ez_inactive_img = pygame.image.load(os.path.join("data","img","ez_inactive.png")).convert()
ez_active_img = pygame.image.load(os.path.join("data","img","ez_active.png")).convert()
ez_active_img.set_colorkey(BLACK)
ez_imgs = [ez_inactive_img,ez_active_img]

hr_inactive_img = pygame.image.load(os.path.join("data","img","hr_inactive.png")).convert()
hr_active_img = pygame.image.load(os.path.join("data","img","hr_active.png")).convert()
hr_active_img.set_colorkey(BLACK)
hr_imgs = [hr_inactive_img,hr_active_img]

one_fourth_inactive_img = pygame.image.load(os.path.join("data","img","one_fourth_inactive.png")).convert()
one_fourth_active_img = pygame.image.load(os.path.join("data","img","one_fourth_active.png")).convert()
one_fourth_active_img.set_colorkey(BLACK)
one_fourth_imgs = [one_fourth_inactive_img,one_fourth_active_img]

one_fourth_one_sixth_inactive_img = pygame.image.load(os.path.join("data","img","one_fourth_one_sixth_inactive.png")).convert()
one_fourth_one_sixth_inactive_img.set_colorkey(BLACK)
one_fourth_one_sixth_active_img = pygame.image.load(os.path.join("data","img","one_fourth_one_sixth_active.png")).convert()
one_fourth_one_sixth_active_img.set_colorkey(BLACK)
one_fourth_one_sixth_imgs = [one_fourth_one_sixth_inactive_img,one_fourth_one_sixth_active_img]

mini_one_fourth_one_sixth_img = pygame.transform.scale(one_fourth_one_sixth_inactive_img,(50,50))

one_sixth_inactive_img = pygame.image.load(os.path.join("data","img","one_sixth_inactive.png")).convert()
one_sixth_active_img = pygame.image.load(os.path.join("data","img","one_sixth_active.png")).convert()
one_sixth_active_img.set_colorkey(BLACK)
one_sixth_imgs = [one_sixth_inactive_img,one_sixth_active_img]

proportion_left_arrow_img = pygame.image.load(os.path.join("data","img","proportion_left_arrow.png")).convert()
proportion_left_arrow_img.set_colorkey(BLACK)
proportion_left_arrow_imgs = [proportion_left_arrow_img,proportion_left_arrow_img]

proportion_right_arrow_img = pygame.image.load(os.path.join("data","img","proportion_right_arrow.png")).convert()
proportion_right_arrow_img.set_colorkey(BLACK)
proportion_right_arrow_imgs = [proportion_right_arrow_img,proportion_right_arrow_img]

back_img = pygame.image.load(os.path.join("data","img","back.png")).convert()
back_imgs = [back_img,back_img]

clock_img = pygame.image.load(os.path.join("data","img","clock.png")).convert()

menu_donchan_img = pygame.image.load(os.path.join("data","img","menu_donchan.png")).convert()

#載入音樂
red_sound = pygame.mixer.Sound(os.path.join("data","sound","red.ogg"))
red_sound.set_volume(VOLUME/100)#調整音量大小,介於1~0之間
blue_sound = pygame.mixer.Sound(os.path.join("data","sound","blue.ogg"))
blue_sound.set_volume(VOLUME/100)
#pygame.mixer.music.load(os.path.join("sound","background.ogg"))

#def backstage_info():
#    print(f"FPS:{FPS}")
#    print(f":{}")
#    print(f":{}")
#    print(f":{}")
#    print(f":{}")
#    print(f":{}")
#    print(f":{}")
#    print(f":{}")
#    print(f":{}")
#    print(f":{}")
#    print(f":{}")
#    pass

#引入字體pygame.font.Font(None, size)
#font_name = pygame.font.match_font('arial')
font_name = None
def draw_text(surf,text,size,center_x,center_y):#將文字寫到畫面上
    font = pygame.font.Font(font_name,size)#文字物件,(字體,文字大小)
    text_surface = font.render(text,True,WHITE)#渲染,(要渲染的文字,是(True)否(False)要用反鋸齒(使字體看起來比較滑順),文字顏色)
    text_rect = text_surface.get_rect()#定位
    text_rect.centerx = center_x
    text_rect.centery = center_y
    surf.blit(text_surface,text_rect)

def draw_texts(surf,texts,size,x,y):#將多行(列表)文字寫到畫面上
    i=0
    while i<len(texts):
        font = pygame.font.Font(font_name,size)#文字物件,(字體,文字大小)
        text_surface = font.render(texts[i],True,WHITE)#渲染,(要渲染的文字,是(True)否(False)要用反鋸齒(使字體看起來比較滑順),文字顏色)
        text_rect = text_surface.get_rect()#定位
        text_rect.x = x
        text_rect.y = y + (i*size)
        surf.blit(text_surface,text_rect)
        i+=1

def draw_menu_info():
    size=125
    draw_text(screen,"Taiko Simulator",size,525,200)
    screen.blit(menu_donchan_img,(910,97)) 
    #draw_text(screen,"start",70,WIDTH/2,350)

P_NEED_RELEASE=0 #p鍵狀態(是否觸發)的全域偵測
RETURN_NEED_RELEASE=0 #回車鍵狀態(是否觸發)的全域偵測
s_need_release=0


#def menu_option():
#    global IS_MENU
#    global IS_PLAY
#    global IS_SETTING
#    global P_NEED_RELEASE
#    global s_need_release 
#    key_pressed = pygame.key.get_pressed()
#    if key_pressed[pygame.K_p] == True and P_NEED_RELEASE == 0:#start play
#        IS_MENU=0
#        P_NEED_RELEASE=1
#        IS_PLAY=1
#        
#    if key_pressed[pygame.K_s] == True and s_need_release == 0:#setting
#        IS_MENU=0
#        s_need_release=1
#        IS_SETTING=1
#    #release
#    if key_pressed[pygame.K_p] == False and P_NEED_RELEASE == 1:
#        P_NEED_RELEASE=0
#    if key_pressed[pygame.K_s] == False and s_need_release == 1:
#        s_need_release=0

def draw_pause():#暫停的顯示畫面
    draw_text(screen,"Taiko Simulator 2.0",40,170,50)
    draw_text(screen,"pause",150,WIDTH/2,NOTE_Y)
    draw_text(screen,"Enter \"p\" to play",60,WIDTH/2,NOTE_Y+150)
    #font = pygame.font.Font(font_name,150)
    #text_surface = font.render("pause",True,WHITE)#渲染,(要渲染的文字,是(True)否(False)要用反鋸齒(使字體看起來比較滑順),文字顏色)
    #text_rect = text_surface.get_rect()#定位
    #text_rect.centerx = WIDTH/2
    #text_rect.bottom = NOTE_Y
    #screen.blit(text_surface,text_rect)

NOTE_LIST = []#all notes
def new_note(color,note_x,note_y):#生成note
    if color=="red":
        #r = Red_note(note_x,note_y)
        NOTE_LIST.insert(0,Red_note(note_x,note_y))
        all_sprites.add(NOTE_LIST[0])
        notes.add(NOTE_LIST[0])
    if color=="blue":
        #r = Blue_note(note_x,note_y)
        NOTE_LIST.insert(0,Blue_note(note_x,note_y))
        all_sprites.add(NOTE_LIST[0])
        notes.add(NOTE_LIST[0])

def new_hit(position):#打擊效果
    if position=="red_left":
        h = Hit_red_left()
        all_sprites.add(h)
        hits.add(h)
    if position=="red_right":
        h = Hit_red_right()
        all_sprites.add(h)
        hits.add(h)
    if position=="blue_left":
        h = Hit_blue_left()
        all_sprites.add(h)
        hits.add(h)
    if position=="blue_right":
        h = Hit_blue_right()
        all_sprites.add(h)
        hits.add(h)

def new_barline(x,y):#生成小節線
    bl = Barline(x,y)
    all_sprites.add(bl)
    barlines.add(bl)

def barline_position_calculate(bpm,left_limit):#oribpm,pre_end_center
    bl_posi=[]
    dis=DISTANCE
    spacing = DISTANCE/(bpm/(60/PLAYTIME))
    while dis-spacing>left_limit:
        dis -= spacing
        bl_posi.insert(0,dis)
    
    return bl_posi

def time_transform(seconds):
    secs = seconds%60
    mins = seconds//60
    hours = mins//60
    mins = mins - (hours*60)
    days = hours//24
    hours = hours - (days*24)
    timel=[]
    timel.append(days)
    timel.append(hours)
    timel.append(mins)
    timel.append(secs)
    count=0
    while True:
        if timel[0]==0 and count<2:
            del timel[0]
            count+=1
        else:
            break
    result=""
    i=0
    while i<len(timel):
        if timel[i]<10:
            result += f"0{timel[i]}:"
        else:
            result += f"{timel[i]}:"
        i+=1
    rl=list(result)
    rl[len(rl)-1]=""
    result="".join(rl)
    return result

def game_info():
    size=36
    l=[f"bpm: {ori_BPM}",f"time: ~ {time_transform(PLAYTIME)}",f"notes density: {POSSIBILITY_LIST[POSSIBILITY_INDEX]}%"]
    if IS_ONE_FOURTH_AND_ONE_SIXTH == 1:
        l=[f"bpm: {ori_BPM}",f"time: ~ {time_transform(PLAYTIME)}",f"notes density: {POSSIBILITY_LIST[POSSIBILITY_INDEX]}%",f"(1/4 : 1/6):  ({ONE_FOURTH_PROPORTION} : {ONE_SIXTH_PROPORTION})",f"(4n : 7n):  ({FOUR_NOTES_PROPORTION} : {SEVEN_NOTES_PROPORTION})"]
    draw_texts(screen,l,size,GAME_INFO_X,GAME_INFO_Y)

def end_info():
    size=45
    l=[POSSIBLE_NOTE,TOTAL_NOTE,RED_NOTE,BLUE_NOTE,BUILD_TIME_COST,TOTAL_PLAYTIME]
    draw_texts(screen,l,size,END_INFO_X,END_INFO_Y)

def one_fourth_one_sixth_propotion():
    draw_text(screen,str(ONE_FOURTH_PROPORTION)+" : "+str(ONE_SIXTH_PROPORTION),50,550,385)
#random_note_two=[]
#i=0
#while i<9:
#    a=random.randint(0,1)
#    if a==0:
#        random_note_two.append("red")
#    if a==1:
#        random_note_two.append("blue")
#    i+=1



#sprite 畫面上的所有物件
#創建note
class Red_note(pygame.sprite.Sprite):#用自定義的類別繼承內建sprite類別
    def __init__(self,note_x,note_y):
        pygame.sprite.Sprite.__init__(self)#呼叫內建sprite初始函式
        #self.image = pygame.Surface((50,40))#屬性1,要顯示的圖片,初始以平面(pygame.Surface())表示
        #self.image.fill(GREEN)#設定圖片顏色
        self.image = red_img #轉換圖片大小,(圖片,像素)(已改)
        self.image.set_colorkey(BLACK)#把黑色的部分變透明
        self.rect = self.image.get_rect()#屬性2,定位圖片位置,把圖片框起來,就能設定位置相關數據
        #設定rect左上角座標
        #self.rect.x = NOTE_X
        #self.rect.y = NOTE_Y
        #設定中心座標
        self.rect.center = (note_x,note_y)
        #設定速度變數
        self.radius = 20#半徑
        #畫出來確認碰撞範圍
        pygame.draw.circle(self.image,YELLOW,self.rect.center,1)#畫圓,(畫布,顏色,中心,半徑)
        self.speedx = SPEED
        self.last_update = pygame.time.get_ticks()
        #self.rect.centerx = WIDTH/2
        #self.rect.bottom = HEIGHT - 10
        self.is_in=0
        self.rr_need_release=0
        self.lr_need_release=0

        self.color="red"

    def update(self):#更新函式
        global lr_TAP_IS_USE
        global rr_TAP_IS_USE
        global COMBO
        if IS_STOP==0:
            self.rect.x -= self.speedx
            if self.rect.right<0:
                #if self.is_in==0:
                #    print("fail")
                self.kill()

            key_pressed = pygame.key.get_pressed()#回傳一整串布林值,代表鍵盤上的按鍵是(True)否(False)有被按下
            if self.rect.center[0]<=CENTER+(SPEED*4) and self.rect.center[0]>=CENTER-(SPEED*4):#良 #前:CENTER+-GREAT_RANGE
                now = pygame.time.get_ticks()
                self.is_in=1
                #print(now-self.last_update)
                if IS_AUTO==0:
                    if key_pressed[pygame.K_COMMA] and self.rr_need_release==0 and rr_TAP_IS_USE == 0:#判斷,是否有被按下
                        rr_TAP_IS_USE = 1
                        COMBO += 1
                        self.kill()
                    elif key_pressed[pygame.K_x] and self.lr_need_release==0 and lr_TAP_IS_USE == 0:#判斷x是否有被按下
                        lr_TAP_IS_USE = 1
                        COMBO += 1
                        self.kill()

                if IS_AUTO==1: #auto模式
                    red_sound.play()
                    COMBO += 1
                    self.kill()

            if key_pressed[pygame.K_COMMA] and self.rr_need_release==0:#判斷,是否有被按下
                self.rr_need_release=1
            elif key_pressed[pygame.K_x] and self.lr_need_release==0:#判斷x是否有被按下
                self.lr_need_release=1
            if key_pressed[pygame.K_COMMA] == False  and self.rr_need_release==1:
                self.rr_need_release =0
            if key_pressed[pygame.K_x] == False  and self.lr_need_release==1:
                self.lr_need_release =0
        
class Blue_note(pygame.sprite.Sprite):#用自定義的類別繼承內建sprite類別
    def __init__(self,note_x,note_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = blue_img #轉換圖片大小,(圖片,像素)(已改)
        self.image.set_colorkey(BLACK)#把黑色的部分變透明
        self.rect = self.image.get_rect()#屬性2,定位圖片位置,把圖片框起來,就能設定位置相關數據
        self.speedx = SPEED
        self.is_in=0
        self.rect.center = (note_x,note_y)
        self.last_update = pygame.time.get_ticks()
        self.lb_need_release=0
        self.rb_need_release=0
        self.color = "blue"

    def update(self):#更新函式
        global lb_TAP_IS_USE
        global rb_TAP_IS_USE
        global COMBO
        if IS_STOP==0:
            now = pygame.time.get_ticks()
            self.rect.x -= self.speedx
            if self.rect.right<0:
                self.kill()

            key_pressed = pygame.key.get_pressed()#回傳一整串布林值,代表鍵盤上的按鍵是(True)否(False)有被按下
            if self.rect.center[0]<=CENTER+(SPEED*4) and self.rect.center[0]>CENTER-(SPEED*4):#良
                now = pygame.time.get_ticks()
                self.is_in=1
                #print(now-self.last_update)
                if IS_AUTO==0:
                    if key_pressed[pygame.K_PERIOD] and self.rb_need_release==0 and rb_TAP_IS_USE == 0:#判斷.是否有被按下x,x
                        rb_TAP_IS_USE = 1
                        COMBO += 1
                        self.kill()
                    elif key_pressed[pygame.K_z] and self.lb_need_release==0 and lb_TAP_IS_USE == 0:#判斷z是否有被按下
                        lb_TAP_IS_USE = 1
                        COMBO += 1
                        self.kill()

                if IS_AUTO==1: #auto模式
                    blue_sound.play()
                    COMBO += 1
                    self.kill()

            if key_pressed[pygame.K_PERIOD] and self.rb_need_release==0:#判斷.是否有被按下
                self.rb_need_release=1
            elif key_pressed[pygame.K_z] and self.lb_need_release==0:#判斷z是否有被按下
                self.lb_need_release=1
            if key_pressed[pygame.K_PERIOD] == False and self.rb_need_release==1:
                self.rb_need_release =0
            if key_pressed[pygame.K_z] == False and self.lb_need_release==1:
                self.lb_need_release =0

class Circle(pygame.sprite.Sprite):#判定圈
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = circle_img #轉換圖片大小,(圖片,像素)(已改)
        self.image.set_colorkey(BLACK)#把黑色的部分變透明
        self.rect = self.image.get_rect()#屬性2,定位圖片位置,把圖片框起來,就能設定位置相關數據
        #self.radius = 20#半徑
        #self.rect.y = NOTE_Y
        #self.rect.x = 100
        self.speedx = SPEED
        self.rect.center = (CENTER,NOTE_Y)
        #self.f=1
        self.lb_need_release=0
        self.lr_need_release=0
        self.rr_need_release=0
        self.rb_need_release=0
        #self.rect.centerx = WIDTH/2
        #self.rect.bottom = HEIGHT - 10
    def update(self):#更新函式
        global lr_TAP_IS_USE
        global rr_TAP_IS_USE
        global lb_TAP_IS_USE
        global rb_TAP_IS_USE
        global NOTE_LIST
        if IS_PLAY == 0:
            self.kill()

        #if self.f==1:
        #    self.f=0
        #    #print(self.rect.left)
        #    #print(self.rect.right)
        
        #if NOTE_LIST[0].color == "red":
            
        #if self.rect.center[0]<=CENTER+SPEED and self.rect.center[0]>CENTER-SPEED:#良

        key_pressed = pygame.key.get_pressed()#回傳一整串布林值,代表鍵盤上的按鍵是(True)否(False)有被按下
        if key_pressed[pygame.K_COMMA] and self.rr_need_release==0:#判斷,是否有被按下
            new_hit("red_right")
            self.rr_need_release=1
            if IS_AUTO==0:
                red_sound.play()
                


        elif key_pressed[pygame.K_x] and self.lr_need_release==0:#判斷x是否有被按下
            new_hit("red_left")
            self.lr_need_release=1
            if IS_AUTO==0:
                red_sound.play()
        if key_pressed[pygame.K_PERIOD] and self.rb_need_release==0:#判斷.是否有被按下
            new_hit("blue_right")
            self.rb_need_release=1
            if IS_AUTO==0:
                blue_sound.play()
        elif key_pressed[pygame.K_z] and self.lb_need_release==0:#判斷z是否有被按下
            new_hit("blue_left")
            self.lb_need_release=1
            if IS_AUTO==0:
                blue_sound.play()
        if key_pressed[pygame.K_COMMA] == False and self.rr_need_release==1:
            self.rr_need_release =0
            rr_TAP_IS_USE = 0
        if key_pressed[pygame.K_x] == False and self.lr_need_release==1:
            self.lr_need_release =0
            lr_TAP_IS_USE = 0
        if key_pressed[pygame.K_PERIOD] == False and self.rb_need_release==1:
            self.rb_need_release =0
            rb_TAP_IS_USE = 0
        if key_pressed[pygame.K_z] == False and self.lb_need_release==1:
            self.lb_need_release =0
            lb_TAP_IS_USE = 0

class Hit_red_left(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = red_hit_left_img #轉換圖片大小,(圖片,像素)(已改)
        self.image.set_colorkey(BLACK)#把黑色的部分變透明
        self.rect = self.image.get_rect()#屬性2,定位圖片位置,把圖片框起來,就能設定位置相關數據
        self.rect.right = COMBO_X
        self.rect.centery = COMBO_Y
        #self.rect.center = (,)
        self.display_duration_start=pygame.time.get_ticks()

    def update(self):
        display_duration_finish=pygame.time.get_ticks()
        if display_duration_finish-self.display_duration_start>100:
            self.kill()

class Hit_blue_right(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = blue_hit_right_img #轉換圖片大小,(圖片,像素)(已改)
        self.image.set_colorkey(BLACK)#把黑色的部分變透明
        self.rect = self.image.get_rect()#屬性2,定位圖片位置,把圖片框起來,就能設定位置相關數據
        self.rect.left = COMBO_X
        self.rect.centery = COMBO_Y
        #self.rect.center = (,)
        self.display_duration_start=pygame.time.get_ticks()

    def update(self):
        display_duration_finish=pygame.time.get_ticks()
        if display_duration_finish-self.display_duration_start>100:
            self.kill()

class Hit_red_right(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = red_hit_right_img #轉換圖片大小,(圖片,像素)(已改)
        self.image.set_colorkey(BLACK)#把黑色的部分變透明
        self.rect = self.image.get_rect()#屬性2,定位圖片位置,把圖片框起來,就能設定位置相關數據
        self.rect.left = COMBO_X
        self.rect.centery = COMBO_Y
        #self.rect.center = (,)
        self.display_duration_start=pygame.time.get_ticks()

    def update(self):
        display_duration_finish=pygame.time.get_ticks()
        if display_duration_finish-self.display_duration_start>100:
            self.kill()

class Hit_blue_left(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = blue_hit_left_img #轉換圖片大小,(圖片,像素)(已改)
        self.image.set_colorkey(BLACK)#把黑色的部分變透明
        self.rect = self.image.get_rect()#屬性2,定位圖片位置,把圖片框起來,就能設定位置相關數據
        self.rect.right = COMBO_X
        self.rect.centery = COMBO_Y
        #self.rect.center = (,)
        self.display_duration_start=pygame.time.get_ticks()

    def update(self):
        display_duration_finish=pygame.time.get_ticks()
        if display_duration_finish-self.display_duration_start>100:
            self.kill()

class Barline(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = barline_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speedx=SPEED

    def update(self):
        if IS_STOP==0:
            if self.rect.x >= 0:
                self.rect.x -= self.speedx
            if self.rect.x < 0:
                self.kill()

class End_barline(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = end_barline_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (PRE_CENTER+500,NOTE_Y)
        self.speedx=SPEED

    def update(self):
        global running
        global TOTAL_PLAY_TIME_finish
        global TOTAL_PLAYTIME
        global IS_END
        if IS_STOP==0:
            if self.rect.x > 0:
                self.rect.x -= self.speedx
            else:
                IS_END = 1
                #running=False
                TOTAL_PLAY_TIME_finish=pygame.time.get_ticks()
                TOTAL_PLAYTIME=f"total playtime: {(TOTAL_PLAY_TIME_finish-TOTAL_PLAY_TIME_start)/1000}s"

                size = 70
                opx=20
                opy=450
                end_option = Option_list(opx,opy,3,["new game","retry","back to menu"],size,3)
                all_sprites.add(end_option)

                self.kill()

class Arrow(pygame.sprite.Sprite):
    def __init__(self,center_x,center_y,movespeed):
        pygame.sprite.Sprite.__init__(self)
        self.image = arrow_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (center_x,center_y)
        self.move_wait_time_start=pygame.time.get_ticks()
        self.move_type=1
        self.movespeed=movespeed
        self.move_wait_times = int((FPS/60)-1)
        #print(self.move_wait_times)
        self.move_wait_time_count=0
        #self.updown_distance=updown_distance
        self.move_right_limit = center_x
        self.move_left_limit = center_x - 40
        #self.up_need_release=0
        #self.down_need_release=0
        #self.up_times_limit=up_times_limit
        #self.down_times_limit=down_times_limit


    def update(self):
        #if IS_MENU == 0:
        #    self.kill()
        #移動動畫
        if self.rect.x >= self.move_right_limit or self.rect.x <= self.move_left_limit:
            if self.rect.x >= self.move_right_limit:
                self.rect.x = self.move_right_limit-1
            else:
                self.rect.x = self.move_left_limit+1
            #print(f"{self.rect.x}>={self.move_right_limit},{self.rect.x}<={self.move_left_limit}")
            self.move_type *= -1
        #print(self.move_type,self.rect.x , self.move_right_limit ,self.move_left_limit)
        if self.move_type == 1:
            if self.move_wait_time_count < self.move_wait_times:
                self.move_wait_time_count += 1
            else:
                self.rect.x += self.movespeed
                self.move_wait_time_count = 0
        if self.move_type == -1:
            if self.move_wait_time_count < self.move_wait_times:
                self.move_wait_time_count += 1
            else:
                self.rect.x -= self.movespeed
                self.move_wait_time_count = 0

        #上下移動
        #key_pressed = pygame.key.get_pressed()
        #if key_pressed[pygame.K_UP] and self.up_need_release == 0 and self.up_times_limit > 0:
        #    self.up_need_release=1
        #    self.up_times_limit -= 1
        #    self.down_times_limit += 1
        #    self.rect.centery -= self.updown_distance
        #if key_pressed[pygame.K_DOWN] and self.down_need_release == 0 and self.down_times_limit > 0:
        #    self.down_need_release=1
        #    self.up_times_limit += 1
        #    self.down_times_limit -= 1
        #    self.rect.centery += self.updown_distance

        ##release
        #if key_pressed[pygame.K_UP] == False and self.up_need_release == 1:
        #    self.up_need_release=0
        #if key_pressed[pygame.K_DOWN] == False and self.down_need_release == 1:
        #    self.down_need_release=0
    
    def get_y(self,centery):
        self.rect.centery=centery

class Image_button(pygame.sprite.Sprite):
    def __init__(self,button_imgs,centerx,centery,button_type,active_status):
        self.button_type = button_type #-21=audio left, -22=audio right,-1=back, 0=auto, 1=ez, 2=hr, 3=1/4, 4=1/4+1/6, 5=1/6, 41=1/4&1/6 left arrow, 42=1/4&1/6 right arrow, 43=4notes&7notes left arrow, 44=4notes&7notes right arrow,31=notes density left arrow, 32=notes density right arrow
        pygame.sprite.Sprite.__init__(self)
        self.active_index = 0
        if active_status == 1:
            self.active_index = 1    
        self.button_imgs = [button_imgs[0],button_imgs[1]]
        self.image = self.button_imgs[self.active_index]
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.centerx = centerx
        self.centery = centery
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        self.button_box = pygame.Rect(self.rect.left, self.rect.top, self.rect.width,self.rect.height)

    def update(self):
        if IS_SETTING == 0 and IS_PAUSE == 0:
            self.kill()
        if self.button_type == 1 and EZ_STATUS == 0 and self.active_index == 1:
            self.active_index = 0
            self.img_update()
        if self.button_type == 2 and HR_STATUS == 0 and self.active_index == 1:
            self.active_index = 0
            self.img_update()
        if self.button_type == 3 and IS_ONE_FOURTH == 0 and self.active_index == 1:
            self.active_index = 0
            self.img_update()
        if self.button_type == 4 and IS_ONE_FOURTH_AND_ONE_SIXTH == 0 and self.active_index == 1:
            self.active_index = 0
            self.img_update()
        if self.button_type == 5 and IS_ONE_SIXTH == 0 and self.active_index == 1:
            self.active_index = 0
            self.img_update()

    def click(self):
        #print(self.button_type)
        global IS_AUTO
        global AT_STATUS
        global EZ_STATUS
        global HR_STATUS
        global IS_SETTING
        global IS_MENU
        global menu_init
        global IS_ONE_FOURTH
        global IS_ONE_FOURTH_AND_ONE_SIXTH
        global IS_ONE_SIXTH
        global IS_PLAY
        global game_init
        global ONE_FOURTH_PROPORTION
        global ONE_SIXTH_PROPORTION
        global FOUR_NOTES_PROPORTION
        global SEVEN_NOTES_PROPORTION
        global POSSIBILITY_INDEX
        global POSSIBILITY
        global POSSIBILITY_RED_RIGHT
        global POSSIBILITY_BLUE_LEFT
        global POSSIBILITY_BLUE_RIGHT
        global VOLUME

        #狀態切換
        
        if self.active_index == 0:
            self.active_index = 1
        elif self.button_type == 3 and IS_ONE_FOURTH_AND_ONE_SIXTH == 0 and IS_ONE_SIXTH == 0:
            pass
        elif self.button_type == 4 and IS_ONE_FOURTH == 0 and IS_ONE_SIXTH == 0:#1/4+1/6 off
            pass
        elif self.button_type == 5 and IS_ONE_FOURTH == 0 and IS_ONE_FOURTH_AND_ONE_SIXTH ==0:#1/6 off
            pass
        else:
            self.active_index = 0

        self.img_update()
        
        #數值更新
        if self.button_type == -1:#back on
            IS_MENU = 1
            menu_init = True
            #game_init = True
            IS_SETTING = 0

        
        if self.active_index == 0:#off
            if self.button_type == 0:#auto off
                IS_AUTO = 0
                AT_STATUS = 0
            if self.button_type == 1:#ez off
                EZ_STATUS = 0
            if self.button_type == 2:#hr off
                HR_STATUS = 0
            if self.button_type == 3 and IS_ONE_FOURTH_AND_ONE_SIXTH != 0 and IS_ONE_SIXTH != 0:#1/4 off
                IS_ONE_FOURTH = 0
            if self.button_type == 4 and IS_ONE_FOURTH != 0 and IS_ONE_SIXTH != 0:#1/4+1/6 off
                IS_ONE_FOURTH_AND_ONE_SIXTH = 0
            if self.button_type == 5 and IS_ONE_FOURTH != 0 and IS_ONE_FOURTH_AND_ONE_SIXTH:#1/6 off
                IS_ONE_SIXTH = 0
        if self.active_index == 1:#on
            if self.button_type == 0:#auto on
                IS_AUTO = 1
                AT_STATUS = 1
            if self.button_type == 1:#ez on, then hr off
                EZ_STATUS = 1
                HR_STATUS = 0
            if self.button_type == 2:#hr on, then ez off
                HR_STATUS = 1
                EZ_STATUS = 0
            if self.button_type == 3:#1/4 on, others off
                IS_ONE_FOURTH = 1
                IS_ONE_FOURTH_AND_ONE_SIXTH = 0
                IS_ONE_SIXTH = 0
            if self.button_type == 4:#1/4+1/6 on, others off
                IS_ONE_FOURTH_AND_ONE_SIXTH = 1
                IS_ONE_FOURTH = 0
                IS_ONE_SIXTH = 0
            if self.button_type == 5:#1/6 on, others off
                IS_ONE_SIXTH = 1
                IS_ONE_FOURTH = 0
                IS_ONE_FOURTH_AND_ONE_SIXTH = 0
        
        #1/4 + 1/6
        if self.button_type == 41 and ONE_FOURTH_PROPORTION < 9:#left arrow
            ONE_FOURTH_PROPORTION += 1
            ONE_SIXTH_PROPORTION -= 1
        if self.button_type == 42 and ONE_SIXTH_PROPORTION < 9:#right arrow
            ONE_SIXTH_PROPORTION += 1
            ONE_FOURTH_PROPORTION -= 1
        if self.button_type == 43 and FOUR_NOTES_PROPORTION < 9:#left arrow
            FOUR_NOTES_PROPORTION += 1
            SEVEN_NOTES_PROPORTION -= 1
        if self.button_type == 44 and SEVEN_NOTES_PROPORTION < 9:#right arrow
            SEVEN_NOTES_PROPORTION += 1
            FOUR_NOTES_PROPORTION -= 1
        
        #note density
        if self.button_type == 31 and POSSIBILITY_INDEX >0 :
            POSSIBILITY_INDEX -= 1
            POSSIBILITY = POSSIBILITY_LIST[POSSIBILITY_INDEX]
            POSSIBILITY_RED_RIGHT = POSSIBILITY/2
            POSSIBILITY_BLUE_LEFT = POSSIBILITY_RED_RIGHT+1
            POSSIBILITY_BLUE_RIGHT = POSSIBILITY
        if self.button_type == 32 and POSSIBILITY_INDEX <9 :
            POSSIBILITY_INDEX += 1
            POSSIBILITY = POSSIBILITY_LIST[POSSIBILITY_INDEX]
            POSSIBILITY_RED_RIGHT = POSSIBILITY/2
            POSSIBILITY_BLUE_LEFT = POSSIBILITY_RED_RIGHT+1
            POSSIBILITY_BLUE_RIGHT = POSSIBILITY
        
        #audio set
        if self.button_type == -21 and VOLUME > 0:#left
            VOLUME -= 5
            red_sound.set_volume(VOLUME/100)
            blue_sound.set_volume(VOLUME/100)
        if self.button_type == -22 and VOLUME < 100 :#left
            VOLUME += 5
            red_sound.set_volume(VOLUME/100)
            blue_sound.set_volume(VOLUME/100)
        
    def img_update(self):#換圖片

        self.image = self.button_imgs[self.active_index]
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        self.button_box = pygame.Rect(self.rect.left, self.rect.top, self.rect.width,self.rect.height)

class Input_num_box(pygame.sprite.Sprite):
    def __init__(self,info_text,x,y,init_text,size,is_time,max_limit,min_limit,active_info):
        pygame.sprite.Sprite.__init__(self)
        self.image = input_box_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.num = int(init_text)
        self.text = str(self.num)
        if init_text == "":
            self.text = "0"
        self.font = pygame.font.Font(None, size)
        self.input_box = pygame.Rect(100, 100, 140, size)
        self.active = False

        self.text_surface = self.font.render(self.text, True, WHITE)
        input_box_width = max(100, self.text_surface.get_width()+10)
        self.input_box.w = input_box_width

        self.is_time = is_time
        self.time_text = ""
        if self.is_time:
            self.time_text = time_transform(self.num)
            self.text = self.time_text
        self.max_limit = max_limit
        self.min_limit = min_limit

        self.info_box = pygame.Rect(100, 100, 140, size)
        self.info_text = info_text
        self.info_surface = self.font.render(self.info_text, True, WHITE)

        self.active_info_box = pygame.Rect(100, 100, 140, size-15)
        self.active_info_text = active_info
        self.active_font = pygame.font.Font(None, size-15)
        self.active_info_surface = self.active_font.render(self.active_info_text, True, WHITE)


    def text_save(self):
        global PLAYTIME
        global ori_BPM
        is_num = 1
        i=0
        while i<len(self.text):
            if self.text[i] != "0" and self.text[i] != "1" and self.text[i] != "2" and self.text[i] != "3" and self.text[i] != "4" and self.text[i] != "5" and self.text[i] != "6" and self.text[i] != "7" and self.text[i] != "8" and self.text[i] != "9":
                is_num=0
                break
            i+=1
        if self.text == "":
            is_num = 0
        if is_num == 1:
            if int(self.text) <= self.max_limit and int(self.text) >= self.min_limit:
                self.num = int(self.text)
        self.text = str(self.num)

        #is_time
        if self.is_time:
            self.time_text = time_transform(self.num)
            self.text = self.time_text
            PLAYTIME = self.num
        if self.is_time == False:
            ori_BPM = self.num

    def update(self):
        
        #畫

        #info
        self.info_surface = self.font.render(self.info_text, True, WHITE)
        info_box_width = max(100, self.info_surface.get_width()+10)
        self.info_box.w = info_box_width
        self.info_box.x = self.rect.x
        self.info_box.y = self.rect.y
        screen.blit(self.info_surface, (self.info_box.x+5, self.info_box.y+5))

        #數字
        self.text_surface = self.font.render(self.text, True, WHITE)#字體.render(要畫的文字,平滑值,文字顏色,背景顏色(沒填就是沒有)) #將文字以此字體渲染成可畫物件
        input_box_width = max(100, self.text_surface.get_width()+10)
        self.input_box.w = input_box_width
        self.input_box.x = self.rect.x + self.info_box.w
        self.input_box.y = self.rect.y
        screen.blit(self.text_surface, (self.input_box.x+5, self.input_box.y+5))#畫文字

        #active_info
        self.active_info_surface = self.active_font.render(self.active_info_text, True, WHITE)
        info_box_width = max(100, self.active_info_surface.get_width()+10)
        self.active_info_box.w = info_box_width
        self.active_info_box.x = self.input_box.x + self.input_box.w + 10
        self.active_info_box.y = self.rect.y + 7

        if self.active:
            pygame.draw.rect(screen, WHITE, self.input_box, 3)#畫邊框
            screen.blit(self.active_info_surface, (self.active_info_box.x+5, self.active_info_box.y+5))
        
        if IS_SETTING==0:
            self.kill()

class Option_list(pygame.sprite.Sprite):
    def __init__(self,x,y,option_num,option_name_list,option_name_size,option_position):
        self.option_position=option_position
        #option_position: Option_list所處位置(主選單(0) or 設定(1) or ...)
        #Option_list所處位置不同會有不同status_list
        self.option_status_list_index = 0
        #主選單(0)
        self.menu_option_status_list=[[0,1,0,False,True,True],[0,0,1,True,False,True],[0,0,0,False,False,False]]#[IS_MENU,IS_PLAY,IS_SETTING,setting_init,game_init,running] #[0]=start, [1]=setting, [2]=quit
        #設定(1)
        self.setting_option_status_list=[]
        #遊玩暫停(2)
        self.play_pause_option_status_list=[[0,1,0,0,0,0,False,False],[0,1,0,1,0,0,False,True],[1,0,0,0,0,0,True,True]]#[IS_MENU,IS_PLAY,IS_END,IS_RETRY,IS_STOP,menu_init,game_init] #[0]=continue, [1]=retry, #[2]=back
        #遊玩結束(3)
        self.play_end_option_status_list=[[0,1,0,0,False,True],[0,1,0,1,False,True],[1,0,0,0,True,True]]#[IS_MENU,IS_PLAY,IS_END,IS_RETRY,menu_init,game_init] #[0]=new game, [1]=retry, #[2]=back
        #pygame.draw.polygon(screen,WHITE,((x,y),(x,y+l),(x+math.sqrt((l*l)-((l/2)*(l/2))),y+(l/2))))
        pygame.sprite.Sprite.__init__(self)
        self.image = option_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.option_num=option_num
        self.option_name_list=[]
        i=0
        while i<len(option_name_list):
            self.option_name_list.append(option_name_list[i])
            i+=1
        self.option_name_size=option_name_size
        self.arrow_centerx=x+50
        self.arrow_centery=y+25

        self.Arrow = Arrow(self.arrow_centerx,self.arrow_centery,1)#WIDTH/2-125,350,1,70
        
        #選單位置(箭頭加入的不同群組)
        if self.option_position == 0:#menu
            menu_sprites.add(self.Arrow)
        if self.option_position == 1:#setting
            pass
        if self.option_position == 2:#play pause
            all_sprites.add(self.Arrow)
        if self.option_position == 3:#play end
            all_sprites.add(self.Arrow)
        
        self.arrow_distancey=option_name_size

        self.up_need_release=0
        self.down_need_release=0
        self.up_times_limit=0
        self.down_times_limit=option_num-1

        #self.enter_need_release=0

    def update(self):
        global IS_MENU
        global IS_PLAY
        global IS_SETTING
        global IS_END
        global IS_RETRY
        global IS_STOP
        global menu_init
        global game_init
        global setting_init
        global running
        global RETURN_NEED_RELEASE #回車鍵狀態(是否觸發)的全域偵測
        global ESC_NEED_RELEASE
        global IS_PAUSE
        #顯示文字
        draw_texts(screen,self.option_name_list,self.option_name_size,self.rect.x+110,self.rect.y)
        #箭頭上下移動操作
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP] and self.up_need_release == 0:
            self.up_need_release=1
            if self.up_times_limit > 0:
                self.up_times_limit -= 1
                self.down_times_limit += 1
                self.arrow_centery -= self.arrow_distancey
                self.option_status_list_index -= 1
            else:
                self.up_times_limit = self.option_num-1
                self.down_times_limit = 0
                self.arrow_centery += (self.arrow_distancey * (self.option_num-1))
                self.option_status_list_index = self.option_num-1
            self.Arrow.get_y(self.arrow_centery)

        if key_pressed[pygame.K_DOWN] and self.down_need_release == 0:
            self.down_need_release=1
            if self.down_times_limit > 0:
                self.up_times_limit += 1
                self.down_times_limit -= 1
                self.arrow_centery += self.arrow_distancey
                self.option_status_list_index += 1
            else:
                self.up_times_limit = 0
                self.down_times_limit = self.option_num-1
                self.arrow_centery -= (self.arrow_distancey * (self.option_num-1))
                self.option_status_list_index = 0
            self.Arrow.get_y(self.arrow_centery)

        #release
        if key_pressed[pygame.K_UP] == False and self.up_need_release == 1:
            self.up_need_release=0
        if key_pressed[pygame.K_DOWN] == False and self.down_need_release == 1:
            self.down_need_release=0
        
        #確認ENTER
        if key_pressed[pygame.K_RETURN] and RETURN_NEED_RELEASE == 0:
            RETURN_NEED_RELEASE=1
            #選單位置
            if self.option_position == 0:#menu
                IS_MENU=self.menu_option_status_list[self.option_status_list_index][0]
                IS_PLAY=self.menu_option_status_list[self.option_status_list_index][1]
                IS_SETTING=self.menu_option_status_list[self.option_status_list_index][2]
                setting_init=self.menu_option_status_list[self.option_status_list_index][3]
                game_init=self.menu_option_status_list[self.option_status_list_index][4]
                running=self.menu_option_status_list[self.option_status_list_index][5]
            
            if self.option_position == 2:#play pause
                IS_MENU=self.play_pause_option_status_list[self.option_status_list_index][0]
                IS_PLAY=self.play_pause_option_status_list[self.option_status_list_index][1]
                IS_END=self.play_pause_option_status_list[self.option_status_list_index][2]
                IS_RETRY=self.play_pause_option_status_list[self.option_status_list_index][3]
                IS_STOP=self.play_pause_option_status_list[self.option_status_list_index][4]
                IS_PAUSE=self.play_pause_option_status_list[self.option_status_list_index][5]
                menu_init=self.play_pause_option_status_list[self.option_status_list_index][6]
                game_init=self.play_pause_option_status_list[self.option_status_list_index][7]

            if self.option_position == 3:#play end
                IS_MENU=self.play_end_option_status_list[self.option_status_list_index][0]
                IS_PLAY=self.play_end_option_status_list[self.option_status_list_index][1]
                IS_END=self.play_end_option_status_list[self.option_status_list_index][2]
                IS_RETRY=self.play_end_option_status_list[self.option_status_list_index][3]
                menu_init=self.play_end_option_status_list[self.option_status_list_index][4]
                game_init=self.play_end_option_status_list[self.option_status_list_index][5]

            self.Arrow.kill()
            self.kill()
        
        #release
        if key_pressed[pygame.K_RETURN] == False and RETURN_NEED_RELEASE == 1:
            RETURN_NEED_RELEASE=0

ESC_NEED_RELEASE = 0
class Keyboard_shortcut_list(pygame.sprite.Sprite):#遊戲時的快捷鍵
    #esc暫停,`重來
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = shortcut_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0,0)
        self.stop_time_start = 0
        self.stop_time_finish = 0
        #object
        self.Pause_option = 0
        self.Audio = 0
        self.pause_audio_set_la = 0
        self.pause_audio_set_ra = 0

    def update(self):
        global IS_STOP
        global ESC_NEED_RELEASE
        global TOTAL_PLAY_TIME_start
        global BUTTON_LIST
        global IS_PAUSE
        key_pressed = pygame.key.get_pressed()
        #print(key_pressed[pygame.K_p])
        if key_pressed[pygame.K_ESCAPE] == True and ESC_NEED_RELEASE == 0 and IS_END == 0:#esc暫停
            ESC_NEED_RELEASE=1
            if IS_STOP == 0:
                IS_STOP = 1
                IS_PAUSE = 1
                self.stop_time_start = pygame.time.get_ticks()
                size = 70
                self.Pause_option = Option_list(400,400,3,["continue","retry","back to menu"],size,2)
                all_sprites.add(self.Pause_option)
                self.Audio = Audio_set(990,520)
                all_sprites.add(self.Audio)
                BUTTON_LIST=[]
                self.pause_audio_set_la = Image_button(proportion_left_arrow_imgs,1010,613,-21,0)
                self.pause_audio_set_ra = Image_button(proportion_right_arrow_imgs,1110,613,-22,0)
                all_sprites.add(self.pause_audio_set_la)
                BUTTON_LIST.append(self.pause_audio_set_la)
                all_sprites.add(self.pause_audio_set_ra)
                BUTTON_LIST.append(self.pause_audio_set_ra)
            
            else:#暫停結束
                IS_STOP = 0
                self.stop_time_finish = pygame.time.get_ticks()
                TOTAL_PLAY_TIME_start += (self.stop_time_finish - self.stop_time_start)
                self.Pause_option.Arrow.kill()
                self.Pause_option.kill()
                self.Audio.kill()
                self.pause_audio_set_la.kill()
                self.pause_audio_set_ra.kill()

        #release
        if key_pressed[pygame.K_ESCAPE] == False and ESC_NEED_RELEASE == 1:
            ESC_NEED_RELEASE=0

class Audio_set(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = sound_img
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.right_need_release = 0
        self.left_need_release = 0
        #self.left_arrow_box = pygame.Rect(self.rect.left-100, self.rect.top-100, self.rect.width,self.rect.height)
        #self.left_arrow_box = pygame.Rect(self.rect.left+100, self.rect.top-100, self.rect.width,self.rect.height)


    def update(self):
        if IS_STOP == 0:
            self.kill()
        global VOLUME
        draw_text(screen,str(VOLUME)+"%",60,self.rect.centerx+128,self.rect.centery-5)
        screen.blit(left_arrow_img,(self.rect.centerx,self.rect.centery+64))
        screen.blit(right_arrow_img,(self.rect.centerx+100,self.rect.centery+64))
        #調整音量(左右鍵)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT] and self.right_need_release == 0 and VOLUME < 100:
            self.right_need_release=1
            VOLUME += 5
            red_sound.set_volume(VOLUME/100)
            blue_sound.set_volume(VOLUME/100)

        if key_pressed[pygame.K_LEFT] and self.left_need_release == 0 and VOLUME > 0:
            self.left_need_release=1
            VOLUME -= 5
            red_sound.set_volume(VOLUME/100)
            blue_sound.set_volume(VOLUME/100)

        #release
        if key_pressed[pygame.K_RIGHT] == False and self.right_need_release == 1:
            self.right_need_release=0
        if key_pressed[pygame.K_LEFT] == False and self.left_need_release == 1:
            self.left_need_release=0
    
    #def click(self):
    #    pass

class Clock(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = clock_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #self.rect.center = (x,y)
        self.x=x
        self.y=y
        self.start_time = pygame.time.get_ticks()
        #print(self.start_time)
        self.pause_start = pygame.time.get_ticks()
        self.pause_finish = pygame.time.get_ticks()
        #self.time_length = time_length_sec
        self.is_stop = 1
        self.text=""
        self.now = pygame.time.get_ticks()
        #print(self.now)
        #print()

    def update(self):
        #if IS_MENU==1:
        #    #print(1)
        #    self.kill()
        if self.is_stop == 0:
            self.now = pygame.time.get_ticks()  # - (self.pause_finish - self.pause_start)
            
            self.text=time_transform(int((self.now-self.start_time)/1000))
        else:
            self.pause_finish = pygame.time.get_ticks()
        draw_text(screen,self.text,50,self.x,self.y)
        
        if IS_END == 1:
            self.pause()
        
        #print(pygame.time.get_ticks(),self.start_time,self.now, self.pause_start,self.pause_finish)
    
    def pause(self):
        self.is_stop = 1
        self.pause_start = pygame.time.get_ticks()
    
    def play(self):
        self.is_stop = 0
        self.start_time += (self.pause_finish - self.pause_start)
        #print(self.start_time,self.now)
class Map(pygame.sprite.Sprite):
    def __init__(self,barline_list,note_list,bpm,time,is_new,mapid):
        global MAPID_SEED
        self.id=0
        if is_new:
            self.id=MAPID_SEED
            MAPID_SEED+=1
        else:
            self.id=int(mapid)
        self.bpm = bpm
        self.time=time
        self.barline_list = []
        i=0
        while i<len(barline_list):
            self.barline_list.append(barline_list[i])
            i+=1
        
        self.note_list=[]
        i=0
        while i<len(note_list):
            self.note_list.append(note_list[i])
            i+=1
        
    def update(self):
        pass

#class Pre_construct(pygame.sprite.Sprite):
#    def __init__(self):
#        global IS_BUILD
#        global USE_FPS
#        IS_BUILD = 1
#        USE_FPS = 0
#        pygame.sprite.Sprite.__init__(self)
#        self.image = pre_dot_img #轉換圖片大小,(圖片,像素)(已改)
#        self.image.set_colorkey(BLACK)#把黑色的部分變透明
#        self.rect = self.image.get_rect()#屬性2,定位圖片位置,把圖片框起來,就能設定位置相關數據
#        #self.radius = 20#半徑
#        #self.rect.y = NOTE_Y
#        #self.rect.x = 100
#        self.speedx = PRE_SPEED
#        self.rect.center = (PRE_CENTER,NOTE_Y)
#        self.f=1
#        self.lb_need_release=0
#        self.lr_need_release=0
#        self.rr_need_release=0
#        self.rb_need_release=0
#        
#        self.possible_note_count=0
#        self.total_note_count=0
#        self.red_note_count=0
#        self.blue_note_count=0
#        
#        self.total_time_start=pygame.time.get_ticks()
#        self.bpm_count_start=pygame.time.get_ticks()
#        #self.rect.centerx = WIDTH/2
#        #self.rect.bottom = HEIGHT - 10
#
#        #小節線plan a
#        #bl_born_posi_list = barline_position_calculate(ori_BPM/4,PRE_END_CENTER)
#        #i=0
#        #while i<len(bl_born_posi_list):
#        #    new_barline(bl_born_posi_list[i],NOTE_Y)
#        #    i+=1
#
#        #小節線plan b
#        self.barline_posi_count = 0
#
#    def update(self):#更新函式
#        global IS_STOP
#        #global FPS
#        global TOTAL_PLAY_TIME_start
#        global POSSIBLE_NOTE
#        global TOTAL_NOTE
#        global RED_NOTE
#        global BLUE_NOTE
#        global BUILD_TIME_COST
#        global USE_FPS
#        global IS_BUILD
#        self.rect.x -= self.speedx
#        #小節線plan b
#        self.barline_posi_count += 1
#        if self.barline_posi_count == BARLINE:
#            new_barline(self.rect.center[0],self.rect.center[1])
#            self.barline_posi_count = 0
#        #預先生成note
#        now=pygame.time.get_ticks()
#        bpm_count_finish=now
#        #if bpm_count_finish-self.bpm_count_start>=TIME:#bpm
#        self.possible_note_count+=1
#        self.bpm_count_start=bpm_count_finish
#        note_seed=random.randint(0,2)
#        if note_seed == 0:
#            self.total_note_count += 1
#            self.red_note_count += 1
#            new_note("red",self.rect.center[0],self.rect.center[1])
#        if note_seed == 1:
#            self.total_note_count += 1
#            self.blue_note_count += 1
#            new_note("blue",self.rect.center[0],self.rect.center[1])
#        if self.rect.x < PRE_END_CENTER:
#            IS_STOP=0
#            #FPS=60
#            USE_FPS=1
#            IS_BUILD=0
#            total_time_finish=pygame.time.get_ticks()
#            TOTAL_PLAY_TIME_start=pygame.time.get_ticks()
#            POSSIBLE_NOTE=f"possible notes: {self.possible_note_count}"
#            TOTAL_NOTE=f"total notes: {self.total_note_count}"
#            RED_NOTE=f"red notes: {self.red_note_count}"
#            BLUE_NOTE=f"blue notes: {self.blue_note_count}"
#            BUILD_TIME_COST=f"build time cost: {(total_time_finish-self.total_time_start)/1000}s"
#            self.kill()

def random_color():
    seed=random.randint(0,1)
    color = ""
    if seed == 0:
        color = "red"
    else:
        color = "blue"
    return color

RETRY_NOTE_LIST=[]
RETRY_BARLINE_LIST=[]
NOTE_TYPE_LIST = []#0=no note, 1=1/4, 2=1/6
def pre_construct():
    global IS_BUILD
    IS_BUILD = 1
    global IS_STOP
    global TOTAL_PLAY_TIME_start
    global POSSIBLE_NOTE
    global TOTAL_NOTE
    global RED_NOTE
    global BLUE_NOTE
    global BUILD_TIME_COST
    global RETRY_NOTE_LIST
    global RETRY_BARLINE_LIST
    global ONE_SIXTH_NEED_NUM
    global NOTE_TYPE_LIST
    IS_STOP = 1
    global PRE_SPEED
    global NOTE_LIST
    NOTE_LIST=[]
    #1/6
    if IS_ONE_SIXTH == 1 and IS_RETRY == 0:
        PRE_SPEED *= (2/3)
    speedx = PRE_SPEED
    

    rect_center = [PRE_CENTER,NOTE_Y]
    
    possible_note_count=0
    total_note_count=0
    red_note_count=0
    blue_note_count=0
    total_time_start=pygame.time.get_ticks()
    barline_posi_count = 0
    if IS_RETRY==1:
        map_save()
    i=0
    while IS_RETRY==1 and i<len(RETRY_BARLINE_LIST):
        new_barline(RETRY_BARLINE_LIST[i][0],RETRY_BARLINE_LIST[i][1])
        i+=1
    i=0
    while IS_RETRY==1 and i<len(RETRY_NOTE_LIST):
        new_note(RETRY_NOTE_LIST[i][0],RETRY_NOTE_LIST[i][1],RETRY_NOTE_LIST[i][2])
        i+=1

    if IS_RETRY==0:
        NOTE_TYPE_LIST=[]
        RETRY_NOTE_LIST=[]
        RETRY_BARLINE_LIST=[]

    while IS_RETRY==0:#生成新note&barline並記錄到retrylist裡
        rect_center[0] -= speedx
        #小節線plan b
        barline_posi_count += 1
        if barline_posi_count == BARLINE:
            new_barline(rect_center[0],rect_center[1])
            RETRY_BARLINE_LIST.append([rect_center[0],rect_center[1]])
            barline_posi_count = 0
        #預先生成note 
        possible_note_count+=1
        note_seed=random.randint(1,100)
        if note_seed >= 1 and note_seed <= POSSIBILITY_RED_RIGHT:#red
            total_note_count += 1
            red_note_count += 1
            if IS_ONE_FOURTH == 1 or IS_ONE_SIXTH == 1:
                new_note("red",rect_center[0],rect_center[1])
            if IS_ONE_FOURTH_AND_ONE_SIXTH == 1:
                NOTE_TYPE_LIST.append(1)
            RETRY_NOTE_LIST.append(["red",rect_center[0],rect_center[1]])
            
        elif note_seed >= POSSIBILITY_BLUE_LEFT and note_seed <= POSSIBILITY_BLUE_RIGHT:#blue
            total_note_count += 1
            blue_note_count += 1
            if IS_ONE_FOURTH == 1 or IS_ONE_SIXTH == 1:
                new_note("blue",rect_center[0],rect_center[1])
            if IS_ONE_FOURTH_AND_ONE_SIXTH == 1:
                NOTE_TYPE_LIST.append(1)
            RETRY_NOTE_LIST.append(["blue",rect_center[0],rect_center[1]])
            
        else:#no note
            if IS_ONE_FOURTH_AND_ONE_SIXTH == 1:
                NOTE_TYPE_LIST.append(0)
            RETRY_NOTE_LIST.append(["none",0,0])
        if rect_center[0] < PRE_END_CENTER:
            POSSIBLE_NOTE=f"possible notes: {possible_note_count}"
            TOTAL_NOTE=f"total notes: {total_note_count}"
            RED_NOTE=f"red notes: {red_note_count}"
            BLUE_NOTE=f"blue notes: {blue_note_count}"
            break
    
    #1/4 + 1/6
    if IS_ONE_FOURTH_AND_ONE_SIXTH == 1 and IS_RETRY == 0:
        #calculate ONE_SIXTH_NEED_NUM
        one_fourth_num = 0
        i=0
        while i<len(NOTE_TYPE_LIST):
            if NOTE_TYPE_LIST[i]==1:
                one_fourth_num += 1
            i+=1
        ONE_SIXTH_NEED_NUM = one_fourth_num / 10 * ONE_SIXTH_PROPORTION
        one_six_num = 0
        possible_min_group_num = 0#min 1/6 group num
        one_sixth_group_num = 0
        note_combo = 0
        #calculate min 1/6 group num
        i=0
        while i<len(NOTE_TYPE_LIST):
            if NOTE_TYPE_LIST[i] == 0:
                if note_combo >= 5:
                    possible_min_group_num += 1
                    left_num = (note_combo-5) // 9 #oooo xxxxx, oooo xxxxx, oooo xxxxx, ...
                    #print
                    possible_min_group_num += left_num
                note_combo = 0

            if NOTE_TYPE_LIST[i] == 1:
                note_combo += 1
            i+=1
        try_times_limit = len(NOTE_TYPE_LIST)
        try_time = 0
        
        while one_six_num < ONE_SIXTH_NEED_NUM and try_time < try_times_limit:#1/6 change
            #4notes or 7notes
            one_sixth_type_seed = random.randint(1,10)
            next_note_need_num = 0
            if one_sixth_type_seed >= 1 and one_sixth_type_seed <= FOUR_NOTES_PROPORTION:#4notes
                next_note_need_num = 2
            else:#7notes
                next_note_need_num = 4
            
            #random 1/6 position
            random_index = random.randint(0,len(NOTE_TYPE_LIST)-5)
            while NOTE_TYPE_LIST[random_index] != 1:
                random_index = random.randint(0,len(NOTE_TYPE_LIST)-5)
            
            #check if can change
            can_change = 1
            i=0
            while i<next_note_need_num:
                if NOTE_TYPE_LIST[random_index+i+1]!=1:
                    can_change=0
                    break
                i+=1
            
            #change
            if can_change == 1:
                #print(RETRY_NOTE_LIST)
                NOTE_TYPE_LIST[random_index]=2#1/6 note
                NOTE_TYPE_LIST[random_index + next_note_need_num]=2#1/6 note
                distance = RETRY_NOTE_LIST[random_index][1] - RETRY_NOTE_LIST[random_index + next_note_need_num][1]#note interval 
                #print(distance)
                distance_divided = 0
                del_num = 0
                one_six_num_add = 0
                insert_num = 0
                if next_note_need_num == 2:#4notes
                    distance_divided = 3
                    del_num = 1
                    one_six_num_add = 3
                    insert_num = 3
                    #new_note("blue",RETRY_NOTE_LIST[random_index + next_note_need_num][1],200)

                if next_note_need_num == 4:#7notes
                    distance_divided = 6
                    del_num = 3
                    one_six_num_add = 5
                    insert_num = 6
                    #new_note("blue",RETRY_NOTE_LIST[random_index + next_note_need_num][1],400)
                
                start_x = RETRY_NOTE_LIST[random_index ][1]
                y = RETRY_NOTE_LIST[random_index][2]
                single_distance = distance / distance_divided

                #del note between "random_index" and "random_index + next_note_need_num"
                i=0
                
                while i<del_num:
                    
                    del RETRY_NOTE_LIST[random_index + 1]
                    del NOTE_TYPE_LIST[random_index + 1]
                    i+=1
                
                start_index = random_index + 1 #insert index
                i=0
                while i<insert_num:#insert
                    #random color
                    color=""
                    note_seed = random.randint(0,1)
                    if note_seed == 0:#red
                        color = "red"
                    else:#blue
                        color = "blue"
                    #if next_note_need_num == 2:
                    #    new_note("blue",RETRY_NOTE_LIST[random_index + next_note_need_num][1],200)
                    RETRY_NOTE_LIST.insert(start_index,[color,start_x - (single_distance * i+1),y])
                    NOTE_TYPE_LIST.insert(start_index,2)#1/6 note
                    start_index+=1
                    i+=1
                #if next_note_need_num == 2:
                #    color = random_color()
                #    RETRY_NOTE_LIST.insert(start_index,[color,start_x - (single_distance),y])
                #    NOTE_TYPE_LIST.insert(start_index,2)#1/6 note

                
                one_six_num += one_six_num_add
                one_sixth_group_num += 1
            
            if one_sixth_group_num >= possible_min_group_num and can_change == 0:#達到最小組數量後才開始算,防止運氣不好明明還有但連續試不中的情況
                try_time += 1
            if one_sixth_group_num >= possible_min_group_num and can_change == 1:#達到最小組數量後才開始算,防止運氣不好明明還有但連續試不中的情況
                try_time = 0
            #print(one_sixth_group_num,possible_min_group_num)
        
        i=0
        total_note_count = 0
        red_note_count = 0
        blue_note_count = 0
        while i<len(RETRY_NOTE_LIST):
            new_note(RETRY_NOTE_LIST[i][0],RETRY_NOTE_LIST[i][1],RETRY_NOTE_LIST[i][2])
            if NOTE_TYPE_LIST[i] != 0:
                total_note_count += 1
            if RETRY_NOTE_LIST[i][0] == "red":
                red_note_count += 1
            if RETRY_NOTE_LIST[i][0] == "blue":
                blue_note_count += 1
            i+=1
        
        POSSIBLE_NOTE=f"possible notes: {len(NOTE_TYPE_LIST)}"
        TOTAL_NOTE=f"total notes: {total_note_count}"
        RED_NOTE=f"red notes: {red_note_count}"
        BLUE_NOTE=f"blue notes: {blue_note_count}"
                
    #construct finish
    IS_STOP=0
    IS_BUILD=0
    total_time_finish=pygame.time.get_ticks()
    TOTAL_PLAY_TIME_start=pygame.time.get_ticks()
    BUILD_TIME_COST=f"build time cost: {(total_time_finish-total_time_start)/1000}s"

class Setting(pygame.sprite.Sprite):#設定
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pre_dot_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (PRE_END_CENTER,NOTE_Y)

        self.stop_need_release = 0 #p暫停
        self.auto_need_release = 0 #auto mode

        self.stop_time_start = 0
        self.stop_time_finish = 0

        self.first_stop_ignore = 1

    def update(self):#更新函式
        global IS_STOP
        global IS_AUTO
        global TOTAL_PLAY_TIME_start
        global P_NEED_RELEASE
        key_pressed = pygame.key.get_pressed()
        #print(key_pressed[pygame.K_p])
        if key_pressed[pygame.K_p] == True and P_NEED_RELEASE == 0:
            if IS_STOP==0:
                IS_STOP=1
                self.stop_time_start = pygame.time.get_ticks()
            else:
                IS_STOP=0
                self.stop_time_finish = pygame.time.get_ticks()
                TOTAL_PLAY_TIME_start += (self.stop_time_finish - self.stop_time_start)
            #self.stop_need_release=1
            P_NEED_RELEASE=1

        if IS_STOP==1:#暫停後的設定介面
            if key_pressed[pygame.K_TAB] == True and self.auto_need_release == 0:#auto mode
                if IS_AUTO == 0:
                    IS_AUTO=1
                else:
                    IS_AUTO=0
                self.auto_need_release=1

        #release
        if key_pressed[pygame.K_p] == False and P_NEED_RELEASE == 1:
            P_NEED_RELEASE=0
        if key_pressed[pygame.K_TAB] == False and self.auto_need_release == 1:
            self.auto_need_release=0

IS_PLAY=0
IS_MENU=1
IS_SETTING=0
INPUT_BOX_LIST=[]
BUTTON_LIST=[]
AUDIO_LIST=[]
snum=0
game_clock = Clock(1200,45)
while running:
    if USE_FPS == 1:
        clock.tick(FPS)
    
    #畫面顯示
    screen.fill(BLACK)#設定顏色(r,g,b)
    screen.blit(background_img,(0,0))#bilt()畫,(要畫的圖片,要畫的位置)#####底,要顯示的東西放在這後面
    for event in pygame.event.get():#pygame.event.get()回傳現在發生的所有事件,ex:滑鼠滑到哪或鍵盤按了甚麼按鍵,回傳列表
        if event.type == pygame.QUIT:#偵測事件類型是否把遊戲關閉
            #setting_sav()
            running=False
        
        if IS_SETTING == 1:#設定區的事件偵測
            if event.type == pygame.MOUSEBUTTONDOWN:#當按下滑鼠按鍵時
                
                i=0
                while i<len(INPUT_BOX_LIST):#輸入框事件偵測
                    if INPUT_BOX_LIST[i].input_box.collidepoint(event.pos):#當鼠標位置在輸入框內時
                        INPUT_BOX_LIST[i].text = ""
                        INPUT_BOX_LIST[i].active = True   
                    else:
                        INPUT_BOX_LIST[i].active = False
                        INPUT_BOX_LIST[i].text_save()
                    i+=1
                
                i=0
                while i<len(BUTTON_LIST):#按鈕事件偵測
                    if BUTTON_LIST[i].button_box.collidepoint(event.pos):#當鼠標位置在按鈕內時
                        BUTTON_LIST[i].click()
                    i+=1
                    
                    
            if event.type == pygame.KEYDOWN:
                i=0
                while i<len(INPUT_BOX_LIST):#輸入框事件偵測
                    if INPUT_BOX_LIST[i].active:
                        if event.key == pygame.K_RETURN:
                            INPUT_BOX_LIST[i].active = False
                            INPUT_BOX_LIST[i].text_save()
                            
                        elif event.key == pygame.K_BACKSPACE:
                            INPUT_BOX_LIST[i].text = INPUT_BOX_LIST[i].text[:-1]
                        elif len(INPUT_BOX_LIST[i].text) < 9:
                            INPUT_BOX_LIST[i].text += event.unicode
                    i+=1
        if IS_PLAY == 1:#遊戲區事件偵測
            if event.type == pygame.MOUSEBUTTONDOWN:#當按下滑鼠按鍵時
                
                i=0
                while i<len(BUTTON_LIST):#按鈕事件偵測
                    if BUTTON_LIST[i].button_box.collidepoint(event.pos):#當鼠標位置在按鈕內時
                        BUTTON_LIST[i].click()
                    i+=1

            
    if IS_MENU==1:#主畫面
        if menu_init:
            AUDIO_LIST=[]
            menu_init = False
            menu_sprites = pygame.sprite.Group()
            #a = Arrow(WIDTH/2-125,350,1)
            #menu_sprites.add(a)
            op_names = ["start","setting","quit"]
            size = 85
            opx=450
            opy=340
            option = Option_list(opx,opy,3,op_names,size,0)
            menu_sprites.add(option)
            #newsnum=len(BUTTON_LIST)
            #print(snum,newsnum)



        menu_sprites.update()
        menu_sprites.draw(screen)
        draw_menu_info()
        newsnum=len(BUTTON_LIST)
        #if newsnum != snum:
        #    print(snum,newsnum)
        #menu_option()

    if IS_SETTING==1:
        if setting_init:
            AUDIO_LIST=[]
            setting_init = False
            setting_sprites = pygame.sprite.Group()
            bpm_input_box = Input_num_box("BPM:",300,40,ori_BPM,50,False,300,1,"(1~300)")
            time_input_box = Input_num_box("TIME: ~",700,40,PLAYTIME,50,True,300,1,"(1~300) (s)")
            setting_sprites.add(bpm_input_box)
            setting_sprites.add(time_input_box)
            INPUT_BOX_LIST=[]
            INPUT_BOX_LIST.append(bpm_input_box)
            INPUT_BOX_LIST.append(time_input_box)

            at_button=Image_button(at_imgs,350,175,0,AT_STATUS)
            setting_sprites.add(at_button)
            ez_button=Image_button(ez_imgs,500,175,1,EZ_STATUS)
            setting_sprites.add(ez_button)
            hr_button=Image_button(hr_imgs,650,175,2,HR_STATUS)
            setting_sprites.add(hr_button)
            BUTTON_LIST=[]
            BUTTON_LIST.append(at_button)
            BUTTON_LIST.append(ez_button)
            BUTTON_LIST.append(hr_button)

            one_fourth_button=Image_button(one_fourth_imgs,350,300,3,IS_ONE_FOURTH)
            setting_sprites.add(one_fourth_button)
            one_fourth_one_sixth_button=Image_button(one_fourth_one_sixth_imgs,500,305,4,IS_ONE_FOURTH_AND_ONE_SIXTH)
            setting_sprites.add(one_fourth_one_sixth_button)
            one_sixth_button=Image_button(one_sixth_imgs,650,300,5,IS_ONE_SIXTH)
            setting_sprites.add(one_sixth_button)
            BUTTON_LIST.append(one_fourth_button)
            BUTTON_LIST.append(one_fourth_one_sixth_button)
            BUTTON_LIST.append(one_sixth_button)

            back_button = Image_button(back_imgs,117,675,-1,False)
            setting_sprites.add(back_button)
            BUTTON_LIST.append(back_button)

            ofos_la = Image_button(proportion_left_arrow_imgs,1085,260,41,0)
            ofos_ra = Image_button(proportion_right_arrow_imgs,1235,260,42,0)
            setting_sprites.add(ofos_la)
            BUTTON_LIST.append(ofos_la)
            setting_sprites.add(ofos_ra)
            BUTTON_LIST.append(ofos_ra)

            fnsn_la = Image_button(proportion_left_arrow_imgs,1085,340,43,0)
            fnsn_ra = Image_button(proportion_right_arrow_imgs,1235,340,44,0)
            setting_sprites.add(fnsn_la)
            BUTTON_LIST.append(fnsn_la)
            setting_sprites.add(fnsn_ra)
            BUTTON_LIST.append(fnsn_ra)

            notes_density_la = Image_button(proportion_left_arrow_imgs,340,425,31,0)
            notes_density_ra = Image_button(proportion_right_arrow_imgs,510,425,32,0)
            setting_sprites.add(notes_density_la)
            BUTTON_LIST.append(notes_density_la)
            setting_sprites.add(notes_density_ra)
            BUTTON_LIST.append(notes_density_ra)

            audio_set_la = Image_button(proportion_left_arrow_imgs,340,540,-21,0)
            audio_set_ra = Image_button(proportion_right_arrow_imgs,510,540,-22,0)
            setting_sprites.add(audio_set_la)
            BUTTON_LIST.append(audio_set_la)
            setting_sprites.add(audio_set_ra)
            BUTTON_LIST.append(audio_set_ra)
            #.kill並不會將列表中元素刪除,要另外用del才可以
            


        draw_text(screen,"setting",75,125,50)
        draw_text(screen,"mods:",60,125,175)
        draw_text(screen,"type:",60,125,300)
        screen.blit(mini_one_fourth_one_sixth_img,(760,280))
        draw_text(screen,"set:",45,850,300)
        draw_text(screen,"(1/4 : 1/6):",45,960,260)
        draw_text(screen,str(ONE_FOURTH_PROPORTION)+" : "+str(ONE_SIXTH_PROPORTION),50,1160,260)
        #draw_text(screen,"",40,560,130)
        draw_text(screen,"(4notes : 7notes):",30,960,340)
        draw_text(screen,str(FOUR_NOTES_PROPORTION)+" : "+str(SEVEN_NOTES_PROPORTION),50,1160,340)
        draw_text(screen,"notes density:",45,125,425)
        draw_text(screen,str(POSSIBILITY_LIST[POSSIBILITY_INDEX])+" %",50,425,425)
        screen.blit(sound_img,(70,475))
        draw_text(screen,str(VOLUME)+" %",50,425,540)

        setting_sprites.update()
        setting_sprites.draw(screen)
        #newsnum=len(BUTTON_LIST)
        #if newsnum != snum:
        #    print(snum,newsnum)

    if IS_PLAY==1:
        if game_init:
            #print("game init")
            AUDIO_LIST=[]
            BUTTON_LIST=[]
            ##################################################
            if EZ_STATUS == 1:
                MODS_INDEX = 1
            elif HR_STATUS == 1:
                MODS_INDEX = 2
            else:
                MODS_INDEX = 0
            SPEED = ori_BPM / MODS[MODS_INDEX] #流速sv 1s移動 SPEED像素*FPS(60), 60s => SPEED*3600 #5=hr,10=nm,15=ez
            #speed=2.5, 1min, 9000格
            #speed=10, 1min, 36000格
            BPM = ori_BPM *multi #原始為1/1(四分音符)
            BARLINE = 4 *multi #原始為1/1(四拍四分音符(全音音符)), bpm*多少BARLINE就*多少
            DISTANCE = SPEED*FPS*PLAYTIME #pre_construct跑的總距離 (生成區總長) #每次移動距離*每秒更新次數*總遊玩秒數 = 總遊玩時間的移動距離
            PRE_SPEED = DISTANCE/(BPM/(60/PLAYTIME)) #生成點間距
            PRE_CENTER = PRE_END_CENTER + DISTANCE #生成區右邊線
            #音符密度(出現機率)
            POSSIBILITY = POSSIBILITY_LIST[POSSIBILITY_INDEX]
            POSSIBILITY_RED_RIGHT = POSSIBILITY/2
            POSSIBILITY_BLUE_LEFT = POSSIBILITY_RED_RIGHT+1
            POSSIBILITY_BLUE_RIGHT = POSSIBILITY
            ##################################################
            #print(DISTANCE,PRE_SPEED)
            all_sprites = pygame.sprite.Group()
            notes = pygame.sprite.Group()
            barlines = pygame.sprite.Group()
            circles = pygame.sprite.Group()
            circle = Circle()
            circles.add(circle)
            all_sprites.add(circle)
            game_sc = Keyboard_shortcut_list()
            all_sprites.add(game_sc)
            pre_construct()
            game_clock.kill()
            game_clock = Clock(1200,45)
            all_sprites.add(game_clock)
            game_clock.play()
            #close = draw_init()
            #if close:
            #    break
            game_init = False
            
            endbarline = End_barline()
            all_sprites.add(endbarline)

            #pre_const = Pre_construct()
            #all_sprites.add(pre_const)

            #set = Setting()
            #all_sprites.add(set)

            hits = pygame.sprite.Group()

            COMBO = 0
            #print(f"{FPS}:{SPEED}")
        
        #mods img
        if AT_STATUS == 1:
            screen.blit(at_inactive_img,(650,100))
        if EZ_STATUS == 1:
            screen.blit(ez_inactive_img,(750,100))
        if HR_STATUS == 1:
            screen.blit(hr_inactive_img,(850,100))
        if IS_ONE_FOURTH == 1:
            screen.blit(one_fourth_inactive_img,(950,100))
        if IS_ONE_FOURTH_AND_ONE_SIXTH == 1:
            screen.blit(one_fourth_one_sixth_inactive_img,(1050,100))
        if IS_ONE_SIXTH == 1:
            screen.blit(one_sixth_inactive_img,(1150,100))
        
        if IS_STOP == 1:
            if pause_init == True:
                pause_init = False
                game_clock.pause()
                
        if IS_STOP == 0 and pause_init == False:
            pause_init = True
            game_clock.play()



        screen.blit(donchan_img,(50,15))#donchan

        #取得輸入
        #key_pressed = pygame.key.get_pressed()
        #if key_pressed[pygame.K_SPACE]:#判斷右鍵是否有被按下
        #    player.shoot()

        #for event in pygame.event.get():#pygame.event.get()回傳現在發生的所有事件,ex:滑鼠滑到哪或鍵盤按了甚麼按鍵,回傳列表
        #    if event.type == pygame.QUIT:#偵測事件類型是否把遊戲關閉
        #        running=False
        
        #    
        #    if event.type == pygame.KEYDOWN:#判斷事件是否為"按下"按鍵
        #        if event.key == pygame.K_SPACE:#如果是空白鍵就發射子彈
        #            player.shoot()

        #更新遊戲
        
        all_sprites.update()#執行群組內每一個物件的update函式
        
        #hits = pygame.sprite.groupcollide(notes,bullets,True,True)#判斷碰撞,以及碰撞後該物件是否要刪除,回傳字典,包含碰撞到的物件
        #note_seed=random.randint(0,99)
        #if note_seed == 0:
        #    note = new_note("red")
        #if note_seed == 1:
        #    note = new_note("blue")

        #for hit in hits:#碰撞刪除後補充物件
        #    random.choice(expl_sound).play()
        #    score += hit.radius
        #    expl = Explosion(hit.rect.center,'lg')
        #    all_sprites.add(expl)
        #    if random.random() > 0.95:
        #        powe = Power(hit.rect.center)
        #        all_sprites.add(powe)
        #        powers.add(powe)
        #    new_rock()

        #碰撞到就扣血
        #hits = pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle)#將碰撞判斷從預設的矩形改成圓形,要給半徑(radius)
        #for hit in hits:
        #    new_rock()
        #    player.health -= hit.radius
        #    expl = Explosion(hit.rect.center,'sm')
        #    all_sprites.add(expl)
        #    if player.health <= 0:#死亡
        #        death_expl = Explosion(player.rect.center,'player')
        #        all_sprites.add(death_expl)
        #        die_sound.play()
        #        player.lives -= 1
        #        player.health = 100
        #        player.hide()#緩衝一段時間後再復活
        #        #running = False

        #寶物飛船相撞
        #hits = pygame.sprite.spritecollide(player,powers,True)
        #for hit in hits:
        #    if hit.type == 'shield':
        #        player.health += 20
        #        if player.health > 100:
        #            player.health = 100
        #        shield_sound.play()
        #    elif hit.type == 'gun':
        #        player.gunup()
        #        gun_sound.play()


        #if player.lives == 0 and not(death_expl.alive()):#讓最後一次動畫撥放完再結束
        #    game_init = True

        all_sprites.draw(screen)#將群組內所有sprite物件畫到螢幕上
        draw_text(screen,str(COMBO),70,COMBO_X,COMBO_Y)#印出combo
        game_info()#印出bpm,time
        if IS_END == 1:
            end_info()
            #size = 70
            #opx=800
            #opy=350
            #end_option = Option_list(opx,opy,2,["retry","back"],size,3)
            #all_sprites.add(end_option)

        #if IS_STOP == 1 and IS_BUILD == 0:
        #    #screen.blit(pause_img,(0,0))
        #    draw_pause()
        #draw_health(screen,player.health,5,15)#印出生命條
        #draw_lives(screen,player.lives,player_mini_img,WIDTH-100,15)
    pygame.display.update()#更新畫面
setting_sav()
#end_info()