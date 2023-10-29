import cfg
import bsp
import dip
import uasyncio

async def obj_tog(fn_tog, delay_ms):
    while True:
        fn_tog()
        await uasyncio.sleep_ms(delay_ms)

async def obj_on(fn_on, fn_off, delay_ms):
    fn_on()
    await uasyncio.sleep_ms(delay_ms)
    fn_off()

async def obj_on_double(fn_on, fn_off, delay_ms):
    fn_on()
    await uasyncio.sleep_ms(delay_ms)
    fn_off()
    await uasyncio.sleep_ms(delay_ms)
    fn_on()
    await uasyncio.sleep_ms(delay_ms)
    fn_off()

async def btn_long_press():
    bsp.btn_long_press_running = 1
    await uasyncio.sleep_ms(cfg.BTN_LONG_CYCLE)
    bsp.btn_long_press_flag = 1
    bsp.btn_long_press_running = 0

async def btn_press():
    while True:
        bsp.btn_stt_1 = bsp.btn_stt_2
        bsp.btn_stt_2 = bsp.btn_stt_3
        bsp.btn_stt_3 = bsp.btn_read()

        if (bsp.btn_stt_3 == bsp.btn_stt_2) and (bsp.btn_stt_2 == bsp.btn_stt_1): # BTN is stable
            if bsp.btn_stt_3 == bsp.BTN_PRESS: # BTN is press
                if bsp.btn_stt_latch == bsp.BTN_RELEASE: # BTN release to press
                    # call btn_long_press()
                    btn_long_press_task = uasyncio.create_task(btn_long_press())
                else: # BTN still press => det_btn_long_press() is running => do nothing
                    pass
            else: # BTN is release
                if bsp.btn_stt_latch == bsp.BTN_PRESS: # BTN press to release
                    if bsp.btn_long_press_running == 1: # if long press still run
                        # stop long press and press, and set flag
                        btn_long_press_task.cancel()
                        bsp.btn_long_press_running = 0 # make sure
                        bsp.btn_press_flag = 1
                    else: # long press is finish => do nothing
                        pass
                else: # BTN still keep release => do nothing
                    pass
            
            bsp.btn_stt_latch = bsp.btn_stt_3 # save new state BTN

        await uasyncio.sleep_ms(cfg.BTN_CYCLE)

async def btn_press_timer():
    bsp.btn_press_timer_running = 1
    bsp.btn_nb_click += 1
    await uasyncio.sleep_ms(cfg.BTN_DELAY)
    bsp.btn_press_timer_flag = 1
    bsp.btn_press_timer_running = 0

async def page_init_():
    bsp.bsp_init()

    if cfg.USE_ONLY_DEFAULT_RATIO:
        bsp.ratio = cfg.RATIO_DEFAULT
    else:
        val = bsp.data_load()
        if val == 0 or val == "":
            bsp.ratio = cfg.RATIO_DEFAULT
        else:
            bsp.ratio = float(val)
    
    print(f'ratio = {bsp.ratio}')

    if cfg.USE_OLED:
        bsp.oled_show("Khoi dong")

    await uasyncio.sleep_ms(1500)

    # Init task dip and btn
    uasyncio.create_task(dip.run())
    uasyncio.create_task(btn_press())    

    bsp.menu = bsp.PAGE_LENG # move to leng page

def page_init():
    pass
    
async def page_leng_():
    bsp.idx = bsp.OBJ_IDX

    if cfg.USE_OLED:
        bsp.oled_show("Do chieu dai")
    
    if cfg.USE_PRINT:
        print('Do chieu dai')

    await uasyncio.sleep_ms(1500)

