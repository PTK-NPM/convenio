from django.contrib import admin
from .models import Beneficiario, Procedimento, ProfissionalSolicitante, CBOs, Executante

admin.site.register(Beneficiario)
admin.site.register(Procedimento)
admin.site.register(ProfissionalSolicitante)
admin.site.register(CBOs)
admin.site.register(Executante)