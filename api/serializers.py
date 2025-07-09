from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, ResumeProfile, JobPost, Proposal, Message, ChatRoom

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to token payload
        token['email'] = user.email
        token['role'] = user.role
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add additional response data
        data['id'] = self.user.id
        data['email'] = self.user.email
        data['role'] = self.user.role
        data['full_name'] = self.user.full_name
        data['username'] = self.user.username
        data['profile_picture'] = self.user.profile_picture.url if self.user.profile_picture else None

        return data
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirm password",
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'password2', 'full_name', 'country', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # remove confirm password
        password = validated_data['password']
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'full_name', 'country', 'bio', 'profile_picture']
        read_only_fields = ['email']


class ResumeProfileSerializer(serializers.ModelSerializer):
    user = RegisterSerializer(read_only=True)

    class Meta:
        model = ResumeProfile
        fields = ['id', 'user', 'skills', 'experience', 'education', 'resume_file']

class JobPostSerializer(serializers.ModelSerializer):
    employer = RegisterSerializer(read_only=True)

    class Meta:
        model = JobPost
        fields = ['id', 'employer', 'title', 'description', 'required_skills', 'budget', 'status', 'created_at']


class ProposalSerializer(serializers.ModelSerializer):
    freelancer = RegisterSerializer(read_only=True)
    resume_file = serializers.SerializerMethodField()  # ✅ this line makes get_resume_file work

    class Meta:
        model = Proposal
        fields = [
            'id', 'freelancer', 'job', 'cover_letter',
            'submitted_at', 'score', 'status', 'resume_file'
        ]
        read_only_fields = ['freelancer', 'submitted_at', 'score', 'resume_file']

    def update(self, instance, validated_data):
        new_status = validated_data.get('status', instance.status)

        # ✅ Update proposal status
        instance.status = new_status
        instance.save()

        # ✅ If proposal is shortlisted, close the job
        if new_status == 'shortlisted':
            instance.job.status = 'Closed'  # or 'closed' if your choices are lowercase
            instance.job.save()
        elif new_status == 'rejected':
            instance.job.status = 'Open'  # or 'closed' if your choices are lowercase
            instance.job.save()

        return instance

    def get_resume_file(self, obj):
        try:
            return obj.freelancer.resume.resume_file.url if obj.freelancer.resume.resume_file else None
        except:
            return None


class MessageSerializer(serializers.ModelSerializer):
    sender_full_name = serializers.CharField(source='sender.full_name', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'sender_full_name', 'content', 'timestamp']
        read_only_fields = ['room', 'sender', 'sender_full_name', 'timestamp']

class ChatRoomSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'job', 'job_title', 'freelancer', 'employer']


