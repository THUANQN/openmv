# Digital Image Processing

import cfg
import bsp
import sensor
import math
import uasyncio

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max) => LAB
# The below thresholds track in general red/green/blue things. You may wish to tune them...

async def run():
    ''' Implement algorithm for identify object size '''
    while True:
        img = sensor.snapshot() 

        blobs = img.find_blobs(
                [cfg.THRESHOLDS[bsp.idx]],
                roi = cfg.ROIS[bsp.idx],
                pixels_threshold=cfg.PIXEL_MIN,
                area_threshold=cfg.AREA_MIN,
                merge=True
            )

        if len(blobs) == 0:
            bsp.state = bsp.STT_RESET
        else:
            for blob in blobs:
                if bsp.menu == bsp.PAGE_LENG or bsp.menu == bsp.PAGE_INIT:
                    major_len = math.sqrt(math.pow(blob.min_corners()[0][0] - blob.min_corners()[1][0], 2) + math.pow(blob.min_corners()[0][1] - blob.min_corners()[1][1], 2))
                    minor_len = math.sqrt(math.pow(blob.min_corners()[1][0] - blob.min_corners()[2][0], 2) + math.pow(blob.min_corners()[1][1] - blob.min_corners()[2][1], 2))

                    bsp.len_obj[0] = bsp.len_obj[1]
                    bsp.len_obj[1] = bsp.len_obj[2]
                    # bsp.len_obj[2] = min(major_len, minor_len)
                    bsp.len_obj[2] = max(major_len, minor_len) # Get max for vertical projection of object

                    bsp.len_obj_avg = sum(bsp.len_obj) / len(bsp.len_obj)
                    len_obj_lo = bsp.len_obj_avg - cfg.LEN_OBJ_DEL
                    len_obj_hi = bsp.len_obj_avg + cfg.LEN_OBJ_DEL

                    if bsp.len_obj[0] <= len_obj_hi and bsp.len_obj[0] >= len_obj_lo \
                        and bsp.len_obj[1] <= len_obj_hi and bsp.len_obj[1] >= len_obj_lo \
                        and bsp.len_obj[2] <= len_obj_hi and bsp.len_obj[2] >= len_obj_lo:

                        bsp.len_obj_new = bsp.len_obj_avg # save stable value
                        bsp.state = bsp.STT_NEW

                        # if cfg.USE_PRINT:
                        #     print(f'len_pix: {bsp.len_obj_new} pix')                    
            
                        if bsp.menu == bsp.PAGE_LENG:
                            bsp.len_obj_mm = bsp.ratio * bsp.len_obj_new + cfg.LEN_OBJ_OFFSET_MM

                            if bsp.len_obj_mm < bsp.RANGE_LENG_MIN and bsp.len_obj_mm >= cfg.LEN_OBJ_MIN_MM:
                                bsp.state = bsp.STT_LOW
                            elif bsp.len_obj_mm < cfg.RANGE1_LENG[1] and bsp.len_obj_mm >= cfg.RANGE1_LENG[0]:
                                bsp.state = bsp.STT_RANGE1 
                            elif bsp.len_obj_mm < cfg.RANGE2_LENG[1] and bsp.len_obj_mm >= cfg.RANGE2_LENG[0]:
                                bsp.state = bsp.STT_RANGE2 
                            elif bsp.len_obj_mm < cfg.LEN_OBJ_MAX_MM and bsp.len_obj_mm >= bsp.RANGE_LENG_MAX:
                                bsp.state = bsp.STT_HIGH 
                            else:
                                bsp.state = bsp.STT_RESET
                            
                            if cfg.USE_PRINT:
                                print(f'len_mm: {bsp.len_obj_mm} mm')

                        elif bsp.menu == bsp.PAGE_CALIB:
                            if blob.roundness() > 0.99:
                                bsp.ratio_tmp = cfg.LEN_REF_MM / bsp.len_obj_new

                                if cfg.USE_PRINT:
                                    print(f'ratio: {bsp.ratio_tmp}')
                        
                    if cfg.USE_DRAW:
                        img.draw_line(blob.min_corners()[0][0], blob.min_corners()[0][1], blob.min_corners()[1][0], blob.min_corners()[1][1], color=cfg.COLORS[bsp.idx], thickness = 3)
                        img.draw_line(blob.min_corners()[1][0], blob.min_corners()[1][1], blob.min_corners()[2][0], blob.min_corners()[2][1], color=cfg.COLORS[bsp.idx], thickness = 3) 
                        img.draw_line(blob.min_corners()[2][0], blob.min_corners()[2][1], blob.min_corners()[3][0], blob.min_corners()[3][1], color=cfg.COLORS[bsp.idx], thickness = 3) 
                        img.draw_line(blob.min_corners()[3][0], blob.min_corners()[3][1], blob.min_corners()[0][0], blob.min_corners()[0][1], color=cfg.COLORS[bsp.idx], thickness = 3)
                
                elif bsp.menu == bsp.PAGE_AREA:
                    
                    bsp.area_obj[0] = bsp.area_obj[1]
                    bsp.area_obj[1] = bsp.area_obj[2]
                    bsp.area_obj[2] = blob.pixels()

                    bsp.area_obj_avg = sum(bsp.area_obj) / len(bsp.area_obj)
                    area_obj_lo = bsp.area_obj_avg - cfg.AREA_OBJ_DEL
                    area_obj_hi = bsp.area_obj_avg + cfg.AREA_OBJ_DEL

                    # if cfg.USE_PRINT:
                    #         print(f'area_pix: {bsp.area_obj_avg} pix2')

                    if bsp.area_obj[0] <= area_obj_hi and bsp.area_obj[0] >= area_obj_lo \
                        and bsp.area_obj[1] <= area_obj_hi and bsp.area_obj[1] >= area_obj_lo \
                        and bsp.area_obj[2] <= area_obj_hi and bsp.area_obj[2] >= area_obj_lo:

                        bsp.area_obj_new = bsp.area_obj_avg # save stable value
                        bsp.state = bsp.STT_NEW

                        if cfg.USE_PRINT:
                            print(f'area_pix: {bsp.area_obj_new} pix2')  

                        bsp.area_obj_mm = bsp.ratio * bsp.ratio * bsp.area_obj_new + cfg.AREA_OBJ_OFFSET_MM

                        if bsp.area_obj_mm < bsp.RANGE_AREA_MIN and bsp.area_obj_mm >= cfg.AREA_OBJ_MIN_MM:
                            bsp.state = bsp.STT_LOW
                        elif bsp.area_obj_mm < cfg.RANGE1_AREA[1] and bsp.area_obj_mm >= cfg.RANGE1_AREA[0]:
                            bsp.state = bsp.STT_RANGE1 
                        elif bsp.area_obj_mm < cfg.RANGE2_AREA[1] and bsp.area_obj_mm >= cfg.RANGE2_AREA[0]:
                            bsp.state = bsp.STT_RANGE2 
                        elif bsp.area_obj_mm < cfg.AREA_OBJ_MAX_MM and bsp.area_obj_mm >= bsp.RANGE_AREA_MAX:
                            bsp.state = bsp.STT_HIGH 
                        else:
                            bsp.state = bsp.STT_RESET
                        
                        if cfg.USE_PRINT:
                            print(f'area_mm: {bsp.area_obj_mm} mm2') 
                        
                    
                    if cfg.USE_DRAW:
                        img.draw_rectangle(blob.rect(), color=cfg.COLORS[bsp.idx], thickness = 3)

                else:
                    pass

        await uasyncio.sleep_ms(cfg.SEN_CYCLE)   


# Refer 
# These values depend on the blob not being circular - otherwise they will be shaky.
#        if blob.elongation() > 0.5:
#            img.draw_edges(blob.min_corners(), color=(255, 0, 0))
#            img.draw_line(blob.major_axis_line(), color=(0, 255, 0))
#            img.draw_line(blob.minor_axis_line(), color=(0, 0, 255))
        # These values are stable all the time.
#        img.draw_rectangle(blob.rect())
#        img.draw_cross(blob.cx(), blob.cy())
        # Note - the blob rotation is unique to 0-180 only.
#        img.draw_keypoints(
#            [(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20
#        )

#        print('w=', blob.w())
#        print('h=', blob.h())
#        print('the area of the bounding box', blob.area())
#        print('the number of pixels that are apart of this blob', blob.pixels())
#        print('the number of pixels on this blob perimeter', blob.perimeter())
#        print('the density ratio of the blob', blob.density()) # (pixels/area)
#        print('the compactness ratio of the blob', blob.compactness()) # like density, base on perimeter ????
#        print('the solidity ratio of the blob', blob.solidity()) # like density, base on minimum the area of the rotated bounding box, more accurate!
#        print('the rotation of the blob in degree ', blob.rotation_deg()) # ???