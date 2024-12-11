# 定义签名码
signature_code = "rb3"

# 创建并写入文件
with open("make/signature.txt", "w") as file:
    file.write(signature_code)

print("签名码文件 'signature.txt' 已创建，内容为：", signature_code)