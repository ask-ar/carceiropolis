# coding: utf-8
import logging
import operator
from collections import OrderedDict, defaultdict
from csv import DictReader
from functools import reduce
import json
import base64

from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.messages import info, error
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.text import slugify
from mezzanine.accounts import get_profile_form
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.views import paginate
from mezzanine.utils.urls import login_redirect, next_url
from bokeh.embed import server_document

from .models import (AreaDeAtuacao, Especialidade, Especialista, Publicacao,
                     UnidadePrisional)
from carceropolis import charts

# from mezzanine.utils.views import render

User = get_user_model()

log = logging.getLogger(__name__)


# def setlanguage(request):
    # return render(request, 'set-language.html',
                  # {'LANGUAGES':settings.LANGUAGES,
                   # 'SELECTEDLANG':request.LANGUAGE_CODE})


###############################################################################
# PUBLICACOES
###############################################################################

def publicacao_home(request):
    """Display the Publicações Home page, which is a matrix with all available
    categories (only categories, not the items from the Publicação Class).
    """
    categorias = AreaDeAtuacao.objects.all()
    categorias = categorias.order_by('ordem')
    templates = ["carceropolis/publicacao/publicacao_home.html"]
    context = {'categorias': categorias}
    return TemplateResponse(request, templates, context)


def publicacao_list_tag(request, tag, extra_context=None):
    """Display a list of blog posts that are filtered by tag, year, month,
    author or categoria. Custom templates are checked for using the name
    ``carceropolis/publicacao/publicacao_list_XXX.html`` where ``XXX`` is
    either the categoria slug or author's username if given.
    """
    templates = []
    template = "carceropolis/publicacao/publicacao_list.html"
    publicacoes = Publicacao.objects.published()
    tag = get_object_or_404(Keyword, slug=tag)
    publicacoes = publicacoes.filter(keywords__keyword=tag)

    prefetch = ("categorias", "keywords__keyword")
    publicacoes = publicacoes.prefetch_related(*prefetch)
    publicacoes = paginate(publicacoes, request.GET.get("page", 1),
                           settings.PUBLICACAO_PER_PAGE,
                           settings.MAX_PAGING_LINKS)
    context = {"publicacoes": publicacoes, "tag": tag,}
    context.update(extra_context or {})
    templates.append(template)
    return TemplateResponse(request, templates, context)


def publicacao_list_categoria(request, categoria, extra_context=None):
    """Display a list of Publicacao for a specific Categoria with some filters.

    The list can be filtered by tag, year, author.
    """
    templates = []
    template = "carceropolis/publicacao/publicacao_list.html"

    log.debug('Getting list of Publicacoes for category %s', categoria)

    categoria = get_object_or_404(AreaDeAtuacao, slug=categoria)

    publicacoes = Publicacao.objects.filter(categorias=categoria)

    ano = request.GET.get('ano', None)
    if ano:
        log.debug('    filtering ano: %s', ano)
        publicacoes = publicacoes.filter(ano_de_publicacao=ano)

    autoria = request.GET.get('autoria', None)
    if autoria:
        log.debug('    filtering autoria: %s', autoria)
        publicacoes = publicacoes.filter(autoria__icontains=autoria)

    tags = request.GET.get('tag', None)
    if tags:
        log.debug('    filtering tags: %s', tags)
        publicacoes = publicacoes.filter(keywords__keyword__title__iregex=r'(' + '|'.join(tags.split()) + ')')

    search = request.GET.get('q', None)
    if search is not None and search:
        terms = search.split()
        log.debug('    general filtering: %s', terms)

        publicacoes = publicacoes.filter(reduce(operator.and_,
                                                (Q(title__icontains=q) for q in terms)) |
                                         reduce(operator.or_,
                                                (Q(autoria__icontains=q) for q in terms)) |
                                         reduce(operator.or_,
                                                (Q(content__icontains=q) for q in terms)) |
                                         reduce(operator.or_,
                                                (Q(description__icontains=q) for q in terms)) |
                                         reduce(operator.or_,
                                                (Q(keywords__keyword__title__icontains=q) for q in terms))
                                         )

    order_by = request.GET.get('order_by', None)
    sort = request.GET.get('sort', 'ASC')
    if order_by:
        if sort == 'ASC':
            publicacoes = publicacoes.order_by(order_by)
        else:
            publicacoes = publicacoes.order_by('-' + order_by)

    #: Get only unique results
    publicacoes = publicacoes.distinct()

    prefetch = ("categorias", "keywords__keyword")
    publicacoes = publicacoes.prefetch_related(*prefetch)
    publicacoes = paginate(publicacoes, request.GET.get("page", 1),
                           settings.PUBLICACAO_PER_PAGE,
                           settings.MAX_PAGING_LINKS)

    context = {"publicacoes": publicacoes, "ano": ano, "tag": tags,
               "categoria": categoria, "autoria": autoria, "q": search}
    context.update(extra_context or {})

    templates.append(template)

    return TemplateResponse(request, templates, context)


