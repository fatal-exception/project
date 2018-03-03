import xmlrpc.client, json, sys, dbm
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import authenticate as auth
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

ROOT = "http://127.0.0.1:"

config = {
    'pyu': 11213,
    'siddham': 11214,
    'FT': 11215,
    'wellcome': 11216,
    'bowls': 11217,
    'genesis': 11218,
}

server = {
    'pyu':  xmlrpc.client.ServerProxy(ROOT+str(config['pyu']), allow_none=True), 
    'siddham': xmlrpc.client.ServerProxy(ROOT+str(config['siddham']), allow_none=True), 
    'bowls': xmlrpc.client.ServerProxy(ROOT+str(config['bowls']), allow_none=True), 
    'FT': xmlrpc.client.ServerProxy(ROOT+str(config['FT']), allow_none=True), 
    'wellcome': xmlrpc.client.ServerProxy(ROOT+str(config['wellcome']), allow_none=True), 
    'genesis': xmlrpc.client.ServerProxy(ROOT+str(config['genesis']), allow_none=True), 
    'vasari': xmlrpc.client.ServerProxy(config['vasari'], allow_none=True), 
    'microsoft': xmlrpc.client.ServerProxy(config['microsoft'], allow_none=True), 
}

KML_data = dbm.open('/home/mhroot/public_www/Samtlas/SAMTLA/location.data', 'r')
people_data = dbm.open('/home/mhroot/public_www/Samtlas/SAMTLA/people.data', 'r')
cachedata = dbm.open('/home/mhroot/public_www/Samtlas/SAMTLA/cache.data', 'c')

NER_meta = {
    'Location': KML_data,
    'People': people_data,
}

global corpus, s

def signin(request):
    context = {}
    return render(request, 'samtla/login.html', context)

def changepassword(request):
    context = {}
    return render(request, 'samtla/registration.html', context)

    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        newpassword = request.POST.get('newpassword')
        user = auth(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user.set_password(password)
                user.save()
                # Redirect to a success page.
                message = "You've successfully changed your password."
            else:
                message = "You don't have an active account"
                # Return a 'disabled account' error message
        else:
            # Return an 'invalid login' error message.
            message = "Login failed."
        context = {}
        return render(request, 'samtla/registration.html', context)

def register(request):
    message = "You've successfully registered."
    if request.method == 'GET':
        context = {}
        return render(request, 'samtla/registration.html', context)

    if request.method == 'POST':
        reg_user = request.POST.get('user')
        reg_password = request.POST.get('password')
        reg_email = request.POST.get('email')
        reg_name = request.POST.get('name')
        register = User.objects.create_user(
            reg_user, 
            reg_email, 
            reg_password
        )
        register.save()
        return redirect('/')

def signout(request):
    tic = time.clock()	
    resultmode = True
    searchmode = False
    feedbackmode = False
    toc = time.clock()	
    time_taken = str(toc - tic)
    userid = request.user.id
    logout(request)
    return redirect('/')

def authenticate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth(username=username, password=password)
    if user is not None:
        if user.is_active:
            #print(request.POST.keys(), user)
            login(request, user)
            message = "Login correct"
            userid = request.user.id
            #print ("userID", user, message)
            if username[:5] == "guest": 
                return redirect('/home?corpus=genesis')
            else:
                return redirect('/home?corpus=genesis')
        else:
            message = "Account disabled"
    else:
        message = "Login invalid"
        data = message
        context = {'data': data}
        return redirect('/')


def home(request):
    corpus = getCorpus(request)
    context = {'username': str(request.user).title(), 'corpus': corpus}
    return render(request, 'samtla/index_v1.html', context)

def select(request):
    context = {}
    return render(request, 'samtla/choice.html', context)
    

def Search(request):
    if request.method == 'GET' and request.is_ajax():
        q = request.GET.get('q', "")
        corpus = getCorpus(request)
        ranking = server[corpus].Search(request.user, q)
        related_queries = s.RelatedQueries(request.user, q)
        dataout = {
            'ranking': ranking, 
            'relatedqueries': related_queries
        }
        return JsonResponse(dataout)


def RelatedQueries(request):
    q = request.GET.get('q', "")
    corpus = getCorpus(request)
    related_queries = server[corpus].RelatedQueries(q)
    return JsonResponse(related_queries, safe=False)

def getCorpus(request):
    return request.GET.get('corpus', '').split('#')[0]

def Document(request):
    docID = request.GET.get('docID', 0)
    highlighted_flag = request.GET.get('highlighted', 0)
    corpus = getCorpus(request)
    title = server[corpus].getDocumentTitle(docID)

    if highlighted_flag == 'true':
        document = server[corpus].QueryDocument(docID)
    else:
        document = server[corpus].ViewOriginal(request.user, docID)
    return JsonResponse({'title': title, 'document': document})


def Original(request):
    docID = request.GET.get('docID', 0)
    corpus = getCorpus(request)
    document = server[corpus].ViewOriginal(docID)
    return JsonResponse(document, safe=False)

def RelatedDocuments(request):
    if request.method == 'GET' and request.is_ajax():
        docID = request.GET.get('docID', 0)
        corpus = getCorpus(request)
        data = server[corpus].RelatedDocuments(docID)
        return JsonResponse(data, safe=False)

def DocumentTitle(request):
    docID = request.GET.get('docID', 0)
    corpus = getCorpus(request)
    data = server[corpus].DocumentTitle(docID)
    return JsonResponse(data, safe=False)

def DocumentMetadata(request):
    if request.method == 'GET' and request.is_ajax():
        docID = request.GET.get('docID', 0)
        corpus = getCorpus(request)
        data = server[corpus].DocumentMetadata(docID)
        return JsonResponse(data, safe=False)

def Compare(request):
    docID = request.GET.get('docID', 0)
    doc2 = request.GET.get('doc2', 0)
    corpus = getCorpus(request)
    data = server[corpus].compare(docID, doc2)
    return JsonResponse(data, safe=False)#jsonify(data)


def Browse(request):
    if request.method == 'GET' and request.is_ajax():
        corpus = getCorpus(request)
        path = request.GET.get('path', 0).lstrip(',').replace('%20', ' ').split(',')
        data = server[corpus].Browse(path)
        return JsonResponse(data, safe=False)


def NER(request):
    docID = request.GET.get('docID', False)
    typeof = request.GET.get('NERtype', False)
    NER = request.GET.get('NER', False)
    if request.method == 'GET' and request.is_ajax():
        corpus = getCorpus(request)
        data = server[corpus].getNER(docID, typeof, NER)
        return JsonResponse(data, safe=False)

def KML(request):
    if request.method == 'GET' and request.is_ajax():
        corpus = getCorpus(request)
        NER = bytes(request.GET.get('NER', False), 'utf8')
        cat = request.GET.get('cat', False)
        data = KML_data.get(NER, {})
        if data != {}:
            data = data.decode('utf8')
        return JsonResponse(data, safe=False)
