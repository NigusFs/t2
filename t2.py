from skimage import io
from skimage.color import rgb2gray
from skimage.filters.rank import entropy, gradient
from skimage.morphology import disk
import numpy as np
import matplotlib.pyplot as plt
import sys


def get(y, x, t):
    m = len(t) #rows
    n = len(t[0]) #cols
    if x < 0 or x >= n: return sys.maxsize
    if y < 0 or y >= m: return sys.maxsize
    return t[y][x]
    
## Transform the image to gray
## Calculate the entropy or gradient
## Get the path with less energy
## Return the energy as an integer, and the 
## path with less energy as a list of (x,y)
def memo(n,m): # las filas y columnas de la imagen
    d=[[-1] * (m+1) for i in range(n)] # el +1 es para guardar la sumatoria de la energia minima y la posicion q hay q borrar
    return d #yo
def spath(matriz,i,j,d): 
    #d matriz en donde se guardan los valores ya analizados
    #i filas
    #j columnas    
    if j >= len(matriz):
        return 0
    if j < 0 or j > len(matriz[0])-1:
        return 10**5
    if i > len(matriz)-1:
        return 0
    if d[i][j] != -1:
        return d[i][j]
    
    a=int(matriz[i][j]) + spath(matriz,i+1,j-1,d)

    b=int(matriz[i][j]) + spath(matriz,i+1,j,d)

    c=int(matriz[i][j]) + spath(matriz,i+1,j+1,d)
    k=min(a,b,c)
    if d[i][j] == -1:
        d[i][j]=k #guarda los valores
        if  d[i][len(d[0])-1]== -1 or k < d[i][len(d[0])-1][0] : 
            d[i][len(d[0])-1]=[k,i,j] # guarda la posicion del path para dps borrarlo

    return int(k) # yo    

def energy(img):
    # filas = m, columnas = n
    m, n = img.shape   
    d=memo(m,n)
    for j in range (0,len(img[0])):#bien
        spath(img,0,j,d)

    ## ESTO ES LO QUE DEBE IMPLEMENTAR

    ans=[0]*m
    e=d[0][len(d[0])-1][0]
    
    for j in range (0,len(img)):
        ans[j]=[j,d[j][len(d[0])-1][2]]

    return e, ans


def togray(image):
    image_bw = rgb2gray(image)
    # using the entropy
    #image_e = entropy(image_bw,disk(1))
    #return energy(image_e)
    
    # using gradient
    image_g = gradient(image_bw,disk(1))
    return image_g

## Remove one pixel per row... the one
## in the path min energy

def remove(image, pixel):
    ans = []
    for i, k in pixel:
        ans.append(np.delete(image[i], k, 0))
    return np.array(ans)


if __name__=='__main__':
    import sys
    
    image = io.imread('image.png')
    img_gray = togray(image)
    plt.figure()
    plt.imshow(image)
    plt.figure()
    plt.imshow(img_gray)
    plt.show()
    
    percent = 0.75
    
    m,n,_ = image.shape
    new_n = int(n * percent)
    
    img = image
    ims = []
    for i in range(n-new_n): 
        print("Iteracion numero {}/{}".format(i+1, n-new_n))
        img_gray = togray(img)
        e, p = energy(img_gray)
        img_new = remove(img, p)
        
        img = img_new
    
    plt.figure()
    plt.imshow(image) # imagen original
    plt.figure()
    plt.imshow(img) # imagen escalada
    plt.show()
