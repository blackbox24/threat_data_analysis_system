from django.shortcuts import render
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
# from .forms import IncidentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout,authenticate
import random
from django.db.models import Count
from django.contrib.auth.forms import AuthenticationForm
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *

import psutil
import GPUtil
import json
from django.http import JsonResponse
import time

def get_system_data():
    cpu_data = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'cpu_freq': psutil.cpu_freq()._asdict(),
        'cpu_cores': psutil.cpu_count(logical=False),
        'cpu_total_cores': psutil.cpu_count(logical=True)
    }

    gpus = GPUtil.getGPUs()
    gpu_data = []
    for gpu in gpus:
        gpu_data.append({
            'id': gpu.id,
            'name': gpu.name,
            'load': gpu.load * 100,
            'free_memory': gpu.memoryFree,
            'used_memory': gpu.memoryUsed,
            'total_memory': gpu.memoryTotal,
            'temperature': gpu.temperature
        })

    return {'cpu': cpu_data, 'gpu': gpu_data}

@login_required
def system_data_view(request):
    data = get_system_data()
    return render(request, "dashboard/systemhealth.html", {"data": json.dumps(data)})

@login_required
def system_data_api(request):
    data = get_system_data()
    return JsonResponse(data)

    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user is an admin
            user_ = CustomUser.objects.filter(username=username)
            print(user.role)
            if user.role == "admin":
                return redirect('dashboard')
            else:
                return redirect('home')
        else:
            return redirect('login')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form':form})
    
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             print(user)
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             print("not valid")
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Check if the user is an admin
            print(user.role == "admin")
            print(request)
            if user.role == "admin":
                return redirect('dashboard')
            else:
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    return render(request, 'dashboard/home.html')



@login_required
def dashboard_view(request):
    # Aggregate threat data for pie chart
    threat_data = Threat.objects.values(
        'attack_type').annotate(count=Count('attack_type'))

    # Convert SystemHealth data to a format that can be serialized to JSON
    system_health_data = SystemHealth.objects.order_by(
        'timestamp').values('timestamp', 'cpu_usage', 'memory_usage')

    # Aggregate data for System Health Distribution
    system_health_distribution = SystemHealth.objects.aggregate(
        avg_cpu=Avg('cpu_usage'),
        avg_memory=Avg('memory_usage'),
        avg_disk=Avg('disk_usage')
    )
    print(system_health_distribution)
    # Convert datetime objects to strings in system health data
    system_health_data_list = [
        {
            'timestamp': health['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            'cpu_usage': health['cpu_usage'],
            'memory_usage': health['memory_usage']
        }
        for health in system_health_data
    ]

    # Preparing data for the frontend (JSON serialization)
    threat_data_json = json.dumps(list(threat_data))
    system_health_data_json = json.dumps(system_health_data_list)
    system_health_distribution_json = json.dumps(system_health_distribution)

    context = {
        'threat_data': threat_data_json,
        'system_health_data': system_health_data_json,
        'system_health_distribution': system_health_distribution_json,
    }
    return render(request, 'dashboard/dashboard.html', context)

def custom_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('logged_out')
    return redirect('login')


@login_required
def incident_report_overview(request):
    # Aggregate threat data
    threat_counts = Threat.objects.values("attack_type").annotate(count=Count("attack_type"))
    threat_labels = [item['attack_type'] for item in threat_counts]
    threat_data = [item['count'] for item in threat_counts]

    # Aggregate system health data
    health_data = {
        'cpu_usage': list(SystemHealth.objects.values_list('cpu_usage', flat=True)),
        'memory_usage': list(SystemHealth.objects.values_list('memory_usage', flat=True)),
        'disk_usage': list(SystemHealth.objects.values_list('disk_usage', flat=True))
    }
    print(threat_counts)
    print(threat_labels)
    print(threat_data)
    # Simulate monthly trends
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    cpu_trend = [random.uniform(10, 90) for _ in months]
    memory_trend = [random.uniform(20, 80) for _ in months]

    return render(request, 'dashboard/report_overview.html', {
        'threat_labels': threat_labels,
        'threat_data': threat_data,
        'health_data': health_data,
        'cpu_trend': cpu_trend,
        'memory_trend': memory_trend,
        'months': months
    })

@login_required
def incident_report(request):
    if request.method == 'POST':
        incident_type = request.POST['incident_type']
        description = request.POST['description']
        occurrence_time = request.POST['occurrence_time']
        severity = request.POST['severity']

        # Save the incident report to the database
        incident = IncidentReport(
            user=request.user,
            incident_type=incident_type,
            description=description,
            occurrence_time=occurrence_time,
            severity=severity
        )
        incident.save()

        # Redirect to a success page or the dashboard
        
        if request.user.role == 'admin':
            return redirect('dashboard')
        else:
            return redirect("home")

    return render(request, 'dashboard/incident_report.html')

@login_required
def submit_incident(request):
    if request.method == 'POST':
        incident_type = request.POST.get('incident_type')
        description = request.POST.get('description')
        date_occurred = request.POST.get('date_occurred')
        severity = request.POST.get('severity')
        # logged-in user is reporting the incident
        user = request.user
        
        # Create an IncidentReport instance
        Incident_report = IncidentReport.objects.create(
            user=user,
            incident_type=incident_type,
            description=description,
            occurrence_time=date_occurred,
            severity= severity,
        )

        incident = Incident.objects.create(
            title=incident_type,
            description=description,
            reported_by=user,
            status='open',
        )

        threat = Threat.objects.create(
            source_ip="192.168.7.1",
            attack_type=incident_type,
            details=description,
        )

        if request.user.role == 'admin':
            messages.success(request, 'Incident report submitted successfully!')
            return redirect('dashboard') 
        else:
            messages.success(request, 'Incident report submitted successfully!')
            return redirect("home")
        
    return render(request, 'incident_report.html', {'form': 'form'} )

@login_required
def view_incidents(request):
    incidents = IncidentReport.objects.all()  # or .all() for all users
    return render(request, 'dashboard/incident_list.html', {'incidents': incidents})

@login_required
def threat(request):
    threats = Threat.objects.all()
    return render(request, 'dashboard/threat_report.html',{"threats":threats})

@login_required
def report_threat(request):
    if request.method == 'POST':
        form = ThreatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ThreatForm()
    return render(request, 'dashboard/report_threat.html', {'form': form})

@login_required
def submit_threat(request):
    if request.method == 'POST':
        attack_type = request.POST.get('attack_type')
        detail = request.POST.get('detail')
        source_ip = request.POST.get('source_ip')
        # logged-in user is reporting the threat
        user = request.user
        
        # Create an IncidentReport instance
       
        threat = Threat.objects.create(
            source_ip=source_ip,
            attack_type=attack_type,
            details=detail,
        )

        if request.user.role == 'admin':
            messages.success(request, 'Threat report submitted successfully!')
            return redirect('dashboard') 
        else:
            messages.success(request, 'Incident report submitted successfully!')
            return redirect("home")
        
    return render(request, 'incident_report.html', {'form': 'form'} )
