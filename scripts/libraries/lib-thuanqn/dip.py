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
    ''' Implement algorithm for measure object size '''
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
                major_len = math.sqrt(math.pow(blob.min_corners()[0][0] - blob.min_corners()[1][0], 2) + math.pow(blob.min_corners()[0][1] - blob.min_corners()[1][1], 2))
                minor_len = math.sqrt(math.pow(blob.min_corners()[1][0] - blob.min_corners()[2][0], 2) + math.pow(blob.min_corners()[1][1] - blob.min_corners()[2][1], 2))

                bsp.len_obj[0] = bsp.len_obj[1]
                bsp.len_obj[1] = bsp.len_obj[2]
                # bsp.len_obj[2] = min(major_len, minor_len)
                bsp.len_obj[2] = max(major_len, minor_len) # Get max for vertical projection of object

                if cfg.USE_DRAW:
                    img.draw_line(blob.min_corners()[0][0], blob.min_corners()[0][1], blob.min_corners()[1][0], blob.min_corners()[1][1], color=cfg.COLORS[bsp.idx], thickness = 3)
                    img.draw_line(blob.min_corners()[1][0], blob.min_corners()[1][1], blob.min_corners()[2][0], blob.min_corners()[2][1], color=cfg.COLORS[bsp.idx], thickness = 3) 
                    img.draw_line(blob.min_corners()[2][0], blob.min_corners()[2][1], blob.min_corners()[3][0], blob.min_corners()[3][1], color=cfg.COLORS[bsp.idx], thickness = 3) 
                    img.draw_line(blob.min_corners()[3][0], blob.min_corners()[3][1], blob.min_corners()[0][0], blob.min_corners()[0][1], color=cfg.COLORS[bsp.idx], thickness = 3)

                bsp.len_obj_avg = sum(bsp.len_obj) / len(bsp.len_obj)
                len_obj_lo = bsp.len_obj_avg - cfg.LEN_OBJ_DEL
                len_obj_hi = bsp.len_obj_avg + cfg.LEN_OBJ_DEL

                if bsp.len_obj[0] <= len_obj_hi and bsp.len_obj[0] >= len_obj_lo \
                    and bsp.len_obj[1] <= len_obj_hi and bsp.len_obj[1] >= len_obj_lo \
                    and bsp.len_obj[2] <= len_obj_hi and bsp.len_obj[2] >= len_obj_lo:

                    bsp.len_obj_new = bsp.len_obj_avg # save stable value
                    bsp.state = bsp.STT_NEW

                    if cfg.USE_PRINT:
                        print(f'len_pix: {bsp.len_obj_new} pix')                    
        
                    if bsp.menu == bsp.PAGE_MEASURE:
                        bsp.len_obj_mm = bsp.ratio * bsp.len_obj_new + cfg.LEN_OBJ_OFFSET_MM

                        if bsp.len_obj_mm < bsp.RANGE_MIN and bsp.len_obj_mm >= cfg.LEN_OBJ_MIN_MM:
                            bsp.state = bsp.STT_LOW
                        elif bsp.len_obj_mm < cfg.RANGE1[1] and bsp.len_obj_mm >= cfg.RANGE1[0]:
                            bsp.state = bsp.STT_RANGE1 
                        elif bsp.len_obj_mm < cfg.RANGE2[1] and bsp.len_obj_mm >= cfg.RANGE2[0]:
                            bsp.state = bsp.STT_RANGE2 
                        # elif bsp.len_obj_mm < cfg.RANGE3[1] and bsp.len_obj_mm >= cfg.RANGE3[0]:
                        #     bsp.state = bsp.STT_RANGE3
                        elif bsp.len_obj_mm < cfg.LEN_OBJ_MAX_MM and bsp.len_obj_mm >= cfg.RANGE2[1]:
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