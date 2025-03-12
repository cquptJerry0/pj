import os
import shutil

from django import forms
from django.shortcuts import render
from django.http import JsonResponse
from app.models import ResidentsInfo
from app.utils.transresidentinfo import get_table_info
from app.utils.pagination import Pagination
from app.utils.bootstrap import BootStrapModelForm
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError


class MultipleFileField(forms.FileField):
    def clean(self, data, initial=None):
        if not data:
            if self.required:
                raise ValidationError(self.error_messages['required'])
            return initial

        # 如果是单个文件，转换为列表
        if not isinstance(data, list):
            data = [data]

        result = []
        for file in data:
            cleaned_file = super().clean(file)
            result.append(cleaned_file)

        return result


class ResidentModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = []

    class Meta:
        model = ResidentsInfo
        fields = '__all__'


def resident_list(request):
    """
    后台管理之民居列表查询操作
    @param request: 请求对象
    @return: 返回 resident_list.html 页面
    """

    form = ResidentModelForm()

    # 搜索条件
    province = request.GET.get('province', '')
    if province:
        # 符合搜索条件的数据
        residents_info = get_table_info(condition={'resident_province': province})
    else:
        # 数据库所有数据
        residents_info = get_table_info()

    error_msg = ''
    # 数据库中不存在该数据
    if residents_info[1] == 0:
        error_msg = '数据不存在！请重新输入'
        data = {
            'table_name': ResidentsInfo._meta.verbose_name,
            'residents_info': get_table_info()[1],
            'records_name': residents_info[0],
            'search': province,
            'error_msg': error_msg,
            'form': form,
        }
        return render(request, 'resident_list.html', data)

    # 分页数据
    page_object = Pagination(request, residents_info[1])
    page_queryset = page_object.page_queryset
    page_html = page_object.html()

    data = {
        'table_name': ResidentsInfo._meta.verbose_name,
        'residents_info': residents_info[1],
        'records_name': residents_info[0],
        'page_queryset': page_queryset,
        'page_html': page_html,
        'search': province,
        'error_msg': error_msg,
        'form': form,
    }

    return render(request, 'resident_list.html', data)


class ResidentAddModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = []

    class Meta:
        model = ResidentsInfo
        fields = '__all__'

    # 重写民居编号的验证钩子方法
    def clean_resident_number(self):
        resident_number = self.cleaned_data['resident_number']

        exists = ResidentsInfo.objects.filter(resident_number=resident_number).exists()
        if exists:
            raise ValidationError('该民居编号已存在！')

        # 验证通过，把用户输入的值返回
        return resident_number


@csrf_exempt
def resident_add(request):
    form = ResidentAddModelForm(data=request.POST)
    if form.is_valid():
        ResidentsInfo.objects.create(
            resident_province=form.data.get('resident_province'),
            resident_number=form.data.get('resident_number'),
            resident_type=form.data.get('resident_type'),
            resident_overview=form.data.get('resident_overview'),
            distribution=form.data.get('distribution'),
            structure=form.data.get('structure'),
            construct=form.data.get('construct'),
            represent_building=form.data.get('represent_building'),
            factor=form.data.get('factor'),
            comparison_evolution=form.data.get('comparison_evolution'),
        )
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def resident_edit(request, nid):
    form = ResidentModelForm(data=request.POST)
    if form.is_valid():
        condition = {'id': nid}
        ResidentsInfo.objects.filter(**condition).update(
            resident_type=form.data.get('resident_type'),
            resident_overview=form.data.get('resident_overview'),
            distribution=form.data.get('distribution'),
            structure=form.data.get('structure'),
            construct=form.data.get('construct'),
            represent_building=form.data.get('represent_building'),
            factor=form.data.get('factor'),
            comparison_evolution=form.data.get('comparison_evolution'),
        )
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def resident_delete(request, nid):
    """
    后台管理之民居删除操作 (Ajax 请求)
    @param request: 请求对象
    @param nid: 当前选择的民居 id
    @return: 返回 Ajax 响应
    """

    condition = {'id': nid}

    # 判断当前要删除的对象是否存在
    exists = ResidentsInfo.objects.filter(**condition).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '删除失败，数据不存在！请尝试刷新页面！'})

    # 删除数据库中的记录
    ResidentsInfo.objects.filter(**condition).delete()

    return JsonResponse({'status': True})





