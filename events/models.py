from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Event(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    event_type = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    maximum_attendees = models.IntegerField(default=50)
    list_of_attendees = models.ManyToManyField(
        User, default=None, related_name="attendees"
    )
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def status(self):
        """Returns the status of events
        inactive = cancelled, active+future date = happening at xyz, active+past date = held on
        """
        if self.active:
            if self.start_date > timezone.now():
                return f"Happening at {self.start_date}"
            return f"Held on {self.start_date}"
        return "Cancelled"

    @property
    def number_of_attendees(self):
        return self.list_of_attendees.count()

    def __str__(self):
        return self.name
