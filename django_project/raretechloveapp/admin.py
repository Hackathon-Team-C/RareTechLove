from django.contrib import admin
from .models import Rt_mst_user, Rt_mst_article, Rt_tbl_difficulty, Rt_tbl_q_count, Rt_tbl_question
# Register your models here.

admin.site.register(Rt_mst_user)
admin.site.register(Rt_mst_article)
admin.site.register(Rt_tbl_difficulty)
admin.site.register(Rt_tbl_q_count)
admin.site.register(Rt_tbl_question)