def display_stable(val):
    if bsp.oled_disp[0] == 0:
        bsp.oled_disp[0] = val 
        return val 
    if bsp.oled_disp[1] == 0:
        if abs(bsp.oled_disp[0] - val) > bsp.OLED_DISP_DEL:
            bsp.oled_disp[1] = val
            return (bsp.oled_disp[0] + bsp.oled_disp[1]) / 2
        else:
            return bsp.oled_disp[0]
    if bsp.oled_disp[2] == 0:
        if abs(bsp.oled_disp[0] - val) > bsp.OLED_DISP_DEL \
            and abs(bsp.oled_disp[1] - val) > bsp.OLED_DISP_DEL:
            bsp.oled_disp[2] = val
            return sum(bsp.oled_disp) / len(bsp.oled_disp)
        else:
            return (bsp.oled_disp[0] + bsp.oled_disp[1]) / 2
    
    del0 = abs(bsp.oled_disp[0] - val)
    del1 = abs(bsp.oled_disp[1] - val)
    del2 = abs(bsp.oled_disp[2] - val)
    if del0 > bsp.OLED_DISP_DEL and del1 > bsp.OLED_DISP_DEL and del2 > bsp.OLED_DISP_DEL:
        if del0 <= del1 and del0 <= del2:
            bsp.oled_disp[0] = val
        elif del1 <= del0 and del1 <= del2:
            bsp.oled_disp[1] = val
        else:
            bsp.oled_disp[2] = val
    
    return sum(bsp.oled_disp) / len(bsp.oled_disp)
    
def page_leng():
    if bsp.btn_press_flag == 1:
        # Reset flag
        bsp.btn_press_flag = 0
        # Call btn_press_timer()
        if bsp.btn_press_timer_running == 0:
            bsp.btn_press_timer_task = uasyncio.create_task(btn_press_timer())
        else:
            bsp.btn_press_timer_task.cancel()
            bsp.btn_press_timer_running = 0 # make sure
            bsp.btn_press_timer_task = uasyncio.create_task(btn_press_timer()) # re-create

        # Handle task => should move btn_nb_click = 1 in btn_press_timer_flag if use n click

    if bsp.btn_long_press_flag == 1:
        # Reset task
        bsp.btn_long_press_flag = 0
        # Handle task
        bsp.menu = bsp.PAGE_AREA # move to page area

    if bsp.btn_press_timer_flag == 1:
        # Reset flag
        bsp.btn_press_timer_flag = 0
        # Handle task
        if bsp.btn_nb_click == 2:
            bsp.menu = bsp.PAGE_CALIB # move to page calib

        bsp.btn_nb_click = 0 
        
    if bsp.state == bsp.STT_LOW:
        # Handle task
        if bsp.new_state == 0:
            uasyncio.create_task(obj_on(bsp.ld4_on, bsp.ld4_off, cfg.LED_DELAY))
        
        if cfg.USE_OLED:
            bsp.oled_val = display_stable(bsp.len_obj_mm)
            # bsp.oled_show_dimension(round(bsp.len_obj_mm, 2))
            bsp.oled_show_dimension(round(bsp.oled_val, 2))

        bsp.new_state = 1
    elif bsp.state == bsp.STT_RANGE1:
        # Handle task
        if bsp.new_state == 0:
            uasyncio.create_task(obj_on(bsp.ld0_on, bsp.ld0_off, cfg.LED_DELAY))
            uasyncio.create_task(obj_on(bsp.buz_on, bsp.buz_off, cfg.BUZ_DELAY))

        if cfg.USE_OLED:
            bsp.oled_val = display_stable(bsp.len_obj_mm)
            # bsp.oled_show_dimension(round(bsp.len_obj_mm, 2))
            bsp.oled_show_dimension(round(bsp.oled_val, 2))

        bsp.new_state = 1
    elif bsp.state == bsp.STT_RANGE2:
        # Handle task
        if bsp.new_state == 0:
            uasyncio.create_task(obj_on(bsp.ld2_on, bsp.ld2_off, cfg.LED_DELAY))
            uasyncio.create_task(obj_on_double(bsp.buz_on, bsp.buz_off, int (cfg.BUZ_DELAY / 3)))

        if cfg.USE_OLED:
            bsp.oled_val = display_stable(bsp.len_obj_mm)
            # bsp.oled_show_dimension(round(bsp.len_obj_mm, 2))
            bsp.oled_show_dimension(round(bsp.oled_val, 2))

        bsp.new_state = 1

    elif bsp.state == bsp.STT_HIGH:
        # Handle task
        if bsp.new_state == 0:
            uasyncio.create_task(obj_on(bsp.ld4_on, bsp.ld4_off, cfg.LED_DELAY))

        if cfg.USE_OLED:
            bsp.oled_val = display_stable(bsp.len_obj_mm)
            # bsp.oled_show_dimension(round(bsp.len_obj_mm, 2))
            bsp.oled_show_dimension(round(bsp.oled_val, 2))

        bsp.new_state = 1
    else: # STT_RESET state
        # Handle task
        if cfg.USE_OLED:
            bsp.oled_disp = [0, 0, 0]
            bsp.oled_show("D = ...")

        bsp.new_state = 0

