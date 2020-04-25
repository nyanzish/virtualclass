from django.shortcuts import render, get_object_or_404
from .forms import Overviewform,Uploadform,Applyform,CommentForm
from django.shortcuts import redirect
from django.contrib import messages
#from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import Group, Permission 
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    UserProfile,
    Class_table,
    Subjects,
    Teacher_apply,
    Subjects_overview,
    Subscription,
    PaymentRecords,
    Upload_topics,
    Math,
    Physics,
    Chemistry,
    Biology,
    Geography,
    English,
    History,
    Islam,
    CRE,
    Agriculture,
    Computer,
    TechnicalDrawing,
    Art,
    French,
    German,
    Chinese,
    Luganda,
    GeneralPaper,
    Comment

)

# Create your views here.
def index(request):
    global lista_two            
    lista_one = []
    lista_two = []
    lista_three = []
    lista_four = []
    lista_all = []
    subjects = Subjects.objects.all()
    for value in subjects:
        lista_one.append(value.subject_image.url)
        lista_two.append(value.subject_name)
        lista_four.append(value.id)
        subject_o = Subjects_overview.objects.filter(subject = value.id).count() 
        lista_three.append(subject_o)
    # #print(lista_one)
    # print(lista_two)
    # print(lista_three)
    for x in range(len(lista_one)):
        all_variables = lista_one[x],lista_two[x],lista_three[x],lista_four[x]
        lista_all.append(all_variables)
    print(lista_all)

    context = {
        "lista_all": lista_all
        }
    return render(request,'index.html',context)

def post_detail(request):
    template_name = 'post_detail.html'
    post = get_object_or_404(Upload_topics, id=1)
    comments = post.comments.filter(active=True, parent__isnull=True)
    new_comment = None

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.topic = post
            # Save the comment to the database
            new_comment.save()
            return redirect('e_learning:post_detail')
    else:
        
        comment_form = CommentForm(initial={'name': request.user,'email':request.user.userprofile.email})

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def subject_get(request):
    sub_id = request.POST.get('get_subject')
    # ids=[]
    # for name in lista_two:
    #     sub_id = request.POST.get(f'{name}')
    #     ids.append(sub_id)
    #     print(sub_id,'iiiiiiiiiiiiiiiiiiiiiiiiiii')

    # print(ids)
    subject_details = Subjects_overview.objects.filter(subject = sub_id)
    subject_detailz = Subjects_overview.objects.filter(subject = sub_id).count()
    print(subject_detailz)
    # print(subject_details)
    #counter = sub_id
    #for x
    for sub_details in subject_details:
        print(sub_details)

    context = {
        'subject_details' : subject_details,
    }

    return render(request,'particular_.html',context)       

def my_profile(request):
    content = UserProfile.objects.get(user= request.user)
    print(content)
    context = {
        'content':content,
        }
    
    if request.method == "POST":
        content.firstname = request.POST.get('first_name')
        content.lastname = request.POST.get('last_name')
        content.location = request.POST.get('location')
        content.telephone = request.POST.get('contact')
        #if 'image' in request.FILES:
        if request.FILES:
            content.image = request.FILES.get('myfile')
        content.save()
        messages.success(request, 'Profile details updated.')
    return render(request,'my_profile.html',context)

def upload(request):
    
    #new_record=
    teacher_id=Teacher_apply.objects.get(user=request.user.id)
    print(teacher_id.id)
    subject=Teacher_apply.objects.filter(user=request.user.id)
    global class_id
    global subject_id
    class_id=request.POST.get('class_id')
    subject_id=request.POST.get('subject_id')
    print(class_id,subject_id,'2222222222222222')
    try:
        overview=Subjects_overview.objects.get(class_n__exact=class_id,subject__exact=subject_id,teacher=teacher_id.id)
        print(overview)

    except ObjectDoesNotExist:
        messages.info(request, "You do not have an overview for this particular class ,First create an overview.")
        return redirect('e_learning:overview')
     


    return redirect('e_learning:upload_to')

def name ():
    sub_results=Subjects.objects.get(id=subject_id)
    return sub_results.subject_name


