from django.db import models
from django.contrib.auth.models import User

RANK_CHOICES = [
    ('Assistant Professor', 'Assistant Professor'),
    ('Associate Professor', 'Associate Professor'),
    ('Professor', 'Professor'),
]

PROMOTION_STATUS = [
    ('Pending', 'Pending'),
    ('Eligible', 'Eligible'),
    ('Not Eligible', 'Not Eligible'),
    ('Promoted', 'Promoted'),
]

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    current_rank = models.CharField(max_length=30, choices=RANK_CHOICES, default='Assistant Professor')
    years_of_experience = models.PositiveIntegerField(default=0)
    publications = models.PositiveIntegerField(default=0)
    conferences_attended = models.PositiveIntegerField(default=0)
    books_published = models.PositiveIntegerField(default=0)
    phd_completed = models.BooleanField(default=False)
    api_score = models.PositiveIntegerField(default=0, blank=True, null=True)
    promotion_status = models.CharField(max_length=20, choices=PROMOTION_STATUS, default='Pending')

    def __str__(self):
        return self.name

    def calculate_api_score(self):
        """
        Calculate API score based on faculty profile.
        """
        score = 0
        score += self.years_of_experience * 1       # 1 point per year
        score += self.publications * 5             # 5 points per publication
        score += self.conferences_attended * 2     # 2 points per conference
        score += self.books_published * 15         # 15 points per book
        if self.phd_completed:
            score += 10                             # 10 points for PhD
        self.api_score = score
        self.save()

    def is_eligible_for_promotion(self):
        """
        Custom logic for promotion eligibility based on rank and API score.
        """
        self.calculate_api_score()  # Ensure API score is up-to-date

        if self.current_rank == 'Assistant Professor':
            return (
                self.years_of_experience >= 4 and
                self.publications >= 3 and
                self.phd_completed
            )
        elif self.current_rank == 'Associate Professor':
            return (
                self.years_of_experience >= 5 and
                self.publications >= 5 and
                self.conferences_attended >= 3 and
                self.books_published >= 1 and
                self.phd_completed
            )
        elif self.current_rank == 'Professor':
            return False  # Already highest rank

        return False

    def promote(self):
        """
        Update the current rank if eligible and set promotion status.
        """
        if self.is_eligible_for_promotion():
            if self.current_rank == 'Assistant Professor':
                self.current_rank = 'Associate Professor'
            elif self.current_rank == 'Associate Professor':
                self.current_rank = 'Professor'
            self.promotion_status = 'Promoted'
        else:
            self.promotion_status = 'Not Eligible'
        self.save()
