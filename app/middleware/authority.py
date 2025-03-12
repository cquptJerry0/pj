from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthorityMiddleware(MiddlewareMixin):
    """
        后台管理访问权限设置，如果没登录过，就一直让你登录，不可以直接通过 url 访问后台管理操作
    """

    def process_request(self, request):
        """
        访问权限函数设置
        @param request: 前端页面响应请求
        @return: 返回相应的页面
        """

        # 排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的 URL ： 首页和登录页面以及民居详情页面
        if request.path_info == '/' or request.path_info == '/admin/login/' or request.path_info.__contains__('/detail/'):
            return

        # 读取当前访问的管理员的 session 信息，若能读到，说明已登录过，就可以继续往后走
        admin_info = request.session.get('admin_info')
        if admin_info:
            return

        # 没有登录过
        return redirect('/admin/login/')