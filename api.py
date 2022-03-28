from email import message
from functools import wraps
from re import template
from sys import prefix
import traceback
from flask import Flask, make_response, render_template, request, Blueprint,abort, send_from_directory
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore,auth


angular = Blueprint('angular', __name__,template_folder='angular/dist/angular')




db=firestore.client()
def checkToken(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        print("hello")
        if not 'Authorization' in request.headers:
            abort(401,{'message':'Unauthozized caller'})

        user =None
        try:
            data=request.headers['Authorization']
            header_token=str(data)
            token=header_token.split(" ")[-1]
            user=auth.verify_id_token(token)
            kws['uid']= user['uid']
            kws['email']=user['email']
            
        except Exception:
            traceback.print_exc()
            abort(401)
        return f(*args,**kws)

    return decorated_function








@angular.route('/addtask',methods=['POST'])
@checkToken
def addtask(*args, **kws):
    if (request.method=='POST'):
        task_info=request.json
        task_info["uid"]=kws['uid']
        docRef=db.collection("task").document()
        docRef.set(task_info)
    return "1",200
        
@angular.route('/updatetask',methods=['POST'])
@checkToken
def updatetask(*args, **kws):
    if (request.method=='POST'):
        taskname =request.json.get("taskname")
        description = request.json.get("description")
        uid = kws['uid']
        tid = request.json.get("pani_id")
        data = db.collection("task").document(tid)
        data.update({'taskname':taskname, 'description':description,'uid':uid})
        return "1"

@angular.route('/showtask',methods=['POST'])
@checkToken
def showtask(*args, **kws):
    if (request.method=='POST'):
        uid=kws['uid']
        docRef = db.collection('task').where('uid',u'==',uid).get()
        tasks_list = []
        for doc in docRef:
            t = db.collection('task').document(doc.reference.id).get()
            t = t.to_dict()
            t['task_id'] = doc.reference.id
            tasks_list.append(t)
        dicty = {'key' : tasks_list}
        return dicty

@angular.route('/deletetask',methods=['POST'])
@checkToken
def deletetask(*args, **kws):
    if (request.method=='POST'):
        tid=request.json.get('task_id')
        db.collection('task').document(tid).delete()
        return "1"

