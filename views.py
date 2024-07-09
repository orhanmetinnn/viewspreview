from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import requests
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm, NewsletterSubscriptionForm
from .models import BlogPost

def blog_list(request):
    blog_posts_about = BlogPost.objects.filter(category='about')
    blog_posts_hr = BlogPost.objects.filter(category='hr')
    blog_posts_training = BlogPost.objects.filter(category='training')
    blog_posts_software = BlogPost.objects.filter(category='software')

    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return render(request, 'html/index.html', {
                'form': form,
                'error_message': 'Bu e-posta adresi zaten mevcut. Lütfen başka bir adres deneyin.',
                'blog_posts_about': blog_posts_about,
                'blog_posts_hr': blog_posts_hr,
                'blog_posts_training': blog_posts_training,
                'blog_posts_software': blog_posts_software
            })
    else:
        form = NewsletterSubscriptionForm()

    context = {
        'form': form,
        'blog_posts_about': blog_posts_about,
        'blog_posts_hr': blog_posts_hr,
        'blog_posts_training': blog_posts_training,
        'blog_posts_software': blog_posts_software
    }

    return render(request, 'html/index.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    blog_posts_about = BlogPost.objects.filter(category='about')
    blog_posts_hr = BlogPost.objects.filter(category='hr')
    blog_posts_training = BlogPost.objects.filter(category='training')
    blog_posts_software = BlogPost.objects.filter(category='software')

    context = {
        'post': post,
        'blog_posts_about': blog_posts_about,
        'blog_posts_hr': blog_posts_hr,
        'blog_posts_training': blog_posts_training,
        'blog_posts_software': blog_posts_software,
    }
    return render(request, 'html/iktree.html', context)


def iletisim(request):
    blog_posts_about = BlogPost.objects.filter(category='about')
    blog_posts_hr = BlogPost.objects.filter(category='hr')
    blog_posts_training = BlogPost.objects.filter(category='training')
    blog_posts_software = BlogPost.objects.filter(category='software')

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        newsletter_form = NewsletterSubscriptionForm(request.POST)
        captcha_response = request.POST.get('recaptcha_response')

        if captcha_response:
            payload = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': captcha_response
            }
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
            result = response.json()

            if result.get('success'):
                if 'newsletter_submit' in request.POST:
                    if newsletter_form.is_valid():
                        newsletter_form.save()
                        success_message = 'Aboneliğiniz başarıyla tamamlandı!'
                        contact_form = ContactForm()
                        return render(request, 'html/iletisimform.html', {
                            'contact_form': contact_form,
                            'newsletter_form': newsletter_form,
                            'success_message': success_message,
                            'blog_posts_about': blog_posts_about,
                            'blog_posts_hr': blog_posts_hr,
                            'blog_posts_training': blog_posts_training,
                            'blog_posts_software': blog_posts_software
                        })
                    else:
                        error_message = 'Bu e-posta adresi zaten mevcut. Lütfen başka bir adres deneyin.'
                        return render(request, 'html/iletisimform.html', {
                            'contact_form': contact_form,
                            'newsletter_form': newsletter_form,
                            'error_message': error_message,
                            'blog_posts_about': blog_posts_about,
                            'blog_posts_hr': blog_posts_hr,
                            'blog_posts_training': blog_posts_training,
                            'blog_posts_software': blog_posts_software
                        })
                elif 'contact_submit' in request.POST:
                    if contact_form.is_valid():
                        contact = contact_form.save()
                        send_mail(
                            subject=f"New Contact Form Submission: {contact.subject}",
                            message=contact.message,
                            from_email=contact.email,
                            recipient_list=[settings.EMAIL_RECEIVER],
                            fail_silently=False,
                        )
                        success_message = 'Formunuz başarıyla gönderildi!'
                        contact_form = ContactForm()
                        return render(request, 'html/iletisimform.html', {
                            'contact_form': contact_form,
                            'newsletter_form': newsletter_form,
                            'success_message': success_message,
                            'blog_posts_about': blog_posts_about,
                            'blog_posts_hr': blog_posts_hr,
                            'blog_posts_training': blog_posts_training,
                            'blog_posts_software': blog_posts_software
                        })
                    else:
                        error_message = 'Formunuz gönderilirken bir hata oluştu.'
                        return render(request, 'html/iletisimform.html', {
                            'contact_form': contact_form,
                            'newsletter_form': newsletter_form,
                            'error_message': error_message,
                            'blog_posts_about': blog_posts_about,
                            'blog_posts_hr': blog_posts_hr,
                            'blog_posts_training': blog_posts_training,
                            'blog_posts_software': blog_posts_software
                        })
            else:
                error_message = 'CAPTCHA doğrulaması başarısız. Lütfen tekrar deneyin.'
                return render(request, 'html/iletisimform.html', {
                    'contact_form': contact_form,
                    'newsletter_form': newsletter_form,
                    'error_message': error_message,
                    'blog_posts_about': blog_posts_about,
                    'blog_posts_hr': blog_posts_hr,
                    'blog_posts_training': blog_posts_training,
                    'blog_posts_software': blog_posts_software
                })
        else:
            error_message = 'CAPTCHA yanıtı bulunamadı. Lütfen tekrar deneyin.'
            return render(request, 'html/iletisimform.html', {
                'contact_form': contact_form,
                'newsletter_form': newsletter_form,
                'error_message': error_message,
                'blog_posts_about': blog_posts_about,
                'blog_posts_hr': blog_posts_hr,
                'blog_posts_training': blog_posts_training,
                'blog_posts_software': blog_posts_software
            })
    else:
        contact_form = ContactForm()
        newsletter_form = NewsletterSubscriptionForm()

    context = {
        'contact_form': contact_form,
        'newsletter_form': newsletter_form,
        'blog_posts_about': blog_posts_about,
        'blog_posts_hr': blog_posts_hr,
        'blog_posts_training': blog_posts_training,
        'blog_posts_software': blog_posts_software
    }

    return render(request, 'html/iletisimform.html', context)

