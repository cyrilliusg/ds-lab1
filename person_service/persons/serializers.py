from rest_framework import serializers
from .models import Person


class PersonRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("name", "age", "address", "work")
        extra_kwargs = {
            "name": {"required": True},
            "age": {"required": False, "allow_null": True},
            "address": {"required": False, "allow_null": True},
            "work": {"required": False, "allow_null": True},
        }


class PersonResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "name", "age", "address", "work")
        read_only_fields = ("id",)
