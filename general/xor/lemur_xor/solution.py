from PIL import Image

lemur = Image.open("lemur.png")
flag = Image.open("flag.png")

pixels_lemur = lemur.load()
pixels_flag = flag.load()

for i in range(lemur.size[0]):
    for j in range(lemur.size[1]):
        l = pixels_lemur[i,j]
        f = pixels_flag[i,j]
        pixels_flag[i,j] = (l[0] ^ f[0], l[1] ^ f[1], l[2] ^ f[2])

flag.save("lemur_xor_flag.png")
