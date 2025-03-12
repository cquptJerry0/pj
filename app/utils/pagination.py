import copy
from django.utils.safestring import mark_safe


class Pagination(object):
    """
        自定义分页组件类

        在视图函数中：
            # 1. 根据自己的情况去筛选自己的数据
            residents_info = get_table_info()
            # 2. 实力划分也对象
            page_object = Pagination(request, residents_info[0])
            page_queryset = page_object.page_queryset
            page_html = page_object.html()

        在HTML页面中：
            <!-- 分页 -->
            <div class="page-footer">
                <div aria-label="Page navigation">
                    <ul class="pagination">
                        {{ page_html }}
                    </ul>
                </div>
            </div>
    """

    def __init__(self, request, queryset, page_param='page', page_size=6, per=5):
        """
        @param request: 请求的对象
        @param queryset: 符合条件的数据（根据这些数据进行分页处理）
        @param page_param: 在 URL 中传递的获取分页的参数，例如：/resident_list/?page=2
        @param page_size: 每页显示多少条数据
        @param per: 显示当前页的前或后几页（显示分页的列表长度：当前页 + 前 per 页 + 后 per 页）
        """

        get_url = copy.deepcopy(request.GET)   # 深拷贝一份当前的 url 参数（分页参数后面在拼接上搜索参数）
        get_url._mutable = True
        self.get_url = get_url                 # 当前请求的 url 参数列表
        self.page_param = page_param

        # 默认显示第一页数据
        page = request.GET.get(page_param, '1')
        # 判断分页参数是否为数字，若否，设置显示第一页
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size  # 当前页该显示的数据列表的开始位置
        self.end = page * page_size  # 当前页该显示的数据列表的结束位置

        self.page_queryset = queryset[self.start:self.end]  # 当前页该显示的数据列表（从所有符合条件的数据中截取）

        total_count = queryset.count()  # 所有符合条件的数据总条数
        total_page_count, mod = divmod(total_count, page_size)
        if mod:
            total_page_count += 1
        self.total_page_count = total_page_count  # 所有符合条件的数据总共该分几页

        self.flag = 0
        if self.get_url.keys().__contains__(self.page_param) and \
                int(self.get_url[self.page_param]) > self.total_page_count:
            self.flag = 1

        self.per = per

    def html(self):
        """
        根据当前的 url 参数和分页参数进行分页操作
        @return: 分页的 HTML 代码
        """

        # 显示当前页的前五页和后五页
        if self.total_page_count <= 2 * self.per + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            # 如果数据库中数据很多分页数大于11
            if self.page <= self.per:  # 当前页 < 5
                start_page = 1
                end_page = 2 * self.per + 1
            else:
                # 当前页 > 5
                if (self.page + self.per) > self.total_page_count:  # 当前页 + 5 > 总分页
                    start_page = self.total_page_count - 2 + self.per
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.per
                    end_page = self.page + self.per

        # HTML 代码
        page_str_list = []
        # 首页
        self.get_url.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.get_url.urlencode()))

        # 上一页
        if self.page > 1:
            self.get_url.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}" aria-label="Previous">' \
                   '<span aria-hidden="true">&laquo;</span></a></li>'.format(self.get_url.urlencode())
        else:
            prev = '<li class="disabled"><a aria-label="Previous">' \
                   '<span aria-hidden="true">&laquo;</span></a></li>'
        page_str_list.append(prev)

        # 分页
        for i in range(start_page, end_page + 1):
            self.get_url.setlist(self.page_param, [i])
            if i == self.page:
                elements = '<li class="active"><a href="?{}">{}<span class="sr-only">(current)</span></a></li>'\
                    .format(self.get_url.urlencode(), i)
            else:
                elements = '<li><a href="?{}">{}</a></li>'.format(self.get_url.urlencode(), i)
            page_str_list.append(elements)

        # 下一页
        if self.page < self.total_page_count:
            self.get_url.setlist(self.page_param, [self.page + 1])
            next = '<li><a href="?{}" aria-label="Next">' \
                   '<span aria-hidden="true">&raquo;</span></a></li>'.format(self.get_url.urlencode())
        else:
            next = '<li class="disabled"><a aria-label="Next">' \
                   '<span aria-hidden="true">&raquo;</span></a></li>'
        page_str_list.append(next)

        # 尾页
        self.get_url.setlist(self.page_param, [self.total_page_count])
        if self.flag:
            page_str_list.append('<li><a href="?{}"><span>尾页</span></a></li>'.format(self.get_url.urlencode()))
        else:
            page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.get_url.urlencode()))
        # 添加 HTML 代码安全字符串标志，使之将字符串中的内容执行为 HTML 代码
        page_html = mark_safe(''.join(page_str_list))

        return page_html
