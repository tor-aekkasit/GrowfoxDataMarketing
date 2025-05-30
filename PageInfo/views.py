from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from .models import PageGroup, PageInfo
from .forms import PageGroupForm, PageURLForm
from .fb_page_info import PageInfo as FBPageInfo
from .fb_page_info import PageFollowers  # ✅ เพิ่มบรรทัดนี้
from .tiktok_page_info import get_tiktok_info  # แก้เป็น import get_tiktok_info
from .ig_page_info import get_instagram_info
import re

def add_page(request, group_id):
    group = PageGroup.objects.get(id=group_id)

    if request.method == 'POST':
        form = PageURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            platform = form.cleaned_data['platform']
            allowed_fields = {f.name for f in PageInfo._meta.get_fields()}

            if platform == 'facebook':
                fb_data = FBPageInfo(url)
                if 'page_id' in fb_data:
                    follower_data = PageFollowers(fb_data['page_id'])
                    if follower_data:
                        fb_data.update(follower_data)
                filtered_data = {k: v for k, v in fb_data.items() if k in allowed_fields}

                for key in ['page_likes_count', 'page_followers_count']:
                    value = filtered_data.get(key)
                    if isinstance(value, str):
                        filtered_data[key] = int(value.replace(',', ''))
                    elif isinstance(value, int):
                        filtered_data[key] = value

                filtered_data['platform'] = 'facebook'
                PageInfo.objects.create(page_group=group, **filtered_data)

            elif platform == 'tiktok':
                tiktok_data = get_tiktok_info(url)
                if tiktok_data:
                    filtered_data = {
                        'page_username': tiktok_data.get('username'),
                        'page_name': tiktok_data.get('nickname'),
                        'page_followers': tiktok_data.get('followers'),
                        'page_likes': tiktok_data.get('likes'),
                        'page_description': tiktok_data.get('bio'),
                        'profile_pic': tiktok_data.get('profile_pic'),
                        'page_url': tiktok_data.get('url'),
                        'platform': 'tiktok'
                    }
                    filtered_data = {k: v for k, v in filtered_data.items() if k in allowed_fields}
                    PageInfo.objects.create(page_group=group, **filtered_data)
                else:
                    form.add_error(None, "❌ ไม่สามารถดึงข้อมูล TikTok ได้ กรุณาตรวจสอบ URL หรือรอสักครู่")
                    return render(request, 'PageInfo/add_page.html', {'form': form, 'group': group})

            elif platform == 'instagram':
                match = re.search(r"instagram\.com/([\w\.\-]+)/?", url)
                if match:
                    username = match.group(1)
                    ig_data = get_instagram_info(username)
                    if ig_data:
                        filtered_data = {
                            'page_username': ig_data.get('username'),
                            'page_name': ig_data.get('username'),
                            'page_followers': ig_data.get('followers_count'),
                            'page_website': ig_data.get('website'),
                            'page_category': ig_data.get('category'),
                            'post_count': ig_data.get('post_count'),
                            'page_description': ig_data.get('bio'),
                            'profile_pic': ig_data.get('profile_pic'),
                            'page_url': ig_data.get('url'),
                            'platform': 'instagram'
                        }
                        filtered_data = {k: v for k, v in filtered_data.items() if k in allowed_fields}
                        PageInfo.objects.create(page_group=group, **filtered_data)
                    else:
                        form.add_error(None, "❌ ไม่สามารถดึงข้อมูล Instagram ได้ กรุณาตรวจสอบ URL หรือรอสักครู่")
                        return render(request, 'PageInfo/add_page.html', {'form': form, 'group': group})
                else:
                    form.add_error(None, "❌ URL Instagram ไม่ถูกต้อง")
                    return render(request, 'PageInfo/add_page.html', {'form': form, 'group': group})


            elif platform == 'lemon8':

                lm8_data = get_lemon8_info(url)  # ใช้ url เต็ม ไม่ต้องตัด username

                if lm8_data:

                    allowed_fields = {f.name for f in PageInfo._meta.get_fields()}

                    filtered_data = {

                        'page_username': lm8_data.get('username'),

                        'page_name': lm8_data.get('username'),

                        'page_followers': lm8_data.get('followers_count'),

                        'page_likes': lm8_data.get('likes_count'),

                        'following_count': lm8_data.get('following_count'),

                        'age': lm8_data.get('age'),

                        'page_description': lm8_data.get('bio'),

                        'page_website': lm8_data.get('website'),

                        'profile_pic': lm8_data.get('profile_pic'),

                        'page_url': lm8_data.get('url'),

                        'platform': 'lemon8'

                    }

                    filtered_data = {k: v for k, v in filtered_data.items() if k in allowed_fields}

                    PageInfo.objects.create(page_group=group, **filtered_data)

                else:

                    form.add_error(None, "❌ ไม่สามารถดึงข้อมูล Lemon8 ได้ กรุณาตรวจสอบ URL หรือรอสักครู่")

                    return render(request, 'PageInfo/add_page.html', {'form': form, 'group': group})

            return redirect('group_detail', group_id=group.id)

    else:
        form = PageURLForm()

    return render(request, 'PageInfo/add_page.html', {'form': form, 'group': group})


def create_group(request):
    if request.method == 'POST':
        form = PageGroupForm(request.POST)
        if form.is_valid():
            page_group = form.save()
            return redirect('group_detail', group_id=page_group.id)
    else:
        form = PageGroupForm()
    return render(request, 'PageInfo/create_group.html', {'form': form})

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
