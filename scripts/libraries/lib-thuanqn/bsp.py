# BOARD SUPPORT PACKAGE

import cfg
from pyb import LED
from pyb import Pin
from machine import I2C
import sensor
import uos

from libs import ssd1306
from libs import writer
from libs import freesans20

# ALL LEDs
# DEFINES
# LED RGB + IR
LED_R = LED(1)
LED_G = LED(2)
LED_B = LED(3)
LED_IR = LED(4)

# LED 0 ~ 4
# LED 0: P0 - Red 
# LED 1: P1 - Yellow 
# LED 3: P2 - Green 
# LED 3: P3 - Blue 
# LED 4: P6 - Red 
LED_0 = Pin('P0', Pin.OUT_PP)
LED_1 = Pin('P1', Pin.OUT_PP)
LED_2 = Pin('P2', Pin.OUT_PP)
LED_3 = Pin('P3', Pin.OUT_PP)
LED_4 = Pin('P6', Pin.OUT_PP)

# FUNCTIONS
def ld_init():
    ''' LED init '''
    ld0_off()
    ld1_off()
    ld2_off()
    ld3_off()
    ld4_off()

def ld_on(led):
    ''' LED on '''
    if (led == LED_R) or (led == LED_G) or (led == LED_B) or (led == LED_IR):
        led.on()
    else:
        led.low()

def ld_off(led):
    ''' LED off '''
    if (led == LED_R) or (led == LED_G) or (led == LED_B) or (led == LED_IR):
        led.off()
    else:
        led.high()

def ld_tog(led):
    ''' LED toggle '''
    if (led == LED_R) or (led == LED_G) or (led == LED_B) or (led == LED_IR):
        led.toggle()
    else:
        if led.value() == 1:
            led.value(0)
        else:
            led.value(1)

def ldr_on():
    ''' LED RED on '''    
    LED_R.on()

def ldr_off():
    ''' LED RED off '''    
    LED_R.off()

def ldr_tog():
    ''' LED RED toggle '''    
    LED_R.toggle()

def ldg_on():
    ''' LED GREEN on '''    
    LED_G.on()

def ldg_off():
    ''' LED GREEN off '''    
    LED_G.off()

def ldg_tog():
    ''' LED GREEN toggle '''    
    LED_G.toggle()

def ldb_on():
    ''' LED BLUE on '''    
    LED_B.on()

def ldb_off():
    ''' LED BLUE off '''    
    LED_B.off()

def ldb_tog():
    ''' LED BLUE toggle '''    
    LED_B.toggle()

def ldir_on():
    ''' LED IR on '''    
    LED_IR.on()

def ldir_off():
    ''' LED IR off '''    
    LED_IR.off()

def ldir_tog():
    ''' LED IR toggle '''    
    LED_IR.toggle()

def ld0_on():
    ''' LED 0 on '''    
    LED_0.low()

def ld0_off():
    ''' LED 0 off '''    
    LED_0.high()

def ld0_tog():
    ''' LED 0 toggle '''    
    if LED_0.value() == 1:
        LED_0.value(0)
    else:
        LED_0.value(1)

def ld1_on():
    ''' LED 1 on '''    
    LED_1.low()

def ld1_off():
    ''' LED 1 off '''    
    LED_1.high()

def ld1_tog():
    ''' LED 1 toggle '''    
    if LED_1.value() == 1:
        LED_1.value(0)
    else:
        LED_1.value(1)

def ld2_on():
    ''' LED 2 on '''    
    LED_2.low()

def ld2_off():
    ''' LED 2 off '''    
    LED_2.high()

def ld2_tog():
    ''' LED 2 toggle '''    
    if LED_2.value() == 1:
        LED_2.value(0)
    else:
        LED_2.value(1)

def ld3_on():
    ''' LED 3 on '''    
    LED_3.low()

def ld3_off():
    ''' LED 3 off '''    
    LED_3.high()

def ld3_tog():
    ''' LED 3 toggle '''    
    if LED_3.value() == 1:
        LED_3.value(0)
    else:
        LED_3.value(1)

def ld4_on():
    ''' LED 4 on '''    
    LED_4.low()

def ld4_off():
    ''' LED 4 off '''    
    LED_4.high()

def ld4_tog():
    ''' LED 4 toggle '''    
    if LED_4.value() == 1:
        LED_4.value(0)
    else:
        LED_4.value(1)

# BUZZER
# DEFINES
BUZ = Pin('P7', Pin.OUT_PP)

# FUNCTIONS
def buz_init():
    ''' BUZ init '''
    pass

def buz_on():
    ''' BUZ on '''    
    BUZ.high()

def buz_off():
    ''' BUZ off '''    
    BUZ.low()

def buz_tog():
    ''' BUZ toggle '''    
    if BUZ.value() == 1:
        BUZ.value(0)
    else:
        BUZ.value(1)

# BUTTON
# DEFINES
BTN = Pin('P8', Pin.IN, Pin.PULL_UP)
# BTN1 = Pin('P9', Pin.IN, Pin.PULL_UP) # Spare
BTN_PRESS = 0
BTN_RELEASE = 1
# VARIABLES
btn_stt_1 = BTN_RELEASE
btn_stt_2 = BTN_RELEASE
btn_stt_3 = BTN_RELEASE
btn_stt_latch = BTN_RELEASE
btn_press_flag = 0
btn_long_press_flag = 0
btn_long_press_running = 0
btn_press_timer_flag = 0
btn_press_timer_running = 0
global btn_press_timer_task
btn_nb_click = 0
# FUNCTIONS
def btn_init():
    ''' BTN init '''
    pass

