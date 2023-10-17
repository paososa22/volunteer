from django.shortcuts import render, redirect
from .forms import AuthenticationUserForm , CreateUserForm , UserProfileForm, UserLanguageForm,NuevaOrg1,OrgSearchForm,CommentForm,EditOrganization,InteresaForm,EditMailOrganization,EditNameOrganization
from .models import ExtendedData,PreferredLanguage,Organization1,Comment,Interesados
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import get_user
from django.shortcuts import render
import requests, uuid, json

# Create your views here.
@login_required
def inicio_comunidad(request):
    user_request=User.objects.get(username=request.user.username)
    user_extended_data=ExtendedData.objects.get(user=user_request)
    data_context ={'user_data':user_request,'user_extended_data':user_extended_data}
    print(user_request.username)
    return render(request,'home.html',data_context)

def createuser(request):
    user_form = CreateUserForm()
    user_profile=UserProfileForm()
    user_language=UserLanguageForm()
    error_message = None
    data_context = {'user_form':user_form,'user_profile':user_profile,'user_language':user_language}
    if request.method=='POST':
        print(request.POST)
        user_form=CreateUserForm(request.POST)
        user_profile=UserProfileForm(request.POST)
        user_language=UserLanguageForm(request.POST)
        print(user_form.errors,user_profile.errors,user_language.errors)
        if user_form.is_valid():
            user_form.save()
            user_to_profile = User.objects.get(username=request.POST.get('username'))
            user_extended_data = ExtendedData.objects.create(user=user_to_profile,user_type=request.POST.get('user_type'))
            user_extended_data.save()
            user_to_profile = User.objects.get(username=request.POST.get('username'))
            user_preferred_language =PreferredLanguage.objects.create(user=user_to_profile,preferred_language=request.POST.get('preferred_language'))
            user_preferred_language.save()
            return redirect('login')
        else:
            error_message = "Verifica tus datos, contiene valores NO validos"
    data_context['error_message']=error_message
    return render(request,'create_user.html',data_context)

@login_required
def get_volunteerdata(request,user_id):
    vol = User.objects.get(id=user_id)
    data_context = {'volunteer':vol}
    return render(request,'get_volunteerdata.html',data_context)

@login_required
def manager_getdata(request,user_id):
    man = User.objects.get(id=user_id)
    data_context = {'user':man}
    return render(request,'get_managerdata.html',data_context)

