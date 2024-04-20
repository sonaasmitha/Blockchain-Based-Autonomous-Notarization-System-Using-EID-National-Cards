from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import json
from web3 import Web3, HTTPProvider
import hashlib

global username, usersList, notaryList, contract, web3


#function to call contract
def getContract():
    global contract, web3
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Notary.json' #Logistic contract file
    deployed_contract_address = '0x2167D0F790f09df9d2C3f58A3600FF5C64a44a5a' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
getContract()

def getUsersList():
    global usersList, contract
    usersList = []
    count = contract.functions.getUserCount().call()
    for i in range(0, count):
        user = contract.functions.getUsername(i).call()
        password = contract.functions.getPassword(i).call()
        phone = contract.functions.getPhone(i).call()
        email = contract.functions.getEmail(i).call()
        address = contract.functions.getAddress(i).call()
        usersList.append([user, password, phone, email, address])

def getNotary():
    global notaryList, contract
    notaryList = []
    count = contract.functions.getNotaryCount().call()
    for i in range(0, count):
        uname = contract.functions.getOwner(i).call()
        fname = contract.functions.getFilename(i).call()
        hashcode = contract.functions.getHashcode(i).call()
        dd = contract.functions.getDate(i).call()
        signature = contract.functions.getSignature(i).call()
        key = contract.functions.getKey(i).call()
        notaryList.append([uname, fname, hashcode, signature, dd, key])        

getUsersList()
getNotary()

