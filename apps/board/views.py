from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic

from . import forms, models


def index(request):
    """Unused view"""
    context = {'boards': models.Board.objects.all()}
    return render(request, 'index.html', context)


class BoardListView(generic.ListView):
    model = models.Board
    context_object_name = 'boards'
    template_name = 'index.html'


def board_topics(request, pk):
    """Unused view"""
    board = get_object_or_404(models.Board, pk=pk)
    queryset = board.topics.order_by(
        '-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    return render(request, 'topics.html', {'board': board, 'topics': topics})


class TopicListView(generic.ListView):
    model = models.Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(models.Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by(
            '-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


@login_required
def new_topic(request, pk):
    board = get_object_or_404(models.Board, pk=pk)

    if request.method == 'POST':
        form = forms.NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = models.Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('reply_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = forms.NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    """Unused view"""
    topic = get_object_or_404(models.Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


class PostListView(generic.ListView):
    model = models.Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(
            models.Topic,
            board__pk=self.kwargs.get('pk'),
            pk=self.kwargs.get('topic_pk')
        )
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def reply_posts(request, pk, topic_pk):
    topic = get_object_or_404(models.Topic, board__pk=pk, pk=topic_pk)

    if request.method == 'POST':
        form = forms.PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = forms.PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(generic.UpdateView):
    model = models.Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'topic_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect(
            'topic_posts',
            pk=post.topic.board.pk,
            topic_pk=post.topic.pk
        )
