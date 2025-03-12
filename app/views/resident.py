
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
from app.utils.widgets import MultipleFileInput


class ResidentModelForm(BootStrapModelForm):
    attached_picture = forms.FileField(
        label='附图',
        required=False,
        widget=MultipleFileInput(attrs={'multiple': True})
    )

    bootstrap_exclude_fields = ['attached_picture']

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
    attached_picture = forms.FileField(
        label='附图',
        required=False,
        widget=MultipleFileInput(attrs={'multiple': True})
    )

    bootstrap_exclude_fields = ['attached_picture']

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
    """
    后台管理之民居新建操作 (Ajax 请求)
    @param request: 请求对象
    @return: 返回 Ajax 响应
    """

    form = ResidentAddModelForm(data=request.POST, files=request.FILES)

    if form.is_valid():
        # 获取当前上传图片应存放的文件夹
        resident_province = form.data.get('resident_province')
        resident_number = form.data.get('resident_number')
        file_path = r'app/media/' + resident_province + '/' + resident_number
        # 如果文件夹不存在就创建文件夹
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        # 获取上传的图片文件对象
        attached_picture = form.files.getlist('attached_picture')
        if attached_picture:
            # 获取图片文件的路径
            db_attached_picture = []
            for img in attached_picture:
                db_file_path = file_path[3:] + '/' + img.name
                db_attached_picture.append(db_file_path)
            # 读取图片内容，写入到 media 文件夹中
            for i in range(len(db_attached_picture)):
                path = db_attached_picture[i]
                # 写入图片
                with open(r'app/' + path, mode='wb+') as file:
                    for chunk in attached_picture[i].chunks():
                        file.write(chunk)
            # 将数据及图片路径写入到数据库中
            # form.save()
            ResidentsInfo.objects.create(
                resident_province=resident_province,
                resident_number=resident_number,
                resident_type=form.data.get('resident_type'),
                resident_overview=form.data.get('resident_overview'),
                distribution=form.data.get('distribution'),
                structure=form.data.get('structure'),
                construct=form.data.get('construct'),
                represent_building=form.data.get('represent_building'),
                factor=form.data.get('factor'),
                comparison_evolution=form.data.get('comparison_evolution'),
                attached_picture=db_attached_picture
            )

        ResidentsInfo.objects.create(
            resident_province=resident_province,
            resident_number=resident_number,
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
    """
    后台管理之民居编辑操作 (Ajax 请求)
    @param request: 请求对象
    @param nid: 当前选择的民居 id
    @return: 返回 Ajax 响应
    """

    condition = {'id': nid}

    if request.method == 'GET':
        current_info = ResidentsInfo.objects.filter(**condition).values('resident_province', 'resident_number',
                                                                        'resident_type', 'resident_overview',
                                                                        'distribution', 'structure', 'construct',
                                                                        'represent_building',
                                                                        'factor', 'comparison_evolution',
                                                                        'attached_picture').first()
        if not current_info:
            return JsonResponse({'status': False, 'error': '编辑失败，数据不存在！请尝试刷新页面！'})

        return JsonResponse({'status': True, 'data': current_info})

    form = ResidentModelForm(data=request.POST, files=request.FILES)

    if form.is_valid():
        # 获取当前上传图片应存放的文件夹
        resident_province = form.data.get('resident_province')
        resident_number = form.data.get('resident_number')
        file_path = r'app/media/' + resident_province + '/' + resident_number
        # 获取上传的图片文件对象
        attached_picture = form.files.getlist('attached_picture')
        if attached_picture:
            # 如果文件夹不存在就创建文件夹
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            else:
                # 存在删除所有文件
                for file in os.listdir(file_path):
                    os.remove(os.path.join(os.getcwd(), 'app', 'media', resident_province, resident_number, file))
            # 获取图片文件的路径
            db_attached_picture = []
            for img in attached_picture:
                db_file_path = file_path[3:] + '/' + img.name
                db_attached_picture.append(db_file_path)
            # 读取图片内容，写入到 media 文件夹中
            for i in range(len(db_attached_picture)):
                path = db_attached_picture[i]
                # 写入图片
                with open(r'app/' + path, mode='wb+') as file:
                    for chunk in attached_picture[i].chunks():
                        file.write(chunk)
            # 将数据及图片路径在数据库中更新
            # form.save()
            ResidentsInfo.objects.filter(**condition).update(
                resident_type=form.data.get('resident_type'),
                resident_overview=form.data.get('resident_overview'),
                distribution=form.data.get('distribution'),
                structure=form.data.get('structure'),
                construct=form.data.get('construct'),
                represent_building=form.data.get('represent_building'),
                factor=form.data.get('factor'),
                comparison_evolution=form.data.get('comparison_evolution'),
                attached_picture=db_attached_picture
            )

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

    # 删除相关附图
    attached_picture = get_table_info(condition)[1][0].attached_picture
    if attached_picture:
        file_path = '/'.join(attached_picture[0].split('/')[:3])
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
    # 删除数据库中的记录
    ResidentsInfo.objects.filter(**condition).delete()

    return JsonResponse({'status': True})




