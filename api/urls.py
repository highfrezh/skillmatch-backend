from django.urls import path
from .views import (
    RegisterView,
    ResumeProfileView,
    JobPostView,
    ProposalView,
    ChatRoomView,
    MessageListCreateView,
    CustomTokenObtainPairView,
    EmployerJobListView,
    JobDetailView,
    ProfileView   ,
    ResumeDetailView,
    HasAppliedProposalView,
    JobProposalListView,
    ProposalUpdateStatusView, 
    FreelancerProposalsView,
)
from .views import get_or_create_chat_room

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # 🔐 Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 👤 Profile
    path('profile/', ProfileView.as_view(), name='profile'),

    # 📄 Freelancer Resume
    path('resume/', ResumeProfileView.as_view(), name='resume'),
    path('resume/<int:user_id>/', ResumeDetailView.as_view(), name='resume-detail'),

    # 📌 Job Posts
    path('jobs/', JobPostView.as_view(), name='job_list_create'),
    path('jobs/employer/<int:employer_id>/', EmployerJobListView.as_view()),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    

    # ✉️ Proposals
    path('proposals/', ProposalView.as_view(), name='proposal_list_create'),
    path('jobs/<int:job_id>/has-applied/', HasAppliedProposalView.as_view(), name='has-applied'),
    path('jobs/<int:job_id>/proposals/', JobProposalListView.as_view(), name='job-proposals'),
    path('proposals/<int:pk>/update/', ProposalUpdateStatusView.as_view(), name='update-proposal'),
    path('proposals/freelancer/', FreelancerProposalsView.as_view(), name='freelancer-proposals'),


    # path('proposals/', ProposalCreateView.as_view(), name='submit-proposal'),

    # 💬 Messaging
    path('chat/rooms/', ChatRoomView.as_view(), name='chat-rooms'),
    path('chat/rooms/<int:room_id>/messages/', MessageListCreateView.as_view(), name='chat-messages'),
    path('chat/start/', get_or_create_chat_room, name='start-chat'),

    
]
