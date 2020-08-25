
import os
import csv
import time
import glob
import shutil
import string

drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
print(drives)

num = range(0,len(drives))
print('choice', '-------', 'drive')
d = dict(zip(num, drives))
for i in d:
    print(i + 1 ,'------------', d[i])
selection = input('Please select network picture drive: ')
selection = int(selection) - 1
os.chdir(d[selection])
os.chdir('My Drive')
my_dir = (os.getcwd())
print('contents of "%s"' %my_dir)
files = os.listdir(my_dir)
n_files = range(0, len(files))
df = dict(zip(n_files, files))
for j in df:
    print(j + 1, '------------', df[j])
d_choice = input('PLease select the picture folder: ')
d_choice = int(d_choice) - 1
os.chdir(df[d_choice])
cur_dir = os.getcwd()
print('folder selected: %s' %cur_dir)


time_ref = time.strftime('%m_%d_%y_%H_%M_%S')
info = ['RMA', 'Serial Number', 'Date', 'Time']
with open('phone_db_' + time_ref + '.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(info)

station = False
while not station:
    io = input('Please select or Scan [Inbound][i] or [Outbound][o] Station: ')
    station_response = ['i', 'I', 'inbound','o', 'O', 'outbound']
    if io in station_response:
        station = True

finished = False

def cleanup():
    os.chdir(cur_dir)
    print('looking into folder %s ' %os.getcwd())
    print(os.getcwd())
    shutil.rmtree('Camera')

while not finished:

    rma = False
    while not rma:
        answers = ['', 'y', 'Y']
        start = False
        while not start:
            rma_in = input('Scan RMA and press ENTER: ')
            if len(rma_in) != 0:
                start = True
        yesno = input('If RMA "%s" is correct press Enter, [y/Y] or [N/n] if need to re-scan ' % rma_in)
        if yesno in answers:
            rma = True


    scan_complete = False

    while not scan_complete:
        answers = ['', 'y', 'Y']
        start = False
        while not start:
            scan = input('Place phone face up, scan Serial Number and press ENTER: ')
            if len(scan) != 0:
                start = True
        yesno = input('If Serial Number "%s" is correct press Enter, [y/Y] or [N/n] if need to re-scan ' % scan)
        if yesno in answers:
            scan_complete = True


    print("cleaning camera's memory")
    os.system('adb shell rm /sdcard/DCIM/Camera/*jpg')

    def remove_folder():
        shutil.rmtree('Camera')

    os.system('adb shell input keyevent KEYCODE_FOCUS')
    print('Focusing lens.. waiting 3 seconds')
    time.sleep(2)
    os.system('adb shell input keyevent KEYCODE_CAMERA')
    time.sleep(8)
    os.system('adb pull /sdcard/DCIM/Camera/ .')
    time.sleep(3)
    os.system('adb shell rm /sdcard/DCIM/Camera/*.jpg')

    cam_dir = os.path.dirname('Camera')

    try:
        os.stat('Camera')
    except:
        os.mkdir('Camera')

    files = glob.glob('IMG*')
    for i in files:
        shutil.copy(i, 'Camera')
        print(i)
        os.remove(i)
    os.chdir('Camera')
    pic = glob.glob('*jpg')
    pic = ' '.join(pic)
    print(pic)
    station_i = ['i', 'I', 'inbound']
    station_o = ['o', 'O', 'outbound']
    time.sleep(2)
    if io in station_i:
        shutil.copy2(pic, 'RMA_' + rma_in + '_SN_' + scan + '_inb_' + '_front_' + time.strftime('%m%d%y%H%M%S') + '.jpg')
    elif io in station_o:
        shutil.copy2(pic, 'RMA_' + rma_in + '_SN_' + scan + '_out_' + '_front_' + time.strftime('%m%d%y%H%M%S') + '.jpg')
    file_to_go = glob.glob('IMG*')
    file_to_go = ' '.join(file_to_go)
    os.remove(file_to_go)
    file_to_move = glob.glob('*jpg')
    file_to_move = ' '.join(file_to_move)
    shutil.copy2(file_to_move, cur_dir)
    time.sleep(2)
    os.remove(file_to_move)
    os.chdir(cur_dir)

    user = input('Turn phone upsidedown and press ENTER ')

    upsidedown = False
    while not upsidedown:
         if user == '':
            print('SN: "%s"' % scan)
            upsidedown = True

    os.system('adb shell input keyevent KEYCODE_FOCUS')
    print('Focusing lens.. waiting 3 seconds')
    time.sleep(2)
    os.system('adb shell input keyevent KEYCODE_CAMERA')
    time.sleep(8)
    os.system('adb pull /sdcard/DCIM/Camera/ .')
    time.sleep(3)
    os.system('adb shell rm /sdcard/DCIM/Camera/*.jpg')
    files = glob.glob('IMG*')
    for i in files:
        shutil.copy(i, 'Camera')
        os.remove(i)
    os.chdir('Camera')
    pic = glob.glob('IMG*')
    pic = ' '.join(pic)
    station_i = ['i', 'I', 'inbound']
    station_o = ['o', 'O', 'outbound']
    time.sleep(2)
    if io in station_i:
        shutil.copy2(pic, 'RMA_' + rma_in + '_SN_' + scan + '_inb_' + '_back_' + time.strftime('%m%d%y%H%M%S') + '.jpg')
    elif io in station_o:
        shutil.copy2(pic, 'RMA_' + rma_in + '_SN_' + scan + '_out_' + '_back_' + time.strftime('%m%d%y%H%M%S') + '.jpg')
    file_to_go = glob.glob('IMG*')
    file_to_go = ' '.join(file_to_go)
    os.remove(file_to_go)
    file_to_move = glob.glob('*jpg')
    file_to_move = ' '.join(file_to_move)
    shutil.copy2(file_to_move, cur_dir)
    time.sleep(2)
    os.remove(file_to_move)
    os.chdir(cur_dir)
    remove_folder()

    items = [rma_in, scan, time.strftime('%m/%d/%y/'), time.strftime ('%H:%M:%S')]
    with open('phone_db_' + time_ref + '.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(items)

    print(80*'-')
    print(' ')
    print(80*'-')

    out = input('to exit type "q" or "any key" to continue: ')
    if out == 'q':
        finished = True
