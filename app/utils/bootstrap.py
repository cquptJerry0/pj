from django import forms


class BootStrapModelForm(forms.ModelForm):
    """
        自定义 ModelForm 使用 Bootstrap 样式
    """

    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        # 继承 ModelForm 类的所有属性和函数
        super().__init__(*args, **kwargs)

        # 循环 ModelForm 中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            # 字段中有属性，保留原来的属性，没有属性，才增加
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': field.label,
                }