def upload_to(request):
    
    teacher_id=Teacher_apply.objects.get(user=request.user.id)
    #print(teacher_id.id)
    print(class_id,subject_id,'88888888888888888')
    overview=Subjects_overview.objects.get(class_n__exact=class_id,subject__exact=subject_id,teacher=teacher_id)
    print(overview)
    global subject_one
    global subject_two
    subject=Teacher_apply.objects.filter(user=request.user.id)
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two
    #print(class_id,subject_id)
    # sub_results=Subjects.objects.get(id=subject_id)
    # subject_table=sub_results.subject_name
    topics=eval(name()).objects.filter(class_n__exact=class_id,subject__exact=subject_id)
    result= topics
    #print(topics)
    form = Uploadform(initial={'overview': overview.id,'teacher':teacher_id.id,'class_level':str(class_id),'subject':str(subject_id)})
    context= {
        'subject_two':subject_two,
        'subject_one':subject_one,
        'form':form,
        'result':result


    }
    if request.method=='POST':
        form = Uploadform(request.POST, request.FILES)
        
        form.fields['overview'].initial=overview.id
        form.fields['overview'].type='hidden'
        form.fields['teacher'].initial=teacher_id
        form.fields['teacher'].value=teacher_id
        form.fields['teacher'].type='hidden'
        form.fields['class_level'].initial=class_id
        form.fields['class_level'].value=class_id
        form.fields['class_level'].type='hidden'
        form.fields['subject'].initial=subject_id
        form.fields['class_level'].value=subject
        form.fields['subject'].type='hidden'
        
        topic = request.POST.get('topic')
        print(topic)
        save_form = form.save(commit=False)
        #overview_value = form.cleaned_data.get('overview')
        form.cleaned_data.get('overview')
        form.cleaned_data.get('teacher')
        form.cleaned_data.get('class_level')
        form.cleaned_data.get('subject')
        form.cleaned_data.get('topic')
        form.cleaned_data.get('content')

        teacher = request.POST.get('teacher')
        print(teacher)
        content =request.POST.get('content')
        print(content)
        class_level =request.POST.get('class_level')
        print(class_level)
        subject = request.POST.get('subject')
        print(subject)
        save_form.attached_file = request.FILES['attached_file']
        save_form.video= request.FILES['videos']
        attached_file = request.FILES['attached_file']
        print(attached_file)
        videos = request.FILES['videos']
        print(videos)
        save_form.save()
        # upload_topics=Upload_topics(
        #     overview=overview,
        #     teacher=teacher_id,
        #     class_level=class_level,
        #     subject=subject,
        #     topic=topic,
        #     content=content,
        #     attached_file=attached_file,
        #     videos= videos

        # )
        # upload_topics.save()
        print('done_saving')
        messages.info(request, "Topic successfully added")

    
    return render(request,'upload.html',context)


def overview(request):
    form = Overviewform()
    teacher_id=Teacher_apply.objects.get(user=request.user.id)
    print(teacher_id.id)
    print(class_id,subject_id,'999999999999999999')
    class_object= get_object_or_404(Class_table, id=int(class_id))
    subject_object= get_object_or_404(Subjects, id=int(subject_id))
    form = Overviewform(initial={'subject': subject_object.id,'teacher':teacher_id.id,'class_n':class_object.id})

    subject=Teacher_apply.objects.filter(user=request.user.id)
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two
    context= {
        'subject_two':subject_two,
        'subject_one':subject_one,
        'form':form

    }
    if request.method=='POST':
        if form.is_valid:
            form = Overviewform(request.POST, request.FILES)
            
            form.fields['subject'].initial=subject_object.id
            form.fields['class_n'].initial=class_object.id
            form.fields['teacher'].initial=teacher_id
            form.fields['subject'].value=subject_object.id
            form.fields['class_n'].value=class_object.id
            form.fields['teacher'].value=teacher_id.id
            #overview_value = form.cleaned_data.get('overview')
            save_form = form.save(commit=False)
            form.cleaned_data.get('over_view')
            form.cleaned_data.get('teacher')
            form.cleaned_data.get('class_n')
            form.cleaned_data.get('subject')
            form.cleaned_data.get('duration')
            form.cleaned_data.get('price')
            save_form.video= request.FILES['video']
            save_form.save()
            print('done_saving')
            messages.info(request, "Overview successfully added,now continue to the class")
            return redirect('e_learning:teacher_homepage')
            

    return render(request,'overview.html',context)

def upload_content(request):
    content=Content.objects.all().order_by('-id')
    form = Contentform()
    context = {"form": form,"content":content}
    if request.method == 'POST':
        form = Contentform(request.POST, request.FILES)
        if form.is_valid():
            topic = form.cleaned_data.get("topic")
            subject= form.cleaned_data.get("subject")
            class_level= form.cleaned_data.get("class_level")
            content= form.cleaned_data.get("content")
            notes = form.cleaned_data.get("notes")
            video= form.cleaned_data.get("video")
            content_form = Content(
                    user=request.user,
                    topic=topic,
                    subject=subject,
                    class_level=class_level,
                    content=content,
                    notes=notes,
                    video=video

                )
            content_form.save()
            #user_pr = form.save(commit=False)
            #user_pr.save()
            messages.info(request, "Topic was added.")
            return redirect('e_learning:view_new_uploaded_content')
            print("saved")
        else:
            messages.info(request, "something went wrong.")
            print('didnt save')
	    #return redirect('e_learning:upload_content')
	    
	#return render(request,'index.html', context)
    return render(request,'upload_content.html',context)

