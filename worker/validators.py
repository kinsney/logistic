from django.core.validators import RegexValidator

class IdCardValidator(RegexValidator):
    def __init__(self, message='请输入合法的中国大陆身份证号', code=None):
        RegexValidator.__init__(self, regex='^[0-9]{17}[0-9X]$',
            message=message, code=code)
