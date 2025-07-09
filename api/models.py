from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

# -----------------------------
# 1. Custom User Model
# -----------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('freelancer', 'Freelancer'),
        ('employer', 'Employer'),
    )

    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.FileField(upload_to='profiles/', default='default/default-user.jpg', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.full_name or self.username} ({self.role})"
    
    def save(self, *args, **kwargs):
        email_username = self.email.split('@')[0]
        if self.username == "" or self.username is None:
            self.username = email_username

        super(User, self).save(*args, **kwargs)

# -----------------------------
# 2. Resume Profile (Freelancer only)
# -----------------------------
class ResumeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    skills = models.TextField(help_text="Comma-separated skill tags")
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Resume"

# -----------------------------
# 3. Job Post (Employer)
# -----------------------------
class JobPost(models.Model):
    STATUS = (
        ("Open", "Open"),
        ("Closed", "Closed"),
        ("Matched", "Matched"),
    )
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField(help_text="Comma-separated skill tags")
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.employer.username}"
    
    class Meta:
        ordering = ['-created_at']


# -----------------------------
# 4. Proposal (Freelancer → Job)
# -----------------------------
class Proposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    )

    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='proposals')
    cover_letter = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('job', 'freelancer')
        ordering = ['-submitted_at']


# -----------------------------
# 5. MessageThread (one per job & user pair)
# -----------------------------
class MessageThread(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='threads')
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        usernames = ', '.join([user.username for user in self.participants.all()])
        return f"Thread for {self.job.title} ({usernames})"

# -----------------------------
# 6. Message (chat message)
# -----------------------------
# class Message(models.Model):
#     thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.sender.username}: {self.content[:30]}..."
    
#     class Meta:
#         ordering = ['timestamp']

class ChatRoom(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employer_chats')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_chats')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'employer', 'freelancer')

    def __str__(self):
        return f"Chat for {self.job.title} ({self.employer} ↔ {self.freelancer})"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
