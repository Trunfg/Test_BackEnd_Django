from datetime import datetime
# from pyexpat.errors import messages
import bcrypt
from django.contrib import messages
from urllib import request
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from .serializers import taskSerializer, UserSerializer
from app_2.models import User, Task

class taskView(APIView):
    def get(self, request, format=None):
        id = request.session.get('id')
        user = None
        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                # Xử lý trường hợp nếu không tìm thấy người dùng với id_user cung cấp
                pass
        arr = []
        tasks = Task.objects.all()
        for task in tasks:
            users_in_task = task.users.all()
            users_tasks = ''
            for i in users_in_task:
                users_tasks = i.name if not users_tasks else users_tasks + ", " + i.name
            arr.append({
                    'users_tasks': users_tasks,
                    'id_task': task.id_task,
                    'name_task': task.name_task,
                    'description_task': task.description_task,
                    'date_create_task': task.date_create_task,
                })
        return render(request, 'task.html', {'user':user, 'arr':arr})
    def post(self, request, format=None):
        tasks = Task.objects.all()
        date = datetime.now().date()
        data={
            'name_task': request.POST.get('name_task'),
            'description_task': request.POST.get('description_task'),
            'date_create_task':date,
        }
        serializer = taskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Tạo công việc thành công.')
            return redirect('task')
        messages.success(request, 'Lỗi dữ liệu.')
        return redirect('task')

class DetailView(APIView):
    def get_task(self, id_task):
        try:
            return Task.objects.get(id_task=id_task)
        except Task.DoesNotExist:
            return None
    def get(self, request, pk, format=None):
        task = self.get_task(pk)
        id = request.session.get('id')
        user = None
        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                # Xử lý trường hợp nếu không tìm thấy người dùng với id_user cung cấp
                pass
        return render(request, 'detail_task.html', {'task':task, 'user':user})
    def post(self, request, pk, format=None):
        task = self.get_task(pk)
        task.name_task = request.POST.get('name_task')
        task.description_task = request.POST.get('description_task')
        date = datetime.strptime(request.POST.get('date_create_task'), '%Y-%m-%d')
        date_now = datetime.now().date()
        if date.date() > date_now:
            messages.error(request, 'Ngày không hợp lệ.')
            return redirect('detail_task', pk=pk)
        task.date_create_task = date
        if not (task.name_task and task.description_task and task.date_create_task):
            messages.error(request, 'Nhập đầy đủ thông tin.')
            return redirect('detail_task', pk=pk)
        task.save()
        tasks = Task.objects.all()
        messages.success(request, 'Sửa công việc thành công.')
        return redirect('task')
    
class deletecheckedView(APIView):
    def post(self, request, format=None):
        selected_task_ids = request.POST.get('selected_tasks').split(',')
        if selected_task_ids==['']:
            messages.success(request, 'Chưa chọn công việc nào.')
            return redirect('task')
        for id in selected_task_ids:
            task = Task.objects.get(id_task=id)
            task.delete()
        messages.success(request, 'Đã xóa các công việc được chọn.')
        return redirect('task')

class deleteView(APIView):
    def post(self, request, pk, format=None):
        task = Task.objects.get(id_task=pk)
        task.delete()
        messages.success(request, 'Đã xóa công việc.')
        return redirect('task')

class searchView(APIView):
    def get(self, request, format=None):
        # start_date = datetime.strptime(request.GET.get('startDate'), '%Y-%m-%d').date()
        # end_date = datetime.strptime(request.GET.get('endDate'), '%Y-%m-%d').date()
        tasks = Task.objects.all()
        start_date = request.GET.get('startDate')
        end_date = request.GET.get('endDate')
        test = request.GET.get('test')
        if test and start_date and end_date:
            tasks = Task.objects.filter(
                date_create_task__range=[start_date, end_date],
                description_task__icontains=test
            )
            messages.success(request, 'Danh sách công việc tìm kiếm theo mô tả và ngày tạo công việc')
            return render(request, 'task.html', {'tasks':tasks, 'messages': messages.get_messages(request)})
        if not start_date or not end_date:
            if test:
                tasks = Task.objects.filter(description_task__icontains=test)
                messages.success(request, 'Danh sách công việc tìm kiếm theo mô tả')
                return render(request, 'task.html', {'tasks':tasks, 'messages': messages.get_messages(request)})
            
            messages.success(request, 'Chưa nhập ngày bắt đầu, ngày kết thúc hoặc mô tả công việc.')
            return redirect('task')
        if start_date < end_date:
            tasks = tasks.filter(date_create_task__range=[start_date, end_date])
            messages.success(request, 'Danh sách được duyệt theo ngày tạo.')
            return render(request, 'task.html', {'tasks':tasks, 'messages': messages.get_messages(request)})

# User
class userView(APIView):
    def get(self, request, format=None):
        id = request.session.get('id')
        user = None
        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                # Xử lý trường hợp nếu không tìm thấy người dùng với id_user cung cấp
                pass
        return render(request, 'create_user.html', {'user':user})
    def post(self, request, format=None):
        data={
            'name': request.POST.get('name'),
            'username': request.POST.get('username'),
            'avatar': request.FILES.get('avatar'),
            'address': request.POST.get('address'),
            'school': request.POST.get('school'),
            'date_of_birth': request.POST.get('date_of_birth'),
        }
        user = User.objects.filter(username=data['username']).first()
        if user:
            messages.success(request, 'Tài khoản đã tồn tại.')
            return redirect('user')
        dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
        current_year = datetime.now().year
        if dob.year > current_year:
            messages.success(request, 'Ngày không hợp lệ')
            return redirect('user')
        raw_password = request.POST.get('password')
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_password.decode('utf-8')  # Chuyển bytes thành chuỗi để lưu vào cơ sở dữ liệu
            
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Tạo user thành công.')
            return redirect('user')
        messages.success(request, 'Nhập đầy đủ thông tin.')
        return redirect('user')
class loginView(APIView):
    def get(self, request, format=None):
        return render(request, 'login.html')
    def post(self, request, *args, **kwargs):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.filter(username=username).first()
            if user:
                hashed_password = user.password.encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    request.session['id'] = user.id
                    messages.success(request, 'Đăng nhập thành công.')
                    return redirect('task')
                else:
                    raise ValueError('Sai mật khẩu.')
            else:
                raise ValueError('Tài khoản không tồn tại')
        except ValueError as e:
            messages.success(request, str(e))
            return redirect('login')
class logoutView(APIView):
    def get(self, request, format=None):
        request.session.pop('id', None)
        messages.success(request, 'Đăng xuất tài khoản.')
        return redirect('login')

class profileView(APIView):
    def get(self, request, format=None):
        id = request.session.get('id')
        user = User.objects.get(id=id)
        return render(request, 'profile.html', {'user':user})

class addppView(APIView):
    def get(self, request, pk, format=None):
        id = request.session.get('id')
        user = None
        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                # Xử lý trường hợp nếu không tìm thấy người dùng với id_user cung cấp
                pass
        task = Task.objects.get(id_task=pk)
        listUser = User.objects.all()
        return render(request, 'add_people_to_task.html', {'task':task, 'user':user, 'listUser':listUser})
    def post(self, request, pk, format=None):
        task = Task.objects.get(id_task=pk)
        selected_user_ids = request.POST.get('selected_People').split(',')
        if selected_user_ids==['']:
            messages.success(request, 'Chưa chọn người nào.')
            return redirect('add_people_task')
        for id in selected_user_ids:
            user = User.objects.get(id=id)
            task.users.add(user)
        messages.success(request, 'Đã thêm những người được chọn vào làm công việc.')
        return redirect('task')