from django.shortcuts import render, redirect


def admin_login(request):
    """
    登录后台管理视图函数
    @param request: 请求对象
    @return: 返回 admin_login.html 页面
    """

    # 如果不是表单 post 请求，刷新页面
    if request.method == 'GET':
        return render(request, 'admin_login.html')

    # 如果当前是表单 post 请求，得到当前的管理员输入的用户名和密码
    admin_name = request.POST.get('admin_name', '');
    password = request.POST.get('password', '');

    # 当前简单设置的三位初始管理员
    admin_list = [
        {
            'admin_name': 'admin',
            'password': 'admin',
        },
        {
            'admin_name': 'admin1',
            'password': 'admin1',
        },
        {
            'admin_name': 'admin2',
            'password': 'admin2',
        }
    ]

    # 若管理员用户名和密码都输入了
    if admin_name and password:
        for admin in admin_list:
            if admin['admin_name'] == admin_name and admin['password'] == password:
                # 登录成功
                request.session['admin_info'] = '管理员: ' + admin_name
                # 重定向到后台管理页面
                return redirect('/resident/list/')
        # 错误信息
        error_msg = '管理员用户名或密码错误！'
    else:
        # 用户名或密码没输入
        error_msg = '管理员用户名和密码不能为空！'

    data = {
        'admin_name': admin_name,
        'password': password,
        'error_msg': error_msg,
    }

    # 登录失败，返回错误信息
    return render(request, 'admin_login.html', data)


def admin_logout(request):
    """
    管理员注销功能
    @param request: 请求对象
    @return: 注销后，返回登录界面
    """

    # 清空 session 存储的登录信息
    request.session.clear()

    # 重定向到登录页面
    return redirect('/admin/login/')



