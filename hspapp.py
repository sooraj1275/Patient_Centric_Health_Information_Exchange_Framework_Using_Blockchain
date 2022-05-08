from base64 import b64decode
import json
import re
from flask import Flask, render_template, request, session, redirect, jsonify
from DBConnection import Db
import datetime
import web3
from web3 import HTTPProvider,Web3
path="D:\\counterfiet\\counterfiet\\static\\"
compiled_contract_path=r"D:\b\build\contracts\StructDemo.json"
deployed_contract_address="0xE43996494Bb5eE0f5311b62fDeC8d0a8A84F17A4"
import json
web3 = Web3(HTTPProvider("HTTP://127.0.0.1:7545"))





app = Flask(__name__)
app.secret_key="kkk"
static_path = "D:\\Likhil\\Web\\Web\\static\\"

@app.route('/')
def adm_login():
    return render_template("user/indexlogin.html")

@app.route('/login')
def adm_logins():
    return render_template("user/indexlogin.html")



@app.route('/adm_login_post',methods=['post'])
def adm_login_post():
   username=request.form['textfield']
   password=request.form['textfield2']
   session["password"]=password
   session["pass"]=password
   db=Db()
   qry="SELECT * FROM `login` WHERE `username`='"+username+"' AND `password`='"+password+"'"
   print(qry)
   res=db.selectOne(qry)
   if  res is not None:
       session["lid"]=str(res["lid"])
       print(res)
       if res["type"]=="doctor":
           return render_template("doctor/home.html")
       elif res["type"] == "user":
           return render_template("user/home.html")
       elif res["type"] == "research":
           return  render_template("research/home.html")
       elif res["type"] == "healthinsurance":
           return  render_template("heakthins/home.html")
       else:
           return "<script>alert('Invalid username or password');window.location='/';</script>"
   else:
       return "<script>alert('Invalid username or password');window.location='/';</script>"

@app.route('/uhome')
def uhome():
    return render_template("user/home.html")
@app.route('/hhome')
def hhome():
    return render_template("heakthins/home.html")
@app.route('/rhome')
def rhome():
    return render_template("research/home.html")


@app.route('/dhome')
def dochome():
    return render_template("doctor/home.html")
@app.route('/adm_addmedicines')
def adm_addmedicines():
    return render_template("admin/addmecines.html")

@app.route("/user_uploadphr")
def useruploadphr():
    return render_template("user/uploadehr.html")


@app.route("/useruploadphtpost",methods=['post'])
def useruploadphtpost():
    file=request.files['file']
    filetype=request.form['filetype']
    description=request.form["description"]

    ehrpath="D:\\Likhil\\Web\\Web\\static\\ehr\\"
    from datetime import datetime

    filename= datetime.now().strftime("%Y%m%d%H%M%S")

    file.save(ehrpath+filename+".pdf")

    filepath="/static/ehr/"+ filename+".pdf"

    web3.eth.defaultAccount = web3.eth.accounts[0]

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        print(contract_abi)
    #
    # product = self.web3.eth.contract(abi=self._abi,
    #                                  address="0xEcf4D2312b9AAE8da53C0f8F3c42B58042dA93F2",
    #                                  bytecode=self._bytecode)
    #


    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()

    print(blocknumber)
    # return  str(blocknumber)+""
    from datetime import datetime
    dte=datetime.now().strftime("%Y/%m/%d")

    message2 = contract.functions.addEmployee(blocknumber + 1, str(blocknumber+1),str(session['lid']),filepath,filetype, description,dte,str(session['lid']),'user').transact()
    #
    #
    #
    #
    # db=Db()
    # qry="INSERT INTO `files` (`plid`,`filename`,`type`,`description`,`dte`,`uploadedbyid`,`uploadedtype`) VALUES ('"+str(session['lid'])+"','"+filepath+"','"+filetype+"','"+description+"',CURDATE(),'"+str(session['lid'])+"','user')"
    # db.insert(qry)
    return "<script>alert('File uploaded successflly');window.location='/user_uploadphr'</script>"


@app.route("/doctor_uploadphr/<lid>")
def doctor_uploadphr(lid):
    session["lids"]=lid
    return render_template("doctor/uploadehr.html")


@app.route("/doctor_uploadphrpost",methods=['post'])
def doctor_uploadphrpost():
    file=request.files['file']
    filetype=request.form['filetype']
    description=request.form["description"]

    ehrpath="D:\\Likhil\\Web\\Web\\static\\ehr\\"
    from datetime import datetime

    filename= datetime.now().strftime("%Y%m%d%H%M%S")

    file.save(ehrpath+filename+".pdf")

    filepath="/static/ehr/"+ filename+".pdf"

    web3.eth.defaultAccount = web3.eth.accounts[0]

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        print(contract_abi)


    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()

    print(blocknumber)









    # return  str(blocknumber)+""
    from datetime import datetime
    dte = datetime.now().strftime("%Y/%m/%d")

    message2 = contract.functions.addEmployee(blocknumber + 1, str(blocknumber + 1), str(session['lids']), filepath,
                                              filetype, description, dte, str(session['lid']), 'doctor').transact()


    return "<script>alert('File uploaded successflly');window.location='/docviewpatients'</script>"


@app.route("/research_viewusers")
def research_viewusers():
    qry="SELECT * FROM `users`"
    db=Db()
    res=db.select(qry)
    return render_template("research/viewusers.html",data=res)

@app.route("/health_viewusers")
def healthviewusers():
    qry = "SELECT * FROM `users`"
    db = Db()
    res = db.select(qry)
    return render_template("heakthins/viewusers.html", data=res)