async def page_calib_():
    bsp.idx = bsp.CALIB_IDX

    if cfg.USE_OLED:
        bsp.oled_show("Hieu chinh")
    
    if cfg.USE_PRINT:
        print('Hieu chinh')

    await uasyncio.sleep_ms(1500)

def page_calib():
    if bsp.btn_press_flag == 1:
        # Reset flag
        bsp.btn_press_flag = 0
        # Call btn_press_timer()
        if bsp.btn_press_timer_running == 0:
            bsp.btn_press_timer_task = uasyncio.create_task(btn_press_timer())
        else:
            bsp.btn_press_timer_task.cancel()
            bsp.btn_press_timer_running = 0 # make sure
            bsp.btn_press_timer_task = uasyncio.create_task(btn_press_timer()) # re-create

        # Handle task => should move btn_nb_click = 1 in btn_press_timer_flag if use n click

    if bsp.btn_long_press_flag == 1:
        # Reset task
        bsp.btn_long_press_flag = 0
        # Handle task
        if cfg.USE_ONLY_DEFAULT_RATIO:
            bsp.menu = bsp.PAGE_LENG # move to page leng
        else:
            bsp.menu = bsp.PAGE_UPDATE # move to page update

    if bsp.btn_press_timer_flag == 1:
        # Reset flag
        bsp.btn_press_timer_flag = 0
        # Handle task
        # if bsp.btn_nb_click == 2:
        #     pass

        bsp.btn_nb_click = 0 

    if bsp.state == bsp.STT_NEW:
        # Handle task        
        if cfg.USE_OLED:
            bsp.oled_show_ratio(round(bsp.ratio_tmp, 4))

async def page_update_():
    bsp.ratio = bsp.ratio_tmp
    bsp.data_save(bsp.ratio)

    if cfg.USE_OLED:
        bsp.oled_show("Da cap nhat")
    
    if cfg.USE_PRINT:
        print('Update ratio: ', bsp.ratio)

    await uasyncio.sleep_ms(1500)

    bsp.menu = bsp.PAGE_LENG  # move to page leng   

def page_update():
    pass

async def page_area_():
    bsp.idx = bsp.OBJ_IDX

    if cfg.USE_OLED:
        bsp.oled_show("Do dien tich")
    
    if cfg.USE_PRINT:
        print('Do dien tich')

    await uasyncio.sleep_ms(1500)

