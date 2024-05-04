from django.db import models
import random

class Usuario(models.Model):
    ESTADO_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('Desaprobado', 'Desaprobado'),
        ('Pendiente', 'Pendiente'),
        ('Actualización de documentos necesaria', 'Actualización de documentos necesaria')
    ]
    
    id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=100, choices=ESTADO_CHOICES)

    def __str__(self):
        return f'{self.nombre} ({self.id})'

    @classmethod
    def generate_users(cls):
        if not cls.objects.exists():
            for _ in range(50):
                id = random.choice([i for i in range(1000, 10000) if i != 1020])
                nombre = cls.generate_random_name()
                estado = random.choice(['Aprobado', 'Desaprobado', 'Pendiente', 'Actualización de documentos necesaria'])
                cls.objects.create(id=id, nombre=nombre, estado=estado)

    @staticmethod
    def generate_random_name():
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
        name_length = random.randint(5, 10)
        name = ''.join(random.choice(consonants) + random.choice(vowels) for _ in range(name_length))
        return name.capitalize()
