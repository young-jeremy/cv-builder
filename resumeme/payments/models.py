from django.db import models
from accounts.models import User
from django.utils import timezone


class Plan(models.Model):
    BILLING_CYCLE_CHOICES = (
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('one_time', 'One-time Purchase')
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES)
    features = models.TextField(help_text="Enter features separated by newlines")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    # Plan capabilities
    allow_resume_export = models.BooleanField(default=True)
    max_resumes = models.IntegerField(default=1)
    allow_cover_letters = models.BooleanField(default=False)
    allow_premium_templates = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'price']

    def __str__(self):
        return self.name

    def get_features_list(self):
        return self.features.split('\n')


class Subscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired'),
        ('trial', 'Trial')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    payment_id = models.CharField(max_length=100, blank=True)
    subscription_id = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'}"

    def is_active(self):
        if self.status != 'active':
            return False
        if self.end_date and timezone.now() > self.end_date:
            self.status = 'expired'
            self.save()
            return False
        return True

    def can_export_resume(self):
        return self.is_active() and self.plan.allow_resume_export


class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency} - {self.status}"