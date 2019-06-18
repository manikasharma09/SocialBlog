from django.shortcuts import render,redirect ,HttpResponse,HttpResponseRedirect
from accounts.forms import EditProfileForm,UserCreationForm 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.utils.html import format_html
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from accounts.forms import HomeForm
from accounts.models import Post
from google.cloud import translate
from django.http import HttpResponse
from django.db.models import Q
import os
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.getcwd()+"/translate.json"  #Getting language translation data from json file
translate_client = translate.Client()  # Setting up Client for Translation
def register(request):
	if request.method=="POST":
		form=UserCreationForm(request.POST)
		if form.is_valid():
			#update_session_auth_hash(request,form.user)
			form.save()
		return redirect('/account')
	else:
		form=UserCreationForm()
	args={'form':form}
	return render(request,'accounts/register1.html',args) #Changed name from reg_html to register1


def view_profile(request):
    posts_list=Post.objects.all().order_by('-created')
    post_list = posts_list.filter(user=request.user)
    args = {'user':request.user,'posts':post_list}
    return render(request,'accounts/profile.html',args)


def edit_profile(request):
    if request.method=="POST":
        form=EditProfileForm(request.POST,instance=request.user)
        if form.is_valid():
        	form.save()
        	return redirect('/account/profile')	
    else:
        form=EditProfileForm(instance=request.user)
        args={'form': form}
        return render(request,'accounts/edit_profile.html',args)


   	
def change_password(request):
    if request.method=="POST":
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
        	form.save()
        	return redirect('/account/profile')	
        else:
            return redirect('/account/change-password')	
    else:
        form=PasswordChangeForm(user=request.user)
        args={'form': form}
        return render(request,'accounts/change_password.html',args)



class HomeView(TemplateView):
    template_name='accounts/home.html'

    def get(self,request):
        #form=HomeForm()
        posts_list=Post.objects.all().order_by('-created')
        user=User.objects.all().order_by('-created')
        page = request.GET.get('page', 1)
        paginator = Paginator(posts_list, 10)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        args={'posts':posts ,'users':user }
        return render(request,self.template_name,args)

    def post(self,request):
        # form =HomeForm(request.POST)    
        # if form.is_valid():
        #     post=form.save(commit=False)
        #     post.user=request.user
        #     post.save()
        #     text=form.cleaned_data['post']
        #     form =HomeForm()
        #     return redirect('/')
        # args={'form':form ,'text':text }
        text=request.POST.get('q')
        translated_description = translate_client.translate(text,target_language='hi')
        translated_post = translated_description['translatedText']
        # text=text.replace('<p>', '')
        # text=text.replace('</p>',' ')
        print(text)
        #text=text.replace('<p>', '')
        #text=text.replace('</p>',' ')
        #print(len(request.FILES))
        if(request.FILES['submission_file']!=0):
            obj,notif=Post.objects.get_or_create(post=text,translated_post=translated_post, user=request.user, postImg=request.FILES['submission_file'])

        elif(request.FILES['video_file']!=0):
            obj,notif=Post.objects.get_or_create(post=text,translated_post=translated_post, user=request.user, postVid=request.FILES['video_file'])

        else:
            obj,notif=Post.objects.get_or_create(post=text,translated_post=translated_post, user=request.user)
        #print(text)
        #print(request.POST)
        #print(request.user)
        #user=request.user
        
        if notif is True:
            obj.save()
        return HttpResponseRedirect('/')  



       
# def edit(request):
#     if(request.method=="POST"):
#         #print(request.POST.get("text")[3:((len(request.POST.get("text")))-4)])
#         text=request.POST.get('q')
#         text=text.replace('<p>', '')
#         text=text.replace('</p>',' ')
#         print(text)
#         print(request.POST)
#     return render(request, 'accounts/editor.html')

def STT(request):
    import speech_recognition as sr 
    mic_name = "Speakers / Headphones (Realtek"
    #Sample rate is how often values are recorded 
    sample_rate = 48000
    #Chunk is like a buffer. It stores 2048 samples (bytes of data) 
    #here.  
    #it is advisable to use powers of 2 such as 1024 or 2048 
    chunk_size = 2048
    #Initialize the recognizer 
    r = sr.Recognizer() 
      
    #generate a list of all audio cards/microphones 
    mic_list = sr.Microphone.list_microphone_names() 
    device_id=0
    #the following loop aims to set the device ID of the mic that 
    #we specifically want to use to avoid ambiguity. 
    for i, microphone_name in enumerate(mic_list):
        #print(microphone_name, i)
        if microphone_name == mic_name: 
            device_id = i
            #print(i)
      
    #use the microphone as source for input. Here, we also specify  
    #which device ID to specifically look for incase the microphone  
    #is not working, an error will pop up saying "device_id undefined" 
    with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                            chunk_size = chunk_size) as source: 
        #wait for a second to let the recognizer adjust the  
        #energy threshold based on the surrounding noise level 
        r.adjust_for_ambient_noise(source) 
        print ("Say Something....")
        #listens for the user's input 
        audio = r.listen(source) 
              
        try: 
            text = r.recognize_google(audio) 
            print ("you said: " + text )
            translated_description = translate_client.translate(text,target_language='hi')
            translated_post = translated_description['translatedText']
            obj,notif=Post.objects.get_or_create(post=text, translated_post=translated_post ,user=request.user)
            if notif is True:
                obj.save()
          
        #error occurs when google could not understand what was said 
          
        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio") 
          
        except sr.RequestError as e: 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return HttpResponseRedirect('/')
