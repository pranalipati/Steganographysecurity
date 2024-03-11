#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pand
import os
import cv2
from matplotlib import pyplot as plt


# In[2]:


def txt_encode(text):
    l=len(text)
    i=0
    add=''
    while i<l:
        t=ord(text[i])
        if(t>=32 and t<=64):
            t1=t+48
            t2=t1^170       #170: 10101010
            res = bin(t2)[2:].zfill(8)
            add+="0011"+res
        
        else:
            t1=t-48
            t2=t1^170
            res = bin(t2)[2:].zfill(8)
            add+="0110"+res
        i+=1
    res1=add+"111111111111"
    print("The string after binary conversion appyling all the transformation :- " + (res1))   
    length = len(res1)
    print("Length of binary after conversion:- ",length)
    HM_SK=""
    ZWC={"00":u'\u200C',"01":u'\u202C',"11":u'\u202D',"10":u'\u200E'}      
    file1 = open("Sample_cover_files/cover_text.txt","r+")
    nameoffile = input("\nEnter the name of the Stego file after Encoding(with extension):- ")
    file3= open(nameoffile,"w+", encoding="utf-8")
    word=[]
    for line in file1: 
        word+=line.split()
    i=0
    while(i<len(res1)):  
        s=word[int(i/12)]
        j=0
        x=""
        HM_SK=""
        while(j<12):
            x=res1[j+i]+res1[i+j+1]
            HM_SK+=ZWC[x]
            j+=2
        s1=s+HM_SK
        file3.write(s1)
        file3.write(" ")
        i+=12
    t=int(len(res1)/12)     
    while t<len(word): 
        file3.write(word[t])
        file3.write(" ")
        t+=1
    file3.close()  
    file1.close()
    print("\nStego file has successfully generated")


# In[3]:


def encode_txt_data():
    count2=0
    file1 = open("Sample_cover_files/cover_text.txt","r")
    for line in file1: 
        for word in line.split():
            count2=count2+1
    file1.close()       
    bt=int(count2)
    print("Maximum number of words that can be inserted :- ",int(bt/6))
    text1=input("\nEnter data to be encoded:- ")
    l=len(text1)
    if(l<=bt):
        print("\nInputed message can be hidden in the cover file\n")
        txt_encode(text1)
    else:
        print("\nString is too big please reduce string size")
        encode_txt_data()


# In[4]:


def BinaryToDecimal(binary):
    string = int(binary, 2)
    return string


# In[5]:


def decode_txt_data():
    ZWC_reverse={u'\u200C':"00",u'\u202C':"01",u'\u202D':"11",u'\u200E':"10"}
    stego=input("\nPlease enter the stego file name(with extension) to decode the message:- ")
    file4= open(stego,"r", encoding="utf-8")
    temp=''
    for line in file4: 
        for words in line.split():
            T1=words
            binary_extract=""
            for letter in T1:
                if(letter in ZWC_reverse):
                     binary_extract+=ZWC_reverse[letter]
            if binary_extract=="111111111111":
                break
            else:
                temp+=binary_extract
    print("\nEncrypted message presented in code bits:",temp) 
    lengthd = len(temp)
    print("\nLength of encoded bits:- ",lengthd)
    i=0
    a=0
    b=4
    c=4
    d=12
    final=''
    while i<len(temp):
        t3=temp[a:b]
        a+=12
        b+=12
        i+=12
        t4=temp[c:d]
        c+=12
        d+=12
        if(t3=='0110'):
            decimal_data = BinaryToDecimal(t4)
            final+=chr((decimal_data ^ 170) + 48)
        elif(t3=='0011'):
            decimal_data = BinaryToDecimal(t4)
            final+=chr((decimal_data ^ 170) - 48)
    print("\nMessage after decoding from the stego file:- ",final)


# In[6]:


