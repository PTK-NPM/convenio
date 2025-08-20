from django.db import models

class Beneficiario(models.Model):
    nome = models.CharField(max_length = 150)
    CPF = models.CharField(max_length = 11, unique = True)
    data_nascimento = models.DateField()
    carteirinha = models.CharField(max_length = 10, unique = True, blank = True, editable = False)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.carteirinha:
            self.carteirinha = f'{self.id:08d}'
            super().save(update_fields=['carteirinha'])


