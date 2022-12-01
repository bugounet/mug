from PIL import Image
import numpy as np
import glob


def format_image(input_name, output_name):
    img = Image.open(input_name)
    img = img.resize((104, 104))
    ary = np.array(img)

    # Split the three channels
    r,g,b = np.split(ary,3,axis=2)
    r=r.reshape(-1)
    g=r.reshape(-1)
    b=r.reshape(-1)

    # Standard RGB to grayscale 
    bitmap = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2], 
    zip(r,g,b)))
    bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
    bitmap = np.dot((bitmap > 128).astype(float),255)
    im = Image.fromarray(bitmap.astype(np.uint8))
    im.save(output_name)

avatars = glob.glob("*")
for avatar in avatars:
    print(avatar)
    img = Image.open(avatar)
    img = img.convert(mode="1")
    img.tobitmap()
    print(avatar)
    parts = avatar.split("_")
    print(parts[1])
    img.save(parts[1])
    

# def format_image_bw(name):
#     image = Image.open("avatars/Aric.jpeg")
#     image = image.resize((104, 104))
    
#     image.tobitmap()



# format_image_bw("a")