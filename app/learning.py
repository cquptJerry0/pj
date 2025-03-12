from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from django import forms
from app.utils.bootstrap import BootStrapModelForm
from app import models
from django.core.exceptions import ValidationError
from app.utils.encrypt import md5


class AdminModalForm(BootStrapModelForm):
    """
        学习用
    """

    confirm_password = forms.CharField(
        label='确认密码',
        # widget=forms.PasswordInput   # 密码在验证完会默认清空
        widget=forms.PasswordInput(render_value=True)   # 验证完不要清空密码
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    # 钩子方法的载入顺序是根据模型中的每个字段的位置依次载入

    # 修改模型中本来就有的字段的默认钩子方法
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    # 给新字段添加钩子验证方法，可以自己写前缀 clean_ 加字段名
    def clean_confirm_password(self):
        print(self.cleaned_data)
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))

        if confirm != pwd:
            raise ValidationError('密码不一致，请重新输入')    # 抛出错误

        # 规定返回值 必须为当前字段值（即当前字段输入框中用户自己输入的值）
        # 返回什么，此字段以后保存到数据库就是什么
        return confirm


def admin_add(request):

    title = '新建管理员'

    if request.method == 'GET':
        form = AdminModalForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModalForm(data=request.POST)

    if form.is_valid():
        # {'username': 'admin', 'password': '123, 'confirm_password': '333'}
        print(form.cleaned_data)    # 验证成功之后, form 中的数据
        form.save()
        return redirect('/admin/list')

    return render(request, 'change.html', {'form': form, 'title': title})


class PrettyModalForm(BootStrapModelForm):

    # 验证方式 1：
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式有误'), ],
        disabled=True  # 该字段不可修改
    )

    class Meta:
        model = models.PrettyNum
        # fields = '__all__'
        # exclude = ['level']
        fields = ['mobile', 'price', 'level', 'status']

    # 验证方式 2： 钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        # 如果验证不通过，抛出一个错误
        if len(txt_mobile) != 11:
            raise ValidationError('格式错误')

        exists = models.PrettyNum.objects.filter(moblie=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在')

        # 验证通过，把用户输入的值返回
        return txt_mobile


class UserMoalForm(BootStrapModelForm):
    name = forms.CharField(min_length=3, label='用户名')
    # password = forms.CharField(label='密码', validators=正则表达式)


# 编辑手机号：排除自己以外，其他的数据是否手机号重复
# exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(moblie=txt_mobile).exists()

