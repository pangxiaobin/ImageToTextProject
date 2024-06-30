from django.db import models

# Create your models here.


# 记录生成的历史记录
class ImageToTextHistory(models.Model):
    image = models.ImageField(upload_to="images/")
    image_text = models.TextField(null=True, blank=True)
    llm_model = models.CharField(max_length=32, null=True, blank=True)
    model_name = models.CharField(max_length=32, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
