from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, viewsets, status, filters, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, ResumeProfile, JobPost, Proposal, Message, ChatRoom
from .serializers import (
    RegisterSerializer,
    ResumeProfileSerializer,
    JobPostSerializer,
    ProposalSerializer,
    MessageSerializer,
    CustomTokenObtainPairSerializer,
    ProfileUpdateSerializer,
    ChatRoomSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
import fitz  # PyMuPDF
import spacy
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q



# This code defines a DRF View class called MyTokenObtainPairView, which inherits from TokenObtainPairView.
class CustomTokenObtainPairView(TokenObtainPairView):
    # Here, it specifies the serializer class to be used with this view.
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ProfileUpdateSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResumeProfileView(generics.RetrieveUpdateAPIView):
    queryset = ResumeProfile.objects.all()
    serializer_class = ResumeProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return ResumeProfile.objects.get_or_create(user=self.request.user)[0]
    
class ResumeDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ResumeProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResumeProfile.objects.all()

    def get_object(self):
        user_id = self.kwargs['user_id']
        return ResumeProfile.objects.get(user__id=user_id)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class JobPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'

class JobPostView(generics.ListCreateAPIView):
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = JobPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'required_skills', 'description']

    def get_queryset(self):
        return JobPost.objects.filter(status='Open').order_by('-created_at')
    
    def perform_create(self, serializer):
        # ✅ Attach the currently logged-in user as employer
        serializer.save(employer=self.request.user)

class EmployerJobListView(generics.ListAPIView):
    serializer_class = JobPostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        employer_id = self.kwargs['employer_id']
        return JobPost.objects.filter(employer__id=employer_id)
    
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]


# class ProposalView(generics.ListCreateAPIView):
#     serializer_class = ProposalSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Proposal.objects.filter(job__employer=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(freelancer=self.request.user)

def extract_text_from_pdf(pdf_file):
        text = ""
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text

class ProposalView(generics.CreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user
        job_id = self.request.data.get('job')
        nlp = spacy.load("en_core_web_sm")

        if user.role != 'freelancer':
            raise serializers.ValidationError("Only freelancers can apply to jobs.")

        if Proposal.objects.filter(job_id=job_id, freelancer=user).exists():
            raise serializers.ValidationError("You've already submitted a proposal for this job.")

        job = JobPost.objects.get(id=job_id)
        freelancer_profile = getattr(user, 'resume', None)

        if freelancer_profile:
            # 1. Extract resume text from PDF if uploaded
            resume_text = ""
            if freelancer_profile.resume_file:
                try:
                    resume_text = extract_text_from_pdf(freelancer_profile.resume_file)
                except Exception as e:
                    print("Resume extraction failed:", e)

            # 2. Combine all text sources
            combined_text = " ".join([
                freelancer_profile.skills or "",
                freelancer_profile.experience or "",
                freelancer_profile.education or "",
                resume_text
            ]).lower()

            # 3. Process with spaCy NLP
            doc = nlp(combined_text)
            tokens = set([chunk.text.strip().lower() for chunk in doc.noun_chunks])

            # 4. Compare with job skills
            job_skills = set(s.strip().lower() for s in job.required_skills.split(',') if s)
            matches = job_skills & tokens
            score = (len(matches) / len(job_skills)) * 100 if job_skills else 0
        else:
            score = 0

        serializer.save(freelancer=user, score=round(score, 2))


class FreelancerProposalsView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Proposal.objects.filter(freelancer=self.request.user).select_related('job')



class HasAppliedProposalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        user = request.user
        has_applied = Proposal.objects.filter(job_id=job_id, freelancer=user).exists()
        return Response({'has_applied': has_applied})
    

class JobProposalListView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        job = JobPost.objects.get(id=job_id)

        # ✅ Only the employer who owns the job can view proposals
        if self.request.user != job.employer:
            raise PermissionDenied("You do not have permission to view proposals for this job.")

        return Proposal.objects.filter(job=job).order_by('-submitted_at')
    

class ProposalUpdateStatusView(generics.UpdateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        proposal = self.get_object()

        if request.user != proposal.job.employer:
            raise PermissionDenied("You do not have permission to update this proposal.")

        print("PATCH received:", request.data)  # DEBUG

        return self.partial_update(request, *args, **kwargs)


class ChatRoomView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(Q(employer=user) | Q(freelancer=user))

    def perform_create(self, serializer):
        serializer.save()


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return Message.objects.filter(room_id=room_id).order_by('timestamp')

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user,
            room_id=self.kwargs['room_id']
        )



# class MessageListCreateView(generics.ListCreateAPIView):
#     serializer_class = MessageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         room_id = self.kwargs['room_id']
#         return Message.objects.filter(room_id=room_id).order_by('timestamp')

#     def perform_create(self, serializer):
#         serializer.save(sender=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def get_or_create_chat_room(request):
    job_id = request.data.get('job_id')
    freelancer_id = request.data.get('freelancer_id')
    
    if not job_id or not freelancer_id:
        return Response({"detail": "Missing job_id or freelancer_id"}, status=400)

    try:
        job = JobPost.objects.get(id=job_id)
        freelancer = User.objects.get(id=freelancer_id)
        user = request.user

        # 💡 Check if user is part of this chat
        if user != freelancer and user != job.employer:
            return Response({'detail': 'Unauthorized'}, status=403)

        # ✅ Only allow chat if proposal was shortlisted
        from .models import Proposal
        if not Proposal.objects.filter(job=job, freelancer=freelancer, status='shortlisted').exists():
            return Response({'detail': 'Only shortlisted proposals can chat'}, status=403)

        room, _ = ChatRoom.objects.get_or_create(
            job=job,
            employer=job.employer,
            freelancer=freelancer
        )

        return Response({'room_id': room.id})

    except Exception as e:
        return Response({'error': str(e)}, status=400)

