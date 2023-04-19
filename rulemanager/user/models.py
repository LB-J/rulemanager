from django.db import models


# Create your models here.
class UserExpand(models.Model):
    user = models.ForeignKey('auth.User', related_name="perm_user", on_delete=models.CASCADE)
    phone = models.CharField(max_length=16,  default="186000000", verbose_name="user phone num")
    erp_id = models.CharField(max_length=30,  default="186000000", verbose_name="user dongdong erp count")
    alert_channel = models.IntegerField(choices=((0, 'email'), (1, 'wechat'), (2, 'jd')), default=0,
                                        verbose_name="alert channel")

    def __str__(self):
        return self.user.username

