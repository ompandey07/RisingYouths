from django.db import models

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('job_inquiry', 'Job Inquiry'),
        ('consultant_request', 'Consultant Request'),
        ('training_information', 'Training Information'),
        ('travel_services', 'Travel Services'),
        ('general_questions', 'General Questions'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
