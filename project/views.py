import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rapidfuzz import process

FAQS = [
    ("hello", "Hello! How can I help you today?"),
    ("hi", "Hi there! How can I assist you?"),
    ("how do I apply", "To apply for a job, click the <a href='/jobs/' class='chatbot-link'>Browse Job</a> button and then the 'Apply' button."),
    ("how to apply", "To apply for a job, click the <a href='/jobs/' class='chatbot-link'>Browse Job</a> button and then the 'Apply' button."),
    ("apply for a job", "To apply for a job, click the <a href='/jobs/' class='chatbot-link'>Browse Job</a> button and then the 'Apply' button."),
    ("application process", "To apply for a job, click the <a href='/jobs/' class='chatbot-link'>Browse Job</a> button and then the 'Apply' button."),
    ("how to save a job", "Click the <span class='chatbot-link' style='color:#007bff;font-weight:bold;'>heart icon</span> on any job card to save it to your wishlist."),
    ("how do I save a job", "Click the <span class='chatbot-link' style='color:#007bff;font-weight:bold;'>heart icon</span> on any job card to save it to your wishlist."),
    ("how do I see my saved jobs", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> to see your wishlist of saved jobs.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>see your wishlist now?</a>"),
    ("where are my saved jobs", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> to see your wishlist of saved jobs.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>see your wishlist now?</a>"),
    ("show my wishlist", "You can view your wishlist on your <a href='/accounts/profile/' class='chatbot-link'>profile page</a>.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>see your wishlist now?</a>"),
    ("view my wishlist", "You can view your wishlist on your <a href='/accounts/profile/' class='chatbot-link'>profile page</a>.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>see your wishlist now?</a>"),
    ("see saved jobs", "Check your saved jobs on your <a href='/accounts/profile/' class='chatbot-link'>profile page</a>.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>see your wishlist now?</a>"),
    ("my saved jobs", "Your saved jobs are listed on your <a href='/accounts/profile/' class='chatbot-link'>profile page</a>.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>see your wishlist now?</a>"),
    ("wishlist", "You can find your wishlist on your <a href='/accounts/profile/' class='chatbot-link'>profile page</a>.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>see your wishlist now?</a>"),
    ("how do I contact support", "You can contact us using the <a href='/contact/' class='chatbot-link'>contact form</a> on the Contact page."),
    ("contact", "You can contact us using the <a href='/contact/' class='chatbot-link'>contact form</a> on the Contact page."),
    ("reset password", "Click <a href='/accounts/password_reset/' class='chatbot-link'>Forgot password?</a> on the login page to reset your password."),
    ("forgot password", "Click <a href='/accounts/password_reset/' class='chatbot-link'>Forgot password?</a> on the login page to reset your password."),
    ("change password", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile settings</a> to change your password."),
    ("edit profile", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> and click 'Edit Profile' to update your information.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>edit your profile now?</a>"),
    ("update profile", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> and click 'Edit Profile' to update your information.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>edit your profile now?</a>"),
    ("change my profile", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> and click 'Edit Profile' to update your information.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>edit your profile now?</a>"),
    ("edit my profile", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> and click 'Edit Profile' to update your information.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>edit your profile now?</a>"),
    ("profile settings", "You can update your information in your <a href='/accounts/profile/' class='chatbot-link'>profile page</a>.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>edit your profile now?</a>"),
    ("update my info", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> and click 'Edit Profile' to update your information.<br>Would you like to <a href='/accounts/profile/' class='chatbot-link'>edit your profile now?</a>"),
    ("what is this site", "This is a job board where you can <a href='/jobs/' class='chatbot-link'>search</a>, save, and apply for jobs easily!"),
    ("what jobs are available", "Browse the <a href='/jobs/' class='chatbot-link'>job listings page</a> to see all available jobs."),
    ("how do I post a job", "If you are an employer, go to your <a href='/job/company/dashboard/' class='chatbot-link'>dashboard</a> and click 'Post a Job'."),
    ("how to post a job", "If you are an employer, go to your <a href='/job/company/dashboard/' class='chatbot-link'>dashboard</a> and click 'Post a Job'."),
    ("how do I delete my account", "Please <a href='/contact/' class='chatbot-link'>contact support</a> to request account deletion."),
    ("bye", "Goodbye! If you have more questions, just ask."),
    ("view my profile", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> to view your information."),
    ("profile page", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> to view your information."),
    ("show my profile", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> to view your information."),
    ("see my profile", "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> to view your information."),
]

@csrf_exempt
@require_POST
def chatbot_ask(request):
    data = json.loads(request.body.decode('utf-8'))
    user_message = data.get('message', '').lower()

    # Keyword filtering for key pages/actions
    if 'profile' in user_message:
        return JsonResponse({'reply': "Go to your <a href='/accounts/profile/' class='chatbot-link'>profile page</a> to view your information."})
    if 'job' in user_message and ('list' in user_message or 'browse' in user_message):
        return JsonResponse({'reply': "Browse all jobs on the <a href='/jobs/' class='chatbot-link'>job listings page</a>."})
    if 'saved' in user_message or 'wishlist' in user_message:
        return JsonResponse({'reply': "See your saved jobs on your <a href='/accounts/profile/' class='chatbot-link'>profile page</a>."})
    if 'contact' in user_message or 'support' in user_message:
        return JsonResponse({'reply': "You can contact us using the <a href='/contact/' class='chatbot-link'>contact form</a>."})
    if 'home' in user_message or 'main page' in user_message:
        return JsonResponse({'reply': "Return to the <a href='/' class='chatbot-link'>home page</a>."})
    if 'login' in user_message or 'sign in' in user_message:
        return JsonResponse({'reply': "You can <a href='/accounts/login/' class='chatbot-link'>sign in here</a>."})
    if 'logout' in user_message or 'sign out' in user_message:
        return JsonResponse({'reply': "You can <a href='/accounts/logout/' class='chatbot-link'>sign out here</a>."})
    if 'register' in user_message or 'sign up' in user_message:
        return JsonResponse({'reply': "You can <a href='/accounts/signup/' class='chatbot-link'>register here</a>."})
    if 'post' in user_message and 'job' in user_message:
        return JsonResponse({'reply': "To post a job, go to <a href='/jobs/add' class='chatbot-link'>add a job</a>."})
    if 'edit' in user_message and 'profile' in user_message:
        return JsonResponse({'reply': "Edit your profile on your <a href='/accounts/profile/' class='chatbot-link'>profile page</a>."})

    # Fuzzy matching fallback
    questions = [q for q, a in FAQS]
    match, score, idx = process.extractOne(user_message, questions)
    if score > 70:
        return JsonResponse({'reply': FAQS[idx][1]})
    return JsonResponse({'reply': "I'm not sure about that. Please try rephrasing your question or <a href='/contact/' class='chatbot-link'>contact support</a>!"}) 