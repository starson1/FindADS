import csv
import datetime
filename = input("$MFT path : ")

fp = open(filename,"rb")
data = fp.read()
def BtoL(bytearr):
    res = "0x00"
    for i in range(0,len(bytearr)):
        res += format(bytearr[-1],'02x')
        bytearr = bytearr[:-1]
    return res
name_list =[]
for i in range(0,len(data),0x400):
    chnk = data[i:i+0x400]
    count =0
    attr = chnk[0x38:0x4C]
    offset = 0x38
    if chnk[:4] == b'FILE':
        datastr = []
        while(attr != b'\xff\xff\xff\xff'):
            attr = chnk[offset:offset+4]
            leng = eval(BtoL(chnk[offset+4:offset+8]))
            if attr == b'\x80\x00\x00\x00':
                count +=1
                datastr.append(chnk[offset+0x10:offset+leng])
                
            if attr == b'\x30\x00\x00\x00':
                name = chnk[offset+0x5a:offset+leng]
                try:
                    ctime = datetime.datetime.fromtimestamp(eval(BtoL(chnk[offset+0x20:offset+0x28]))/10000000 -11644473600)
                    atime = datetime.datetime.fromtimestamp(eval(BtoL(chnk[offset+0x28:offset+0x30]))/10000000 -11644473600)   
                    mtime = datetime.datetime.fromtimestamp(eval(BtoL(chnk[offset+0x30:offset+0x38]))/10000000 -11644473600)
                    rtime = datetime.datetime.fromtimestamp(eval(BtoL(chnk[offset+0x38:offset+0x40]))/10000000 -11644473600)
                except:
                    ctime=""
                    atime=""
                    mtime=""
                    rtime=""
            if offset > 0x400:
                break
            offset += leng
        if count >= 2:
                try:
                    name_list.append([hex(i),name.decode('utf-8'),ctime,atime,mtime,rtime,datastr])
                except:
                    name_list.append([hex(i),name,ctime,atime,mtime,rtime])
    print("Searching offset : "+str(hex(i)),end='\r')

with open('result.csv','w',newline='') as f:
    write = csv.writer(f)
    for i in range(0,len(name_list)):
        write.writerow(name_list[i])
    


