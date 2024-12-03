"""
URL configuration for ShengPAY project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from Ledger.models import Ledger
from mqttclient.models import MqttTopic,MqttServer,MqttMessage
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django_filters import FilterSet,DateFilter,CharFilter 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import routers,serializers,viewsets,filters
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response

#ledger filter payitem
class PayitemFilter(FilterSet):
    paytime_gte = DateFilter(field_name='paytime', lookup_expr='gte')
    paytime_lte = DateFilter(field_name='paytime', lookup_expr='lte')

#ledger page payitem
class PayitemPagination(PageNumberPagination):
    page_size = 100  
    page_size_query_param = 'maxitem' 
    max_page_size = 200 

    class Meta:
        model = Ledger
        fields = ['paytime_gte', 'paytime_lte']
#ledger
class PayItemSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Ledger
        fields='__all__'
    
class PayItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PayItemSerialize
    queryset = Ledger.objects.all()
    filter_backends=[DjangoFilterBackend,filters.OrderingFilter]
    filterset_class=PayitemFilter
    pagination_class=PayitemPagination
    ordering_fields=["paytime"]

#mqttclient 
class ServerSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=MqttServer
        fields='__all__'

class TopicSerialize(serializers.HyperlinkedModelSerializer):
    server=ServerSerialize(read_only=False)
    class Meta:
        model=MqttTopic
        fields='__all__'
    
    def create(self, validated_data):

        server_str = validated_data["server"]["server"]
        topic_str = validated_data["topic"]
        try:
            server=MqttServer.objects.get(server=server_str)
        except MqttServer.DoesNotExist:
            return
        if not topic_str:
            return 
        topic_instance = MqttTopic.objects.create(server=server,topic=topic_str)
        return topic_instance
    
    
class MessageSerialize(serializers.HyperlinkedModelSerializer):
    topic=TopicSerialize(read_only=False)
    class Meta:
        model=MqttMessage
        fields='__all__'
    
    def create(self, validated_data):
        print(validated_data)
        server_str = validated_data["topic"]["server"]["server"]
        topic_str = validated_data["topic"]["topic"]
        messageq = validated_data["message"]
        type_ = validated_data["msgtype"]
        try:
            server=MqttServer.objects.get(server=server_str)
            topic=MqttTopic.objects.get(server=server,topic=topic_str)
        except (MqttServer.DoesNotExist,MqttServer.DoesNotExist):
            return
        message_instance = MqttMessage.objects.create(topic=topic,message=messageq,msgtype=type_)
        return message_instance
    

class TopicViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = TopicSerialize 
    queryset = MqttTopic.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]

    def list(self,request):
        server_str = request.query_params.get("server")
        if not server_str:
            return Response({'error':"server_str parameters are required"},status=400)
        filter_final = MqttTopic.objects.filter(server__server=server_str)
        serializers=self.get_serializer(filter_final,many="True")
        return Response(serializers.data)
    
    def delete(self,request):
        server_str = request.data.get("server")
        topic_str = request.data.get("topic")
        if not server_str or not topic_str:
            return Response({'error': 'server_str , topic_str parameters are required'}, status=400)
        try:
            server=MqttServer.objects.get(server=server_str)
            MqttTopic.objects.get(topic=topic_str,server=server).delete()
        except (MqttServer.DoesNotExist,MqttTopic.DoesNotExist):
            return Response("server dose not exist or topic dose not exist!",status=400 )
        return Response("ok!",status=200)

class ServerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = ServerSerialize
    queryset = MqttServer.objects.all()
    filter_backends = [DjangoFilterBackend]

    def list(self,request):
        server_str = request.query_params.get('server')
        if not server_str:
            return Response({"error":"server parameter is required"},status=400)
        filter_final=MqttServer.objects.filter(server=server_str)
        serializers=self.get_serializer(filter_final,many="True")
        return Response(serializers.data)

        

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = MessageSerialize
    queryset = MqttMessage.objects.all()
    filter_backends = [DjangoFilterBackend]
    
    def list(self, request):
        server_str = request.query_params.get('server')
        topic_str =request.query_params.get('topic')
        if not server_str or not topic_str:
            return Response({'error': 'server_str , topic_str parameters are required'}, status=400)
        filter_final=MqttMessage.objects.filter(topic__topic=topic_str,topic__server__server=server_str)
        serializer=self.get_serializer(filter_final,many="True")
        return Response(serializer.data)


router=routers.DefaultRouter()
router.register(r'payitem', PayItemViewSet)
router.register(r'gettopic', TopicViewSet)
router.register(r'getserver', ServerViewSet)
router.register(r"getmessage", MessageViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ledger', include("Ledger.urls")),
    path("mqttclient", include("mqttclient.urls")),
    path("sapi/", include(router.urls)),
    path("sapitk/",obtain_auth_token),
]


from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
