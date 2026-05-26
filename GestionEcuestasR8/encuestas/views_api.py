from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Encuesta
from .serializers import EncuestaSerializer


@api_view(['GET'])
def api_lista_encuestas(request):
    """
    API mínima para Vue.

    Devuelve las encuestas en formato JSON para que el frontend de Vue
    pueda leerlas usando fetch().
    """

    encuestas = Encuesta.objects.all().order_by('id')

    serializer = EncuestaSerializer(
        encuestas,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
def api_detalle_encuesta(request, encuesta_id):
    """
    API mínima para consultar una encuesta concreta desde Vue.
    """

    encuesta = get_object_or_404(
        Encuesta,
        id=encuesta_id
    )

    serializer = EncuestaSerializer(encuesta)

    return Response(serializer.data)
