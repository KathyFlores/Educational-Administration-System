from django.contrib import admin
from .models import CreditNeed, Curriculum, TimeSlot, SelectControl
admin.site.register(CreditNeed)
admin.site.register(Curriculum)
admin.site.register(SelectControl)
admin.site.register(TimeSlot)
