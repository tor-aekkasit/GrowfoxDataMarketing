from django.db import models

class PageGroup(models.Model):
    group_name = models.CharField(max_length=255, default='Unnamed Group')

    def __str__(self):
        return self.group_name


class PageInfo(models.Model):
    page_group = models.ForeignKey(PageGroup, on_delete=models.CASCADE, related_name='pages')

    # ข้อมูลทั่วไป
    page_name = models.CharField(max_length=255, null=True, blank=True)
    page_url = models.URLField(max_length=500, null=True, blank=True)
    profile_pic = models.URLField(max_length=500, null=True, blank=True)
    page_username = models.CharField(max_length=255, null=True, blank=True)
    page_id = models.CharField(max_length=100, null=True, blank=True)
    is_business_page = models.BooleanField(null=True, blank=True)

    # Meta HTML
    page_followers = models.CharField(max_length=100, null=True, blank=True)
    page_likes = models.CharField(max_length=100, null=True, blank=True)
    page_followers_count = models.IntegerField(null=True, blank=True)
    page_likes_count = models.CharField(max_length=100, null=True, blank=True)
    page_talking_count = models.CharField(max_length=100, null=True, blank=True)
    page_were_here_count = models.CharField(max_length=100, null=True, blank=True)
    page_description = models.TextField(null=True, blank=True)

    # ข้อมูลโปรไฟล์
    page_category = models.CharField(max_length=255, null=True, blank=True)
    page_address = models.CharField(max_length=500, null=True, blank=True)
    page_phone = models.CharField(max_length=100, null=True, blank=True)
    page_email = models.EmailField(max_length=254, null=True, blank=True)
    page_website = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.page_name or "Unnamed Page"
