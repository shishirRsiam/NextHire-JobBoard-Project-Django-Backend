from .JobPost_App_Import import *
from .models import JobPost, Applied
from .serializers import JobPostSerializer, ApplySerializer

class JobPostApiViewSet(APIView):
    def post(self, request):
        serializer = JobPostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            post.category.set(request.data['category'])  
            post.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    # Update an existing job post
    def put(self, request, pk=None):
        job_post = get_object_or_404(JobPost, pk=pk, user=request.user) 
        serializer = JobPostSerializer(job_post, data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            post.category.set(request.data.get('category', []))
            post.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    # Partial update of an existing job post
    def patch(self, request, pk=None):
        job_post = get_object_or_404(JobPost, pk=pk, user=request.user)
        serializer = JobPostSerializer(job_post, data=request.data, partial=True)
        if serializer.is_valid():
            post = serializer.save()
            if 'category' in request.data:
                post.category.set(request.data.get('category', []))
            post.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def get(self, request, *args, **kwargs):
        job_post_id = kwargs.get('pk')
        if job_post_id:
            try:
                job_post = JobPost.objects.get(id=job_post_id)

                is_delete = request.query_params.get('is_delete', None)
                if is_delete:
                    response = {'message': f"'{job_post.title}' post deleted successfully."}
                    job_post.delete()
                    return Response(response, status=200)
                

                is_application = request.query_params.get('is_application', None)
                if is_application:
                    print('()'*30)
                    print(is_application)
                    all_application = job_post.job_applied.all()
                    all_application_serializer = ApplySerializer(all_application, many=True)
                    job_post_serializer = JobPostSerializer(job_post)
                    response = {
                        'application': all_application_serializer.data,
                        'job_post': job_post_serializer.data,
                    }
                    return Response(response)
                    # return Response(get_user_job_application_response(request, job_post))
                
                serializer = JobPostSerializer(job_post)
                response = {
                    'total_applicants': job_post.job_applied.all().count(),
                    'job_post': serializer.data,
                }
                return Response(response)
            
            except JobPost.DoesNotExist:
                return Response({"error": "Job post not found."}, status=404)
        
        job_posts = JobPost.objects.all()

        search_by_applied = request.query_params.get('searchByApplied', None)
        search_by_profile = request.query_params.get('searchByProfile', None)
        # if search_by_applied:
        #     job_posts = job_posts.filter(applied__user=request.user)


        if search_by_applied:
            if search_by_applied == "Applied":
                job_posts = JobPost.objects.filter(applied__user=request.user)
            elif search_by_applied == "Not Applied":
                job_posts = JobPost.objects.exclude(applied__user=request.user)

        job_posts = job_posts.order_by('-id')
        serializer = JobPostSerializer(job_posts, many=True)
        return Response({
            "authenticated": request.user.is_authenticated,
            "job_posts": serializer.data
        })
    
class JobApplyApiView(APIView):
    def post(self, request, *args, **kwargs):
        job_post_id = kwargs.get('id')
        if job_post_id:
            try:
                job_post = JobPost.objects.get(id=job_post_id)
            except JobPost.DoesNotExist:
                return Response({"error": "Job post not found."}, status=404)
            
        if request.data['is_apply']:
            print('()'*30)
            print(request.data)
            resume = request.user.userprofile.resume
            if not resume:
                response = get_resume_not_found_response()
                return Response(response, status=404)
            
            description = request.data['description']
            Applied.objects.create(user=request.user, job=job_post, resume=resume, description=description)
            response = get_job_job_applied_response(request, job_post)
        else: response = get_job_details_button_name(request, job_post)
        return Response(response)


class SuggestionApiView(APIView):
    def get(self, request, *args, **kwargs):
        job_posts = JobPost.objects.exclude(applied__user=request.user).order_by('-id')[:6]
        serializer = JobPostSerializer(job_posts, many=True)
        return Response(serializer.data)