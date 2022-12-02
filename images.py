'''
Utility functions to read and save an image in our encoding.
Utilities to load/save a PNG file to our encoding.
'''
import png as mypng

def load(filename):
    """ Load the PNG image from file 'filename'. Returns a list of pixel lists.
         Each pixel is a tuple (R, G, B) of the 3 colors with values between 0 and 255.
         Load a PNG image from file 'filename'. Return to list of lists of pixels.
         Each pixel is a tuple (R, G, B) of its 3 colors with values in 0..255.
    """
    with open(filename, mode='rb') as f:
        reader = mypng.Reader(file=f)
        w, h, png_img, _ = reader.asRGB8()
        # slightly tweaked
        w *= 3
        return [ [ (line[i],line[i+1],line[i+2]) 
                   for i in range(0, w, 3) ]
                 for line in png_img ]


def save(img, filename):
    """ Save image 'img' to PNG file 'filename'. img is a list of lists of pixels.
         Each pixel is a tuple (R, G, B) of the 3 colors with values between 0 and 255.
         Save the 'img' image in a 'filename' PNG file. img is a list of lists of pixels.
         Each pixel is a tuple (R, G, B) of its 3 colors with values in 0..255.
    """
    pngimg = mypng.from_array(img,'RGB')
    pngimg.save(filename)

