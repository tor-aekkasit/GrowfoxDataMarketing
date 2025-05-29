from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from .models import PageGroup, PageInfo
from .forms import PageGroupForm, PageURLForm
from .fb_page_info import PageInfo as FBPageInfo
from .fb_page_info import PageFollowers  # ✅ เพิ่มบรรทัดนี้

def create_group(request):
    if request.method == 'POST':
        form = PageGroupForm(request.POST)
        if form.is_valid():
            page_group = form.save()
            return redirect('group_detail', group_id=page_group.id)
    else:
        form = PageGroupForm()
    return render(request, 'PageInfo/create_group.html', {'form': form})

def add_page(request, group_id):
    group = PageGroup.objects.get(id=group_id)

    if request.method == 'POST':
        form = PageURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            platform = form.cleaned_data['platform']  # เพิ่ม platform ในฟอร์ม

            if platform == 'facebook':
                fb_data = FBPageInfo(url)
                if 'page_id' in fb_data:
                    follower_data = PageFollowers(fb_data['page_id'])
                    if follower_data:
                        fb_data.update(follower_data)

                allowed_fields = {f.name for f in PageInfo._meta.get_fields()}
                filtered_data = {k: v for k, v in fb_data.items() if k in allowed_fields}

                for key in ['page_likes_count', 'page_followers_count']:
                    value = filtered_data.get(key)
                    if isinstance(value, str):
                        filtered_data[key] = int(value.replace(',', ''))
                    elif isinstance(value, int):
                        filtered_data[key] = value

                filtered_data['platform'] = 'facebook'  # เพิ่ม platform ใน record
                PageInfo.objects.create(page_group=group, **filtered_data)

            elif platform == 'tiktok':
                from .tiktok_page_info import TikTokPageInfo
                tiktok_data = TikTokPageInfo(url)

                if tiktok_data:
                    # Mapping TikTok fields to PageInfo fields
                    allowed_fields = {f.name for f in PageInfo._meta.get_fields()}
                    filtered_data = {
                        'page_username': tiktok_data.get('username'),
                        'page_name': tiktok_data.get('page_name'),
                        'page_followers': tiktok_data.get('followers'),
                        'page_likes': tiktok_data.get('likes'),
                        'page_description': tiktok_data.get('bio'),
                        'profile_pic': tiktok_data.get('profile_pic'),
                        'page_url': tiktok_data.get('url'),
                        'platform': 'tiktok'
                    }
                    # ตรวจสอบว่าแต่ละ field อยู่ใน allowed_fields
                    filtered_data = {k: v for k, v in filtered_data.items() if k in allowed_fields}

                    PageInfo.objects.create(page_group=group, **filtered_data)
                else:
                    form.add_error(None, "Failed to fetch TikTok data.")
                    return render(request, 'PageInfo/add_page.html', {'form': form, 'group': group})

            return redirect('group_detail', group_id=group.id)

    else:
        form = PageURLForm()

    return render(request, 'PageInfo/add_page.html', {'form': form, 'group': group})
def group_detail(request, group_id):
    group = PageGroup.objects.get(id=group_id)
    pages = group.pages.all()  # ต้องมี related_name='pages'
    return render(request, 'PageInfo/group_detail.html', {
        'group': group,
        'pages': pages
    })

def index(request):
    page_groups = PageGroup.objects.prefetch_related('pages')
    total_groups = page_groups.count()  # นับจำนวนกลุ่มทั้งหมด
    return render(request, 'PageInfo/index.html', {
        'page_groups': page_groups,
        'total_groups': total_groups,  # ส่งจำนวนทั้งหมดไป template
    })

def sidebar_context(request):
    page_groups = PageGroup.objects.all()
    return {'page_groups_sidebar': page_groups, 'page_groups_count': page_groups.count()}

def showgroup(request):
    selected_group = PageGroup.objects.first()  # หรือใช้ get(pk=1) หรือ get(id=...)
    if not selected_group:
        return render(request, 'PageInfo/showgroup.html', {'error': 'No group found'})
    return render(request, 'PageInfo/showgroup.html', {'selected_group': selected_group})

def pageview(request, page_id):
    page = get_object_or_404(PageInfo, id=page_id)
    return render(request, 'PageInfo/pageview.html', {'page': page})
