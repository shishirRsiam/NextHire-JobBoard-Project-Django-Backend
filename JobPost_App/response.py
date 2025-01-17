def get_resume_not_found_response():
    response = {
        'title': 'Resume not found.',
        'message': 'Go to your profile and Please upload your updated resume.',
    }
    return response


def get_job_details_button_name(request, job_post):
    can_apply = False
    button_name = 'Login to Apply'
    if request.user.is_authenticated:
        if job_post.user == request.user:
            button_name = 'You cannot apply for your own job.'
        elif job_post.job_applied.filter(user=request.user).exists():
            button_name = 'Already Applied'
        else:
            can_apply = True
            button_name = 'Apply Now'
    response = {
        'can_apply': can_apply,
        'button_name': button_name
    }
    return response

def get_job_job_applied_response(request, job_post):
    response = {
        'title': "Application Submitted!",
        'message': "Your application has been submitted successfully.",
    }
    return response


