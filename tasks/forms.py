import django_filters
from django import forms
from django.contrib.auth.models import User

from task_manager.models import Label, Status
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label="Статус", empty_label="Все"
    )
    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(), label="Метка"
    )
    performer = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), label="Исполнитель", empty_label="Все"
    )
    
    is_owner = django_filters.BooleanFilter(
        method="filter_is_owner", label="Только свои задачи"
    )

    class Meta:
        model = Task
        fields = [
            "status",
            "labels",
            "performer",
            "is_owner",
        ]

    def filter_is_owner(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(author=self.request.user)


class TaskForm(forms.ModelForm):
    performer = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        label="Исполнитель",
        empty_label="Не выбран",
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "performer",
            "labels",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["performer"].queryset = User.objects.all()
        self.fields["performer"].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(user):
        if user.first_name or user.last_name:
            return f"{user.first_name} {user.last_name}"

        return user.username