@app.route('/doctorviewphrofpatient_uploadedbyhim/<plid>')
def dcotorviewphrofpatient_uploadedbyhimself(plid):
    res = []

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    res = {}
    data = []
    for i in range(blocknumber, 30, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        decoded_input = contract.decode_function_input(a['input'])

        if str(decoded_input[1]['plid'])==plid:
            res = {}
            res['bid'] = decoded_input[1]['bid']
            res['fid'] = decoded_input[1]['fid']
            res['plid'] = decoded_input[1]['plid']
            res['filename'] = decoded_input[1]['filename']
            res['typefile'] = decoded_input[1]['typefile']
            res['description'] = decoded_input[1]['description']
            res['dte'] = decoded_input[1]['dte']
            res['uploadedbyid'] = decoded_input[1]['uploadedbyid']
            res['uploadedtype'] = decoded_input[1]['uploadedtype']
            print(res)
            # if str(decoded_input/z[1]['mid'])==str(session['lid']):
            data.append(res)

    ks = []
    db = Db()
    for i in data:
        if i['uploadedtype'] == "doctor":
            id = str(i['uploadedbyid'])

            if id== str(session['lid']):
                a = {'fid': i['fid'], 'plid': i['plid'], 'filename': i['filename'], 'type': i['typefile'],
                     'description': i['description'], 'dte': i['dte'],
                     'uploadedtype': i['uploadedtype']}
                ks.append(a)

    return render_template("doctor/viewehr_uploadbyhomeforpatientwithid.html", ks=ks)


@app.route("/userviewehrs")
def userviewehr():

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    res = {}
    data=[]
    for i in range(blocknumber, 30, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        decoded_input = contract.decode_function_input(a['input'])

        res={}
        res['bid'] = decoded_input[1]['bid']
        res['fid'] = decoded_input[1]['fid']
        res['plid'] = decoded_input[1]['plid']
        res['filename'] = decoded_input[1]['filename']
        res['typefile'] = decoded_input[1]['typefile']
        res['description'] = decoded_input[1]['description']
        res['dte'] = decoded_input[1]['dte']
        res['uploadedbyid'] = decoded_input[1]['uploadedbyid']
        res['uploadedtype'] = decoded_input[1]['uploadedtype']
        print(res)
        # if str(decoded_input/z[1]['mid'])==str(session['lid']):

        if str(res['plid'])==str(session['lid']):
            data.append(res)

    ks=[]
    db=Db()
    for i in data:
        if i['uploadedtype']=="doctor":
            id=str(i['uploadedbyid'])
            qry="SELECT `name` FROM `doctor` WHERE `lid`='"+id+"'"
            resb=db.selectOne(qry)
            a = {'fid': i['fid'], 'plid': i['plid'], 'filename': i['filename'], 'type': i['typefile'],
                 'description': i['description'], 'dte': i['dte'], 'uploadedbyid':resb['name'] ,
                 'uploadedtype': i['uploadedtype']}
            ks.append(a)


        else:
            a={'fid':i['fid'],'plid':i['plid'],'filename':i['filename'],'type':i['typefile'] ,'description':i['description'],'dte':i['dte'],'uploadedbyid': 'MySelf','uploadedtype': i['uploadedtype']}
            ks.append(a)

    return  render_template("user/viewehr.html",ks=ks)




@app.route("/userviewerequestpending")
def userviewerequestpending():

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    res = {}
    data=[]
    for i in range(blocknumber, 30, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        decoded_input = contract.decode_function_input(a['input'])

        res={}
        res['bid'] = decoded_input[1]['bid']
        res['fid'] = decoded_input[1]['fid']
        res['plid'] = decoded_input[1]['plid']
        res['filename'] = decoded_input[1]['filename']
        res['typefile'] = decoded_input[1]['typefile']
        res['description'] = decoded_input[1]['description']
        res['dte'] = decoded_input[1]['dte']
        res['uploadedbyid'] = decoded_input[1]['uploadedbyid']
        res['uploadedtype'] = decoded_input[1]['uploadedtype']
        print(res)
        db=Db()
        # if str(decoded_input/z[1]['mid'])==str(session['lid']):

        if str(res['plid'])==str(session['lid']):
            qry="SELECT `request`.*,`doctor`.* FROM request INNER JOIN `doctor` ON `doctor`.`lid`=`request`.`lid` WHERE `request`.`blockid`='"+str(res['bid'])+"' AND `request`.`status`='pending'"
            resd=db.selectOne(qry)
            if resd is not None:
                resa = {}
                resa['bid'] = decoded_input[1]['bid']
                resa['fid'] = decoded_input[1]['fid']
                resa['plid'] = decoded_input[1]['plid']
                resa['filename'] = decoded_input[1]['filename']
                resa['typefile'] = decoded_input[1]['typefile']
                resa['description'] = decoded_input[1]['description']
                resa['dte'] = decoded_input[1]['dte']
                resa['uploadedbyid'] = decoded_input[1]['uploadedbyid']
                resa['uploadedtype'] = decoded_input[1]['uploadedtype']
                resa['name']=resd['name']
                resa['email']=resd['email']
                resa['photo']=resd['photo']
                resa['requestid']=resd['requestid']
                data.append(resa)

            qry = "SELECT `request`.*,`research`.* FROM request INNER JOIN `research` ON `research`.`lid`=`request`.`lid` WHERE `request`.`blockid`='" + str(
                res['bid']) + "' AND `request`.`status`='pending'"
            resd = db.selectOne(qry)
            if resd is not None:
                resa = {}
                resa['bid'] = decoded_input[1]['bid']
                resa['fid'] = decoded_input[1]['fid']
                resa['plid'] = decoded_input[1]['plid']
                resa['filename'] = decoded_input[1]['filename']
                resa['typefile'] = decoded_input[1]['typefile']
                resa['description'] = decoded_input[1]['description']
                resa['dte'] = decoded_input[1]['dte']
                resa['uploadedbyid'] = decoded_input[1]['uploadedbyid']
                resa['uploadedtype'] = decoded_input[1]['uploadedtype']
                resa['name'] = resd['name']
                resa['email'] = resd['email']
                resa['photo'] = resd['photo']
                resa['requestid'] = resd['requestid']
                data.append(resa)
            qry = "SELECT `request`.*,`healthinsurance`.* FROM request INNER JOIN `healthinsurance` ON `healthinsurance`.`lid`=`request`.`lid` WHERE `request`.`blockid`='" + str(
                res['bid']) + "' AND `request`.`status`='pending'"
            resd = db.selectOne(qry)
            if resd is not None:
                resa = {}
                resa['bid'] = decoded_input[1]['bid']
                resa['fid'] = decoded_input[1]['fid']
                resa['plid'] = decoded_input[1]['plid']
                resa['filename'] = decoded_input[1]['filename']
                resa['typefile'] = decoded_input[1]['typefile']
                resa['description'] = decoded_input[1]['description']
                resa['dte'] = decoded_input[1]['dte']
                resa['uploadedbyid'] = decoded_input[1]['uploadedbyid']
                resa['uploadedtype'] = decoded_input[1]['uploadedtype']
                resa['name'] = resd['name']
                resa['email'] = resd['email']
                resa['photo'] = resd['photo']
                resa['requestid'] = resd['requestid']
                data.append(resa)

    return  render_template("user/viewrequests.html",ks=data)

@app.route('/acceptrequest/<rid>')
def acceptrequest(rid):
    db=Db()
    qry="UPDATE `request` SET STATUS='verified' WHERE `requestid`='"+rid+"'"
    db.update(qry)

    return "<script>alert('Request accepted');window.location='/userviewerequestpending'</script>"

@app.route('/rejectrequest/<rid>')
def rejectrequest(rid):
    db=Db()
    qry="UPDATE `request` SET STATUS='rejected' WHERE `requestid`='"+rid+"'"
    db.update(qry)

    return "<script>alert('Request Rejected');window.location='/userviewerequestpending'</script>"


@app.route("/userviewdoctors")
def userviewdoctoes():
    db=Db()
    qry="SELECT * FROM `doctor`"
    res=db.select(qry)
    return render_template("user/viewdoctor.html",data=res)

@app.route("/userviewprofile")
def userviewprofile():
    db=Db()
    qry="SELECT * FROM users WHERE `lid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("user/userviewprofile.html",data=res)

@app.route("/researchviewprofile")
def researchviewprofile():
    db=Db()
    qry="SELECT * FROM research WHERE `lid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("research/userviewprofile.html",data=res)


@app.route('/researchviewuser')
def researchviewuser():
    db=Db()
    res=db.select("SELECT * FROM `users`")
    return render_template("research/viewusers.html",data=res)


@app.route("/researchviewfiles/<plid>")
def researchviewfiles(plid):
    res = []

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    res = {}
    data = []
    for i in range(blocknumber, 30, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        decoded_input = contract.decode_function_input(a['input'])

        if str(decoded_input[1]['plid']) == plid:
            res = {}
            res['bid'] = decoded_input[1]['bid']
            res['fid'] = decoded_input[1]['fid']
            res['plid'] = decoded_input[1]['plid']
            res['filename'] = decoded_input[1]['filename']
            res['typefile'] = decoded_input[1]['typefile']
            res['description'] = decoded_input[1]['description']
            res['dte'] = decoded_input[1]['dte']
            res['uploadedbyid'] = decoded_input[1]['uploadedbyid']
            res['uploadedtype'] = decoded_input[1]['uploadedtype']
            print(res)
            db=Db()
            qry="SELECT `status` FROM `request` WHERE `blockid`='"+str(res['bid'])+"' AND `lid`='"+session['lid']+"'"
            resa=db.selectOne(qry)
            if resa is not None:
                res['status']=resa['status']
            else:
                res['status']='request'

            # if str(decoded_input/z[1]['mid'])==str(session['lid']):
            data.append(res)


    return render_template("research/viewfilesbypid.html", ks=data)



@app.route("/healthviewfile/<plid>")
def healthviewfile(plid):
    res = []

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    res = {}
    data = []
    for i in range(blocknumber, 30, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        decoded_input = contract.decode_function_input(a['input'])

        if str(decoded_input[1]['plid']) == plid:
            res = {}
            res['bid'] = decoded_input[1]['bid']
            res['fid'] = decoded_input[1]['fid']
            res['plid'] = decoded_input[1]['plid']
            res['filename'] = decoded_input[1]['filename']
            res['typefile'] = decoded_input[1]['typefile']
            res['description'] = decoded_input[1]['description']
            res['dte'] = decoded_input[1]['dte']
            res['uploadedbyid'] = decoded_input[1]['uploadedbyid']
            res['uploadedtype'] = decoded_input[1]['uploadedtype']
            print(res)
            db=Db()
            qry="SELECT `status` FROM `request` WHERE `blockid`='"+str(res['bid'])+"' AND `lid`='"+session['lid']+"'"
            resa=db.selectOne(qry)
            if resa is not None:
                res['status']=resa['status']
            else:
                res['status']='request'

            # if str(decoded_input/z[1]['mid'])==str(session['lid']):
            data.append(res)


    return render_template("heakthins/viewfilesbypid.html", ks=data)


@app.route("/doctorviewfiles/<plid>")
def doctorviewfiles(plid):
    res = []

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    res = {}
    data = []
    for i in range(blocknumber, 30, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        decoded_input = contract.decode_function_input(a['input'])

        if str(decoded_input[1]['plid']) == plid:
            res = {}
            res['bid'] = decoded_input[1]['bid']
            res['fid'] = decoded_input[1]['fid']
            res['plid'] = decoded_input[1]['plid']
            res['filename'] = decoded_input[1]['filename']
            res['typefile'] = decoded_input[1]['typefile']
            res['description'] = decoded_input[1]['description']
            res['dte'] = decoded_input[1]['dte']
            res['uploadedbyid'] = decoded_input[1]['uploadedbyid']
            res['uploadedtype'] = decoded_input[1]['uploadedtype']
            print(res)
            db=Db()
            qry="SELECT `status` FROM `request` WHERE `blockid`='"+str(res['bid'])+"' AND `lid`='"+session['lid']+"'"
            resa=db.selectOne(qry)
            if resa is not None:
                res['status']=resa['status']
            else:
                res['status']='request'

            # if str(decoded_input/z[1]['mid'])==str(session['lid']):
            data.append(res)


    return render_template("doctor/viewfilesbypid.html", ks=data)






@app.route("/researchrequest/<bid>")
def researchrequest(bid):
    db=Db()
    qry="INSERT INTO `request` (`blockid`,`lid`,`date`,`status`) VALUES ('"+bid+"','"+str(session['lid'])+"',CURDATE(),'pending')"
    db.insert(qry)
    return "<script>alert('Request sent successfully');window.location='/researchviewuser'</script>"


@app.route("/doctorrequest/<bid>")
def doctorrequest(bid):
    db=Db()
    qry="INSERT INTO `request` (`blockid`,`lid`,`date`,`status`) VALUES ('"+bid+"','"+str(session['lid'])+"',CURDATE(),'pending')"
    db.insert(qry)
    return "<script>alert('Request sent successfully');window.location='/docviewpatients'</script>"




@app.route("/healthrequest/<bid>")
def healthrequest(bid):
    db=Db()
    qry="INSERT INTO `request` (`blockid`,`lid`,`date`,`status`) VALUES ('"+bid+"','"+str(session['lid'])+"',CURDATE(),'pending')"
    db.insert(qry)
    return "<script>alert('Request sent successfully');window.location='/health_viewusers'</script>"


@app.route("/healthviewprofile")
def healthviewprofile():
    db=Db()
    qry="SELECT * FROM healthinsurance WHERE `lid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("heakthins/userviewprofile.html",data=res)






@app.route('/adm_change_password')
def adm_change_password():
    return render_template("admin/change password.html")

@app.route('/adm_change_password_post',methods=['post'])
def adm_change_password_post():



    currentpassword=request.form['textfield']
    confirmpassword=request.form['textfield3']
    newpassword = request.form['textfield2']
    if newpassword==confirmpassword:
        if session["password"]==currentpassword:
            db=Db()
            qry="UPDATE `login` SET `password`='"+confirmpassword+"' WHERE `lid`='"+str(session["lid"])+"'"
            db.update(qry)
            return '''<script>alert('success');window.location='/adhome'</script>'''
        else:
            return "invalid"
    else:
        return "invalid"





@app.route('/adm_view_and_approve_doctors')
def adm_view_and_approve_doctors():
    qry="select * from doctor"
    db=Db()
    res=db.select(qry)


    qry="SELECT * FROM `research` WHERE STATUS='Approved'"
    d= db.select(qry)





    return render_template("admin/view and approve doctors.html", data=res,h=d)




#----------------------------doctor---------------------------
@app.route("/userviewarticles",methods=['post'])
def userviewarticles():
    db=Db()
    qry="SELECT * FROM `articlelink`"
    res=db.select(qry)
    return jsonify(status='ok',data=res)

@app.route("/usersentcomment",methods=['post'])
def usersentcomment():
    comment= request.form["comment"]
    pid=request.form["pid"]
    ulid=request.form["lid"]


    qry="INSERT INTO `comment` (`comment`,`postid`,`ulid`,`date`) VALUES ('"+comment+"','"+pid+"','"+ulid+"',CURDATE())"
    db=Db()
    db.insert(qry)
    return jsonify(status='ok')


@app.route("/doctoraddschedule/<dlid>")
def doctoraddschedule(dlid):
    session["dlid"]=dlid
    return render_template("research/addschedule.html")

@app.route("/doctoraddschedulepost",methods=['post'])
def doctoraddschedulepost():
    date=request.form["date"]
    f=request.form["from"]
    t=request.form["to"]

    db=Db()
    qry="INSERT INTO `schedule` (`dlid`,`date`,`fr`,`tot`) VALUES ('"+str(session['dlid'])+"','"+date+"','"+f+"','"+t+"')"
    db.insert(qry)

    return "<script>alert('Schedule added successfully');window.location='/doctoraddschedule/"+session['lid']+"'</script>"

@app.route("/doctorviewschedule")
def doctorviewschedule():
    db=Db()
    qry="SELECT * FROM `schedule` WHERE dlid='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("doctor/viewschedule.html",data=res)

@app.route("/doctordeleteschedule/<id>")
def doctordeleteschedule(id):
    db=Db()
    qry="DELETE FROM `schedule` WHERE scid='"+id+"'"
    db.delete(qry)
    return "<script>alert('Schedule added successfully');window.location='/doctoraddschedule'</script>"
 




@app.route('/doctor_index')
def doctor_index():
    return redirect('/doc_view_profile')


@app.route('/doc_doctor_registeration')
def doctor_registeration():
    return render_template("doctor_registeration.html")

@app.route('/doc_doctor_registeration_post',methods=['post'])
def doc_doctor_registeration_post():
    name=request.form['textfield']

    password=request.form['textfield2']
    gender=request.form['textfield3']
    phone_number=request.form['textfield4']
    email=request.form['textfield5']
    image=request.files['fileField']
    latitude=request.form['textfield6']
    longitude=request.form['textfield7']
    qualification=request.form['textfield8']
    place=request.form['textfield9']
    pin=request.form['textfield10']
    post=request.form['textfield11']
    district=request.form['textfield12']


    db = Db()


    image.save(static_path+"doctor\\" + image.filename)

    p="/static/doctor/"+image.filename

    q="INSERT INTO `login`(username,PASSWORD,TYPE) VALUES ('"+email+"','"+password+"','doctor')"
    lid=db.insert(q)

    qry="INSERT INTO `doctor`(lid,NAME,gender,phonenumber,email,photo,latitude,longitude,qualification,place,pin,post,district) VALUES ('"+str(lid)+"','"+name+"','"+gender+"','"+phone_number+"','"+email+"','"+p+"','"+latitude+"','"+longitude+"','"+qualification+"','"+place+"','"+pin+"','"+post+"','"+district+"')"
    db.insert(qry)
    return "<script>alert('Account created successfully');window.location='/doc_doctor_registeration'</script>"


@app.route("/userregisration")
def userregistration():
    return  render_template("user_registration.html")



@app.route('/user_registeration_post',methods=['post'])
def user_registeration_post():
    name=request.form['textfield']

    password=request.form['textfield2']
    gender=request.form['textfield3']
    phone_number=request.form['textfield4']
    email=request.form['textfield5']
    image=request.files['fileField']

    place=request.form['textfield9']
    pin=request.form['textfield10']
    post=request.form['textfield11']
    district=request.form['textfield12']


    db = Db()


    image.save(static_path+"doctor\\" + image.filename)

    p="/static/doctor/"+image.filename

    q="INSERT INTO `login`(username,PASSWORD,TYPE) VALUES ('"+email+"','"+password+"','user')"
    lid=db.insert(q)

    qry="INSERT INTO `users`(lid,NAME,gender,phonenumber,email,photo,place,pin,post,district) VALUES ('"+str(lid)+"','"+name+"','"+gender+"','"+phone_number+"','"+email+"','"+p+"','"+place+"','"+pin+"','"+post+"','"+district+"')"
    db.insert(qry)
    return "<script>alert('Account created successfully');window.location='/userregisration'</script>"


@app.route("/healthinsurancereg")
def healthinsurancereg():
    return  render_template("healthinsurancereg.html")



@app.route('/healthinsuranceregpost',methods=['post'])
def healthinsuranceregpost():
    name=request.form['textfield']

    password=request.form['textfield2']

    phone_number=request.form['textfield4']
    email=request.form['textfield5']
    image=request.files['fileField']

    place=request.form['textfield9']
    pin=request.form['textfield10']
    post=request.form['textfield11']
    district=request.form['textfield12']


    db = Db()


    image.save(static_path+"doctor\\" + image.filename)

    p="/static/doctor/"+image.filename

    q="INSERT INTO `login`(username,PASSWORD,TYPE) VALUES ('"+email+"','"+password+"','healthinsurance')"
    lid=db.insert(q)

    qry="INSERT INTO `healthinsurance`(lid,NAME,phonenumber,email,photo,place,pin,post,district) VALUES ('"+str(lid)+"','"+name+"','"+phone_number+"','"+email+"','"+p+"','"+place+"','"+pin+"','"+post+"','"+district+"')"
    db.insert(qry)
    return "<script>alert('Account created successfully');window.location='/healthinsurancereg'</script>"



@app.route("/researchsignup")
def researchsignup():
    return  render_template("researchreg.html")



@app.route('/researchsignuppost',methods=['post'])
def researchsignuppost():
    name=request.form['textfield']

    password=request.form['textfield2']

    phone_number=request.form['textfield4']
    email=request.form['textfield5']
    image=request.files['fileField']

    place=request.form['textfield9']
    pin=request.form['textfield10']
    post=request.form['textfield11']
    district=request.form['textfield12']


    db = Db()


    image.save(static_path+"doctor\\" + image.filename)

    p="/static/doctor/"+image.filename

    q="INSERT INTO `login`(username,PASSWORD,TYPE) VALUES ('"+email+"','"+password+"','research')"
    lid=db.insert(q)

    qry="INSERT INTO `research`(lid,NAME,phonenumber,email,photo,place,pin,post,district) VALUES ('"+str(lid)+"','"+name+"','"+phone_number+"','"+email+"','"+p+"','"+place+"','"+pin+"','"+post+"','"+district+"')"
    db.insert(qry)
    return "<script>alert('Account created successfully');window.location='/researchsignup'</script>"









@app.route('/article')
def article():
    return render_template('doctor/add_article.html')

@app.route('/article_post', methods=['post'])
def article_post():
    a = request.form['f_name']
    b = request.files['f_file']

    b.save("C:\\Users\\Bilal Fahmi\\PycharmProjects\\vetapp\\static\\doctor\\" + b.filename)

    upload_b="/static/doctor/"+b.filename
    d = Db()
    qry = "insert into article(doctor_lid,file,artcile_name) values('"+str(session['lid'])+"','"+upload_b+"','"+a+"')"
    res = d.insert(qry)

    return '''<script>alert('Uploaded success');window.location='/article'</script>'''


@app.route('/view_doc_article')
def view_doc_article():
    d = Db()
    qry = "select * from article where doctor_lid='"+str(session['lid'])+"' "
    res = d.select(qry)
    return render_template('doctor/view_article.html',data=res)

@app.route('/view_doc_article_search', methods=['post'])
def view_doc_article_search():
    search = request.form['search1']
    d = Db()
    qry = "select * from article where doctor_lid='"+str(session['lid'])+"' and artcile_name like '%"+search+"%'"
    res = d.select(qry)

    return render_template('doctor/view_article.html',data=res)


@app.route('/delete_article/<aid>')
def delete_article(aid):
    d = Db()
    qry = "delete from article where article_id='"+aid+"'"
    res = d.delete(qry)
    return '''<script>alert('Deleted');window.location='/view_doc_article'</script>'''



@app.route('/doc_change_password')
def doctor_change_password():
    return render_template("doctor/change_password.html")

@app.route('/doc_change_password_post',methods=['post'])
def doc_change_password_post():

    oldpassword= request.form['textfield']
    newpassword = request.form['textfield2']
    password= request.form['textfield3']
    if newpassword == password:
        if session["password"] == oldpassword:
            db = Db()
            qry = "UPDATE `login` SET `password`='" + newpassword + "' WHERE `lid`='" + str(session["lid"]) + "'"
            db.update(qry)
            return '''<script>alert('success');window.location='/'</script>'''
        else:
            return "invalid"
    else:
        return "invalid"
    return"ok"





# @app.route('/doc_research')
# def doctor_research():
#     return render_template("doctor/view research.html")
#
# @app.route('/doc_research',methods=['post'])
# def doc_research_post():
#     return "ok"


@app.route('/doc_view_booking/<sid>')
def doctor_view_booking(sid):
    d = Db()
    qry = "SELECT users.*,`booking`.* FROM `booking` INNER JOIN `users` ON `booking`.`userid`=`users`.`lid` WHERE `booking`.`scid`='"+sid+"'"
    res = d.select(qry)
    return render_template("doctor/view_booking.html", data=res)

@app.route('/doc_view_booking_search',methods=['post'])
def doc_view_booking_search():
    frm = request.form['d1']
    to = request.form['d2']
    d = Db()
    qry = "select booking.*, users.* from users inner join booking on booking.userid=users.lid where docid='"+str(session['lid'])+"' where date between '"+frm+"' and '"+to+"' "
    res = d.select(qry)
    return render_template("doctor/view_booking.html", data=res)


@app.route("/docviewpatients")
def docviewpatients():
    db=Db()
    qry="SELECT * FROM `users`"
    res=db.select(qry)
    return render_template("doctor/viewusers.html",data=res)




@app.route('/doc_view_profile')
def doctor_view_profile():
    db=Db()
    qry="SELECT * FROM `doctor` WHERE `lid`='"+session["lid"]+"'"
    res = db.selectOne(qry)
    return render_template("doctor/view_profile.html",res=res)
4
@app.route('/edit_doctor')
def doctor_edit_doctor():
    db=Db()
    qry="SELECT * FROM `doctor` WHERE `lid`='"+session["lid"]+"'"
    res = db.selectOne(qry)
    return render_template("doctor/editdoctor.html",res=res)


@app.route('/edit_heakthins')
def edit_heakthins():
    db=Db()
    qry="SELECT * FROM `healthinsurance` WHERE `lid`='"+session["lid"]+"'"
    res = db.selectOne(qry)
    return render_template("heakthins/editheakthins.html",res=res)

@app.route('/edit_research')
def edit_research():
    db=Db()
    qry="SELECT * FROM `research` WHERE `lid`='"+session["lid"]+"'"
    res = db.selectOne(qry)
    return render_template("research/editresearch.html",res=res)


@app.route('/doc_update_profile',methods=['post'])
def doc_update_profile():
    name = request.form['textfield']
    gender = request.form['textfield2']
    phone_number = request.form['textfield3']
    email = request.form['textfield4']
    db = Db()
    # location=request.form['textfield5']
    qualification = request.form['textfield6']
    if 'fileField' in request.files:
        image = request.files['fileField']
        if image.filename !="":
            image.save("D:\\Likhil\\Web\\Web\\static\\" + image.filename)

            p = "/static/doctor/" + image.filename
            qry = "UPDATE `doctor`SET NAME='" + name + "',gender='" + gender + "',phonenumber='" + phone_number + "',email='" + email + "',qualification='" + qualification + "',photo='"+p+"' WHERE lid='"+str(session["lid"])+"'"
            print(qry)

            db.update(qry)
        else:
            db=Db()
            qry = "UPDATE `doctor`SET NAME='" + name + "',gender='" + gender + "',phonenumber='" + phone_number + "',email='" + email + "',qualification='" + qualification + "' WHERE lid='"+str(session["lid"])+"'"
            print(qry)

            db.update(qry)
    else:
        qry = "UPDATE `doctor`SET NAME='" + name + "',gender='" + gender + "',phonenumber='" + phone_number + "',email='" + email + "',qualification='" + qualification + "' WHERE lid='"+str(session["lid"])+"'"
        print(qry)
        db.update(qry)

    # db=Db()
    # db.update(qry)

    return '''<script>alert('success');window.location='/dhome'</script>'''



@app.route('/heakthins_update_profile',methods=['post'])
def heakthins_update_profile():
    name = request.form['textfield']
    ph = request.form['textfield2']
    em = request.form['textfield4']
    pl = request.form['textfield5']
    pi = request.form['textfield6']
    po = request.form['textfield3']
    db = Db()
    # location=request.form['textfield5']
    if 'fileField' in request.files:
        image = request.files['fileField']
        if image.filename !="":
            image.save("D:\\Likhil\\Web\\Web\\static\\" + image.filename)

            p = "/static/doctor/" + image.filename
            qry = "UPDATE `healthinsurance`SET name='" + name + "',phonenumber='" + ph + "',email='" + em + "',place='" + pl + "',post='" + po + "',pin='" + pi + "',photo='"+p+"' WHERE lid='"+str(session["lid"])+"'"
            print(qry)
            db.update(qry)
        else:
            db=Db()
            qry = "UPDATE `healthinsurance`SET name='" + name + "',phonenumber='" + ph + "',email='" + em + "',place='" + pl + "',post='" + po + "',pin='" + pi + "' WHERE lid='" + str(
                session["lid"]) + "'"
            print(qry)
            db.update(qry)
    else:
        qry = "UPDATE `healthinsurance`SET name='" + name + "',phonenumber='" + ph + "',email='" + em + "',place='" + pl + "',post='" + po + "',pin='" + pi + "' WHERE lid='" + str(
            session["lid"]) + "'"
        print(qry)
        db.update(qry)

    # db=Db()
    # db.update(qry)

    return '''<script>alert('success');window.location='/hhome'</script>'''


@app.route('/research_update_profile',methods=['post'])
def research_update_profile():
    name = request.form['textfield']
    ph = request.form['textfield2']
    em = request.form['textfield4']
    pl = request.form['textfield5']
    pi = request.form['textfield6']
    po = request.form['textfield3']
    db = Db()
    # location=request.form['textfield5']
    if 'fileField' in request.files:
        image = request.files['fileField']
        if image.filename !="":
            image.save("D:\\Likhil\\Web\\Web\\static\\" + image.filename)

            p = "/static/doctor/" + image.filename
            qry = "UPDATE `research`SET name='" + name + "',phonenumber='" + ph + "',email='" + em + "',place='" + pl + "',post='" + po + "',pin='" + pi + "',photo='"+p+"' WHERE lid='"+str(session["lid"])+"'"
            print(qry)
            db.update(qry)
        else:
            db=Db()
            qry = "UPDATE `research`SET name='" + name + "',phonenumber='" + ph + "',email='" + em + "',place='" + pl + "',post='" + po + "',pin='" + pi + "' WHERE lid='" + str(
                session["lid"]) + "'"
            print(qry)
            db.update(qry)
    else:
        qry = "UPDATE `research`SET name='" + name + "',phonenumber='" + ph + "',email='" + em + "',place='" + pl + "',post='" + po + "',pin='" + pi + "' WHERE lid='" + str(
            session["lid"]) + "'"
        print(qry)
        db.update(qry)

    # db=Db()
    # db.update(qry)

    return '''<script>alert('success');window.location='/rhome'</script>'''




@app.route('/doc_add_research')
def doc_add_research():
    return  render_template("doctor/add research.html")

@app.route('/doc_add researchpost',methods=['post'])
def doc_add_researchpost():
    title=request.form['textfield']
    description=request.form['textfield2']
    content=request.form['textarea']
    image = request.files['fileField']
    image.save("C:\\Users\\Bilal Fahmi\\PycharmProjects\\vetapp\\static\\" + image.filename)
    path = "/static/" +image.filename
    db=Db()
    qry="insert into research(title,description,content,picture)VALUES('"+title+"','"+description+"','"+content+"','"+path+"') "
    db.insert(qry)
    return doc_add_research()

@app.route('/doc_view_research')
def doctor_view_research():
    db=Db()
    qry="SELECT * FROM `research` "
    res = db.select(qry)
    return render_template("doctor/view research.html", res=res)

@app.route('/doc_delete_research/<rid>')
def doc_research(rid):
    qry = "DELETE FROM `research` WHERE researchid='"+rid+"'"
    db=Db()
    res=db.delete(qry)
    return doctor_view_research()



@app.route('/edit_research/<rid>')
def doctor_edit_research(rid):
    db=Db()
    qry="SELECT * FROM `research` WHERE `researchid`='"+rid+"'"
    res = db.selectOne(qry)
    return render_template("doctor/edit research.html",res=res)


@app.route('/doc_edit_research_post',methods=['post'])
def doc_edit_research_post():
   description=request.form['textfield']
   title=request.form['textfield2']
   content = request.form['textarea']
   rid=request.form['hid']
   db = Db()
   dt=str(datetime.datetime.now()).replace("-","").replace(" ","_").replace(":","")
   if 'pic' in request.files:
       image = request.files['pic']
       if image.filename!="":# has image
           image.save("C:\\Users\\Bilal Fahmi\\PycharmProjects\\vetapp\\static\\" + dt+".jpg")
           path = "/static/" + dt+".jpg"
           qry="UPDATE research SET `description`='"+description+"',`title`='"+title+"',`content`='"+content+"',`picture`='"+ path+"' WHERE researchid='"+rid+"'"
           db.update(qry)
           return 'ok'

       else:                                #browser issue
           qry = "UPDATE research SET `description`='" + description +"' ,`title`='" + title + "',`content`='"+content+"' WHERE researchid='" +rid+"'"
           db.update(qry)
           return 'ok'

   else:                                    #no image
       qry = "UPDATE research SET `description`='" + description + "' ,`title`='" + title + "',`content`='"+content+"' WHERE researchid='" +rid+ "'"
       db.update(qry)
       return 'ok'

# @app.route('/')
# def index():
#    return render_template('user/index.html')

@app.route('/indexlogin')
def indexlogin():
   return render_template('user/indexlogin.html')

@app.route('/admin_temp')
def admin_temp():
    return render_template('admin/index.html')


#----------------------_ANDRPOID_METHODS---------------------------------




@app.route('/user_login', methods=['post'])
def and_login():
    db=Db()
    username=request.form['username']
    password=request.form['password']
    qry="SELECT * FROM login WHERE username='"+username+"' AND PASSWORD='"+password+"'"
    res=db.selectOne(qry)
    if res is None:
        return jsonify(status="no")
    else:
        type=res['type']
        if type=="user":

            qry="SELECT * FROM `users` WHERE lid='"+str(res['lid'])+"'"
            resa=db.selectOne(qry)



            print('ok')
            return jsonify(status="ok",lid=res['lid'],type=type,image=resa['photo'],name=resa['name'])
        else:
            return jsonify(status="no")


@app.route("/user_register", methods=['post'])
def and_signup():
    name=request.form['name']
    gender=request.form['gender']
    email=request.form['email']
    phone = request.form['phone']
    image=request.form['img']
    place=request.form['place']

    district=request.form['district']
    pin=request.form['pin']
    password=request.form['phone']

    import time
    dt=time.strftime("%Y%m%d_%H%M%S")
    p=static_path + "user_image\\" + dt+".jpg"
    import base64
    with open(p,"wb") as h:
        h.write(b64decode(image))
        


    path = "/static/user_image/" +  dt+".jpg"
    qry="insert into login(`username`,`password`,`type`)values('"+email+"','"+password+"','user')"
    db=Db()
    lid=db.insert(qry)
    qry1="INSERT INTO users(name,gender,phonenumber,email,photo,place,district,pin,lid)VALUES('"+name+"','"+gender+"','"+phone+"','"+email+"','"+path+"','"+place+"','"+district+"','"+pin+"','"+str(lid)+"')"
    db.insert(qry1)
    return jsonify(status="ok")


@app.route('/and_change_password', methods=['post'])
def and_change_password():
    lid = request.form['lid']
    current_password = request.form['currentpassword']
    new_password = request.form['newpassword']
    d = Db()
    qry = "select * from login where password='"+current_password+"'"
    res =d.selectOne(qry)
    if res!=None:
        qry = "update login set password='"+new_password+"' where lid='"+str('lid')+"' "
        res = d.update(qry)
        return jsonify(status='ok')
    else:
        return jsonify(status='no')


@app.route('/and_view_profile', methods=['post'])
def and_view_profile():
    lid = request.form['lid']
    d = Db()
    qry = "SELECT * FROM users where lid='"+lid+"'"
    res = d.selectOne(qry)
    return jsonify(status='ok', name=res['name'], gender=res['gender'], place=res['place'], district=res['district'], pincode=res['pin'], email=res['email'], phone=res['phonenumber'])


@app.route("/user_view_doctors",methods=['post'])
def and_doctor():
    name=request.form["name"]
    qry="select * from doctor where name like '%"+name+"%'"
    db=Db()
    res=db.select(qry)
    return jsonify(status='ok',data=res)


@app.route("/user_p_Page",methods=['post'])
def user_p_Page():
    lid=request.form["lid"]
    db=Db()
    qry="SELECT * FROM users WHERE lid='"+lid+"'"
    res=db.selectOne(qry)
    return jsonify(status='ok',data=res)

@app.route("/userviewquestions",methods=['post'])
def userviewquestions():
    lid=request.form["lid"]
    db=Db()
    res=db.select("SELECT * FROM `question` WHERE userid='"+lid+"'")
    return jsonify(status='ok',data=res)

@app.route("/useraddquestions",methods=['post'])
def useraddquestions():
    db=Db()
    uid=request.form["lid"]
    question=request.form["question"]
    qry="INSERT INTO `question` (`userid`,`questions`,`reply`,`status`,`date`) VALUES ('"+uid+"','"+question+"','pending','pending',CURDATE())"
    db.insert(qry)
    return jsonify(status="ok")

@app.route("/user_Change_Password",methods=['post'])
def user_Change_Password():
    password=request.form["confirm_password"]
    lid=request.form["lid"]
    db=Db()
    qry="UPDATE login SET `password`='"+password+"' WHERE `lid`='"+lid+"'"
    db.insert(qry)
    return jsonify(status='ok')


@app.route("/useraddpost",methods=['post'])
def useraddpost():
    lid=request.form["lid"]
    p=request.form["post"]
    db=Db()
    qry="INSERT INTO post(post,postdate,lid) VALUES ('"+p+"',CURDATE(),'"+lid+"')"
    db.insert(qry)
    return jsonify(status='ok')


@app.route("/andviewposts",methods=['post'])
def andviewposts():
    qry="SELECT `post`.*,`users`.* FROM `post` INNER JOIN `users` ON `post`.`lid`=`users`.`lid` ORDER BY `postid` DESC"
    db=Db()
    res=db.select(qry)
    return jsonify(status='ok',data=res)


@app.route("/and_tips",methods=['post'])
def and_tips():
    db=Db()
    res=db.select("SELECT * FROM tips")
    return jsonify(status='ok',data=res)


@app.route("/and_viewvaccine",methods=['post'])
def and_viewvaccine():
    db=Db()
    res=db.select("SELECT * FROM vaccine")
    return jsonify(status='ok',data=res)












@app.route("/uind")
def uind():
    return render_template("index.html")



#research

@app.route('/user_register')
def hos_register():
    return render_template('user_registration.html')




@app.route('/viewandapproveital')
def viewandapprovehospital():
    db = Db()
    qry = "SELECT * FROM research WHERE STATUS='pending'"
    res = db.select(qry)
    print(res)
    return render_template('admin/viewandapprovehospital.html', data=res)

@app.route('/search_hospital_post', methods=['post'])
def search_hospital_post():
    search_name = request.form['textfield']

    db = Db()
    qry = "SELECT * FROM research WHERE hospital_name LIKE '%"+search_name+"%' and STATUS='pending'"
    res = db.select(qry)
    print(res)

    return render_template('admin/viewandapprovehospital.html', data=res)


@app.route('/approvehospital/<hlid>')
def approvehospital(hlid):
    db=Db()
    qry="UPDATE research SET STATUS='Approved' WHERE login_id='"+hlid+"'"
    res=db.update(qry)
    return '''<script>alert('Approved');window.location='/viewandapprovehospital'</script>'''

@app.route('/rejecthospital/<hlid>')
def rejecthospital(hlid):
    db=Db()
    qry="UPDATE research SET STATUS='Rejected' WHERE login_id='"+hlid+"'"
    res=db.update(qry)
    return '''<script>alert('Reject');window.location='/viewandapprovehospital'</script>'''


@app.route('/viewapprovehosp')
def viewapprovehosp():
    db = Db()
    qry= "SELECT * FROM research WHERE STATUS='Approved'"
    res = db.select(qry)
    print(res)
    return render_template('admin/viewapprovehosp.html', data=res)

@app.route('/search_approved_post', methods=['post'])
def search_approved_post():
    search_name = request.form['textfield']
    db = Db()
    qry = "SELECT * FROM research WHERE hospital_name LIKE '%"+search_name+"%' AND `status`='Approved'"
    res = db.select(qry)
    print(res)
    return render_template('admin/viewapprovehosp.html',data=res)
@app.route('/viewrejecterhospital')
def viewrejecterhospital():
    db = Db()
    qry = "SELECT * FROM research WHERE STATUS='rejected'"
    res = db.select(qry)
    print(res)
    return render_template('admin/viewrejecterhospital.html',data=res)

@app.route('/search_rejectedhosp_post', methods=['post'])
def search_rejectedhosp_post():
    search_name = request.form['textfield']

    db = Db()
    qry = "SELECT * FROM research WHERE hospital_name LIKE '%" + search_name + "%' AND `status`='Rejected'"
    res = db.select(qry)
    print(res)

    return render_template('admin/viewrejecterhospital.html',data=res)


@app.route("/adminviewusers")
def adminviewusers():
    qry="SELECT * FROM `users`"
    db=Db()
    res=db.select(qry)
    return render_template("admin/viewusers.html",data=res)



@app.route('/adminchange_password')
def adminchange_password():
    return render_template('admin/change_password.html')
@app.route('/changepassoword_post',methods=['post'])
def adminchange_passwordpost():
    old_password=request.form['textfield']
    new_password=request.form['textfield2']
    conf_password=request.form['textfield3']
    lid=session["lid"]
    if new_password==conf_password:
        if session["pass"]==old_password:
            db = Db()
            qry = "update login set password='"+new_password+"' where lid='"+str(lid)+"'"
            res = db.update(qry)
            print(res)

            return '''<script>alert('Password chnaged Successfully');window.location='/'</script>'''
        else:
            return '''<script>alert('Missmatch in password. Try again');window.location='/'</script>'''
    else:
        return '''<script>alert('Missmatch in password. Try again');window.location='/'</script>'''


@app.route("/hspregistration")
def hspregistration():
    return render_template("hsp_registeration.html")



@app.route("/hosp_viewdoctor")
def hosp_viewdoctor():
    db=Db()
    qry="SELECT * FROM `doctor` WHERE `hsplid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("research/viewdoctors.html",data=res)


@app.route("/hosp_deletedoctor/<did>")
def hosp_deletedoctor(did):
    db=Db()
    qry="delete from doctor where doctorid='"+did+"'"
    db.delete(qry)
    return "<script>alert('Doctor deleted successfully');window.location='/hosp_viewdoctor'</script>"





@app.route("/doctorsentcomplaint")
def doctorsentcomplaint():
    return  render_template("doctor/sentcomplaint.html")

@app.route("/doctorsentcomplaintpost",methods=['post'])
def doctorsentcomplaintpost():
    complaint=request.form["textarea"]
    db=Db()
    qry="INSERT INTO `question` (`userid`,`questions`,`reply`,`status`,`date`) VALUES ('"+str(session['lid'])+"','','pending','pending',CURDATE())"
    db=Db()
    db.insert(qry)
    return "<script>alert('Complaint sent successfully');window.location='/doctorsentcomplaint'</script>"

@app.route("/doctorviewcomplaint")
def doctroviewcomplaint():
    uid=session["lid"]
    qry="select * from question WHERE userid='"+uid+"'"
    db=Db()
    res=db.select(qry)
    return render_template("doctor/viewcomplaints.html",data=res)




@app.route("/doctoraddprescription/<bkid>")
def doctoraddprescription(bkid):
    session['bkid']=bkid
    return render_template("doctor/add_prescription.html")

@app.route("/doctoraddprescriptionpost",methods=['post'])
def doctoraddprescriptionpost():
    db=Db()
    p=request.form["prescription"]
    qry="INSERT INTO `prescription` (`bkid`,`prescription`,`pdate`) VALUES ('"+str(session['bkid'])+"','"+p+"',CURDATE())"
    db.insert(qry)
    return "<script>alert('Prescription added successfully');window.location='/doctoraddmedicines'</script>"


@app.route("/doctoraddlabdetails")
def doctroaddlabdetails():
    db=Db()
    qry="SELECT * FROM labdata WHERE bkid='"+str(session['bkid'])+"'"
    res=db.select(qry)
    return render_template("doctor/addlabinfo.html",res=res)


@app.route("/doctoraddlabdetailspost",methods=['post'])
def doctoraddlabdetailspost():
    lab=request.form["lab"]
    qry="INSERT INTO `labdata` (`labname`,`bkid`) VALUES ('"+lab+"','"+str(session['bkid'])+"')"
    db=Db()
    db.insert(qry)
    return "<Script>alert('Labinfo added successfully');window.location='/doctoraddlabdetails'</script>"


@app.route("/doctordeletetest/<id>")
def doctordeletetest(id):
    db=Db()
    db.delete("delete  FROM labdata WHERE lid='"+id+"'")
    return "<Script>alert('Test deleted successfully');window.location='/doctoraddlabdetails'</script>"




@app.route("/doctorbookingmore/<bid>")
def doctorbookingmore(bid):
    db=Db()
    qry="SELECT * FROM labdata WHERE bkid='"+bid+"'"
    l=db.select(qry)
    qry="SELECT `medicneentry`.*,`medicines`.* FROM `medicines` INNER JOIN `medicneentry` ON `medicneentry`.`mid`=`medicines`.`mid` WHERE `medicneentry`.`bkid`='"+bid+"'"
    b=db.select(qry)
    return render_template("doctor/more.html",l=l,b=b)


@app.route("/mx")
def mx():
    return render_template("mains.html")


@app.route("/viewreply",methods=['post'])
def viewreply():
    lid=request.form["lid"]
    db=Db()
    res=db.select("SELECT * FROM question WHERE userid='"+lid+"'")
    return jsonify(status='ok',data=res)



@app.route("/send_complaint",methods=['post'])
def sendcomplaint():
    lid=request.form['lid']
    complaint=request.form['complaint']

    db=Db()

    qry="INSERT INTO `question` (`userid`,`questions`,`reply`,`status`,`date`) VALUES ('"+lid+"','"+complaint+"','pending','pending',CURDATE())"
    db.insert(qry)

    return jsonify(status='ok')

@app.route("/userfeedback",methods=['post'])
def userfeedback():
    db=Db()
    lid=request.form["lid"]
    feedback=request.form["feedback"]
    qry="INSERT INTO `feedback` (`lid`,`feedback`,`fdate`) VALUES ('"+lid+"','"+feedback+"',CURDATE())"
    db.insert(qry)
    return jsonify(status='ok')



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


