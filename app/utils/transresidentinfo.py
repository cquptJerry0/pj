from app.models import ResidentsInfo


def get_resident_info(condition={}, flag=False, start=4, end=11):
    """
    前端数据显示所用的数据信息：获取数据库中某个数据的详情
    @param condition: 数据库查找的条件
    @param flag: 将 queryset 数据转换为字典形式的标志
    @param start: 详情页面内容部分的 for 循环模板开始的字段位置
    @param end: 详情页面内容部分的 for 循环模板结束的字段位置
    @return: 返回民居信息数据结果
    """

    # 根据筛选条件获取数据库中的相关民居数据
    residents_info = ResidentsInfo.objects.filter(**condition)

    # 判断数据库中是否有查找到的数据，没有直接返回0，转至错误页面
    if residents_info.count() < 1:
        return 0

    # 页面内容显示上加上缩进
    tab = 4 * '&nbsp;'
    # 转换附图数据
    for obj in residents_info:
        obj.resident_overview = tab + obj.resident_overview
        obj.distribution = tab + obj.distribution
        obj.structure = tab + obj.structure
        obj.construct = tab + obj.construct
        obj.represent_building = tab + obj.represent_building
        obj.factor = tab + obj.factor
        obj.comparison_evolution = tab + obj.comparison_evolution
        trans = obj.attached_picture.maketrans('', '', '[]\' ')
        obj.attached_picture = obj.attached_picture.translate(trans)
        obj.attached_picture = obj.attached_picture.split(',')

    # 若转换字典 flag 启用并且当前只有一条查找到的数据
    if flag and residents_info.count() == 1:
        obj.__dict__.pop('_state')
        info = list(obj.__dict__.values())
        records_name = []
        for record in ResidentsInfo._meta.fields:
            records_name.append(record.verbose_name)

        # 返回民居表字段信息，当前民居信息，以及要循环的页面信息
        return [records_name, info, zip(records_name[start:end], info[start:end])]

    return residents_info


def get_table_info(condition={}):
    """
    后台管理所有的数据信息：表格形式显示的
    @param condition: 数据库的查找条件
    @return: 返回符合条件的所有数据
    """

    # 根据筛选条件获取数据库中的相关民居数据
    residents_info = ResidentsInfo.objects.filter(**condition)

    # 表中所有字段信息
    records_name = []
    for record in ResidentsInfo._meta.fields:
        records_name.append(record.verbose_name)

    # 判断数据库中是否有查找到的数据
    if residents_info.count() < 1:
        return [records_name, 0]

    # 转换附图数据
    for obj in residents_info:
        trans = obj.attached_picture.maketrans('', '', '[]\' ')
        obj.attached_picture = obj.attached_picture.translate(trans)
        obj.attached_picture = obj.attached_picture.split(',')

    return [records_name, residents_info]

