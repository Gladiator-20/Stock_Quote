from django.shortcuts import render, render, redirect
import finnhub
from .models import Stock
from django.contrib import messages
from .forms import StockForm




def home(request):
	import requests
	import json

	if request.method == "POST":
		ticker = request.POST['ticker']
		
		details = ("Name", "ProfitMargin", "MarketCapitalization", "MostRecentQuarter", "ProfitMargin", "TargetPrice", "Buy", "Hold", "Sell", "ControversyLevel", "SharesOutstanding", "EnterpriseValue", "PriceSalesTTM", "52WeekHigh", "52WeekLow")
		# api_request = requests.get("https://eodhd.com/api/fundamentals/" + ticker + ".US?api_token=demo&fmt=json")
		# api_request = requests.get("https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + ticker + "&apikey=29W6Z1XWV18HCN1K")

		api_request = requests.get("https://finnhub.io/api/v1/stock/profile2?symbol=" + ticker + "&token=ctdeu0hr01qng9geeph0ctdeu0hr01qng9geephg")
		# api = 29W6Z1XWV18HCN1K
		#ctdeu0hr01qng9geeph0ctdeu0hr01qng9geephg


		finnhub_client = finnhub.Client(api_key="ctdeu0hr01qng9geeph0ctdeu0hr01qng9geephg")

		fin = finnhub_client.company_profile2(symbol=ticker)



		try:
			api = json.loads(api_request.content)
			# finval = json.loads(fin)
		except Exception as e:
			api = "Error..."
			# finval = "Error..."
		return render(request, 'home.html', {'fin': fin})

	else:
		return render (request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})


def about(request):
	return render(request, 'about.html', {})

def add_stock(request):
	import requests
	import json
	
	ticker = Stock.objects.all()

	if request.method == "POST":
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added"))
			return redirect('add_stock')
	else:
		output = []
		for ticket_item in ticker:
			finnhub_client = finnhub.Client(api_key="ctdeu0hr01qng9geeph0ctdeu0hr01qng9geephg")

			fin = finnhub_client.company_profile2(symbol=ticket_item)
			output.append(fin)

		# try:
		# 	api = json.loads(api_request.content)
		# 	# finval = json.loads(fin)
		# except Exception as e:
		# 	api = "Error..."
		# 	# finval = "Error..."

		ticker = Stock.objects.all()
		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock has been deleted!"))
	return redirect(delete_stock)

def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})


# result = {}
# for matches in api["bestMatches"]:
# 	for key, value in matches:
# 		if key in details:
# 			result.append({key, value})

