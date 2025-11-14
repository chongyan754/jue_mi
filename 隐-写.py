from PIL import Image
import numpy as np


def string_to_bits(text):
    """将字符串转换为UTF-8编码的二进制位"""
    bytes_data = text.encode('utf-8')
    bits = ''.join(format(byte, '08b') for byte in bytes_data)
    return bits


def embed_bits_in_image(image_path, bits, output_path):
    """将二进制位嵌入到PNG图像的RGBA通道中"""
    # 打开图像
    img = Image.open(image_path)

    # 确保图像是RGBA模式
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # 将图像转换为numpy数组以便处理
    img_array = np.array(img)
    height, width, channels = img_array.shape

    # 在数据末尾添加终止标记（32个连续的1）
    termination_marker = '1' * 32
    bits_with_marker = bits + termination_marker

    # 计算图像能容纳的最大位数
    max_bits = height * width * 4
    if len(bits_with_marker) > max_bits:
        raise ValueError(f"文本太长！图像最多能容纳 {max_bits} 位，但需要 {len(bits_with_marker)} 位")

    # 嵌入数据到每个像素的RGBA通道
    bit_index = 0
    total_bits = len(bits_with_marker)

    for y in range(height):
        for x in range(width):
            for c in range(4):  # RGBA四个通道
                if bit_index < total_bits:
                    current_bit = bits_with_marker[bit_index]

                    # 修改像素值，使其最低有效位等于当前bit
                    pixel_value = img_array[y, x, c]
                    if current_bit == '0':
                        # 确保最低位为0（偶数）
                        if pixel_value % 2 == 1:
                            img_array[y, x, c] = pixel_value - 1 if pixel_value > 0 else pixel_value + 1
                    else:  # current_bit == '1'
                        # 确保最低位为1（奇数）
                        if pixel_value % 2 == 0:
                            img_array[y, x, c] = pixel_value + 1 if pixel_value < 255 else pixel_value - 1

                    bit_index += 1
                else:
                    break
            if bit_index >= total_bits:
                break
        if bit_index >= total_bits:
            break

    # 保存修改后的图像
    result_img = Image.fromarray(img_array, 'RGBA')
    result_img.save(output_path, 'PNG')
    print(f"✓ 数据已成功嵌入到 {output_path}")
    print(f"✓ 原始文本: {len(bits) // 8} 字节")
    print(f"✓ 嵌入位数: {len(bits)} 位 + 32位终止标记")


def main():
    """主编码函数"""
    try:
        # 图像路径
        input_image = "a.png"
        output_image = "a_encoded.png"

        # 检查原图是否存在
        try:
            Image.open(input_image)
        except FileNotFoundError:
            print(f"错误：找不到原图 {input_image}")
            return

        # 用户输入文本
        user_text = input("请输入要隐藏的文本: ")

        if not user_text.strip():
            print("错误：文本不能为空")
            return

        # 将文本转换为二进制位
        bits = string_to_bits(user_text)
        print(f"文本转换为二进制: {bits[:100]}..." if len(bits) > 100 else f"文本转换为二进制: {bits}")

        # 嵌入数据到图像
        embed_bits_in_image(input_image, bits, output_image)

        print(f"\n🎉 编码完成！现在可以把 {output_image} 发给朋友了")

    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    print("🔒 PNG图像隐写编码工具")
    print("=" * 40)
    main()