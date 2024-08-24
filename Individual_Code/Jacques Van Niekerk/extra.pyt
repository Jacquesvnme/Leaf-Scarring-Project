looping = True

while looping == True:
    for i in range(0, h):
        for j in range(0, w):
            if(mask[i, j] == 0):
                print("Pixel found at (",i,",",j,")")
                looping = False