def txt_steg():
    while True:
        print("\n\t\tTEXT STEGANOGRAPHY OPERATIONS") 
        print("1. Encode the Text message")  
        print("2. Decode the Text message")  
        print("3. Exit")  
        choice1 = int(input("Enter the Choice:"))   
        if choice1 == 1:
            encode_txt_data()
        elif choice1 == 2:
            decrypted=decode_txt_data() 
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[7]:


def msgtobinary(msg):
    if type(msg) == str:
        result= ''.join([ format(ord(i), "08b") for i in msg ])
    
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result= [ format(i, "08b") for i in msg ]
    
    elif type(msg) == int or type(msg) == np.uint8:
        result=format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")
    
    return result


# In[8]:


def encode_img_data(img):
    data=input("\nEnter the data to be Encoded in Image :")    
    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')
  
    nameoffile = input("\nEnter the name of the New Image (Stego Image) after Encoding(with extension):")
    
    no_of_bytes=(img.shape[0] * img.shape[1] * 3) // 8
    
    print("\t\nMaximum bytes to encode in Image :", no_of_bytes)
    
    if(len(data)>no_of_bytes):
        raise ValueError("Insufficient bytes Error, Need Bigger Image or give Less Data !!")
    
    data +='*^*^*'    
    
    binary_data=msgtobinary(data)
    print("\n")
    print(binary_data)
    length_data=len(binary_data)
    
    print("\nThe Length of Binary data",length_data)
    
    index_data = 0
    
    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
    cv2.imwrite(nameoffile,img)
    print("\nEncoded the data successfully in the Image and the image is successfully saved with name ",nameoffile)


# In[9]:


def decode_img_data(img):
    data_binary = ""
    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*": 
                    print("\n\nThe Encoded data which was hidden in the Image was :--  ",decoded_data[:-5])
                    return 


# In[10]:


def img_steg():
    while True:
        print("\n\t\tIMAGE STEGANOGRAPHY OPERATIONS\n") 
        print("1. Encode the Text message") 
        print("2. Decode the Text message") 
        print("3. Exit")  
        choice1 = int(input("Enter the Choice: "))   
        if choice1 == 1:
            image=cv2.imread("Sample_cover_files/cover_image.jpg")
            encode_img_data(image)
        elif choice1 == 2:
            image1=cv2.imread(input("Enter the Image you need to Decode to get the Secret message :  "))
            decode_img_data(image1)
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[11]:


def encode_aud_data():
    import wave

    nameoffile=input("Enter name of the file (with extension) :- ")
    song = wave.open(nameoffile, mode='rb')

    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)

    data = input("\nEnter the secret message :- ")

    res = ''.join(format(i, '08b') for i in bytearray(data, encoding ='utf-8'))     
    print("\nThe string after binary conversion :- " + (res))   
    length = len(res)
    print("\nLength of binary after conversion :- ",length)

    data = data + '*^*^*'

    result = []
    for c in data:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    j = 0
    for i in range(0,len(result),1): 
        res = bin(frame_bytes[j])[2:].zfill(8)
        if res[len(res)-4]== result[i]:
            frame_bytes[j] = (frame_bytes[j] & 253)      #253: 11111101
        else:
            frame_bytes[j] = (frame_bytes[j] & 253) | 2
            frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
        j = j + 1
    
    frame_modified = bytes(frame_bytes)

    stegofile=input("\nEnter name of the stego file (with extension) :- ")
    with wave.open(stegofile, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    print("\nEncoded the data successfully in the audio file.")    
    song.close()


# In[12]:


def decode_aud_data():
    import wave

    nameoffile=input("Enter name of the file to be decoded :- ")
    song = wave.open(nameoffile, mode='rb')

    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)

    extracted = ""
    p=0
    for i in range(len(frame_bytes)):
        if(p==1):
            break
        res = bin(frame_bytes[i])[2:].zfill(8)
        if res[len(res)-2]==0:
            extracted+=res[len(res)-4]
        else:
            extracted+=res[len(res)-1]
    
        all_bytes = [ extracted[i: i+8] for i in range(0, len(extracted), 8) ]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "*^*^*":
                print("The Encoded data was :--",decoded_data[:-5])
                p=1
                break  