def btn_read():
    ''' BTN read '''
    return BTN.value()

# def BTN1_Read():
#     ''' BTN read '''
#     return BTN1.value()

# OLED
# DEFINES
I2C = I2C(2)
OLED = ssd1306.SSD1306_I2C(128, 32, I2C)
WRITER = writer.Writer(OLED, freesans20)
OLED_DISP_DEL = 0.01 # [mm]
# VARIABLES
oled_disp = [0, 0, 0]
oled_val = 0
# FUNCTIONS
def oled_init():
    ''' OLED init '''
    oled_show("Khoi dong")

def oled_show_dimension(d: float):
    ''' OLED Show Dimmension '''
    OLED.fill(0)
    WRITER.set_textpos(0, 0)
    WRITER.printstring("D =")
    WRITER.set_textpos(40, 0)
    WRITER.printstring(str(d))
    WRITER.set_textpos(93, 0)
    WRITER.printstring("mm")
    OLED.show()

def oled_show_area(d: float):
    ''' OLED Show Area '''
    OLED.fill(0)
    WRITER.set_textpos(0, 0)
    WRITER.printstring("A =")
    WRITER.set_textpos(38, 0)
    WRITER.printstring(str(d))
    WRITER.set_textpos(85, 0)
    WRITER.printstring("mm2")
    OLED.show()

def oled_show_ratio(d: float):
    ''' OLED Show Dimmension '''
    OLED.fill(0)
    WRITER.set_textpos(0, 0)
    WRITER.printstring("R =")
    WRITER.set_textpos(40, 0)
    WRITER.printstring(str(d))
    OLED.show()

def oled_show(s: str):
    OLED.fill(0)
    WRITER.set_textpos(0, 0)
    WRITER.printstring(s)
    OLED.show()


# SENSORS
# DEFINES
RANGE_LENG_MIN = min(cfg.RANGE1_LENG[0],cfg.RANGE2_LENG[0])
RANGE_LENG_MAX = max(cfg.RANGE1_LENG[1],cfg.RANGE2_LENG[1])
RANGE_AREA_MIN = min(cfg.RANGE1_AREA[0],cfg.RANGE2_AREA[0])
RANGE_AREA_MAX = max(cfg.RANGE1_AREA[1],cfg.RANGE2_AREA[1])
OBJ_IDX = 0
CALIB_IDX = 1
# VARIABLES
enable_lens_corr = False # turn on for straighter lines

len_obj = [0, 0, 0]
len_obj_avg = 0
len_obj_new = 0
len_obj_mm = 0

area_obj = [0, 0, 0]
area_obj_avg = 0
area_obj_new = 0
area_obj_mm = 0

ratio = cfg.RATIO_DEFAULT # [mm/pix]
ratio_tmp = 0
idx = OBJ_IDX 

# FUNCTIONS
def sen_init():
    ''' SENSOR init '''
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    if cfg.USE_HD:
        sensor.set_framesize(sensor.HD)
    else:
        sensor.set_framesize(sensor.VGA)
    sensor.skip_frames(time=2000)

    sen_set_auto(False)

def sen_set_auto(val: bool):
    sensor.set_auto_gain(val)
    sensor.set_auto_whitebal(val)

# DATA
# DEFINES
# FUNCTIONS
# ref  https://docs.openmv.io/reference/filesystem.html
# note On the OpenMV Cam the internal flash is mounted at / 
# unless an SDCard is installed which will be moutned at / instead
def check_file():
    try:
        uos.stat("/" + "data.txt")  # Check file exist
        print("File existed!")
    except OSError as e:
        if e.args[0] == 2:  # Check error ENOENT (Errno 2)
            with open("/" + "data.txt", "w") as f:  # Create file
                pass
            print("Create file config data success!")
        else:
            print("Error file config data", e)

def data_save(val):
    check_file()
    with open("/" + "data.txt", "w") as f:
        print(f'Write config data value is: {str(val)}')
        f.write(str(val))

def data_load():
    check_file()
    with open("/" + "data.txt", "r") as f:
        val = f.read()
        return val

# BSP
# DEFINES
# for menu
PAGE_INIT = 0
PAGE_LENG = 1
PAGE_CALIB = 2
PAGE_UPDATE = 3
PAGE_AREA = 4
FLAG_INIT = 0
FLAG_MEASURE = 1
FLAG_CALIB = 2
FLAG_UPDATE = 3
FLAG_AREA = 4
# for state
STT_RESET = 0
STT_NEW = 1
STT_LOW = 2
STT_RANGE1 = 3
STT_RANGE2 = 4
STT_HIGH = 5

# VARIABLES
# for menu
menu = PAGE_INIT
flag = -1
# for state
state = STT_RESET
new_state = 0
# for task
# task_dip = None
# task_btn = None

def bsp_init():
    ''' BSP Init '''
    ld_init()
    buz_init()
    btn_init()
    oled_init()
    sen_init()