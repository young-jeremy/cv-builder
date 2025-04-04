# In accounts/management/commands/create_missing_profiles.py
from django.core.management.base import BaseCommand
from accounts.models import UserProfile, User


class Command(BaseCommand):
    help = 'Creates missing profiles for users'

    def handle(self, *args, **options):
        created_count = 0

        # Get all users
        all_users = User.objects.all()
        self.stdout.write(f"Found {all_users.count()} users in the database")

        # Get existing profiles
        existing_user_ids = set(UserProfile.objects.values_list('user_id', flat=True))
        self.stdout.write(f"Found {len(existing_user_ids)} existing profiles")

        # Find users without profiles
        for user in all_users:
            if user.id not in existing_user_ids:
                try:
                    # Verify we have a valid user instance
                    if user.pk is None or not isinstance(user, User):
                        self.stdout.write(self.style.WARNING(
                            f"Skipping invalid user: {user} (ID: {user.id})"
                        ))
                        continue

                    # Create a profile
                    UserProfile.objects.create(user=user)
                    created_count += 1
                    self.stdout.write(f"Created profile for user: {user.username}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"Error creating profile for {user.username}: {str(e)}"
                    ))

        self.stdout.write(self.style.SUCCESS(f'Created {created_count} profiles'))