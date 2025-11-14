from PIL import Image
import numpy as np


def bits_to_string(bits):
    """将二进制位转换回字符串"""
    # 将二进制字符串分组为8位一组
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]
        if len(byte_bits) == 8:
            byte_val = int(byte_bits, 2)
            bytes_list.append(byte_val)

    # 将字节转换为字符串
    try:
        text = bytes(bytes_list).decode('utf-8')
        return text
    except UnicodeDecodeError:
        return None


def extract_bits_from_image(image_path):
    """从PNG图像中提取嵌入的二进制位（遇到终止标记停止）"""
    # 打开图像
    img = Image.open(image_path)

    # 确保图像是RGBA模式
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # 将图像转换为numpy数组
    img_array = np.array(img)
    height, width, channels = img_array.shape

    # 提取所有像素的最低有效位，直到遇到终止标记
    extracted_bits = []
    termination_marker = '1' * 32
    marker_buffer = ''

    for y in range(height):
        for x in range(width):
            for c in range(4):  # RGBA四个通道
                pixel_value = img_array[y, x, c]
                # 提取最低有效位
                bit = '1' if pixel_value % 2 == 1 else '0'
                extracted_bits.append(bit)

                # 检查终止标记
                marker_buffer = (marker_buffer + bit)[-32:]
                if marker_buffer == termination_marker:
                    # 找到终止标记，返回之前的数据（不包括终止标记）
                    return ''.join(extracted_bits[:-32])

    # 如果没有找到终止标记，返回所有提取的位
    print("⚠️  警告：未找到终止标记，可能数据不完整")
    return ''.join(extracted_bits)


def main():
    """主解码函数"""
    try:
        # 图像路径
        encoded_image = "a_encoded.png"

        # 检查编码图是否存在
        try:
            Image.open(encoded_image)
        except FileNotFoundError:
            print(f"错误：找不到编码图像 {encoded_image}")
            print("请确保编码图像在当前目录下")
            return

        print("正在提取隐藏信息...")

        # 从图像中提取数据
        extracted_bits = extract_bits_from_image(encoded_image)

        if not extracted_bits:
            print("❌ 未提取到任何数据")
            return

        print(f"提取的二进制位数: {len(extracted_bits)}")

        # 将二进制转换回文本
        recovered_text = bits_to_string(extracted_bits)

        if recovered_text:
            print(f"\n🔓 提取的文本: {recovered_text}")
            print(f"\n✓ 成功提取 {len(recovered_text)} 个字符")
        else:
            print("❌ 解码失败：无法将二进制数据转换为有效文本")

    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    print("🔓 PNG图像隐写解码工具")
    print("=" * 40)
    main()