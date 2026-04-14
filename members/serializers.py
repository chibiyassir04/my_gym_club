from rest_framework import serializers
from .models import Member, Trainer, GymClass

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer(read_only=True)
    trainer_id = serializers.PrimaryKeyRelatedField(
        queryset=Trainer.objects.all(),
        source='trainer',
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Member
        fields = '__all__'

class GymClassSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        source='members',
        write_only=True,
        many=True,
        required=False
    )

    class Meta:
        model = GymClass
        fields = '__all__'