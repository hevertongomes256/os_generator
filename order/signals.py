from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order, Checklist, ChecklistItem


@receiver(post_save, sender=Order)
def created_checklist_receiver(sender, instance, created, **kwargs):
    if created:
        print('Entrou aqui !!!')
        checklist = Checklist.objects.create(order=instance)

        itens_checklist = [
            "Chegou desligado",
            "Cliente possibilita demais testes",
            "Alto falante estourado/chiando",
            "Sensor de proximidade",
            "Câmera frontal",
            "Câmera traseira",
            "Conector de carga",
            "Microfone",
            "Rede e Wi-Fi",
            "Biometria",
            "Bateria inchada",
            "Touch Screen",
            "Tela",
            "Botão de volume/Power",
            "Possui senha",
            "Serviço prestado teve êxito",
            "Botão Power",
            "Leitor biométrico",
            "Auto falante",
            "Auricular",
            "VibraCall",
            "Conector fone de ouvido",
        ]

        ChecklistItem.objects.bulk_create([
            ChecklistItem(checklist=checklist, checked=False, description=desc) for desc in itens_checklist
        ])
