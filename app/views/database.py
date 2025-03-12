import os
from app.models import ResidentsInfo


def database_table_init():
    """
    数据库民居表数据初始化
    """

    file_path = os.path.join(os.getcwd(), 'app\static\data')  # 民居表数据所在路径
    residents_info = []  # 民居表中的记录内容
    flag = 0  # 操作标志

    # 判断数据文件是否存在
    if os.path.exists(file_path):

        residents_number = os.listdir(file_path)  # 民居编号数据
        # 添加民居表中的记录内容
        for file_name in residents_number:

            resident_info = {}  # 每个记录的内容
            resident_info['民居编号'] = file_name
            resident_info['民居省份'] = file_name.split('.')[0]
            resident_info['附图'] = []

            data = os.listdir(os.path.join(file_path, file_name))
            for file in data:
                path = os.path.join(file_path, file_name, file)
                file_type = file.split('.')[-1]
                column = file.split('.')[-2]

                if file_type == 'txt':
                    if column == '整理者':
                        continue

                    with open(path, mode='r') as f:
                        content = f.read()
                        resident_info[column] = content

                else:
                    resident_info['附图'].append('data/' + file_name + '/' + file)

            residents_info.append(resident_info)
        flag = 1

    else:
        print('数据不存在！')

    # 数据初始化到数据库表中
    for resident in residents_info:
        data = ResidentsInfo()  # 实例化一条记录
        # 添加记录
        data.resident_province = resident['民居省份']
        data.resident_number = resident['民居编号']
        data.resident_type = resident['民居类型名称']
        data.resident_overview = resident['民居概述']
        data.distribution = resident['分布']
        data.structure = resident['形制']
        data.construct = resident['建造']
        data.represent_building = resident['代表建筑']
        data.factor = resident['成因']
        data.comparison_evolution = resident['比较与演变']
        data.attached_picture = resident['附图']
        # 将记录保存到数据库表中
        data.save()

    if flag:
        print('数据库表初始化成功！')
    else:
        print('数据库表初始化失败！')