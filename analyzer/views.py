import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import RoundRecord
@ensure_csrf_cookie
def home(request): return render(request, "index.html")
def payload(request):
    try:
        data = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None
@require_GET
def me(request): return JsonResponse({"authenticated":request.user.is_authenticated,"username":request.user.username if request.user.is_authenticated else ""})
@require_POST
def register(request):
    data=payload(request)
    if data is None: return JsonResponse({"error":"البيانات غير صالحة."},status=400)
    username=str(data.get("username","")).strip(); password=str(data.get("password",""))
    if len(username)<3 or len(username)>80: return JsonResponse({"error":"اسم المستخدم يجب أن يكون 3 أحرف على الأقل."},status=400)
    if len(password)<8: return JsonResponse({"error":"كلمة المرور يجب ألا تقل عن 8 أحرف."},status=400)
    if User.objects.filter(username__iexact=username).exists(): return JsonResponse({"error":"اسم المستخدم مستخدم بالفعل."},status=409)
    user=User.objects.create_user(username=username,password=password); login(request,user)
    return JsonResponse({"ok":True,"username":user.username},status=201)
@require_POST
def login_view(request):
    data=payload(request)
    if data is None: return JsonResponse({"error":"البيانات غير صالحة."},status=400)
    user=authenticate(request,username=str(data.get("username","")).strip(),password=str(data.get("password","")))
    if user is None: return JsonResponse({"error":"اسم المستخدم أو كلمة المرور غير صحيحة."},status=401)
    login(request,user); return JsonResponse({"ok":True,"username":user.username})
@require_POST
def logout_view(request): logout(request); return JsonResponse({"ok":True})
@login_required
@require_http_methods(["GET","POST"])
def rounds(request):
    if request.method=="GET": return JsonResponse({"rounds":[r.as_dict() for r in RoundRecord.objects.filter(user=request.user)]})
    data=payload(request)
    if data is None: return JsonResponse({"error":"البيانات غير صالحة."},status=400)
    predictions=data.get("predictions",[]); actuals=data.get("actuals",[0]*50)
    if not isinstance(predictions,list) or len(predictions)!=50 or not all(type(x) is int and x in (0,1,2) for x in predictions): return JsonResponse({"error":"التوقعات يجب أن تحتوي على 50 خانة صحيحة."},status=400)
    if not isinstance(actuals,list) or len(actuals)!=50 or not all(type(x) is int and x in (0,1,2) for x in actuals): return JsonResponse({"error":"النتائج الفعلية يجب أن تحتوي على 50 خانة صحيحة."},status=400)
    try: row_number=max(1,min(10,int(data.get("row_number",1))))
    except (ValueError,TypeError): row_number=1
    record=RoundRecord.objects.create(user=request.user,session_name=str(data.get("session_name",""))[:120],row_number=row_number,multiplier=str(data.get("multiplier",""))[:32],predictions=predictions,actuals=actuals,notes=str(data.get("notes",""))[:500])
    return JsonResponse({"round":record.as_dict()},status=201)
@login_required
@require_http_methods(["PATCH","DELETE"])
def round_detail(request,round_id):
    try: record=RoundRecord.objects.get(pk=round_id,user=request.user)
    except RoundRecord.DoesNotExist: return JsonResponse({"error":"الجولة غير موجودة."},status=404)
    if request.method=="DELETE": record.delete(); return JsonResponse({"ok":True})
    data=payload(request)
    if data is None: return JsonResponse({"error":"البيانات غير صالحة."},status=400)
    if "actuals" in data:
        actuals=data["actuals"]
        if not isinstance(actuals,list) or len(actuals)!=50 or not all(x in (0,1,2) for x in actuals): return JsonResponse({"error":"النتائج الفعلية يجب أن تحتوي على 50 خانة صحيحة."},status=400)
        record.actuals=actuals
    if "notes" in data: record.notes=str(data["notes"])[:500]
    record.save(); return JsonResponse({"round":record.as_dict()})
@require_GET
def healthz(request):
    try:
        with connection.cursor() as cursor: cursor.execute("SELECT 1"); cursor.fetchone()
        return JsonResponse({"status":"ok","database":"connected"})
    except Exception: return JsonResponse({"status":"error","database":"unavailable"},status=503)
