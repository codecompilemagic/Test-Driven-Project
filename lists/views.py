from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Item

# Create your views here.
def home_page(request):
	# return HttpResponse('<html><title>To-Do lists</title></html>')
	# if request.method == 'POST':
	# 	return HttpResponse(request.POST['item_text'])
	# return render(request, 'home.html')
	# item = Item()
	# item.text = request.POST.get('item_text', '')
	# item.save()

	# # return render(request, 'home.html', {'new_item_text': request.POST.get('item_text',''),})
	# return render(request, 'home.html', {'new_item_text': item.text})
	if request.method == 'POST':
		# new_item_text = request.POST['item_text']
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/')
	# else:
		# new_item_text = ''
	# return render(request, 'home.html', {'new_item_text': new_item_text, })
	return render(request, 'home.html')