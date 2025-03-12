# 将模型代码移动到 residents/models.py
# 这里假设 models.py 中的内容是关于居民信息的

from django.db import models


class ResidentsInfo(models.Model):
    """
        数据库中民居表：表中的字段、 表名
    """

    resident_province = models.CharField(max_length=50, verbose_name='民居省份', db_column='民居省份')
    resident_number = models.CharField(max_length=100, verbose_name='民居编号', db_column='民居编号')
    resident_type = models.TextField(verbose_name='民居类型名称', db_column='民居类型名称')
    resident_overview = models.TextField(verbose_name='民居概述', db_column='民居概述')
    distribution = models.TextField(verbose_name='分布', db_column='分布')
    structure = models.TextField(verbose_name='形制', db_column='形制')
    construct = models.TextField(verbose_name='建造', db_column='建造')
    represent_building = models.TextField(verbose_name='代表建筑', db_column='代表建筑')
    factor = models.TextField(verbose_name='成因', db_column='成因')
    comparison_evolution = models.TextField(verbose_name='比较与演变', db_column='比较与演变')
    attached_picture = models.TextField(verbose_name='附图', db_column='附图')

    class Meta:
        db_table = '民居表'
        verbose_name = '民居信息'
        verbose_name_plural = '民居信息'
