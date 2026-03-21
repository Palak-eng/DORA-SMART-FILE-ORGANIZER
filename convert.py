from PIL import Image

img = Image.open("logo.png")

# Resize for best icon sizes
img.save("logo.ico", format="ICO", sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])