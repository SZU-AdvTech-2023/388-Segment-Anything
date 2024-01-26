import threading
import cv2
import numpy as np
from yolo_detect import detect
from io import BytesIO
from flask import send_file
exitFlag = 0

class kn_stone_detect(threading.Thread):
    def __init__(self, image, weights):
        threading.Thread.__init__(self)
        self.image = image
        self.weights = weights
        # self.__runing_flag.set()
        self.results = ""
        
    def run(self):
        self.results = detect(self.image, self.weights)
        
    def get_results(self):
        return self.results
    
    def pause(self):
        self.__runing_flag.clear()
        
    def resume(self):
        self.__runing_flag.set()
    
    # def start(self):
    #     self.__runing_flag.set()
        
    # def stop(self):
    #     self.__runing_flag.clear()
    
def kn_stone_detect(image, weights):
    return detect(image, weights)
    
def addWeightedSmallImgToLargeImg(largeImg,alpha,smallImg,beta,gamma=0.0,regionTopLeftPos=(0,0)):
    srcW, srcH = largeImg.shape[1::-1]
    refW, refH = smallImg.shape[1::-1]
    x,y =  regionTopLeftPos
    if (refW>srcW) or (refH>srcH):
        #raise ValueError("img2's size must less than or equal to img1")
        raise ValueError(f"img2's size {smallImg.shape[1::-1]} must less than or equal to img1's size {largeImg.shape[1::-1]}")
    else:
        if (x+refW)>srcW:
            x = srcW-refW
        if (y+refH)>srcH:
            y = srcH-refH
        destImg = np.array(largeImg)
        tmpSrcImg = destImg[y:y+refH,x:x+refW]
        tmpImg = cv2.addWeighted(tmpSrcImg, alpha, smallImg, beta,gamma)
        destImg[y:y + refH, x:x + refW] = tmpImg
    return destImg

    