def pdf_view(request):
    try:
        return FileResponse(open('{{ object.notes.url }}', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def post_subject(request):

    form = Contentform()
    if request.method == 'POST':
        form = Contentform(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            #user_pr.image = request.FILES['image']
            #file_type = user_pr.image.url.split('.')[-1]
            #file_type = file_type.lower()
            #if file_type not in IMAGE_FILE_TYPES:
            #    return render(request, 'shop/error.html')
            user_pr.save()
            return render(request, 'shop/product2.html', {'user_pr': user_pr})
    context = {"form": form,}
    return render(request, 'shop/farmer.html', context)


def get_video(request,id):
    obj= Upload_topics.objects.get(id=id)
    print(obj)
    
    subject=Teacher_apply.objects.filter(user=request.user.id)
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two
    context= {
        'subject_two':subject_two,
        'subject_one':subject_one,
        'object':obj,
    }
    return render(request, 'video.html', context)

def get_document(request,id):
    obj= Content.objects.get(id=id)
    try:
        return FileResponse(open('{{ obj.notes.url }}', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
    context = {
        'object':obj,
    }
    return render(request, 'document.html', context)




class HomeView(ListView):
    model = Subjects_overview
    paginate_by = 12
    template_name = 'student_homepage.html'
    # Code block for GET request
    overview=Subjects_overview.objects.all()
    # for i in overview:
    #     print(i.price,i.teacher.user,i.class_n,i.subject,i.subject.subject_image)
    #     teacher_user=i.teacher.user
    #     profile=UserProfile.objects.filter(user=teacher_user)[0]
    #     print(profile.firstname, profile.lastname)
    
    def get(self, request, *args, **kwargs):
        context = locals()
        context['overview'] = self.overview
        
        
        return render(self.request,self.template_name, context,)

        #print('# Code block for GET request')

    def post(self, request):
        # Code block for POST request
        print('# Code block for POST request')

def student_homepage(request):
    student_subjects = Subscription.objects.filter(student=request.user.id)
    print(student_subjects)
    for my_course in student_subjects:
        print(my_course.subject)
    context={
        'student_subjects':student_subjects,
    }
    return render(request,'student_personal_homepage.html',context)

def student_personal_homepage(request):
	return render(request,'student_personal_homepage.html')

def apply_to_teach(request):
    print(request.user.userprofile,request.user.userprofile.id)
    applyform=Applyform()
    context = {
        'form':applyform

    }


    if request.method=='POST':
        form = Applyform(request.POST, request.FILES)
        form.fields['user'].initial= request.user
        form.fields['user_profile'].initial= request.user.userprofile
        schools_taught = request.POST.get('schools_taught')
        current_school = request.POST.get('current_school')
        level_of_teaching = request.POST.get('level_of_teaching')
        subject_one = request.POST.get('subject_one')
        subject_two = request.POST.get('subject_two')
        Brief_Self_description = request.POST.get('Brief_Self_description')
        apply_data = Teacher_apply(
            user=request.user,
            user_profile=request.user.userprofile,
            schools_taught=schools_taught,
            current_school=current_school,
            level_of_teaching=level_of_teaching,
            subject_one=subject_one,
            subject_two=subject_two,
            Brief_Self_description =Brief_Self_description

        )
        apply_data.save()

        messages.info(request, "Your application has succefully submitted for review")
            



    return render(request,'apply_to_teach.html',context)

def subject_topic(request):
	return render(request,'subject_topic.html')

def subject_overview(request,slug):
    overview=Subjects_overview.objects.get(id=slug)
    recomend=Subjects_overview.objects.filter(class_n=overview.class_n)
    for i in recomend:
        print(i.price,i.teacher.user,i.class_n,i.subject,i.subject.subject_image)
    context ={
    'overview':overview,
    'recomend':recomend
    }
    return render(request,'subject_overview.html',context)
    

def teacher_homepage(request):
    subject=Teacher_apply.objects.filter(user=request.user.id)
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two
    context={
        'subject_two':subject_two,
        'subject_one':subject_one
    }
    return render(request,'teacher_homepage.html',context)

def about(request):
	return render(request,'about.html')

def error(request):
	return render(request,'error.html')

def teacher_new_base(request):
	return render(request,'teacher_new_base.html')

def view_my_students(request):
    subject=Teacher_apply.objects.filter(user=request.user.id)
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two

    my_teacher_id=Teacher_apply.objects.get(user= request.user.id)
    current_teacher = my_teacher_id.id
    teacher_students=Subscription.objects.filter(teacher=current_teacher)
    for my_studnt in teacher_students:
        print(my_studnt,my_studnt.student.id)
    # student_names = UserProfile.objects.filter(user = my_studnt.student.id)
    # for names in student_names:
    #     print(names.firstname)
    context= {
        'subject_two':subject_two,
        'subject_one':subject_one,
        'teacher_students':teacher_students,
    }
    return render(request,'view_my_students.html',context)

def my_uploaded(request,slug):
    uploaded=Subjects_overview.objects.get(id=slug)
    print(slug)
    Subjects_overview.objects.get(id=slug).delete()
    messages.info(request, "Overview successfully deleted")
    #########Delete item from here##############
    my_teacher_id=Teacher_apply.objects.get(user= request.user.id)
    current_teacher = my_teacher_id.id
    model = Subjects_overview
    teacher_uploaded_subject=Subjects_overview.objects.filter(teacher=current_teacher)
    print(teacher_uploaded_subject)
    for a in teacher_uploaded_subject:
        print(a.subject.id)
    #item6=Item.objects.filter(category=obj.category)
    context={
        'uploaded':uploaded, 
        'teacher_uploaded_subject':teacher_uploaded_subject,
    }
    return render(request,'teacher_uploaded_subjects.html',context)

def edit_my_uploaded(request,slug):
    subject=Teacher_apply.objects.filter(user=request.user.id)
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two
    uploaded=Subjects_overview.objects.get(id=slug)
    print(slug)
    print(uploaded.subject.id)
    print(uploaded.class_n.id)
    #item6=Item.objects.filter(category=obj.category)
    edit_uploaded=Upload_topics.objects.filter(subject__exact=uploaded.subject.id,class_level__exact=uploaded.class_n.id)
    print(edit_uploaded)
    subject_name = uploaded.subject
    context={
        'uploaded':uploaded,
        'edit_uploaded':edit_uploaded, 
        'subject_name':subject_name,
        'subject_two':subject_two,
        'subject_one':subject_one
    }
    return render(request,'teacher_edit_subject_topics.html',context)

def topic_delete(request,slug):
    Upload_topics.objects.get(id=slug).delete()
    # context={
        
    # }
    messages.info(request, "Topic successfully deleted")
    return redirect('e_learning:my_uploaded_subjects')


def edit_my_topic(request,slug):
    form = Uploadform()
    subject=Teacher_apply.objects.filter(user=request.user.id)
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two
    # uploaded=Subjects_overview.objects.get(id=slug)
    # print(slug)
    #print(uploaded.subject.id)
    #item6=Item.objects.filter(category=obj.category)
    edit_uploaded=Upload_topics.objects.get(id=slug)
    print(edit_uploaded,edit_uploaded.topic,'--------------')
    form = Uploadform(initial={'overview': edit_uploaded.overview,'topic':edit_uploaded.topic,'teacher':edit_uploaded.teacher,'class_level':edit_uploaded.class_level,'subject':edit_uploaded.subject,'content':edit_uploaded.content,'attached_file':edit_uploaded.attached_file,'videos':edit_uploaded.videos})

    if request.method=='POST':
        form = Uploadform(request.POST, request.FILES)
        # edit_uploaded.overview = eval(request.POST.get('overview'))

        # edit_uploaded.teacher = request.POST.get('teacher')
        # print(teacher)
        edit_uploaded.content =request.POST.get('content')
        #print(content)
        edit_uploaded.class_level =request.POST.get('class_level')
        #print(class_level)
        # edit_uploaded.subject = request.POST.get('subject')
        # print(subject)
        edit_uploaded.attached_file = request.FILES.get('attached_file')
        edit_uploaded.videos= request.FILES.get('videos')
        #attached_file = request.FILES['attached_file']
        # print(attached_file)
        # videos = request.FILES['videos']
        # print(videos)
        edit_uploaded.save()
        print('done_saving')
        messages.info(request, "Topic successfully updated")
        
        
    context={
        'edit_uploaded':edit_uploaded,
        'subject_two':subject_two,
        'subject_one':subject_one,
        'form':form
    }
    return render(request,'teacher_edit_subject_individual_topics.html',context)

def teacher_uploaded_subjects(request):
    subject=Teacher_apply.objects.filter(user=request.user.id)
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two

    my_teacher_id=Teacher_apply.objects.get(user= request.user.id)
    current_teacher = my_teacher_id.id
    model = Subjects_overview
    teacher_uploaded_subject=Subjects_overview.objects.filter(teacher=current_teacher)
    print(teacher_uploaded_subject)
    for a in teacher_uploaded_subject:
        print(a.subject.id)

    context= {
        'subject_two':subject_two,
        'subject_one':subject_one,
        'teacher_uploaded_subject':teacher_uploaded_subject,
    }
    return render(request,'teacher_uploaded_subjects.html',context)

def transaction_details(request):
    subject=Teacher_apply.objects.filter(user=request.user.id)
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two
    context= {
        'subject_two':subject_two,
        'subject_one':subject_one,
    }
    return render(request,'transaction_details.html',context)

def FAQ(request):
	return render(request,'FAQ.html')

# def my_profile(request):
# 	return render(request,'my_profile.html')

def payment_details(request):
	return render(request,'student_payment_details.html')

def switch_to_teacher_page(request):
    subject=Teacher_apply.objects.filter(user=request.user.id)
    subjects=[]
    for sub in subject:
        subjects.append(sub.subject_one)
        subjects.append(sub.subject_two)

    context= {
        'subjects':subjects,
    }
    return render(request,'teacher_homepage.html',context)

def view_new_uploaded_content(request):
    content=Content.objects.all().order_by('-id')
    subject=Teacher_apply.objects.filter(user=request.user.id)
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two
    context= {
        'subject_two':subject_two,
        'subject_one':subject_one,
        "content":content
        }
    return render(request,'view_new_uploaded_content.html',context)


# class MyFormView(View):
#     form_class = Contentform
#     initial = {'key': 'value'}
#     template_name = 'index.html'

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return HttpResponseRedirect('/')

#         return render(request, self.template_name, {'form': form})


def classes(request):
    subject=Teacher_apply.objects.filter(user=request.user.id)
    class_s=Class_table.objects.all()
    subjects=[]
    for sub in subject:
        subjects.append(sub.subject_one)
        subjects.append(sub.subject_two)
        print(sub.subject_one,sub.subject_two)
    print(subjects)
    #print(subject[0].subject_one.id,subject[0].subject_two.id)
    subject_o=subject[0]
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two
    subject_id=Subjects.objects.get(subject_name=subject[0].subject_one)
    
    #print(subject_id.id)
    subject_id = subject_id.id
    # for i in class_s:
    #     print(i.id)
    context = {
        'subject_two':subject_two,
        'subject':subject,
        'subjects':subjects,
        'subject_one':subject_one,
        'subject_id':subject_id,
        'subject_o':subject_o,
        'class_s':class_s
    }
    #print(class_s.value)
    return render(request,'classes.html',context)

def classes_base(request):
    subject=Teacher_apply.objects.filter(user=request.user.id)
    class_s=Class_table.objects.all()
    
    subjects=[]
    for sub in subject:
        subjects.append(sub.subject_one)
        subjects.append(sub.subject_two)

    print(subjects)
    #print(subject[0].subject_one.id,subject[0].subject_two.id)
    subject_o=subject[0]
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two
    subject_id=Subjects.objects.get(subject_name=subject[0].subject_one)
    #print(subject_id.id)
    subject_id = subject_id.id
    for i in class_s:
        print(i.id)
    context = {
        'subject_two':subject_two,
        'subject':subject,
        'subjects':subjects,
        'subject_one':subject_one,
        'subject_id':subject_id,
        'subject_o':subject_o,
        'class_s':class_s
    }
    #print(class_s.value)
    return render(request,'teacher_base.html',context)

def classes2(request):
    subject=Teacher_apply.objects.filter(user=request.user.id)
    class_s=Class_table.objects.all()
    
    #print(subject[0].subject_one.id,subject[0].subject_two.id)
    subject_o=subject[0]
    subject_one=subject[0].subject_one
    subject_two=subject[0].subject_two
    subject_id=Subjects.objects.get(subject_name=subject[0].subject_two)
    print(subject_id.id,"***********")
    subject_id = subject_id.id
    print(class_s)
    context = {
        'subject_two':subject_two,
        'subject_one':subject_one,
        'subject_id':subject_id,
        'subject_o':subject_o,
        'class_s':class_s
    }

    return render(request,'classes.html',context)

def push(request,slug):
    print(slug)
    # if request.method=='POST':
    #     subject_id=request.POST.get("subject_id")
    #     print(subject_id)

    context = {
       
    }
    return render(request,'classes.html',context)