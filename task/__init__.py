default_app_config = 'task.apps.TaskConfig'
STATUS = (
        ('receive','已出入库'),
        ('load','已装卸货，将前往下一个目的地'),
        ('done','已完成，将前往下一个目的地'),
        ('failed','未进行'),
    )
