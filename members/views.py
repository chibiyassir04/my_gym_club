from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Member, Trainer, GymClass
from .serializers import MemberSerializer, TrainerSerializer, GymClassSerializer
from .permissions import IsAdminOrReadOnly

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by('id')
    serializer_class = MemberSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['membership_type', 'is_active', 'trainer']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'join_date']

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        member = self.get_object()
        member.is_active = False
        member.save()
        return Response({'message': f'{member.name} has been deactivated'})


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all().order_by('id')
    serializer_class = TrainerSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['specialty']
    search_fields = ['name', 'specialty']
    ordering_fields = ['name']

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        trainer = self.get_object()
        members = trainer.members.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

class GymClassViewSet(viewsets.ModelViewSet):
    queryset = GymClass.objects.all().order_by('id')
    serializer_class = GymClassSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['members']
    search_fields = ['name']
    ordering_fields = ['name', 'schedule']

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        gym_class = self.get_object()
        member_id = request.data.get('member_id')

        if not member_id:
            return Response(
                {'error': 'member_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response(
                {'error': 'Member not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        gym_class.members.add(member)
        return Response({'message': f'{member.name} enrolled in {gym_class.name}'})