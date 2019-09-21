from django.shortcuts import redirect, render
from django.template.context_processors import csrf

from .forms import UploadImgForm, AddSkillForm, AddSkillFormSet, AddEducationFormSet
from .models import *


def client_main_page(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'  # test client icon

    return render(request=request,
                  template_name='client/client_main_page.html',
                  context=response)


def client_profile(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    return render(request=request,
                  template_name='client/client_profile.html',
                  context=response)


def client_edit_main(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'
    response['sex'] = Sex.objects.all()  # for a test

    if request.method == 'POST':
        print('client_edit_main - request.POST')

        client = Client(
            user_client=request.user,
            name=request.POST['client_first_name'].title(),  # вАленТиН -> Валентин
            lastname=request.POST['client_last_name'].title(),
            patronymic=request.POST['client_middle_name'].title(),
            sex=Sex(sex_word=request.POST['sex']).save(),
            date_born=request.POST['date_born'],  # mast be NOT ''
            citizenship=Citizenship(country_word=request.POST['citizenship']).save(),
            family_state=FamilyState(state_word=request.POST['family_state']).save(),
            children=Children(children_word=request.POST['children']).save(),
            country=Citizenship(country_word=request.POST['country']).save(),
            city=City(city_word=request.POST['city']).save(),
            street=request.POST['street'],
            house=request.POST['house'],
            flat=request.POST['flat'],
            telegram_link=request.POST['telegram_link'],
            skype=request.POST['skype_id'],
            email=request.POST['email'],
            link_linkedin=request.POST['link_linkedin'],
            state=State(state_word=request.POST['state']).save(),
        )
        client.save()  # TODO uncomment after 'UserLogin' module done!!!

        tel = request.POST.getlist('phone')
        for t in tel:
            Telephone(telephone_number=t).save()

        print(
            request.POST['client_first_name'].title(),
            request.POST['client_last_name'].title(),
            request.POST['client_middle_name'].title(),
            request.POST['sex'],
            request.POST['date_born'],
            request.POST['citizenship'],
            request.POST['family_state'],
            request.POST['children'],
            request.POST['country'],
            request.POST['city'],
            request.POST['street'],
            request.POST['house'],
            request.POST['flat'],
            request.POST.getlist('phone'),
            request.POST['telegram_link'],
            request.POST['skype_id'],
            request.POST['email'],
            request.POST['link_linkedin'],
            request.POST['state'],
        )

        print('client_edit_main - OK')

        return redirect(to='/client/profile')
    else:
        print('client_edit_main - request.GET')

    return render(request=request,
                  template_name='client/client_edit_main.html',
                  context=response)


def client_edit_skills(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        print("client_edit_skills - request.POST")

        skills_arr = request.POST.getlist('skill')
        print("skill: %s" % skills_arr)

        if any(skills_arr):
            for s in skills_arr:
                skill = Skills(skills=s)
                skill.save()  # TODO uncomment after 'UserLogin' module done!!!

                # ОБЪЕДИНЕНИЕ модуля Навыки с конкретным залогиненым клиентом !!!
                client = Client.objects.get(user_client=request.user)
                client.skills = skill
                client.save()
        else:
            print('No skills')

        # -------- test code ---------------------------
        form = AddSkillForm(request.POST)
        if form.is_valid():
            print('skill form.is_valid()')
            # form.save()
            # return redirect(to='/client/edit')

        # -------- Работающий test code с FormSet !!! ---------------------------
        form_set = AddSkillFormSet(request.POST)
        if form_set.is_valid():
            print('set is valid - OK')
            for f in form_set:
                # extract name='skill' from each form and save
                skill = f.cleaned_data.get('skills')
                if skill:
                    print('skill from form_set: %s' % skill)
                    Skills(skills=skill).save()  # TODO uncomment after 'UserLogin' module done!!!

        return redirect(to='/client/edit')
    else:
        print('client_edit_skills - request.GET')
        response['myformset'] = AddSkillFormSet()
        response['form'] = AddSkillForm

    return render(request=request,
                  template_name='client/client_edit_skills.html',
                  context=response)


def client_edit_photo(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        print('client_edit_photo - request.POST')

        form = UploadImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # TODO uncomment after 'UserLogin' module done!!!
            print('client save photo - OK')
            return redirect(to='/client/edit')
    else:
        print('client_edit_photo - request.GET')
        response['form'] = UploadImgForm()

    return render(request=request,
                  template_name='client/client_edit_photo.html',
                  context=response)


def client_edit_cv(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        cv = CV(
            position=request.POST['position'],
            time_job=TimeJob(time_job_word=request.POST['time_job']),  # .save(),
            salary=request.POST['salary'],
            type_salary=TypeSalary(type_word=request.POST['type_salary']),  # .save(),
        )
        cv.save()  # TODO uncomment after 'UserLogin' module done!!!
        print(
            request.POST['position'],
            request.POST['time_job'],
            request.POST['salary'],
            request.POST['type_salary']
        )

        return redirect(to='/client/edit')

    return render(request, 'client/client_edit_cv.html', response)


def client_edit_education(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        print("save_client_education - request.POST")

        education = Education(
            education=request.POST['education'],
            subject_area=request.POST['subject_area'],
            specialization=request.POST['specialization'],
            qualification=request.POST['qualification'],
            date_start=request.POST['date_start'],  # mast be NOT ''
            date_end=request.POST['date_end'],  # mast be NOT ''
            certificate=Certificate(
                img=request.POST['certificate_img'],
                link=request.POST['certificate_url']
            ).save(),
        )
        education.save()  # TODO uncomment after 'UserLogin' module done!!!

        print(
            request.POST['education'],
            request.POST['subject_area'],
            request.POST['specialization'],
            request.POST['qualification'],
            request.POST['date_start'],
            request.POST['date_end'],
            request.POST['certificate_img'],
            request.POST['certificate_url'],
        )

        return redirect('/client/edit')
    else:
        print('client_edit_education - request.GET')

    return render(request, 'client/client_edit_education.html', response)


def client_edit_experience(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        print("save_client_edit_experience - request POST")

        experiences = Experience(
            name=request.POST['experience_1'],
            # TODO Error:
            #  Direct assignment to the forward side of a many-to-many set is prohibited. Use sphere.set() instead.
            # sphere=Sphere(sphere_word=request.POST.getlist('experience_2')),
            position=request.POST['experience_3'],
            start_date=request.POST['exp_date_start'],
            end_date=request.POST['exp_date_end'],
            duties=request.POST['experience_4'],
        )
        experiences.save()  # TODO uncomment after 'UserLogin' module done!!!
        print(
            request.POST['experience_1'],
            request.POST.getlist('experience_2'),
            request.POST['experience_3'],
            request.POST['exp_date_start'],
            request.POST['exp_date_end'],
            request.POST['experience_4'],
        )

        return redirect('/client/edit')

    return render(request, 'client/client_edit_experience.html', response)


# ТЕСТОВАЯ ФОРМА
def form_education(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        print('-------------------------------------------------')
        form_set_edu = AddEducationFormSet(request.POST)
        print('form_set_edu: %s' % form_set_edu)
        if form_set_edu.is_valid():
            print('form_set_edu - OK')
            for f in form_set_edu:
                print('for f in: %s' % f)
                print("items: %s" % f.cleaned_data.items())

                edu = f.cleaned_data.get('education')
                print("edu: %s" % edu)
                s_a = f.cleaned_data.get('subject_area')
                print("s_a: %s" % s_a)
                sp = f.cleaned_data.get('specialization')
                print("sp: %s" % sp)
                qu = f.cleaned_data.get('qualification')
                print("qu: %s" % qu)
                ds = f.cleaned_data.get('date_start')
                print("ds: %s" % ds)
                de = f.cleaned_data.get('date_end')
                print("ds: %s" % de)

                Education(education=edu,
                          subject_area=s_a,
                          specialization=sp,
                          qualification=qu,
                          date_start=ds,
                          date_end=de,
                          ).save()

        return redirect(to='/client/edit/form_edu')
    else:
        response['edu_form'] = AddEducationFormSet()
    return render(request, 'client/form_edu.html', response)
