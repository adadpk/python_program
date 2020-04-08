# coding:utf-8
import piexif
import os
import re
import shutil
import imghdr
import time
import datetime
from PIL import Image


def set_date(image_name, im_time=None):
    image_pwd = os.path.join(in_pwd, image_name)
    exif_info_dict = {
        piexif.ExifIFD.DateTimeOriginal: im_time,
        piexif.ExifIFD.DateTimeDigitized: im_time,
    }
    # todo add Camera Model setting
    # from_set = {272: 'Google Pixel 4XL'}  # Camera Model setting
    # exif_dict = {'Exif': exif_info_dict, '0th': from_set}
    exif_dict = {'Exif': exif_info_dict}
    exif_bytes = piexif.dump(exif_dict)
    im = Image.open(image_pwd)
    im.save(os.path.join(out_pwd, image_name), exif=exif_bytes, quality=100)
    print('set ' + image_name + ' time: ' + im_time)


def image_list():
    return os.listdir(in_pwd)


def handel_name(image_name):
    """
    format 1: 2013-07-15_59
    format 2: IMG_20140423_140222_8
    format 3: 20121117_115926_588 or 20xxxxxxx
    format 4: QQ截图20140513185542_1
    :param image_name: image name
    :return: image token time
    """
    try:
        if '-' == image_name[4] and '-' == image_name[7]:
            # handle format 1: 2013-07-15_59
            date_list = image_name.split('-')
            date_year = date_list[0]
            date_month = date_list[1]
            date_day = date_list[2][:2]
            image_date = date_year + ':' + date_month + ':' + date_day + ' 08:20:00'
            return image_date
        elif '_' == image_name[3] and '_' == image_name[12]:
            # handle format 2: IMG_20140423_140222_8
            date_year = image_name[4:8]
            date_month = image_name[8:10]
            date_day = image_name[10:12]
            image_date = date_year + ':' + date_month + ':' + date_day + ' 08:20:00'
            return image_date
        elif '20' == image_name[:2] and image_name[4:6] in ['01', '02', '03', '04', '05', '06', '07', '08', '09',
                                                            '10', '11', '12'] and int(image_name[6:8]) <= 31:
            # handle format 3: 20121117_115926_588 or 20xxxxxxx
            date_year = image_name[:4]
            date_month = image_name[4:6]
            date_day = image_name[6:8]
            image_date = date_year + ':' + date_month + ':' + date_day + ' 08:20:00'
            return image_date
        else:
            try:
                res = re.search(r'\d+', image_name).group()
                if '20' == res[:2] and res[4:6] in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                                                    '11', '12'] and int(res[6:8]) <= 31:
                    date_year = res[:4]
                    date_month = res[4:6]
                    date_day = res[6:8]
                    image_date = date_year + ':' + date_month + ':' + date_day + ' 08:20:00'
                    return image_date
                else:
                    return ''
            except:
                return ''
    except:
        return ''


def load_image_info(image_name):
    try:
        image_info_dict = piexif.load(os.path.join(in_pwd, image_name))
    except:
        return handel_name(image_name)
    else:
        if {} == image_info_dict['Exif']:
            return handel_name(image_name)
        else:
            # print('keys: ', image_info_dict['Exif'].keys())
            if 36867 in image_info_dict['Exif'].keys() and 36868 in image_info_dict['Exif'].keys():
                return 'copy'
            else:
                return handel_name(image_name)


def copy_file(image_name, info=False):
    """
    copy file to path
    :param image_name: image name
    :param info: no handle file folder
    :return:
    """
    new_pwd = out_pwd + 'not_handle_file/'
    if not os.path.exists(new_pwd):
        os.mkdir(new_pwd)
    if info:
        shutil.copyfile(os.path.join(in_pwd, image_name), os.path.join(out_pwd, image_name))
        print('copy file info ' + image_name)
    else:
        shutil.copyfile(os.path.join(in_pwd, image_name), os.path.join(new_pwd, image_name))
        print('copy file no info ' + image_name)


