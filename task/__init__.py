default_app_config = 'task.apps.TaskConfig'
STATUS = (
        ('receive','已入库'),
        ('load','已装货，将前往下一个目的地'),
        ('done','已完成，将前往下一个目的地'),
        ('failed','未进行'),
        ('finish','已结束')
    )
