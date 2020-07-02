from PIL import Image
from PIL import ImageChops

def trans_paste(fg_img,bg_img,alpha=1.0,box=(0,0)):
    fg_img_trans = Image.new("RGBA",fg_img.size)
    fg_img_trans = Image.blend(fg_img_trans,fg_img,alpha)
    bg_img.paste(fg_img_trans,box,fg_img_trans)
    return bg_img

img1=open('nothing.jpg','rb')
img2=open('well.png','rb')
bg_img = Image.open(img1)
fg_img = Image.open(img2)
p = trans_paste(fg_img,bg_img,1,(250,200))
p.show()
p.save('blended3.png')

img1.close()
img2.close()

"""
img1=open('field.png','rb')
img2=open('well.png','rb')
bg=Image.open(img1)
fg=Image.open(img2)
"""