def publicacao_detail(request, slug, extra_context=None):
    """Presenting a specific publication (publicaço)."""
    template = "carceropolis/publicacao/publicacao_detail.html"
    publicacoes = Publicacao.objects.published().select_related()
    publicacao = get_object_or_404(publicacoes, slug=slug)
    related_posts = publicacao.related_posts.published()
    context = {"publicacao": publicacao, "editable_obj": publicacao,
               "related_posts": related_posts}
    context.update(extra_context or {})
    templates = [template]
    return TemplateResponse(request, templates, context)


def publicacao_feed(request, fmt, **kwargs):
    """Blog posts feeds - maps format to the correct feed view."""
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[fmt](**kwargs)(request)
    except KeyError:
        raise Http404()


###############################################################################
# ESPECIALISTAS
###############################################################################


def especialistas_list(request, extra_context=None):
    """Display a list of blog posts that are filtered by tag, year, month,
    author or categoria. Custom templates are checked for using the name
    ``carceropolis/publicacao/publicacao_list_XXX.html`` where ``XXX`` is
    either the categoria slug or author's username if given.
    """
    areas_de_atuacao = AreaDeAtuacao.objects.all()
    areas_de_atuacao = areas_de_atuacao.order_by('ordem')
    especialistas = Especialista.objects.all()
    especialistas = especialistas.order_by('nome')

    context = {
        'area_atuacao': '',
        'nome': '',
        'especialidade': '',
        'areas_de_atuacao': areas_de_atuacao,
        'especialistas': None,
        'error_message': ''
    }

    if 'nome' in request.GET.keys():
        nome = request.GET.get('nome'),
        nome = nome[0]
        nomes = nome.split('-')
        for item in nomes:
            especialistas = especialistas.filter(
                nome__icontains=item)
        context['nome'] = nomes

    if 'area_atuacao' in request.GET.keys():
        area_atuacao = request.GET.get('area_atuacao'),
        area_atuacao = area_atuacao[0]
        areas = area_atuacao.split('-')
        for area in areas:
            especialistas = especialistas.filter(
                area_de_atuacao__nome__icontains=area)
        context['area_atuacao'] = area_atuacao

    if 'especialidade' in request.GET.keys():
        especialidade = request.GET.get('especialidade'),
        especialidade = especialidade[0]
        especialidades = especialidade.split('-')
        for item in especialidades:
            especialistas = especialistas.filter(
                especialidades__nome__icontains=item)
        context['especialidade'] = especialidade

    prefetch = ("area_de_atuacao", 'especialidades')
    especialistas = especialistas.prefetch_related(*prefetch)
    especialistas = paginate(especialistas, request.GET.get("page", 1),
                             settings.PUBLICACAO_PER_PAGE,
                             settings.MAX_PAGING_LINKS)

    if not especialistas:
        especialistas = Especialista.objects.all()
        context['error_message'] = 'Nenhum(a) especialista encontrado(a) com '
        context['error_message'] += 'os parâmetros passados.'

    context['especialistas'] = especialistas

    templates = ['carceropolis/especialistas/especialistas.html']

    return TemplateResponse(request, templates, context)


def _fileId_from_url(url):
    """Return fileId from a url."""
    index = url.find('~')
    fileId = url[index + 1:]
    # local_id_index = fileId.find('/')

    share_key_index = fileId.find('?share_key')
    if share_key_index == -1:
        return fileId.replace('/', ':')
    else:
        return fileId[:share_key_index].replace('/', ':')


def dados_home(request):
    """Display the Dados Home page, which is a matrix with all available
    categories (only categories, not the items from the Publicação Class).
    """
    templates = ["carceropolis/dados/dados.html"]
    context = {}

    return TemplateResponse(request, templates, context)


def dados_gerais(request):
    """Display the Dados Home page, which is a matrix with all available
    categories (only categories, not the items from the Publicação Class).
    """
    templates = ["carceropolis/dados/dados_gerais.html"]
    return TemplateResponse(request, templates,
                            charts.get_context('dados_gerais'))


