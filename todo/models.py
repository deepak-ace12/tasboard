from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from todo.utils import send_mail


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    domain = models.ForeignKey('todo.Domain', related_name='profiles')

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def is_admin(self):
        return self.user == self.domain.admin


class Domain(models.Model):
    name = models.TextField(max_length=140)
    admin = models.ForeignKey(
        User, null=True, blank=True, related_name='domains')

    def __unicode__(self):
        return self.name


class Todo(models.Model):
    ACTIVE = 'A'
    PENDING = 'P'
    DONE = 'D'
    CANCELLED = 'C'
    
    STATUS = (
        (ACTIVE, 'Active'),
        (PENDING, 'Pending'),
        (DONE, 'Done'),
        (CANCELLED, 'Cancelled')
    )
    task = models.TextField(max_length=140)
    status = models.CharField(max_length=1, choices=STATUS, default=ACTIVE)
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assignee')
    assignor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assignor')

    def __unicode__(self):
        return self.task


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        domain_name = instance.email.split('@')[1]
        domain, domain_created = Domain.objects.get_or_create(
                                    name=domain_name
                                )
        Profile.objects.create(user=instance, domain=domain)

        if domain_created:
            instance.profile.is_approved = True
            instance.profile.save()
            domain.admin = instance
            domain.save()
        else:
            send_mail(
                subject="New registration request",
                body="%s has registered with your domain." % instance.email,
                to=domain.admin.email
            )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
