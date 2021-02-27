import os

def check_img(img_name):
    imgs = os.listdir('./ruler_train')
    if img_name not in imgs:
        return False
    else:
        return True

if __name__ == '__main__':
    #f2 = open('./ruler_val/new_label.txt', "w")
    with open("./ruler_train/Label.txt", "r+",encoding='UTF-8') as f:
        lines = f.read()
        f.seek(0)
        lines = lines.replace('ruler', 'ruler_train')
        f.write(lines)