def main(image_time=None):
    # global image_time
    if not os.path.exists(out_pwd):
        os.mkdir(out_pwd)
    # image_time = '2019:04:04 04:04:04'
    name_list = image_list()
    if image_time:
        for i in name_list:
            if 'jpeg' == imghdr.what(os.path.join(in_pwd, i)):
                set_date(i, im_time=image_time)
            else:
                copy_file(i)
    elif default_image_time:
        # setting default image time
        for i in name_list:
            if 'jpeg' == imghdr.what(os.path.join(in_pwd, i)):
                return_image_time = load_image_info(i)
                if '' != return_image_time and 'copy' != return_image_time:
                    print('set image: ', return_image_time)
                    set_date(i, im_time=return_image_time)
                elif 'copy' == return_image_time:
                    copy_file(i, info=True)
                else:
                    # handle_no_date_image(i, out_pwd, in_pwd)
                    print('set default image: ', return_image_time)
                    set_date(i, im_time=default_image_time)
            else:
                copy_file(i)
    else:
        # not setting default image time
        for i in name_list:
            if 'jpeg' == imghdr.what(os.path.join(in_pwd, i)):
                return_image_time = load_image_info(i)
                if '' != return_image_time and 'copy' != return_image_time:
                    set_date(i, im_time=return_image_time)
                elif 'copy' == return_image_time:
                    copy_file(i, info=True)
                else:
                    copy_file(i)
            else:
                copy_file(i)


def time_handle(input_time):
    # time.struct_time(tm_year=2020, tm_mon=4, tm_mday=7, tm_hour=0,
    # tm_min=40, tm_sec=42, tm_wday=1, tm_yday=98, tm_isdst=0)
    local_time_list = time.localtime()
    try:
        datetime.datetime.strptime(input_time, '%Y:%m:%d %H:%M:%S')
    except ValueError as e:
        return False
    else:
        # 2020:12:31 23: 20:58
        date_1 = input_time.split()[0].split(':')  # ['2020', '12', '31']
        date_2 = input_time.split()[1].split(':')  # ['23', '20', '58']
        if int(date_1[0]) > local_time_list.tm_year:
            return False
        elif int(date_1[0]) == local_time_list.tm_year:
            if int(date_1[1]) > local_time_list.tm_mon:
                return False
            elif int(date_1[1]) == local_time_list.tm_mon:
                if int(date_1[2]) > local_time_list.tm_mday:
                    return False
                elif int(date_1[2]) == local_time_list.tm_mday:
                    if int(date_2[0]) > local_time_list.tm_hour:
                        return False
                    elif int(date_2[0]) == local_time_list.tm_hour:
                        if int(date_2[1]) > local_time_list.tm_min:
                            return False
                        elif int(date_2[1]) == local_time_list.tm_min:
                            if int(date_2[2]) > local_time_list.tm_sec:
                                return False
                            else:
                                return True
                        else:
                            return True
                    else:
                        return True
                else:
                    return True
            else:
                return True
        else:
            return True


def is_folder(folder_path):
    if folder_path.endswith('/') and os.path.isdir(folder_path):
        return True
    else:
        return False


if __name__ == '__main__':
    """
    in_pwd: 图片所在文件夹
    out_pwd: 图片输出文件夹
    res: 图片名称
    image_time: 修改的图片时间
    image_pwd: 图片绝对路径
    """
    print('================菜单=====================\n')
    print('只支持JPEG文件的时间设置\n')
    print('普通手机照片以jpg和jpeg结尾一般都支持\n')
    print('================功能列表=====================')
    print('1.直接设置时间')
    print('2.根据照片名字设置时间')
    com = input('请输入序号：')
    while com not in ['1', '2']:
        com = input('请输入正确的序号：')
    in_pwd = input('请输入要处理的图片绝对路径/格式(/folder1/image/) ').strip()
    while not is_folder(in_pwd):
        in_pwd = input('路径输入错误，请重新输入/格式(/folder1/image/) ').strip()
    default_image_time = None
    out_pwd = os.path.dirname(in_pwd) + '_new/'

    if 1 == int(com):
        set_time = input('请输入要设置的时间/格式为(2020:04:04 08:20:00): ').strip()
        while not time_handle(set_time):
            set_time = input('时间不合法，请重新输入/格式为(2020:04:04 08:20:00): ').strip()
        main(image_time=set_time)

    elif 2 == int(com):
        time_set_com = input('是否要为名称读取时间失败的照片设置默认时间y/n? (默认为n) :')
        if 'y' == time_set_com or 'Y' == time_set_com:
            default_image_time = input('请输入要设置的时间/格式为(2020:04:04 08:20:00): ').strip()
            while not time_handle(default_image_time):
                default_image_time = input('时间不合法，请重新输入/格式为(2020:04:04 08:20:00): ').strip()
            main()
        elif 'n' == time_set_com or 'N' == time_set_com or '' == time_set_com:
            main()
        else:
            main()