# In[13]:


def aud_steg():
    while True:
        print("\n\t\tAUDIO STEGANOGRAPHY OPERATIONS") 
        print("1. Encode the Text message")  
        print("2. Decode the Text message")  
        print("3. Exit")  
        choice1 = int(input("Enter the Choice:"))   
        if choice1 == 1:
            encode_aud_data()
        elif choice1 == 2:
            decode_aud_data()
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[14]:


def KSA(key):
    key_length = len(key)
    S=list(range(256)) 
    j=0
    for i in range(256):
        j=(j+S[i]+key[i % key_length]) % 256
        S[i],S[j]=S[j],S[i]
    return S


# In[15]:


def PRGA(S,n):
    i=0
    j=0
    key=[]
    while n>0:
        n=n-1
        i=(i+1)%256
        j=(j+S[i])%256
        S[i],S[j]=S[j],S[i]
        K=S[(S[i]+S[j])%256]
        key.append(K)
    return key


# In[16]:


def preparing_key_array(s):
    return [ord(c) for c in s]


# In[17]:


def encryption(plaintext):
    print("Enter the key : ")
    key=input()
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(plaintext)))
    plaintext=np.array([ord(i) for i in plaintext])

    cipher=keystream^plaintext
    ctext=''
    for c in cipher:
        ctext=ctext+chr(c)
    return ctext


# In[18]:


def decryption(ciphertext):
    print("Enter the key : ")
    key=input()
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(ciphertext)))
    ciphertext=np.array([ord(i) for i in ciphertext])

    decoded=keystream^ciphertext
    dtext=''
    for c in decoded:
        dtext=dtext+chr(c)
    return dtext


# In[19]:


def embed(frame):
    data=input("\nEnter the data to be Encoded in Video :") 
    data=encryption(data)
    print("The encrypted data is : ",data)
    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')

    data +='*^*^*'
    
    binary_data=msgtobinary(data)
    length_data = len(binary_data)
    
    index_data = 0
    
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
        return frame


# In[20]:


def extract(frame):
    data_binary = ""
    final_decoded_msg = ""
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*": 
                    for i in range(0,len(decoded_data)-5):
                        final_decoded_msg += decoded_data[i]
                    final_decoded_msg = decryption(final_decoded_msg)
                    print("\n\nThe Encoded data which was hidden in the Video was :--\n",final_decoded_msg)
                    return 


# In[21]:


def encode_vid_data():
    cap=cv2.VideoCapture("Sample_cover_files/cover_video.mp4")
    vidcap = cv2.VideoCapture("Sample_cover_files/cover_video.mp4")    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))

    size = (frame_width, frame_height)
    out = cv2.VideoWriter('stego_video.mp4',fourcc, 25.0, size)
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    cap.release()
    print("Total number of Frame in selected Video :",max_frame)
    print("Enter the frame number where you want to embed data : ")
    n=int(input())
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:    
            change_frame_with = embed(frame)
            frame_ = change_frame_with
            frame = change_frame_with
        out.write(frame)
    
    print("\nEncoded the data successfully in the video file.")
    return frame_


# In[22]:


def decode_vid_data(frame_):
    cap = cv2.VideoCapture('stego_video.mp4')
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    print("Total number of Frame in selected Video :",max_frame)
    print("Enter the secret frame number from where you want to extract data")
    n=int(input())
    vidcap = cv2.VideoCapture('stego_video.mp4')
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:
            extract(frame_)
            return


# In[23]:


def vid_steg():
    while True:
        print("\n\t\tVIDEO STEGANOGRAPHY OPERATIONS") 
        print("1. Encode the Text message")  
        print("2. Decode the Text message")  
        print("3. Exit")  
        choice1 = int(input("Enter the Choice:"))   
        if choice1 == 1:
            a=encode_vid_data()
        elif choice1 == 2:
            decode_vid_data(a)
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


