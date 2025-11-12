from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from .models import Person
from .serializers import PersonRequestSerializer, PersonResponseSerializer


# Только в JSON
class JsonOnlyMixin:
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]


class PersonListCreateAPIView(JsonOnlyMixin, generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonResponseSerializer  # для GET /persons

    def create(self, request: Request, *args, **kwargs):
        serializer = PersonRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        person = serializer.save()

        # 201 Created, пустое тело, Location: /api/v1/persons/{id}
        location_path = f"{request.get_full_path()}/{person.id}"
        headers = {"Location": location_path}
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class PersonDetailAPIView(JsonOnlyMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonResponseSerializer  # для GET и ответа PATCH

    def patch(self, request, *args, **kwargs):
        person = self.get_object()  # 404 если нет
        serializer = PersonRequestSerializer(person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Вернуть обновлённый объект
        return Response(PersonResponseSerializer(person).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        person = self.get_object()  # 404 если нет
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def health(request):
    # Проверяем только, что процесс жив
    return JsonResponse({"status": "ok"}, status=200)
