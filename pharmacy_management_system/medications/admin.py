from django.contrib import admin

from .models import Medication
from .models import RefillRequest

admin.site.register(Medication)
admin.site.register(RefillRequest)