def VerifyNotaryAction(request):
    if request.method == 'POST':
        global username, notaryList
        today = date.today()
        pin = request.POST.get('t1', False)
        filedata = request.FILES['t2'].read()
        filename = request.FILES['t2'].name

        hashcode = hashlib.sha256(filedata).hexdigest()
        key = hashlib.sha256(pin.encode()).hexdigest()
        status = "Verification Failed"
        for i in range(len(notaryList)):
            nl = notaryList[i]
            if nl[2] == hashcode and nl[5] == key:
                status = nl
                break
        if status != "Verification Failed":
            output = '<table border=1 align=center>'
            output+='<tr><th><font size=3 color=black>Owner Name</font></th>'
            output+='<th><font size=3 color=black>eID File Name</font></th>'
            output+='<th><font size=3 color=black>Hashcode</font></th>'
            output+='<th><font size=3 color=black>Signature</font></th>'
            output+='<th><font size=3 color=black>Date</font></th>'
            output+='<th><font size=3 color=black>Key</font></th></tr>'
            arr = status[3].split("$")
            output+='<tr><td><font size=3 color=black>'+status[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+status[1]+'</font></td>'
            output+='<td><font size=3 color=black>'+status[2][0:20]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+status[4]+'</font></td>'
            output+='<td><font size=3 color=black>'+status[5][0:20]+'</font></td></tr>'
            output+='<tr><td><font size=3 color=black>Notary Text : '+arr[1]+'</font></td></tr>'
            status = output            
        context= {'data': status}
        return render(request, 'VerifierScreen.html', context)

def VerifyNotary(request):
    if request.method == 'GET':
       return render(request, 'VerifyNotary.html', {})

def AddNotary(request):
    if request.method == 'GET':
       return render(request, 'AddNotary.html', {})

def AddNotaryAction(request):
    if request.method == 'POST':
        global username, notaryList
        today = date.today()
        notary = request.POST.get('t1', False)
        pin = request.POST.get('t2', False)
        filedata = request.FILES['t3'].read()
        filename = request.FILES['t3'].name

        hashcode = hashlib.sha256(filedata).hexdigest()
        key = hashlib.sha256(pin.encode()).hexdigest()
        status = "none"
        for i in range(len(notaryList)):
            nl = notaryList[i]
            if nl[2] == hashcode:
                status = "Your eID Card Alread exists"
                break
        if status == "none":
            msg = contract.functions.RegisterHash(username, filename, hashcode, pin+"$"+notary, str(today), key).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
            notaryList.append([username, filename, hashcode, pin+"$"+notary, str(today), key])
            status = "Your notary details successfully saved in Blockchain using below details<br/>"+str(tx_receipt)
        else:
            status = "Error in saving Notary details"
        context= {'data': status}
        return render(request, 'AddNotary.html', context)

def DeleteNotaryAction(request):
    if request.method == 'GET':
        global uname, contract, notaryList
        rid = request.GET['file']
        contract.functions.deleteKey(int(rid)).transact()
        nl = notaryList[int(rid)]
        nl[2] = "Delete"
        context= {'data': "Given notary key deleted from Blockchain"}        
        return render(request, 'UserScreen.html', context)

def ViewNotary(request):
    if request.method == 'GET':
        global contract, notaryList, username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Owner Name</font></th>'
        output+='<th><font size=3 color=black>eID File Name</font></th>'
        output+='<th><font size=3 color=black>Hashcode</font></th>'
        output+='<th><font size=3 color=black>Signature</font></th>'
        output+='<th><font size=3 color=black>Date</font></th>'
        output+='<th><font size=3 color=black>Key</font></th></tr>'
        for i in range(len(notaryList)):
            nl = notaryList[i]
            if nl[0] == username:
                arr = nl[3].split("$")
                output+='<tr><td><font size=3 color=black>'+nl[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+nl[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+nl[2][0:20]+'</font></td>'
                output+='<td><font size=3 color=black>'+arr[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+nl[4]+'</font></td>'
                output+='<td><font size=3 color=black>'+nl[5][0:20]+'</font></td></tr>'
                output+='<tr><td><font size=3 color=black>Notary Text : '+arr[1]+'</font></td></tr>'
        context= {'data': output}        
        return render(request, 'UserScreen.html', context)     

def DeleteNotary(request):
    if request.method == 'GET':
        global contract, notaryList, username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Owner Name</font></th>'
        output+='<th><font size=3 color=black>eID File Name</font></th>'
        output+='<th><font size=3 color=black>Hashcode</font></th>'
        output+='<th><font size=3 color=black>Signature</font></th>'
        output+='<th><font size=3 color=black>Date</font></th>'
        output+='<th><font size=3 color=black>Key</font></th>'
        output+='<th><font size=3 color=black>Delete Notary</font></th></tr>'
        for i in range(len(notaryList)):
            nl = notaryList[i]
            if nl[0] == username and nl[2] != "Delete":
                arr = nl[3].split("$")
                output+='<tr><td><font size=3 color=black>'+nl[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+nl[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+nl[2][0:20]+'</font></td>'
                output+='<td><font size=3 color=black>'+arr[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+nl[4]+'</font></td>'
                output+='<td><font size=3 color=black>'+nl[5][0:20]+'</font></td>'
                output+='<td><a href=\'DeleteNotaryAction?file='+str(i)+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
                output+='<tr><td><font size=3 color=black>Notary Text : '+arr[1]+'</font></td></tr>'
        context= {'data': output}        
        return render(request, 'UserScreen.html', context)    

def VerifierLoginAction(request):
    if request.method == 'POST':
        global username, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            context= {'data':"Welcome "+username}
            return render(request, 'VerifierScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'VerifierLogin.html', context)  

def VerifierLogin(request):
    if request.method == 'GET':
       return render(request, 'VerifierLogin.html', {}) 

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})    

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})    
    
def SignupAction(request):
    if request.method == 'POST':
        global contract, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        record = 'none'
        for i in range(len(usersList)):
            ul = usersList[i]
            if ul[0] == username:
                record = "exists"
                break
        if record == 'none':
            msg = contract.functions.saveUser(username, password, contact, email, address).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
            usersList.append([username, password, contact, email, address])
            context= {'data':'Signup process completed and record saved in Blockchain<br/>'+str(tx_receipt)}
            return render(request, 'Signup.html', context)
        else:
            context= {'data':username+'Username already exists'}
            return render(request, 'Signup.html', context)
        
def LoginAction(request):
    if request.method == 'POST':
        global username, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        for i in range(len(usersList)):
            ul = usersList[i]
            if ul[0] == username and ul[1] == password:
                status = 'success'
                break
        if status == 'success':
            context= {'data':"Welcome "+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)            
def VerifierLogin(request):
    if request.method == 'GET':
       return render(request, 'VerifierLogin.html', {}) 

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})    

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})    
    
def SignupAction(request):
    if request.method == 'POST':
        global contract, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        record = 'none'
        for i in range(len(usersList)):
            ul = usersList[i]
            if ul[0] == username:
                record = "exists"
                break
        if record == 'none':
            msg = contract.functions.saveUser(username, password, contact, email, address).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
            usersList.append([username, password, contact, email, address])
            context= {'data':'Signup process completed and record saved in Blockchain<br/>'+str(tx_receipt)}
            return render(request, 'Signup.html', context)
        else:
            context= {'data':username+'Username already exists'}
            return render(request, 'Signup.html', context)
        
def LoginAction(request):
    if request.method == 'POST':
        global username, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        for i in range(len(usersList)):
            ul = usersList[i]
            if ul[0] == username and ul[1] == password:
                status = 'success'
                break
        if status == 'success':
            context= {'data':"Welcome "+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)            


        
        
