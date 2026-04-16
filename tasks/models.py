from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.models import Label, Status


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("Имя"))
    description = models.TextField(
        verbose_name=_("Описание"),
        blank=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        verbose_name=_("Статус"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="author_tasks",
        verbose_name=_("Автор"),
    )
    performer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="performer_tasks",
        verbose_name=_("Исполнитель"),
    )

    labels = models.ManyToManyField(
        Label,
        verbose_name=_("метки"),
        blank=True,
        related_name="tasks",
    )

    def __str__(self):
        return self.name

    def clean(self):
        if self.pk is None and Task.objects.filter(name=self.name).exists():
            raise ValidationError({"name": _("уже существует")})

    class Meta:
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")
        ordering = ['id']