# In[24]:


def main():
    print("\t\t      STEGANOGRAPHY")   
    while True:  
        print("\n\t\t\tMAIN MENU\n")  
        print("1. IMAGE STEGANOGRAPHY {Hiding Text in Image cover file}")  
        print("2. TEXT STEGANOGRAPHY {Hiding Text in Text cover file}")  
        print("3. AUDIO STEGANOGRAPHY {Hiding Text in Audio cover file}")
        print("4. VIDEO STEGANOGRAPHY {Hiding Text in Video cover file}")
        print("5. Exit\n")  
        choice1 = int(input("Enter the Choice: "))   
        if choice1 == 1: 
            img_steg()
        elif choice1 == 2:
            txt_steg()
        elif choice1 == 3:
            aud_steg()
        elif choice1 == 4:
            vid_steg()
        elif choice1 == 5:
            break
        else:
            print("Incorrect Choice")
        print("\n\n")


# In[27]:


if __name__ == "__main__":
    main()


# In[ ]:


OUTPUT
		      STEGANOGRAPHY

			MAIN MENU

1. IMAGE STEGANOGRAPHY {Hiding Text in Image cover file}
2. TEXT STEGANOGRAPHY {Hiding Text in Text cover file}
3. AUDIO STEGANOGRAPHY {Hiding Text in Audio cover file}
4. VIDEO STEGANOGRAPHY {Hiding Text in Video cover file}
5. Exit

Enter the Choice: 1

		IMAGE STEGANOGRAPHY OPERATIONS

1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice: 1

Enter the data to be Encoded in Image :their are many things to be learn and explore it

Enter the name of the New Image (Stego Image) after Encoding(with extension):1stegoimage.png
	
Maximum bytes to encode in Image : 203136


0111010001101000011001010110100101110010001000000110000101110010011001010010000001101101011000010110111001111001001000000111010001101000011010010110111001100111011100110010000001110100011011110010000001100010011001010010000001101100011001010110000101110010011011100010000001100001011011100110010000100000011001010111100001110000011011000110111101110010011001010010000001101001011101000010101001011110001010100101111000101010

The Length of Binary data 424

Encoded the data successfully in the Image and the image is successfully saved with name  1stegoimage.png



		IMAGE STEGANOGRAPHY OPERATIONS

1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice: 2
Enter the Image you need to Decode to get the Secret message :  1stegoimage.png


The Encoded data which was hidden in the Image was :--   their are many things to be learn and explore it



		IMAGE STEGANOGRAPHY OPERATIONS

1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice: 3




			MAIN MENU

1. IMAGE STEGANOGRAPHY {Hiding Text in Image cover file}
2. TEXT STEGANOGRAPHY {Hiding Text in Text cover file}
3. AUDIO STEGANOGRAPHY {Hiding Text in Audio cover file}
4. VIDEO STEGANOGRAPHY {Hiding Text in Video cover file}
5. Exit

Enter the Choice: 2

		TEXT STEGANOGRAPHY OPERATIONS
1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice:1
Maximum number of words that can be inserted :-  879

Enter data to be encoded:- i hope i will learn all thing which i have intrest

Inputed message can be hidden in the cover file

The string after binary conversion appyling all the transformation :- 011010010011001111111010011010010010011010010101011011101010011010011111001111111010011010010011001111111010011011101101011010010011011010010110011010010110001111111010011010010110011010011111011010011011011011101000011010010100001111111010011010011011011010010110011010010110001111111010011011101110011010010010011010010011011010010100011010011101001111111010011011101101011010010010011010010011011010011001011010010010001111111010011010010011001111111010011010010010011010011011011011101100011010011111001111111010011010010011011010010100011011101110011011101000011010011111011011101001011011101110111111111111
Length of binary after conversion:-  612

Enter the name of the Stego file after Encoding(with extension):- 1stegotext.txt

