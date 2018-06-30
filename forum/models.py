from django.db import models
from django.utils import timezone
from basicInfo.models import attrib, account

'''
class Pages(object):
    def __init__(self, count, current_page=1, list_rows=40):
        self.total = count
        self._current = current_page
        self.size = list_rows
        self.pages = self.total // self.size + (1 if self.total % self.size else 0)

        if (self.pages == 0) or (self._current < 1) or (self._current > self.pages):
            self.start = 0
            self.end = 0
            self.index = 1
        else:
            self.start = (self._current - 1) * self.size
            self.end = self.size + self.start
            self.index = self._current
        self.prev = self.index - 1 if self.index > 1 else self.index
        self.next = self.index + 1 if self.index < self.pages else self.index


class PostManager(models.Manager):
    def get_all_hot_posts(self):
        query = self.get_queryset().filter(replynum__gt=0).order_by('-replynum')
        query.query.group_by = ['id'] # Django使用GROUP BY方法
        return query

    def get_all_post(self, num=36, current_page=1): # 可以考虑在这里过滤掉没有头像的用户发帖，不显示在主页
        count = self.get_queryset().count()
        page = Pages(count, current_page, num)
        query = self.get_queryset().select_related('node', 'author', 'last_replied_by').\
            all().order_by('-created_date', '-last_replied_time', '-id')[page.start:page.end]
        return query, page

    def get_all_topics_by_node_slug(self, num = 36, current_page = 1, node_slug = None):
        count = self.get_queryset().filter(node__slug=node_slug).count()
        page = Pages(count, current_page, num)
        query = self.get_queryset().select_related('node', 'author', 'last_replied_by').\
            filter(node__slug=node_slug).order_by('-created_date', '-last_replied_time', '-id')[page.start:page.end]
        return query, page

    def get_user_all_topics(self, uid, num = 36, current_page = 1):
        count = self.get_queryset().filter(author__id=uid).count()
        page = Pages(count, current_page, num)
        query = self.get_queryset().select_related('node', 'author', 'last_replied_by').\
            filter(author__id=uid).order_by('-id')[page.start:page.end]
        return query, page

    def get_topic_by_topic_id(self, topic_id):
        query = self.get_queryset().select_related('node', 'author', 'last_replied_by').get(pk=topic_id)
        return query

    def get_user_last_created_topic(self, uid):
        query = self.get_queryset().filter(author__id=uid).order_by('-created_date')[0]
        return query


class Node(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)          # 块，作为node的识别url
    introduction = models.CharField(max_length=500, null=True, blank=True)  # 介绍
    created_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    topic_count = models.IntegerField(null=True, blank=True)


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    replynum = models.IntegerField(default=0)
    node = models.ForeignKey(Node, null=True, blank=True, on_delete=models.CASCADE)
    last_replied_by = models.ForeignKey('auth.User', related_name='post_last', null=True, blank=True,
                                        on_delete=models.CASCADE)
    last_replied_time = models.DateTimeField(null=True, blank=True)
    objects = PostManager()

    file_address = models.CharField(max_length=200, null=True)
    file_name = models.CharField(max_length=200, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Reply(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post',null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text


class Bulletin(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey('auth.User', related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey('auth.User', related_name="receiver", on_delete=models.CASCADE)
    text = models.TextField()
    published_date = models.DateTimeField(
        blank=True, null=True)
    notification = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text
'''


class Pages(object):
    def __init__(self, count, current_page=1, list_rows=40):
        self.total = count
        self._current = current_page
        self.size = list_rows
        self.pages = self.total // self.size + (1 if self.total % self.size else 0)

        if (self.pages == 0) or (self._current < 1) or (self._current > self.pages):
            self.start = 0
            self.end = 0
            self.index = 1
        else:
            self.start = (self._current - 1) * self.size
            self.end = self.size + self.start
            self.index = self._current
        self.prev = self.index - 1 if self.index > 1 else self.index
        self.next = self.index + 1 if self.index < self.pages else self.index


class PostManager(models.Manager):
    def get_all_hot_posts(self):
        query = self.get_queryset().filter(replynum__gt=0).order_by('-replynum')
        query.query.group_by = ['id'] # Django使用GROUP BY方法
        return query

    def get_all_post(self, num=36, current_page=1): # 可以考虑在这里过滤掉没有头像的用户发帖，不显示在主页
        count = self.get_queryset().count()
        page = Pages(count, current_page, num)
        query = self.get_queryset().select_related('node', 'author', 'last_replied_by').\
            all().order_by('-created_date', '-last_replied_time', '-id')[page.start:page.end]
        return query, page

    def get_all_topics_by_node_slug(self, num = 36, current_page = 1, node_slug = None):
        count = self.get_queryset().filter(node__slug=node_slug).count()
        page = Pages(count, current_page, num)
        query = self.get_queryset().select_related('node', 'author', 'last_replied_by').\
            filter(node__slug=node_slug).order_by('-created_date', '-last_replied_time', '-id')[page.start:page.end]
        return query, page

    def get_user_all_topics(self, uid, num = 36, current_page = 1):
        count = self.get_queryset().filter(author__id=uid).count()
        page = Pages(count, current_page, num)
        query = self.get_queryset().select_related('node', 'author', 'last_replied_by').\
            filter(author__id=uid).order_by('-id')[page.start:page.end]
        return query, page

    def get_topic_by_topic_id(self, topic_id):
        query = self.get_queryset().select_related('node', 'author', 'last_replied_by').get(pk=topic_id)
        return query

    def get_user_last_created_topic(self, uid):
        query = self.get_queryset().filter(author__id=uid).order_by('-created_date')[0]
        return query


class Node(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)          # 块，作为node的识别url
    introduction = models.CharField(max_length=500, null=True, blank=True)  # 介绍
    created_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    topic_count = models.IntegerField(null=True, blank=True)


class Post(models.Model):
    author = models.ForeignKey(account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    replynum = models.IntegerField(default=0)
    node = models.ForeignKey(Node, null=True, blank=True, on_delete=models.CASCADE)
    last_replied_by = models.ForeignKey('auth.User', related_name='post_last', null=True, blank=True,
                                        on_delete=models.CASCADE)
    last_replied_time = models.DateTimeField(null=True, blank=True)
    objects = PostManager()

    file_address = models.CharField(max_length=200, null=True)
    file_name = models.CharField(max_length=200, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Reply(models.Model):
    author = models.ForeignKey(account, on_delete=models.CASCADE)
    post = models.ForeignKey('Post',null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text


class Bulletin(models.Model):
    author = models.ForeignKey(account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(account, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(account, related_name="receiver", on_delete=models.CASCADE)
    text = models.TextField()
    published_date = models.DateTimeField(
        blank=True, null=True)
    notification = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text

