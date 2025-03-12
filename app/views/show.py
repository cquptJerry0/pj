from django.shortcuts import render, redirect
from app.views.database import database_table_init
from app.models import ResidentsInfo
from app.utils.transresidentinfo import get_resident_info
from app.utils.pagination import Pagination


def index(request):
    """
    首页视图函数：去 app 目录下的 templates 目录寻找 index.html (根据 app 的注册顺序，逐一去他们的 templates 目录中找)
    @param request: 请求对象
    @return: 返回 index.html 页面
    """

    # 1. 初始化民居表中的数据
    if len(ResidentsInfo.objects.all()) == 0:
        database_table_init()
    else:
        print("数据库民居表已初始化过！")

    # 2. 获取民居表中的所有数据分页显示
    residents_info = get_resident_info()

    # 分页数据
    page_object = Pagination(request, residents_info)
    page_queryset = page_object.page_queryset
    page_html = page_object.html()

    data = {
        'table_name': ResidentsInfo._meta.verbose_name,          # 用于导航条左侧的 logo 显示部分
        'residents_info': residents_info,                        # 用于导航条中的城市选择功能
        'page_queryset': page_queryset,                          # 分页的数据
        'page_html': page_html,                                  # 分页 HTML 代码
    }

    # 3. 表中数据传输到前端首页
    return render(request, 'index.html', data)


def detail(request, nid=0):
    """
    数据详情视图函数
    @param request: 请求对象
    @param nid: 请求显示哪个数据的详情（根据路由中的 nid 参数获取当前请求显示数据的 id 条件）
    @return: 返回 detail.html 页面
    """

    residents_info = get_resident_info()     # 为了显示城市选择功能获取

    city = ''       # 城市搜索框中的条件值
    if nid:
        # 当前所要显示详情的数据（根据 id 条件选择）
        current_info = get_resident_info(condition={'id': nid}, flag=True)
    else:
        city = request.GET.get('city', '')
        if city:
            # 当前所要显示详情的数据（根据 resident_province 条件选择）
            current_info = get_resident_info(condition={'resident_province': city}, flag=True)
        else:
            # 搜索框中什么都没输入，重定向回首页
            return redirect('/')

    # 若果数据库中没有符合条件的数据，显示搜索错误页面
    if current_info == 0:
        return render(request, 'error.html', {
            'table_name': ResidentsInfo._meta.verbose_name,
            'residents_info': residents_info,
            'current_search': city,
        })

    data = {
        'table_name': ResidentsInfo._meta.verbose_name,
        'residents_info': residents_info,
        'current_info': current_info,
        'current_search': city,
    }

    return render(request, 'detail.html', data)