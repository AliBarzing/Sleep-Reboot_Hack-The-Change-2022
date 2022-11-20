from django.db import models
from django.urls import reverse


class user(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=1000)
    firstname = models.CharField(max_length=1000)
    lastname = models.CharField(max_length=1000)
    gender = models.CharField(max_length=1000)
    dateofbirth = models.CharField(max_length=1000)
    educationstatus = models.CharField(max_length=1000)
    weight = models.CharField(max_length=1000)
    height = models.CharField(max_length=1000)

    BDI_score = models.CharField(max_length=1000)
    ISI_score = models.CharField(max_length=1000)

    def __str__(self):
        return 'username =' + self.username + ' password = ' + self.password + 'firstname = ' + self.firstname + 'lastname = ' + self.lastname + 'gender = '+ self.gender + 'datofbirth' + self.dateofbirth + 'educationstatus' + self.educationstatus + 'weight = ' + self.weight + 'height' + self.height + 'BDI_score' + self.BDI_score + 'ISI_score' + self.ISI_score


class Group(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    groupName = models.CharField(max_length=40)
    groupDesc = models.CharField(max_length=1000)
    groupImage = models.CharField(max_length=1000)

    def get_absolute_url(self):
        return reverse('manager:passwords', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Name=' + self.groupName + ' Description= ' + self.groupDesc


class Password(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    password = models.CharField(max_length=100)

    def __str__(self):
        return 'Group' + self.group.groupName + 'Pass. Name=' + self.name + ' Description=' + self.desc