def dados_perfil_populacional(request):
    """First test"""
    templates = [u'carceropolis/dados/perfil_populacional.html']
    context = {}

    return TemplateResponse(request, templates, context)


def dados_infraestrutura(request):
    templates = [u'carceropolis/dados/infraestrutura.html']
    context = {}
    return TemplateResponse(request, templates, context)


def dados_juridico(request):
    templates = [u'carceropolis/dados/juridico.html']
    context = {}
    return TemplateResponse(request, templates, context)


def dados_educacao(request):
    """Second test"""
    templates = [u'carceropolis/dados/educacao.html']
    context = {}
    return TemplateResponse(request, templates, context)


def dados_saude(request):
    templates = [u'carceropolis/dados/saude.html']
    context = {}
    return TemplateResponse(request, templates, context)


def dados_materno_infantil(request):
    templates = [u'carceropolis/dados/materno_infantil.html']
    context = {}
    return TemplateResponse(request, templates, context)


def dados_alas_exclusivas(request):
    templates = [u'carceropolis/dados/alas_exclusivas.html']
    context = {}
    return TemplateResponse(request, templates, context)


def dados_piramide_etaria(request):
    """Third test"""
    templates = [u'carceropolis/dados/piramide_etaria.html']
    context = {}

    return TemplateResponse(request, templates, context)


def unidades_map(request):
    """Display the Unidades Prisionais Map."""
    templates = ["carceropolis/unidades/mapa.html"]

    # Fields included in JSON sent to client
    fields = [
        f.name
        for f in UnidadePrisional._meta.get_fields()
        if f not in ['id', 'response']]
    fields.append('municipio__nome')

    # JSON with unidades grouped by uf
    states = defaultdict(list)
    for unidade in UnidadePrisional.objects.exclude(lat=None).values(*fields):
        unidade['municipio'] = unidade.pop('municipio__nome')
        states[unidade['uf']].append(unidade)
    context = {
        'states': mark_safe(json.dumps(states))
    }

    return TemplateResponse(request, templates, context)


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
        else:
            error(request, "Usuário e/ou senha inválidos.")
    return redirect(next_url(request) or request.META['HTTP_REFERER'])


def register_user(request):
    print("registrando um novo usuário")
    profile_form = get_profile_form()
    form = profile_form(request.POST or None, request.FILES or None)
    print(form)
    print(dir(form))
    print(form.is_valid())
    if request.method == "POST" and form.is_valid():
        print("Método post e form válido")
        new_user = form.save()
        if not new_user.is_active:
            if settings.ACCOUNTS_APPROVAL_REQUIRED:
                print('Usuário cadastrado, aguardando aprovação')
                send_approve_mail(request, new_user)
                info(request, "Obrigado por se cadastrar! Você receberá um "
                              "email quando sua conta for ativada.")
            else:
                print('Usuário cadastrado, aguardando confirmação')
                send_verification_mail(request, new_user, "signup_verify")
                info(request, "Um email de verificação foi enviado com um "
                              "link para ativação de sua conta.")
            return redirect(next_url(request) or "/")
        else:
            print('usuário cadastrado com sucesso')
            info(request, "Cadastro realizado com sucesso")
            login(request, new_user)
            return login_redirect(request)
    else:
        error(request, form)
        return redirect(request.META['HTTP_REFERER']+"#cadastro", kwargs={'registration_form': form})
    return redirect(next_url(request) or request.META['HTTP_REFERER'])


def password_recovery(request):
    # TODO
    pass


def data_dashboard(request, template="dashboard/dashboard.html"):
    """Data bokeh dashboard."""
    HOST = request.get_host().split(':' + str(request.get_port()))[0]
    if request.is_secure():
        PROTOCOL = 'https://'
    else:
        PROTOCOL = 'http://'
    script = server_document(url=PROTOCOL + HOST + ':5006/bkapp')
    if request.GET.urlencode():
        state = base64.urlsafe_b64encode(
            request.GET.urlencode().encode()).decode('utf8')
        mark = 'bokeh-absolute-url'
        insert = 'state=' + state + '&' + mark
        script = script.replace(mark, insert)
    context = {"script": script}
    # context = {"script": ' '.join(
    #     script.splitlines()).replace('/script', 'end-script')}
    templates = [template]

    return TemplateResponse(request, templates, context)