@login_required
def crear_org(request):
    data_context = {'form_nueva_org': NuevaOrg1()}
    if request.method == 'POST':
        formulario = NuevaOrg1(request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            organizacion = formulario.save(commit=False)
            organizacion.user_type = request.user.extendeddata
            organizacion.save()
            data_context['message'] = "Organización registrada"
        else:
            data_context['message'] = "No se pudo registrar la organización , contiene datos No validos"
    return render(request, 'crear_org.html', data_context)


@login_required
def ver_org(request):
    organization = Organization1.objects.filter(user_type=request.user.extendeddata,deleted_date__isnull=True)
    data_context={'my_orglist':organization}
    return render(request, 'lista_organizacion.html', data_context)


@login_required
def vista_org(request):
    organization = Organization1.objects.filter(deleted_date__isnull=True)
    form = OrgSearchForm(request.POST)
    data_context={'org_list':organization,'form':form}
    if request.method == 'POST':
        if form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            tipo = form.cleaned_data.get('tipo')
            if nombre:
                organization = organization.filter(organization_name__icontains=nombre)
            if tipo:
                if tipo!='':
                    organization = organization.filter(organization_type=tipo)

            data_context['org_list'] = organization
    else:
        form = OrgSearchForm()
    data_context['form'] = form
    return render(request, 'vista_org.html', data_context)




@login_required
def get_orgdata(request,organization_id):
    key = "243deaf16b8b4ed6b39ef52fe0ac892e"
    endpoint ="https://api.cognitive.microsofttranslator.com/"
    location = "eastus"

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    organization = Organization1.objects.get(id=organization_id)
    comments = Comment.objects.filter(organization=organization).order_by('-created_date')
    comment_form = CommentForm()
    user = get_user(request)
    preferred_language = user.preferredlanguage.preferred_language
    translated_comments = []

    if request.method == 'POST' and not request.user.extendeddata.user_type == 'R':
        comment_form = CommentForm(request.POST)
        print(comment_form.errors)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.organization = organization
            comment.preferred_language = request.user.preferredlanguage
            for comment in comments:
                source_language = comment.preferred_language.preferred_language
                text_to_translate = comment.text
                translation_params = {
                    'api-version': '3.0',
                    'from': source_language,
                    'to': [preferred_language],
                }
                translation_request = requests.post(constructed_url, params=translation_params, headers=headers, json=[{'text': text_to_translate}])
                translation_response = translation_request.json()
                print(json.dumps(translation_response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
                translated_comments.append(comment)
                comment_form.save()
            comment_form = CommentForm()
    context = {
        'Organitation': organization,
        'comments': translated_comments,
        'comment_form': comment_form,
    }
    return render(request, 'get_orgdata.html', context)

@login_required
def delete_organization(request, organization_id):
    organization = Organization1.objects.get(pk=organization_id)
    data_context = {'organization': organization}
    if request.method == 'POST':
        if 'yes' in request.POST:
            organization.deleted_date = timezone.now()
            organization.save()
            return redirect('ver_org') 
    return render(request, 'delete_org.html', data_context)

@login_required
def update_organizationdata(request, organization_id):
    organization = Organization1.objects.get(id=organization_id)
    data_context = {'organization': organization}
    formulario = EditOrganization()
    data_context['form_edit_organization'] = formulario
    if request.method == "POST":
        formulario = EditOrganization(request.POST, instance=organization)
        if formulario.is_valid():
            formulario.save()
            data_context['message'] = "Datos actualizados"
        else:
            data_context['message'] = "No se pudo actualizar"
    return render(request, 'update_orgdata.html', data_context)

@login_required
def update_organizationname(request, organization_id):
    organization = Organization1.objects.get(id=organization_id)
    data_context = {'organization': organization}
    formularioname = EditNameOrganization()
    data_context ['form_edit_name'] = formularioname
    if request.method == "POST":
        formularioname =EditNameOrganization(request.POST, instance=organization) 
        if formularioname.is_valid():
            formularioname.save()
            data_context['message'] = "Nombre de organización actualizado"
        else:
            data_context['message'] = "No se pudo actualizar el nombre de la organización"

    return render(request, 'update_orgname.html', data_context)

@login_required
def update_organizationmail(request, organization_id):
    organization = Organization1.objects.get(id=organization_id)
    data_context = {'organization': organization}
    formulariomail = EditNameOrganization()
    data_context ['form_edit_mail'] = formulariomail
    if request.method == "POST":
        formulariomail =EditNameOrganization(request.POST, instance=organization) 
        if formulariomail.is_valid():
            formulariomail.save()
            data_context['message'] = "Nombre de organización actualizado"
        else:
            data_context['message'] = "No se pudo actualizar el nombre de la organización"
    return render(request, 'update_orgmail.html', data_context)

@login_required
def view_comments(request, organization_id):
    organization = Organization1.objects.get(id=organization_id)
    comments = Comment.objects.filter(organization=organization).order_by('-created_date')
    context = {
        'Organitation': organization,
        'comments': comments,
    }
    return render(request, 'view_comments.html', context)

from django.db import transaction

@login_required
def get_interesados(request, organization_id):
    try:
        organization = Organization1.objects.get(id=organization_id)
    except Organization1.DoesNotExist:
        return redirect('home')
    if request.user.extendeddata.user_type == 'V':
        interesado_existente = Interesados.objects.filter(organizacion=organization, user=request.user).exists()
        if request.method == 'POST':
            with transaction.atomic():
                interesa_form = InteresaForm(request.POST)
                if interesa_form.is_valid():
                    if not interesado_existente:  
                        interesado = interesa_form.save(commit=False)
                        interesado.user = request.user
                        interesado.organizacion = organization
                        if 'si' in request.POST.get('interes'):
                            interesado.confirmar = 'Y'
                            interesado.save()
                            return redirect('vista_org')
                    else:  
                        if 'no' in request.POST.get('interes'):
                            
                            Interesados.objects.filter(organizacion=organization, user=request.user).delete()
                            return redirect('vista_org')
        else:
            if interesado_existente:
                interesa_form = InteresaForm(initial={'organizacion': organization.id, 'user': request.user.id})


        context = {
            'Organitation': organization,
            'interesados': Interesados.objects.filter(organizacion=organization),
            'interesa_form': interesa_form,
            'interesado_existente': interesado_existente,  # Agregar esto al contexto
        }
        return render(request, 'interesa.html', context)
    else:
        return redirect('home')

@login_required
def view_intereses(request, organization_id):
    try:
        organization = Organization1.objects.get(id=organization_id)
    except Organization1.DoesNotExist:
        return redirect('home')
    user_type = request.user.extendeddata.user_type
    if user_type == 'V':
        interesados_usuario = Interesados.objects.filter(user=request.user)
        context = {
            'Organitation': organization,
            'interesados_usuario': interesados_usuario,
        }
    elif user_type == 'R':
        interesados_organizacion = Interesados.objects.filter(organizacion=organization)
        context = {
            'Organitation': organization,
            'interesados_organizacion': interesados_organizacion,
        }

    return render(request, 'view_intereses.html', context)




