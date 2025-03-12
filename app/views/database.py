import os
from app.models import ResidentsInfo
import logging

logger = logging.getLogger(__name__)


def process_file(file_path, file_name):
    resident_info = {'民居编号': file_name, '民居省份': file_name.split('.')[0], '附图': []}
    data = os.listdir(os.path.join(file_path, file_name))
    for file in data:
        path = os.path.join(file_path, file_name, file)
        file_type = file.split('.')[-1]
        column = file.split('.')[-2]

        if file_type == 'txt' and column != '整理者':
            with open(path, mode='r') as f:
                content = f.read()
                resident_info[column] = content
        else:
            resident_info['附图'].append('data/' + file_name + '/' + file)

    return resident_info


def database_table_init():
    """
    数据库民居表数据初始化
    """

    file_path = os.path.join(os.getcwd(), 'app\static\data')  # 民居表数据所在路径
    residents_info = []  # 民居表中的记录内容

    # 判断数据文件是否存在
    if os.path.exists(file_path):
        residents_number = os.listdir(file_path)  # 民居编号数据
        # 添加民居表中的记录内容
        for file_name in residents_number:
            resident_info = process_file(file_path, file_name)
            residents_info.append(resident_info)

        # 数据初始化到数据库表中
        for resident in residents_info:
            data = ResidentsInfo(
                resident_province=resident['民居省份'],
                resident_number=resident['民居编号'],
                resident_type=resident.get('民居类型名称', ''),
                resident_overview=resident.get('民居概述', ''),
                distribution=resident.get('分布', ''),
                structure=resident.get('形制', ''),
                construct=resident.get('建造', ''),
                represent_building=resident.get('代表建筑', ''),
                factor=resident.get('成因', ''),
                comparison_evolution=resident.get('比较与演变', ''),
                attached_picture=resident['附图']
            )
            data.save()

        logger.info('数据库表初始化成功！')
    else:
        logger.error('数据不存在！')