def page_area():
    if bsp.btn_press_flag == 1:
        # Reset flag
        bsp.btn_press_flag = 0
        # Call btn_press_timer()
        if bsp.btn_press_timer_running == 0:
            bsp.btn_press_timer_task = uasyncio.create_task(btn_press_timer())
        else:
            bsp.btn_press_timer_task.cancel()
            bsp.btn_press_timer_running = 0 # make sure
            bsp.btn_press_timer_task = uasyncio.create_task(btn_press_timer()) # re-create

        # Handle task => should move btn_nb_click = 1 in btn_press_timer_flag if use n click

    if bsp.btn_long_press_flag == 1:
        # Reset task
        bsp.btn_long_press_flag = 0
        # Handle task
        bsp.menu = bsp.PAGE_LENG # move to page leng

    if bsp.btn_press_timer_flag == 1:
        # Reset flag
        bsp.btn_press_timer_flag = 0
        # Handle task
        if bsp.btn_nb_click == 2:
            bsp.menu = bsp.PAGE_CALIB # move to page calib

        bsp.btn_nb_click = 0 

    if bsp.state == bsp.STT_LOW:
        # Handle task
        if bsp.new_state == 0:
            uasyncio.create_task(obj_on(bsp.ld4_on, bsp.ld4_off, cfg.LED_DELAY))
        
        if cfg.USE_OLED:
            bsp.oled_val = display_stable(bsp.area_obj_mm)
            # bsp.oled_show_area(round(bsp.area_obj_mm, 2))
            bsp.oled_show_area(round(bsp.oled_val, 2))

        bsp.new_state = 1
    elif bsp.state == bsp.STT_RANGE1:
        # Handle task
        if bsp.new_state == 0:
            uasyncio.create_task(obj_on(bsp.ld0_on, bsp.ld0_off, cfg.LED_DELAY))
            uasyncio.create_task(obj_on(bsp.buz_on, bsp.buz_off, cfg.BUZ_DELAY))

        if cfg.USE_OLED:
            bsp.oled_val = display_stable(bsp.area_obj_mm)
            # bsp.oled_show_area(round(bsp.area_obj_mm, 2))
            bsp.oled_show_area(round(bsp.oled_val, 2))

        bsp.new_state = 1
    elif bsp.state == bsp.STT_RANGE2:
        # Handle task
        if bsp.new_state == 0:
            uasyncio.create_task(obj_on(bsp.ld2_on, bsp.ld2_off, cfg.LED_DELAY))
            uasyncio.create_task(obj_on_double(bsp.buz_on, bsp.buz_off, int (cfg.BUZ_DELAY / 3)))

        if cfg.USE_OLED:
            bsp.oled_val = display_stable(bsp.area_obj_mm)
            # bsp.oled_show_area(round(bsp.area_obj_mm, 2))
            bsp.oled_show_area(round(bsp.oled_val, 2))

        bsp.new_state = 1

    elif bsp.state == bsp.STT_HIGH:
        # Handle task
        if bsp.new_state == 0:
            uasyncio.create_task(obj_on(bsp.ld4_on, bsp.ld4_off, cfg.LED_DELAY))

        if cfg.USE_OLED:
            bsp.oled_val = display_stable(bsp.area_obj_mm)
            # bsp.oled_show_area(round(bsp.area_obj_mm, 2))
            bsp.oled_show_area(round(bsp.oled_val, 2))

        bsp.new_state = 1
    else: # STT_RESET state
        # Handle task
        if cfg.USE_OLED:
            bsp.oled_disp = [0, 0, 0]
            bsp.oled_show("A = ...")

        bsp.new_state = 0

async def loop_event():
    while True:
        if bsp.menu == bsp.PAGE_INIT:
            if bsp.flag != bsp.FLAG_INIT:
                await page_init_()
                bsp.flag = bsp.FLAG_INIT
            else:
                page_init()
        
        if bsp.menu == bsp.PAGE_LENG:
            if bsp.flag != bsp.FLAG_MEASURE:
                await page_leng_()
                bsp.flag = bsp.FLAG_MEASURE
            else:
                page_leng()

        if bsp.menu == bsp.PAGE_CALIB:
            if bsp.flag != bsp.FLAG_CALIB:
                await page_calib_()
                bsp.flag = bsp.FLAG_CALIB
            else:
                page_calib()

        if bsp.menu == bsp.PAGE_UPDATE:
            if bsp.flag != bsp.FLAG_UPDATE:
                await page_update_()
                bsp.flag = bsp.FLAG_UPDATE
            else:
                page_update()

        if bsp.menu == bsp.PAGE_AREA:
            if bsp.flag != bsp.FLAG_AREA:
                await page_area_()
                bsp.flag = bsp.FLAG_AREA
            else:
                page_area()

        await uasyncio.sleep_ms(cfg.LOOP_CYCLE)

def main():
    # Start event loop and run entry point
    uasyncio.run(loop_event())