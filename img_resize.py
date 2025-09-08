import cv2
import os
from PIL import Image
import numpy as np
import imageio.v2 as imageio

def resize_image(input_path, output_path=None, width=None, height=None, scale_factor=None):
    """
    调整图片大小并保存
    
    参数:
    input_path (str): 输入图片的路径
    output_path (str, optional): 输出图片的路径，如果为None则覆盖原文件
    width (int, optional): 目标宽度
    height (int, optional): 目标高度
    scale_factor (float, optional): 缩放因子，如0.5表示缩小到一半
    
    返回:
    bool: 操作是否成功hho
    """
    try:
        # 首先尝试用OpenCV读取
        img = cv2.imread(input_path)
        
        # 如果OpenCV无法读取，尝试用PIL读取
        if img is None:
            try:
                print(f"OpenCV无法读取，尝试使用PIL读取: {input_path}")
                pil_img = Image.open(input_path)
                # 将PIL图像转换为OpenCV格式
                img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                print(f"成功使用PIL读取图片")
            except Exception as pil_error:
                # 如果PIL也无法读取，尝试使用imageio（支持AVIF等格式）
                try:
                    print(f"PIL无法读取，尝试使用imageio读取: {input_path}")
                    img_array = imageio.imread(input_path)
                    # imageio返回RGB格式，需要转换为BGR
                    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                    print(f"成功使用imageio读取图片")
                except Exception as imageio_error:
                    print(f"错误：无法读取图片 {input_path}")
                    print(f"OpenCV错误：文件可能不存在或格式不支持")
                    print(f"PIL错误：{str(pil_error)}")
                    print(f"ImageIO错误：{str(imageio_error)}")
                    return False
        
        # 获取原始尺寸
        original_height, original_width = img.shape[:2]
        print(f"原始图片尺寸: {original_width} x {original_height}")
        
        # 确定目标尺寸
        if scale_factor is not None:
            # 使用缩放因子
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
        elif width is not None and height is not None:
            # 指定宽度和高度
            new_width = width
            new_height = height
        elif width is not None:
            # 只指定宽度，按比例计算高度
            new_width = width
            new_height = int(original_height * (width / original_width))
        elif height is not None:
            # 只指定高度，按比例计算宽度
            new_height = height
            new_width = int(original_width * (height / original_height))
        else:
            print("错误：必须指定width、height或scale_factor中的至少一个参数")
            return False
        
        print(f"目标图片尺寸: {new_width} x {new_height}")
        
        # 调整图片大小
        resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # 确定输出路径
        if output_path is None:
            output_path = input_path
        
        # 保存图片
        success = cv2.imwrite(output_path, resized_img)
        
        if success:
            print(f"图片已成功保存到: {output_path}")
            return True
        else:
            print(f"错误：保存图片失败 {output_path}")
            return False
            
    except Exception as e:
        print(f"处理图片时发生错误: {str(e)}")
        return False

# 使用示例
if __name__ == "__main__":
    resize_image("/share/project/cwm/houyuan.chen/TEST/dist/assets/img/portfolio/High-Pressure-3-Phase-High-Quality-Horizontal.jpg", width=600, height=450)
    resize_image("/share/project/cwm/houyuan.chen/TEST/dist/assets/img/portfolio/7.jpg", width=600, height=450)
    resize_image("/share/project/cwm/houyuan.chen/TEST/dist/assets/img/portfolio/High-Pressure-Stainless-Steel-Submersible-Clean-3.jpg", width=600, height=450)  
    resize_image("/share/project/cwm/houyuan.chen/TEST/dist/assets/img/portfolio/Industrial-High-Pressure-Factory-Direct-Dirty-Water.jpg", width=600, height=450)
    resize_image("/share/project/cwm/houyuan.chen/TEST/dist/assets/img/portfolio/OEM-Industrial-Stainless-Steel-Single-Screw-Pump.jpg", width=600, height=450)
    resize_image("/share/project/cwm/houyuan.chen/TEST/dist/assets/img/portfolio/Wholesale-High-Quality-OEM-Supported-High-Pressure.jpg", width=600, height=450)
