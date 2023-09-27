from django.shortcuts import render, redirect
from .forms import NuevaOrg1,CreateUserForm,UserProfileForm,OrgSearchForm,EditOrganization,CommentForm, InteresaForm
from .models import ExtendedData,Organization1,Comment,Interesados
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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
    error_message = None
    data_context = {'user_form':user_form,'user_profile':user_profile}
    if request.method=='POST':
        print(request.POST)
        user_form=CreateUserForm(request.POST)
        user_profile=UserProfileForm(request.POST)
        print(user_form.errors,user_profile.errors)
        if user_form.is_valid():
            user_form.save()
            user_to_profile = User.objects.get(username=request.POST.get('username'))
            user_extended_data = ExtendedData.objects.create(user=user_to_profile,user_type=request.POST.get('user_type'))
            user_extended_data.save()
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
    organization = Organization1.objects.filter(user_type=request.user.extendeddata)
    data_context={'my_orglist':organization}
    return render(request, 'lista_organizacion.html', data_context)


@login_required
def vista_org(request):
    organization = Organization1.objects.all()
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
    organization = Organization1.objects.get(id=organization_id)
    comments = Comment.objects.filter(organization=organization).order_by('-created_date')
    comment_form = CommentForm()
    if request.method == 'POST' and not request.user.extendeddata.user_type == 'R':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.organization = organization
            comment.save()
            comment_form = CommentForm()
    context = {
        'Organitation': organization,
        'comments': comments,
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




