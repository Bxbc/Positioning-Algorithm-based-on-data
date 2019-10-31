import os
from struct import *
import binascii

def process_one_record(raw_file):
    s = []

    c = raw_file.read(7)
    if len(c) != 7:
        return
    else: p1 = unpack('4s2s1s',c)
    for i in p1:
        s.append(binascii.b2a_hex(i[::-1]))

    c = raw_file.read(7)
    p2 = unpack('HBBBBB',c)
    for i in p2:
        if isinstance(i, int):
            s.append(i)
        else:
            s.append(int(binascii.b2a_hex(i[::-1]), 16))

    c = raw_file.read(4)
    p3 = unpack('2H',c)
    for i in p3:
        s.append(i)
    # print s

    c = raw_file.read(18)
    p4 = unpack('2Qh',c)
    for i in range(len(p4)):
        if i == 2:
            s.append(float(p4[i])/10)
        else:
            s.append(float(p4[i]) / (10 ** 8))
            # float(i) / (10 ** 8)
    # print s

    c = raw_file.read(18)
    p5 = unpack('dfiH',c)

    for i in p5:
        s.append(i)
    fout = open('C:/Users/BC/Desktop/washing_data/测试.txt', 'a')
    print(s, file=fout)
    fout.close()
    return

if __name__ == '__main__':
    raw_file = open('C:/Users/BC/Desktop/washing_data/bin/32050000_0031_20170717_101949_48MHz_72MHz_25kHz_V_M.bin', 'rb')

    process_one_record(raw_file)
    while raw_file.read(123 * 16 + 6 - 54):
          process_one_record(raw_file)
    raw_file.close()