def image_fuse(src_img_x, src_img_ct, x_weights='x_kidney_stone.pt', ct_weights="ct_kidney_stone.pt"):
    # x_detect_thread =  kn_stone_detect(src_img_x, x_weights)
    # ct_detect_thread =  kn_stone_detect(src_img_ct, ct_weights)
    
    # x_detect_thread.start()
    # ct_detect_thread.start()
    # x_detect_thread.join()
    # ct_detect_thread.join()
    
    # x_stone_info = x_detect_thread.get_results()
    # ct_stone_info = ct_detect_thread.get_results()

    x_stone_info = kn_stone_detect(src_img_x, x_weights)
    ct_stone_info = kn_stone_detect(src_img_ct, ct_weights)
    print("ct_stone_info", ct_stone_info)
    
    # cv2.circle(src_img_ct, (ct_stone_info[0]['position'][0], ct_stone_info[0]['position'][1]), 10, (0,255,0), 2)
    # cv2.imwrite("mark_src_img_ct.jpg", src_img_ct)
    # cv2.circle(src_img_x, (x_stone_info[0]['position'][0], x_stone_info[0]['position'][1]), 10, (0,255,0), 2)
    # print("x_stone_info[0]['position'][0], x_stone_info[0]['position'][1]", x_stone_info[0]['position'][0], x_stone_info[0]['position'][1])
    # cv2.imwrite("mark_src_img_x.jpg", src_img_x)
    
    fx = float(ct_stone_info[0]['position'][2]/x_stone_info[0]['position'][2])
    fy = float(ct_stone_info[0]['position'][3]/x_stone_info[0]['position'][3])
    # print("fx, fy", fx, fy)

    img_x = cv2.resize(src_img_x, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_LANCZOS4)
    x_center_x, x_center_y = int(x_stone_info[0]['position'][0]*fx), int(x_stone_info[0]['position'][1]*fy)   
    # print("x_center_x, x_center_y", x_center_x, x_center_y)
    
    # cv2.circle(img_x, (x_center_x, x_center_y), 10, (255,255,0), 2)
    # cv2.imwrite("mark_img_x.jpg", img_x)
    # x_kd_stone = src_img_x[x_stone_info[0]['position'][1]: x_stone_info[0]['position'][1] + x_stone_info[0]['position'][3], x_stone_info[0]['position'][0]:x_stone_info[0]['position'][0]+x_stone_info[0]['position'][2]]
    # cv2.imwrite("x_kd_stone1.jpg", x_kd_stone)
    # ct_kd_stone = src_img_ct[ct_stone_info[0]['position'][1]: ct_stone_info[0]['position'][1] + x_stone_info[0]['position'][3], ct_stone_info[0]['position'][0]:ct_stone_info[0]['position'][0]+x_stone_info[0]['position'][2]]
    # cv2.imwrite("ct_kd_stone1.jpg", ct_kd_stone)
    
    
    # cv2.imwrite("resize_x.jpg", src_img_x)
    
    if img_x.size > src_img_ct.size:
        crop_h, crop_w = src_img_ct.shape[:2]
        crop_x = img_x[:crop_h, :crop_w]
        # cv2.imwrite("crop_x.jpg", crop_x)
        x_bias = ct_stone_info[0]['position'][0] - x_center_x           #ct_center_x - x_center_x
        y_bias = ct_stone_info[0]['position'][1] - x_center_y           #ct_center_y - x_center_y
        M = np.float32([[1, 0, x_bias], [0, 1, y_bias]])
        crop_x = cv2.warpAffine(crop_x, M, (crop_x.shape[1], crop_x.shape[0]))
        # cv2.imwrite("src_img_ct_1.jpg", src_img_ct)
        # cv2.imwrite("src_img_x_1.jpg", crop_x)
        merge_img = crop_x + src_img_ct
        # cv2.imwrite("new_merge_img.jpg", merge_img)
    else:
        crop_h ,crop_w= img_x.shape[:2]
        crop_ct = src_img_ct[:crop_h, :crop_w]
        x_bias = ct_stone_info[0]['position'][0] - x_center_x         #ct_center_x - x_center_x
        y_bias = ct_stone_info[0]['position'][1] - x_center_y         #ct_center_y - x_center_y
        # cv2.circle(crop_ct, (ct_stone_info[0]['position'][0], ct_stone_info[0]['position'][1]), 10, (255,0,0), 2)
        # cv2.imwrite("mark_ct.jpg", crop_ct)
        # cv2.circle(img_x, (x_center_x, x_center_y), 10, (0,0,255), 2)
        # cv2.imwrite("mark_x.jpg", img_x)
        M = np.float32([[1, 0, x_bias], [0, 1, y_bias]])
        img_x = cv2.warpAffine(img_x, M, (img_x.shape[1], img_x.shape[0]))
        # cv2.imwrite("src_img_ct_1.jpg", crop_ct)
        # cv2.imwrite("src_img_x_1.jpg", img_x)
        merge_img = img_x + crop_ct
        # cv2.imwrite("new_merge_img.jpg", merge_img)
    merge_img = cv2.resize(merge_img, (0, 0), fx= 0.2, fy=0.2, interpolation=cv2.INTER_LANCZOS4)
    _, encoded_img = cv2.imencode('.jpg', merge_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    # # 编码后的图像存储在内存
    img_io = BytesIO(encoded_img)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpg')
    # x_kd_stone = src_img_x[x_stone_info[0]['position'][1]: x_stone_info[0]['position'][1] + x_stone_info[0]['position'][3], x_stone_info[0]['position'][0]:x_stone_info[0]['position'][0]+x_stone_info[0]['position'][2]]
    # cv2.imwrite("x_kd_stone.jpg", x_kd_stone)
    # ct_kd_stone = src_img_ct[ct_stone_info[0]['position'][1]: ct_stone_info[0]['position'][1] + ct_stone_info[0]['position'][3], ct_stone_info[0]['position'][0]:ct_stone_info[0]['position'][0]+ct_stone_info[0]['position'][2]]
    # cv2.imwrite("ct_kd_stone.jpg", ct_kd_stone)
    # stone_merge = x_kd_stone + ct_kd_stone
    # cv2.imwrite("stone_merge.jpg", stone_merge)
    
    # print("x_stone_info", x_stone_info)
    # print("ct_stone_info", ct_stone_info)
    #cal center bias
    
    # x_bias = ct_stone_info[0]['position'][0] - x_stone_info[0]['position'][0]           #ct_center_x - x_center_x
    # y_bias = ct_stone_info[0]['position'][1] - x_stone_info[0]['position'][1]           #ct_center_y - x_center_y
    # M = np.float32([[1, 0, x_bias], [0, 1, y_bias]])
    # src_img_x = cv2.warpAffine(src_img_x, M, (src_img_x.shape[1], src_img_x.shape[0]))
    
    # x_w, x_h = src_img_x.shape[:2]
    # ct_w, ct_h = src_img_ct.shape[:2]
    
    # padding_w, padding_h = 0, 0
    # if x_w > ct_w:
    #     padding_w = x_w - ct_w
    # else:
    #     padding_w = ct_w - x_w
        
    # if x_h > ct_h:
    #     padding_h = x_h - ct_h
    # else:
    #     padding_h = ct_h - x_h
        
    # overlapping = addWeightedSmallImgToLargeImg(src_img_ct, 0.5, src_img_x, 0.8)
    
    # rows, cols = src_img_x.shape[:2]
    # roi = src_img_ct[:rows, :cols]
    
    # src_img_x2gray = cv2.cvtColor(src_img_x, cv2.COLOR_BGR2GRAY)
    # ret, mask = cv2.threshold(src_img_x2gray, 200, 255, cv2.THRESH_BINARY_INV)
    # mask_inv = cv2.bitwise_not(mask)
    # mask_inv = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2BGR)
    # merge = cv2.add(roi, mask_inv)
    # src_img_ct[:rows, :cols] = merge
    
    # cv2.imwrite("mask_inv.jpg", mask_inv)
    # src_img_ct_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    # dst = cv2.add(src_img_ct, mask_inv)
    # src_img_ct[:rows, :cols] = dst
    

if __name__ == "__main__":
    x_weights='x_kidney_stone.pt'  # 权重文件地址   .pt文件
    src_img_x = '20220530_155437.jpg'
    ct_weights = "ct_kidney_stone.pt"
    src_img_ct = "20220530_155448.jpg"
    
    src_img_x = cv2.imread(src_img_x)
    src_img_ct = cv2.imread(src_img_ct)
    image_fuse(src_img_x, src_img_ct, x_weights, ct_weights)