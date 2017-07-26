from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.db.models import F
from shopmanagement.forms import UserForm, CommentForm
from shopmanagement.models import Item, Comment
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def ItemDetailCommentView(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data
            text = text.replace(",", " ")
            text = text.replace(".", " ")
            comment = Comment(user=request.user, item=item, text=text)
            comment.save()
            temp = text.split()
            positive = ['great', 'awesome', 'accept', 'acceptance', 'admirable', 'advantage', 'advantage', 'aim', 'accuracy',
             'achievement', 'achieve', 'adventure', 'affection', 'appreciation', 'appreciate', 'attraction',
             'attracting', 'beatify', 'beneficial', 'benefit', 'beauty', 'beloved', 'best', 'better', 'bless',
             'blessng', 'beauty', 'beautiful', 'care', 'capable', 'celebrate', 'clean', 'comfort', 'caring',
             'commitment', 'concentration', 'confidence', 'cooperation', 'creativity', 'curiosity', 'decent',
             ' desirable', 'delicious', 'dream', 'dreamy', 'dynamic', 'easy', 'easily', 'efficient', 'enjoy',
             'eagerness', 'effectiveness', 'efficiency', 'enthusiasm', 'excite', 'excitement', 'experience',
             'expertise', 'fantastic', 'feel good', 'fabulous', 'fair', 'favorite', 'flexibility', 'fun', 'future',
             'genius', 'genuine', 'gift', 'good', 'goodness', 'goodness', 'good feeling', 'happiness', ' happy',
             'happily', 'humble', 'in love', 'incredible', 'innovate', 'interesting', 'interest', 'interested',
             'improvement', 'joy', 'joyful', 'like', 'learn', 'luxury', 'longevity', 'love', 'love', 'lovable',
             'learning', 'liberty', 'logic', 'luck', 'lucky', 'loving', 'kindness', 'magnificent', 'marvelous',
             'miracle', ' magic', ' making a difference', 'new', ' nice', ' optimist', 'optimistic', 'outstanding',
             'ok', 'perfect', 'perfection', 'quality', 'secured', 'security', 'true', ' trusting', 'thankful', 'trust',
             'truth', 'worth', 'worthy', 'wonderful', 'wonderful', 'good', 'excellent', 'awesome', 'superb', 'nice',
             'cool', 'aweful', 'fun', 'happy']

            negative = ['angry', 'worst', 'awful', 'costly', 'bad', 'boring', 'broken', 'collapse', 'confused', 'cry',
                        'dead', 'damage', 'depressed', 'dirty', 'dishonest', 'distress', 'faulty', 'fear', 'feeble',
                        'filthy', 'foul', 'guilty', 'hard', 'harmful', 'hate', 'horrible', 'hurt', 'hurtful', 'ignore',
                        'ignorant', 'imperfect', 'impossible', 'inelegant', 'lose', 'misshapen', 'missing', 'nasty',
                        'negative', 'never', 'no', 'nonsense', 'pain', 'poor', 'quit', 'reject', 'reject', 'repulsive',
                        'sad', 'scare', 'shocking', 'stressful', 'stupid', 'suspect', 'suspicious', 'terrible', 'terrifying',
                        'threatening', 'ugly', 'undermine', 'unfair', 'unfavorable', 'unhappy', 'unhealthy', 'unpleasant',
                        'upset', 'unsatisfactory', 'unsightly', 'untoward', 'unwanted', 'unwelcome', 'unwholesome',
                        'unwieldy', 'unwise', 'upset', 'worthless']

            for word in temp:
                if (word in positive):
                    item.positive_comments += 1
                    item.total_comments += 1
                if (word in negative):
                    item.total_comments += 1
            if item.total_comments > 0:
                item.rating = (item.positive_comments*5/item.total_comments)
                k = item.rating
                item.save()

            return render(request, 'shopmanagement/item_detail.html', {'form': form, 'item': item})
    else:
        form = CommentForm()
    return render(request, 'shopmanagement/item_detail.html', {'form': form, 'item': item})



def Home(request):
    return render(request, "Home.html")

@method_decorator(login_required,name='dispatch')
class ItemView(ListView):
    model = Item
    template_name = "item_list"

    def get_queryset(self):
        return Item.objects.all().order_by('rating')

@method_decorator(login_required,name='dispatch')
class ItemCreate(CreateView):
    model = Item
    fields = ['product_name','product_type','price_per_piece','discount','description']
    success_url = "list/"
    def get_queryset(self):
        return Item.objects.all()

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ItemCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('item-list')

@method_decorator(login_required,name='dispatch')
class ItemUpdate(UpdateView):
    model = Item
    fields = ['product_name','product_type','price_per_piece','discount','description']

    def get_success_url(self):
        return reverse("item-list")

    def get_queryset(self):
        obj = Item.objects.all()
        return obj
        # return super(CardCreateView, self).get_queryset()

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ItemUpdate, self).form_valid(form)

@method_decorator(login_required,name='dispatch')
class ItemDetailView(DetailView):
    model = Item
    context_object_name = 'items'

    def get_queryset(self):
        obj = Item.objects.all().filter(id=self.kwargs['pk'])
        return obj

@method_decorator(login_required,name='dispatch')
class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('item-list')

def adduser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            return render(request, "Home.html")
    else:
        form = UserForm()

    return render(request, 'adduser.html', {'form': form})

