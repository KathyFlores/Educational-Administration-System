# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Reply, Message, Bulletin
from .forms import PostForm, ReplyForm, BulletinForm, MessageForm
from django.shortcuts import redirect
from basicInfo.models import attrib as Attrib, account as Account
import os

root = os.getcwd()



# Create your views here.
def home(request):
    # a = Post.objects.all()
    # b = a.delete()
    # a = Reply.objects.all()
    # a.delete()
    # a = Bulletin.objects.all()
    # a.delete()
    posts = Post.objects.order_by('-published_date')
    if len(posts) > 6:
        posts1= posts[0:3]
        posts2= posts[3:6]
        posts3= posts[6:9]
        posts4= posts[9:12]
    bulletin = Bulletin.objects.order_by('-published_date')
    if bulletin:
        bulletin = bulletin[0]
    else:
        bulletin = None
    hot_topics = Post.objects.get_all_hot_posts()
    return render(request, 'Forum/home.html', {'posts1': posts1, 'posts2': posts2,'posts3': posts3,'posts4': posts4,'hot_topics': hot_topics, 'bulletin': bulletin})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            account_id = request.session["account_id"]
            account = Account.objects.get(account_id=account_id)
            post.author = account
            # post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'Forum/post_edit.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    replys = Reply.objects.all()
    return render(request, 'Forum/post_detail.html', {'post': post, 'replys': replys})


def post_list(request):
    posts = Post.objects.order_by('-published_date')
    return render(request, 'Forum/post_list.html', {'posts': posts})


def post_search(request):
    request.encoding = 'utf-8'
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        # print('not q')
        error_msg = 'Please input search key'
        return render(request, 'Forum/post_search.html', {'error_msg': error_msg})
    posts = Post.objects.filter(title__contains=q)
    return render(request, 'Forum/post_search.html', {'error_msg': error_msg, 'posts': posts})


def reply_new(request, pk):
    text = request.GET.get('text')
    if not text:
        form = ReplyForm()
        return render(request, 'Forum/reply_edit.html', {'form': form})

    text = request.GET.get('text')
    reply = Reply()
    reply.text = text
    post = get_object_or_404(Post, pk=pk)
    reply.post = post
    account_id = request.session["account_id"]
    account = Account.objects.get(account_id=account_id)
    reply.author = account
    # reply.author = request.user
    reply.published_date = timezone.now()
    reply.save()
    post.replynum += 1
    post.save()
    return redirect('post_detail', pk)


def bulletin_new(request):
    if request.method == "POST":
        form = BulletinForm(request.POST)
        if form.is_valid():
            bulletin = form.save(commit=False)
            account_id = request.session["account_id"]
            account = Account.objects.get(account_id=account_id)
            bulletin.author = account
            # bulletin.author = request.user
            bulletin.created_date = timezone.now()
            bulletin.published_date = bulletin.created_date
            bulletin.save()
            return redirect('forum')
    else:
        form = BulletinForm()
    return render(request, 'Forum/bulletin_new.html', {'form': form})


def message_new(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
        
            account_id = request.session["account_id"]
            account = Account.objects.get(account_id=account_id)
            # message.receiver = account
            message.sender = account
            message.published_date = timezone.now()
            message.save()
            return redirect('message_receive')
    else:
        form = MessageForm()
    return render(request, 'Forum/message_edit.html', {'form': form})


def message_send(request):
    account_id = request.session["account_id"]
    account = Account.objects.get(account_id=account_id)
    msgs = Message.objects.filter(sender=account).order_by('-published_date')
    return render(request, 'Forum/message_send.html', {'msgs': msgs})


def message_receive(request):
    account_id = request.session["account_id"]
    account = Account.objects.get(account_id=account_id)
    msgs = Message.objects.filter(receiver=account).order_by('-published_date')
    return render(request, 'Forum/message_receive.html', {'msgs': msgs})


def upload(request, pk):
    if request.method == 'POST':
        ret = {'status': False, 'data': None, 'error': None}
        try:
            img = request.FILES.get('img')
            if not os.path.exists(os.path.join(root, 'files')):
                os.mkdir(os.path.join(root, 'files'))
            f = open(os.path.join(root, 'files', img.name), 'wb')

            post = get_object_or_404(Post, pk=pk)
            post.file_address = os.path.join(root, 'files', img.name)
            post.file_name = img.name
            post.save()
            for chunk in img.chunks(chunk_size=1024):
                f.write(chunk)
            ret['status'] = True
            ret['data'] = os.path.join('files', img.name)
        except Exception as e:
            print(e)
            ret['error'] = e
        finally:
            f.close()
            print('/post/{}'.format(pk))
            return redirect('post_detail', pk)
    return render(request, 'Forum/upload.html', {'pk': pk})



from django.http import FileResponse


def file_down(request, pk):
    post = get_object_or_404(Post, pk=pk)
    file_address = post.file_address
    file = open(file_address, 'rb')
    file_name = post.file_name
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
    return response


# def get_node_topics(request, slug):
#     node = get_object_or_404(Node, slug=slug)

#     user = request.user
#     if user.is_authenticated():
#         counter = {
#             'topics': user.topic_author.all().count(),
#             'replies': user.reply_author.all().count(),
#             'favorites': user.fav_user.all().count()
#         }
#         notifications_count = user.notify_user.filter(status=0).count()

#     try:
#         current_page = int(request.GET.get('p', '1'))
#     except ValueError:
#         current_page = 1

#     topics, topic_page = Topic.objects.get_all_topics_by_node_slug(node_slug=slug, current_page=current_page)
#     active_page = 'topic'
#     return render_to_response('topic/node_topics.html', locals(),
#         context_instance=RequestContext(request))