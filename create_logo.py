from PIL import Image, ImageDraw, ImageFont

def create_logo():
    # Boyut: 200x60 (NotebookLM logosunu kapatacak kadar)
    width = 250
    height = 80
    bg_color = (102, 126, 234) # Tema rengi (Purple/Blue)
    text_color = (255, 255, 255)
    
    img = Image.new('RGB', (width, height), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Font (Varsayılan kullanıyoruz, sistemde font aramakla uğraşmamak için)
    # Daha şıkı için font yüklenebilir
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
        
    d.text((width/2, height/2), "LGS Zeka", fill=text_color, anchor="mm", font=font)
    
    # Border
    d.rectangle([0, 0, width-1, height-1], outline=(255, 255, 255), width=3)
    
    img.save('assets/lgs_logo_mask.png')
    print("Logo created: assets/lgs_logo_mask.png")

if __name__ == "__main__":
    create_logo()
