from django.db import models
from django.conf import settings

class ParentChild(models.Model):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="children")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parents")

    class Meta:
        unique_together = ("parent", "student")

    def __str__(self):
        return f"{self.parent.name} -> {self.student.name}"

class SchoolStudent(models.Model):
    school = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="school")

    class Meta:
        unique_together = ("school", "student")

    def __str__(self):
        return f"{self.school.name} -> {self.student.name}"
    
class StudentAchievement(models.Model):
    student = models.ForeignKey("authentication.user", on_delete=models.CASCADE, related_name="achievements")
    school_id = models.IntegerField()  # Assuming the school is identified using UUID
    achievement_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.student.name} - {self.achievement_name}"