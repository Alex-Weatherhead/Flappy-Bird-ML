from PIL import Image

spritesheet = Image.open('spritesheet.png')

def background (scalar = 1):

    background = spritesheet.crop(box=(0, 0, 143, 256)).resize((143 * scalar, 256 * scalar))

    return background
    
def foreground (scalar = 1):

    foreground = spritesheet.crop(box=(146, 0, 299, 56)).resize((154 * scalar, 56 * scalar))
    
    return foreground
    
def bird (scalar = 1):
    
    bird = spritesheet.crop(box=(264, 64, 281, 76)).resize((17 * scalar, 12 * scalar))
    
    return bird
    
def lower_pipe (scalar = 1):
    
    lower_pipe = spritesheet.crop(box=(330, 0, 356, 121)).resize((26 * scalar, 121 * scalar))

    return lower_pipe

def upper_pipe (scalar = 1):
    
    upper_pipe = spritesheet.crop(box=(302, 0, 328, 135)).resize((26 * scalar, 135 * scalar))
        
    return upper_pipe