Stego file has successfully generated



		TEXT STEGANOGRAPHY OPERATIONS
1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice:2

Please enter the stego file name(with extension) to decode the message:- 1stegotext.txt

Encrypted message presented in code bits: 011010010011001111111010011010010010011010010101011011101010011010011111001111111010011010010011001111111010011011101101011010010011011010010110011010010110001111111010011010010110011010011111011010011011011011101000011010010100001111111010011010011011011010010110011010010110001111111010011011101110011010010010011010010011011010010100011010011101001111111010011011101101011010010010011010010011011010011001011010010010001111111010011010010011001111111010011010010010011010011011011011101100011010011111001111111010011010010011011010010100011011101110011011101000011010011111011011101001011011101110

Length of encoded bits:-  600

Message after decoding from the stego file:-  i hope i will learn all thing which i have intrest



		TEXT STEGANOGRAPHY OPERATIONS
1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice:3




			MAIN MENU

1. IMAGE STEGANOGRAPHY {Hiding Text in Image cover file}
2. TEXT STEGANOGRAPHY {Hiding Text in Text cover file}
3. AUDIO STEGANOGRAPHY {Hiding Text in Audio cover file}
4. VIDEO STEGANOGRAPHY {Hiding Text in Video cover file}
5. Exit

Enter the Choice: 3

		AUDIO STEGANOGRAPHY OPERATIONS
1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice:1
Enter name of the file (with extension) :- sample.wav

Enter the secret message :- this is nice song and it's lyrisc are very good 

The string after binary conversion :- 011101000110100001101001011100110010000001101001011100110010000001101110011010010110001101100101001000000111001101101111011011100110011100100000011000010110111001100100001000000110100101110100001001110111001100100000011011000111100101110010011010010111001101100011001000000110000101110010011001010010000001110110011001010111001001111001001000000110011101101111011011110110010000100000

Length of binary after conversion :-  384

Enter name of the stego file (with extension) :- sample.wav

Encoded the data successfully in the audio file.



		AUDIO STEGANOGRAPHY OPERATIONS
1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice:2
Enter name of the file to be decoded :- sample.wav
The Encoded data was :-- this is nice song and it's lyrisc are very good 



		AUDIO STEGANOGRAPHY OPERATIONS
1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice:3




			MAIN MENU

1. IMAGE STEGANOGRAPHY {Hiding Text in Image cover file}
2. TEXT STEGANOGRAPHY {Hiding Text in Text cover file}
3. AUDIO STEGANOGRAPHY {Hiding Text in Audio cover file}
4. VIDEO STEGANOGRAPHY {Hiding Text in Video cover file}
5. Exit

Enter the Choice: 4

		VIDEO STEGANOGRAPHY OPERATIONS
1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice:1
Total number of Frame in selected Video : 172
Enter the frame number where you want to embed data : 
90

Enter the data to be Encoded in Video :where is my lucky bag and my good tom
Enter the key : 
pranali-15
The encrypted data is :  G¬â1&]¿NJ­¹tôw·/KR&³iÐ&ëÚ<[C

Encoded the data successfully in the video file.



		VIDEO STEGANOGRAPHY OPERATIONS
1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice:2
Total number of Frame in selected Video : 172
Enter the secret frame number from where you want to extract data
90
Enter the key : 
pranali-15


The Encoded data which was hidden in the Video was :--
 where is my lucky bag and my good tom



		VIDEO STEGANOGRAPHY OPERATIONS
1. Encode the Text message
2. Decode the Text message
3. Exit
Enter the Choice:3




			MAIN MENU

1. IMAGE STEGANOGRAPHY {Hiding Text in Image cover file}
2. TEXT STEGANOGRAPHY {Hiding Text in Text cover file}
3. AUDIO STEGANOGRAPHY {Hiding Text in Audio cover file}
4. VIDEO STEGANOGRAPHY {Hiding Text in Video cover file}
5. Exit

Enter the Choice: 5
