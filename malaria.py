from flask import Flask, render_template, request, session, redirect, jsonify
from DBConnection import Db

app = Flask(__name__)
app.secret_key="haii"


@app.route('/index')
def index():
    return render_template('/ADMIN/blank.html')

@app.route('/index1')
def index1():
    return render_template('/LAB/blank.html')

@app.route('/index2')
def index2():
    return render_template('/LAB/blank.html')

@app.route('/index3')
def index3():
    return render_template('/USER/blank.html')




@app.route('/viewresult')
def viewresult():
    db=Db()
    qry="SELECT `user_registration`.*,`medical_report`.`date`,`medical_report`.`report_id` FROM `user_registration`,`medical_report` WHERE `medical_report`.`lid`='"+str(session['lbid'])+"' AND `medical_report`.`user_id`=`user_registration`.`login_id`"
    res=db.select(qry)
    print(qry)
    return render_template('/LAB/viewresult.html',data=res)

@app.route('/viewresultpost',methods=['post'])
def viewresultpost():
    name=request.form["searchname"]
    db=Db()
    qry="SELECT `user_registration`.*,`medical_report`.`date` FROM `user_registration`,`medical_report` WHERE `medical_report`.`lid`='"+str(session['lbid'])+"' AND `medical_report`.`user_id`=`user_registration`.`login_id` AND `user_registration`.`name` like '%"+name+"%'"
    res=db.select(qry)
    return render_template('/LAB/viewresult.html',data=res)



@app.route('/result_view/<id>')
def result_view(id):
    db=Db()
    qry="SELECT * FROM `medical_report` WHERE `report_id`='"+str(id)+"'"
    res=db.selectOne(qry)
    return render_template('/LAB/result_view.html',data=res)


@app.route('/logins')
def login():
    return render_template('login.html')

@app.route('/')
def lsss():
    return render_template('new_user.html')


@app.route('/userhome')
def userhome():
    return render_template('/USER/userhome.html')

@app.route('/lab_details')
def lab_details():
    db = Db()
    qry = "SELECT * from  `lab_registration`"
    res = db.select(qry)
    return render_template('ADMIN/lab_details.html',data=res)



@app.route('/lab_delete/<docid>')
def doctor_delete(docid):
    db = Db()

    qry="delete from lab_registration where doctor_id='"+docid+"' "
    db.delete(qry)


    qry = "SELECT * from  `lab_registration`"
    res = db.select(qry)
    return render_template('ADMIN/lab_details.html',data=res)






@app.route('/forwarduser/<reqid>')
def forwarduser(reqid):
    db = Db()
    qry = "SELECT * from  `doctor_registration`"
    res = db.select(qry)
    return render_template('USER/lab_details.html',data=res,reqid=reqid)



@app.route('/forwardtousersubmit',methods=['post'])
def forwardtousersubmit():
    dids=request.form.getlist('ids')
    recordid=request.form['recordid']


    print(dids,"ggg",recordid,"hh")


    db=Db()

    for i in dids:
        qry="INSERT INTO `forward_rec` (`recordid`,`doctorloginid`) VALUES ('"+recordid+"','"+i+"')"
        db.insert(qry)

    return "<script>alert('Forwarded Successfully');window.location='/adminputs'</script>"




@app.route('/doctor_verification/<id>')
def doctor_verification(id):
    db=Db()
    qry = "SELECT * FROM `lab_registration` WHERE `doctor_id`='"+str(id)+"'"
    res = db.selectOne(qry)
    session['did']=id
    return render_template('ADMIN/lb_verification.html',data=res)




@app.route('/doctor_verificationedit/<id>')
def doctor_verificationedit(id):
    db=Db()
    qry = "SELECT * FROM `doctor_registration` WHERE `doctor_id`='"+str(id)+"'"
    res = db.selectOne(qry)
    session['did']=id
    return render_template('ADMIN/doctor_edit.html',data=res)






@app.route('/doctor_verification_post',methods=['POST'])
def doctor_verification_post():
    b1=request.form['button']
    db = Db()
    qry = "SELECT * FROM `doctor_registration` WHERE `doctor_id`='" + str(session['did']) + "'"
    res = db.selectOne(qry)

    if b1=="Approve":
        qry1="UPDATE `login_table` SET `type`='doctor' WHERE `lid`='"+str(res['login_id'])+"'"
        res1=db.update(qry1)
        return doctor_details()

    else:
#        qry1="DELETE FROM `doctor_registration` WHERE `doctor_id`='"+str(session['did'])+"'"
#       qry2="DELETE FROM `login_table` WHERE `lid`='"+str(res['login_id'])+"'"
#        res=db.delete(qry1)
 #       res1=db.delete(qry2)
       qry1="UPDATE `login_table` SET `type`='waiting' WHERE `lid`='"+str(res['login_id'])+"'"
       res=db.update(qry1)
       return doctor_details()




@app.route('/feedback')
def feedback():
    return render_template("ADMIN/feedback.html")
@app.route('/feedback_post',methods=['POST'])
def feedback_post():
    db=Db()
    utype=request.form["type"]
    if utype=="lab":
        qry="SELECT * FROM `lab_feedback`,`lab` WHERE `lab_feedback`.`user_type`='"+utype+"' AND `lab_feedback`.`login_id`=`lab`.`login_id`"
        res = db.select(qry)
    elif utype=="doctor":
        qry1="select * from `lab_feedback`,`doctor_registration` where `lab_feedback`.`user_type`='"+utype+"' and `lab_feedback`.`login_id`=`doctor_registration`.`login_id`"
        res = db.select(qry1)
    else:
        qry2="SELECT * FROM `lab_feedback`,`user_registration` WHERE `lab_feedback`.`user_type`='"+utype+"' AND `lab_feedback`.`login_id`=`user_registration`.`login_id`"
        res = db.select(qry2)

    return render_template('ADMIN/feedback.html',data=res)







@app.route('/lab_verification/<id>')
def lab_verification(id):
    db = Db()
    qry = "select * from `lab` where `lab_id`='"+str(id)+"'"
    res = db.selectOne(qry)
    session['lid'] = id
    return render_template('ADMIN/lab_verification.html',data=res)

@app.route('/lab_verification_post',methods=['POST'])
def lab_verification_post():
    b1=request.form['s1']
    db = Db()
    qry = "SELECT * FROM `lab` WHERE `lab_id`='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    if b1 == "Approve":
        qry1 = "UPDATE `login_table` SET `type`='lab' WHERE `lid`='" + str(res['login_id']) + "'"
        res1 = db.update(qry1)
        return lab_details()
    else:
 #       qry1="DELETE FROM `lab` WHERE `lab_id`='"+str(session['lid'])+"'"
  #      qry2="DELETE FROM `login_table` WHERE `lid`='"+str(res['login_id'])+"'"
   #     res=db.delete(qry1)
    #    res1=db.delete(qry2)
        qry1 = "UPDATE `login_table` SET `type`='waiting' WHERE `lid`='" + str(res['login_id']) + "'"
        res = db.update(qry1)

        return lab_details()


@app.route('/view_rejectedlist')
def view_rejectedlist():

    return render_template('ADMIN/view_rejectedlist.html')

@app.route('/view_more/<id>')
def view_more(id):
    utype=session['utype']
    db = Db()
    if utype == 'Doctor':

        qry = "SELECT * FROM `doctor_registration` WHERE `login_id`='" + str(id) + "'"
        res = db.selectOne(qry)
        session['did'] = id
        return render_template('ADMIN/lb_verification.html', data=res)
    else:
       qry2="SELECT * FROM `lab` WHERE `login_id`='" + str(id) + "'"
       res = db.selectOne(qry2)
       session['lbid'] = id
       return render_template('ADMIN/lab_verification.html', data=res)

@app.route('/view_rejectedlists_post',methods=["POST"])
def view_rejectedlists_post():
        db=Db()
        utype=request.form['type']
        session['utype']=utype
        if utype=='Doctor':
            qry1="SELECT `doctor_registration`.`name`,`doctor_registration`.`doctor_id` as lid,`login_table`.`lid` FROM `doctor_registration` ,`login_table` WHERE `login_table`.`type`='waiting' AND `login_table`.`lid`=`doctor_registration`.`login_id`"

            res = db.select(qry1)
            return render_template('ADMIN/view_rejectedlist.html', data=res)

        else:
            qry2="SELECT `lab`.`name`,`lab`.`lab_id` as lid,`login_table`.`lid` FROM `lab`,`login_table` WHERE `login_table`.`type`='waiting' AND `login_table`.`lid`=`lab`.`login_id`"
            res=db.select(qry2)
            return render_template('ADMIN/view_rejectedlist.html',data=res)



@app.route('/ud/<id>')
def ud(id):
    db = Db()
    qry = "SELECT * FROM `user_registration` WHERE `user_id`='" + str(id) + "'"
    res = db.selectOne(qry)

    return render_template('ADMIN/ud.html',data=res)


#@app.route('/ud_post',methods=['POST'])
#def ud_post():
   # db = Db()
   # qry = "SELECT * FROM `user_registration` WHERE `user_id`='" + str(session['usid']) + "'"
    #res = db.selectOne(qry)

    #return render_template('ADMIN/ud.html',data=res)


@app.route('/user_details')
def user_details():
    db = Db()
    qry = "SELECT * FROM `user_registration` "
    res = db.select(qry)
    return render_template('ADMIN/user_details.html', data=res)





@app.route('/labuser_details')
def labuser_details():
    db = Db()
    qry = "SELECT * FROM `user_registration` "
    res = db.select(qry)
    return render_template('LAB/user_details.html', data=res)


path="D:\\backups\\\maniyoormalaria\\maniyoormalaria\\static\\uploads\\"

@app.route('/labuploadphoto/<plid>')
def labuploadphoto(plid):
    return render_template('/LAB/inputs.html',plid=plid)





@app.route('/labuploadphotopost',methods=['post'])
def labuploadphotopost():
    a1=request.files["a1"]
    plid=request.form["plid"]
    dlid=str(session["usid"])


    import time
    timestr = time.strftime("%Y%m%d_%H%M%S")
    a1.save(path+timestr+".jpg")


    fname="/static/uploads/"+timestr+".jpg"

    import tensorflow as tf
    import sys
    import os

    # Disable tensorflow compilation warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    import tensorflow as tf

    # image_path = sys.argv[1]
    # image_path="C:\\Users\\ELCOT-Lenovo\\Documents\\images\\sign_dataset\\test\\A\\color_0_0016"
    # Read the image_data
    image_data = tf.gfile.FastGFile(path+timestr+".jpg",'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile(r"D:\backups\maniyoormalaria\maniyoormalaria\logsold\output_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile(r"D:\backups\maniyoormalaria\maniyoormalaria\logsold\output_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        rs=""
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            rs=rs+human_string+":"+str(score)+"\n"
            print('%s (score = %.5f)' % (human_string, score))

    qry="INSERT INTO uploads (`plid`,`dlid`,`fname`,`result`,`fdate`) VALUES ('"+plid+"','"+dlid+"','"+fname+"','"+rs+"',NOW())"
    db=Db()
    db.insert(qry)


    return render_template('/Lab/inputs.html',rs=rs)

@app.route('/doctorhome')
def doctorhome():
    return render_template('LAB/doctorhome.html')


@app.route('/labhome')
def labhome():
    return render_template('LAB/labhome.html')


@app.route('/userviewhistory')
def userviewhistory():
    qry="SELECT uploads.*,`lab_registration`.*  FROM `lab_registration` INNER JOIN uploads ON `lab_registration`.`login_id`=`uploads`.`dlid` WHERE `uploads`.`plid`='"+str(session['usid'])+"'"
    db=Db()
    res=db.select(qry)
    return render_template('/USER/doctor_details.html')


@app.route('/adminuserviewhistory')
def adminuserviewhistory():
    qry="SELECT uploads.*,`lab_registration`.*,`user_registration`.*  FROM `lab_registration` INNER JOIN uploads ON `lab_registration`.`login_id`=`uploads`.`dlid` inner join `user_registration` on `user_registration`.`login_id`=`uploads`.`plid` WHERE `uploads`.`plid`='"+str(session['usid'])+"'"
    print(qry)
    db=Db()
    res=db.select(qry)
    return render_template('/ADMIN/doctor_details.html')




@app.route('/docfb')
def docfb():
    return render_template('LAB/docfb.html')

@app.route('/docfb_post', methods=["post"])
def docfb_post():
    db=Db()
    feedback=request.form["fd"]
    qry="INSERT INTO `lab_feedback`(`login_id`,`feedback`,`date`,`user_type`)VALUES('"+str(session['drid'])+"','"+feedback+"',curdate(),'doctor')"
    res=db.insert(qry)
    return '<script>alert("added successfully");window.location="/doctorhome"</script>'



@app.route('/docpres')
def docpres():

    db=Db()
    qry="SELECT * FROM `user_registration` AS u1,`patient_record` AS p1 WHERE u1.`user_id`=p1.`user_id` AND p1.`doctor_id`='"+str(session['drid'])+"'"
    res=db.select(qry)

    return render_template('LAB/docpres.html',data=res)





@app.route('/delete_pres/<id>')
def delete_pres(id):
    session['rid'] = id
    db=Db()
    q2 = "DELETE FROM `patient_record` WHERE `record_id`='" + str(session['rid']) + "'"
    res = db.delete(q2)
    return render_template('LAB/docpres.html')



@app.route('/labdetails')
def labdetails():
    return render_template('LAB/labdetails.html')

@app.route('/labviewmore')
def labviewmore():
    return render_template('LAB/labviewmore.html')

@app.route('/presupdate/<id>')
def presupdate(id):
    session['record_id']=id
    return render_template('LAB/presupdate.html')

@app.route('/presupdate_post',methods=['post'])
def presupdate_post():
    pd=request.form['pd']

    db=Db()
    qry="UPDATE `patient_record` SET `prescription`='"+pd+"' WHERE `record_id`='"+str(session['record_id'])+"'"
    res=db.update(qry)
    #return render_template('LAB/presupdate.html')
    return '<script>alert("Updated successfully");window.location="/docpres"</script>'

@app.route('/doctor_registration')
def doctor_registration():
    return render_template('LAB/lab_registration.html')




@app.route('/lab_registration_post',methods=["POST"])
def lab_registration_post():
    db=Db()
    name=request.form["name"]
    onmae=request.form["quali"]

    email=request.form["em"]
    phone=request.form["ph"]
    place=request.form["plc"]
    gender=request.form["RadioGroup1"]
    dob=request.form["dob2"]
    district=request.form["dstrct"]
    photo=request.files["photo"]
    password=request.form["ps"]
    qry = "INSERT INTO login_table(`username`,`password`,`type`)VALUES('" + email + "','" + password + "','lab')"
    lid = db.insert(qry)
    filename = "doc_" + str(lid) + ".jpg"
    photo.save("D:\\backups\\static\\doctor_pics\\" + filename)
    qry2="INSERT INTO lab_registration (`lname`,`oname`,`email`,`phone`,`place`,`gender`,`dob`,`district`,`photo`,`login_id`) VALUES ('"+name+"','"+onmae+"','"+email+"','"+phone+"','"+place+"','"+gender+"','"+dob+"','"+district+"','"+filename+"','"+str(lid)+"')"
    res = db.insert(qry2)
    #return render_template('LAB/lab_registration.html')
    return '<script>alert("Registration successfull");window.location="/signuplab"</script>'






@app.route('/doctor_registration_postedit',methods=["POST"])
def doctor_registration_postedit():
    db=Db()
    name=request.form["name"]
    qualification=request.form["quali"]
    experience=request.form["exprnc"]
    specialisation=request.form["spc"]
    email=request.form["em"]
    phone=request.form["ph"]
    place=request.form["plc"]
    gender=request.form["RadioGroup1"]
    dob=request.form["dob2"]
    district=request.form["dstrct"]
    lid=request.form["lid"]

    qry2="update doctor_registration set name='"+name+"',`qualification`='"+qualification+"',`experience`='"+experience+"',`specialization`='"+specialisation+"',`email`='"+email+"',`phone`='"+phone+"',`place`='"+place+"',`gender`='"+gender+"',`dob`='"+dob+"',`district`='"+district+"' where `login_id`='"+lid+"'"
    print(qry2)
    res = db.insert(qry2)
    #return render_template('LAB/lab_registration.html')
    return '<script>alert("Updation successfull");window.location="/doctor_details"</script>'







@app.route('/logout')
def logout():
    return redirect('/')


@app.route('/p_details')
def p_details():
    db = Db()
    qry = "SELECT * FROM `user_registration` where login_id IN (SELECT `lid` FROM `medical_report` WHERE `report_id` IN (SELECT `recordid` FROM `forward_rec` WHERE `doctorloginid`='"+str(session["usid"])+"'))"
    res = db.select(qry)
    return render_template('LAB/p_details.html', data=res)

@app.route('/p_details_viewmore/<id>')
def p_details_viewmore(id):
    db = Db()
    qry = "SELECT * FROM `user_registration` WHERE `user_id`='" + str(id) + "'"
    res = db.selectOne(qry)
    return render_template('LAB/p_details_viewmore.html',data=res)

@app.route('/prescription/<reportid>')
def prescription(reportid):
    db=Db()

    qry="select * from `medical_report` where `report_id`='"+str(reportid)+"'"
    res=db.selectOne(qry)
    return render_template('LAB/prescription.html',data=res,reportid=reportid)


@app.route('/prescriptionnew/<id>')
def prescriptionnew(id):
    db=Db()
    session['userid']=id
    qry="select * from `medical_report` where `lid`='"+str(id)+"'"
    res=db.selectOne(qry)
    return render_template('LAB/prescription.html',data=res)





@app.route('/prescription_post', methods=["POST"])
def prescription_post():
    pres=request.form["prescription"]
    db=Db()
    doclogid=session['userid']
    reportid=request.form['reportid']


    qry="UPDATE `forward_rec` SET `suggestion`='"+pres+"' WHERE `doctorloginid`='"+str(session['usid'])+"' AND `recordid`='"+reportid+"'"
    print(qry)
    db.insert(qry)
   # return render_template('LAB/prescription.html')
    return '<script>alert("Prescription Submitted successfully");window.location="/p_details"</script>'


@app.route('/labfb')
def labfb():
    return render_template('LAB/labfb.html')

@app.route('/labfb_post', methods=["post"])
def labfb_post():
    db=Db()
    feedback=request.form["fd"]
    qry="INSERT INTO `lab_feedback`(`login_id`,`feedback`,`date`,`user_type`)VALUES('"+str(session['lbid'])+"','"+feedback+"',curdate(),'lab')"
    res=db.insert(qry)
    return '<script>alert("added successfully");window.location="/labhome"</script>'





@app.route('/labreg')
def labreg():
    return render_template('LAB/labreg.html')
@app.route('/labreg_post',methods=["post"])
def labreg_post():
    name=request.form["nm"]
    place=request.form["pl"]
    district=request.form["dstrct"]
    phone=request.form["ph"]
    email=request.form["em"]
    license=request.form["lic"]
    latitude=request.form["la"]
    longitude=request.form["lon"]
    password=request.form["password"]
    db=Db()
    qry="INSERT INTO login_table(`username`,`password`,`type`)VALUES('"+email+"','"+password+"','pending')"
    lid=db.insert(qry)
    qry2="INSERT INTO lab(`name`,`place`,`district`,`phno`,`email`,`license_num`,`lattitude`,`longitude`,`login_id`,`password`) VALUES ('"+name+"','"+place+"','"+district+"','"+phone+"','"+email+"','"+license+"','"+latitude+"','"+longitude+"','"+str(lid)+"','"+password+"')"
    res=db.insert(qry2)
    return '<script>alert("Registration successfull");window.location="/"</script>'
# return render_template('LAB/labreg.html')


@app.route('/labupload/<id>')
def labupload(id):
    db = Db()
    qry = "SELECT * FROM `user_registration` WHERE `user_id`='" + str(id) + "'"
    res = db.selectOne(qry)
    session['lbusr_id']=id
    return render_template('LAB/labupload.html')




@app.route('/labupload_post',methods=["post"])
def labupload_post():
     cp=request.form["cp"]
     trestbps=request.form["tr"]
     chol=request.form["ch"]
     fbs=request.form["fb"]
     resting=request.form["res"]
     thalx=request.form["thl"]
     exang=request.form["ex"]
     oldpeak=request.form["op"]
     slope=request.form["sl"]
     cab=request.form["ca"]
     thal=request.form["tl"]
     num=request.form["nm"]
     db=Db()
     qry1="SELECT * FROM `user_registration` WHERE `login_id`='"+str(session['lbusr_id'])+"'"
     res1=db.selectOne(qry1)
     qry="INSERT INTO `medical_report`(`lid`,`user_id`,`date`,`dob`,`sex`,`cp`,`trestbps`,`chol`,`fbs`,`resting`,`thalx`,`exang`,`oldpeak`,`slope`,`cab`,`thal`,`num`)VALUES('"+str( session['lbid'])+"','"+str( session['lbusr_id'])+"',CURDATE(),'"+str(res1['dob'])+"','"+res1['gender']+"','"+cp+"','"+trestbps+"','"+chol+"','"+fbs+"','"+resting+"','"+thalx+"','"+exang+"','"+oldpeak+"','"+slope+"','"+cab+"','"+thal+"','"+num+"')"
     res=db.update(qry)
     return '<script>alert("Uploaded successfully");window.location="/upload_result"</script>'


@app.route('/upload_result')
def upload_result():
    db=Db()
    qry="SELECT * FROM `user_registration`"
    res=db.select(qry)
    return render_template('LAB/upload_result.html',data=res)


@app.route('/upload_result_post',methods=["POST"])
def upload_result_post():
    db=Db()
    name=request.form["nm"]

    qry="SELECT * FROM `user_registration` WHERE `name` like '%"+name+"%'"
    res = db.select(qry)
    return render_template('LAB/upload_result.html',data=res)

@app.route('/feedback_edit')
def feedback_edit():
    return render_template('USER/feedback_edit.html')

@app.route('/admhomes')
def admhomes():
    return render_template('ADMIN/adminhome.html')




@app.route('/report_view_more/<id>')
def report_view_more(id):
    db = Db()
    qry = "SELECT * FROM `medical_report` WHERE `report_id`='" + str(id) + "'"
    res = db.selectOne(qry)
    return render_template('/USER/result_view.html', data=res)

    return render_template('USER/report_view_more.html')

@app.route('/user_registration')
def user_registration():
    return render_template('USER/user_registration.html')

@app.route('/user_home')
def user_home():

    return render_template('USER/user_home.html')

@app.route('/user_registration_post',methods=["post"])
def user_registration_post():
    name = request.form["nm"]
    dob = request.form["dob"]
    place = request.form["place"]
    dstrct = request.form["dstrct"]
    ph = request.form["phn"]
    em = request.form["email"]
    gen = request.form["RadioGroup1"]
    photo = request.files["photo"]
    pswd = request.form["ps"]
    db = Db()
    qry = "INSERT INTO login_table(`username`,`password`,`type`)VALUES('" + em + "','" + pswd + "','user')"
    lid = db.insert(qry)

    filename="user_"+str(lid)+".jpg"
    photo.save("D:\\backups\\pondichery\\heart\\static\\user_pics\\"+filename)
    qry2="INSERT INTO `user_registration`(`name`,`dob`,`place`,`district`,`phone`,`email`,`gender`,`photo`,`login_id`)VALUES('"+name+"','"+dob+"','"+place+"','"+dstrct+"','"+ph+"','"+em+"','"+gen+"','"+filename+"','"+str(lid)+"')"
    res = db.insert(qry2)
    return '<script>alert("Registration successfull");window.location="/"</script>'

    #return render_template('USER/user_registration.html')



@app.route('/userfb')
def userfb():
    return render_template('USER/userfb.html')

@app.route('/userfb_post', methods=["post"])
def userfb_post():
    db=Db()
    feedback=request.form["fd"]
    qry="INSERT INTO `lab_feedback`(`login_id`,`feedback`,`date`,`user_type`)VALUES('"+str(session['usid'])+"','"+feedback+"',curdate(),'user')"
    res=db.insert(qry)
    return '<script>alert("Feedback Added Successfully");window.location="/user_home"</script>'


@app.route('/view_med_report')
def view_med_report():
    db = Db()
    qry="SELECT `medical_report`.*,`lab`.* FROM `lab`,`medical_report` WHERE `lab`.`login_id`=`medical_report`.`lid` and  `medical_report`.`user_id`='"+str(session['usid'])+"'"
    res=db.select(qry)

    return render_template('USER/view_med_report.html',data=res)


@app.route('/labhomes')
def labhomes():
    return render_template('/LAB/labhome.html')



@app.route('/login',methods=['POST'])
def log():
    username=request.form["username"]
    password=request.form["pass"]
    db=Db()
    qry="SELECT * FROM `login_table` WHERE `username`='"+username+"' AND `password`='"+password+"'"
    res=db.selectOne(qry)
    print(res)
    if res is not None:
        if res["type"]=="lab":
            session['drid'] = res['lid']
            session['usid'] = res['lid']
            return render_template("LAB/doctorhome.html")
        elif res['type']=="user":
            session['usid'] = res['lid']
            return render_template("USER/user_home.html")
        elif res['type']=="admin":
            return render_template("ADMIN/adminhome.html")
        else:
            return '''<script>alert("Sorry...You are not verified");;window.location="/"</script>'''

    else:
        return '''<script>alert("incorrect username or password");;window.location="/"</script>'''

@app.route('/new_user')
def new_user():
       return render_template("/new_user.html")

@app.route('/new_user_post',methods=['POST'])
def new_user_post():
    type= request.form['type']
    if type=="user":
       return render_template("USER/user_registration.html")
    elif type=="doctor":
        return render_template("LAB/lab_registration.html")
    else:
        return render_template("LAB/labreg.html")


@app.route('/signupuser')
def signupuser():
    return render_template("USER/user_registration.html")

@app.route('/signuplab')
def signuplab():
    return render_template("LAB/lab_registration.html")



@app.route('/about')
def about():
    return render_template("about.html")
    pass
    

#########################user portion
@app.route('/training')
def admin_training():
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    datasets = pd.read_csv(r'C:\Users\SREEHARI\Downloads\Compressed\heart\heart\static\heart.xls')
    X = datasets.iloc[:,0:13].values
    Y = datasets.iloc[:, 13].values

    return render_template('/USER/training.html',X=X,Y=Y,lens=len(X))



@app.route('/doctor_chat')
def doctor_chat():
    hid = str(session["usid"])

    return render_template("/LAB/hm_chat.html", data=hid)


@app.route('/user_chat')
def user_chat():
    hid = str(session["usid"])

    return render_template("/USER/hm_chat.html", data=hid)

@app.route('/user_view_msg_users')
def view_msg_users():
    query = "select message,sender_id,receiver_id from chat order by chat_id"
    db=Db()
    json_data=db.select(query)
    return jsonify(json_data)

@app.route('/user_view_chat_users')
def user_view_chat_users():
    query = "select * from doctor_registration"
    db=Db()
    res=db.select(query)
    return jsonify(res)


@app.route('/doctor_view_chat_users')
def doctor_view_chat_users():
    query = "select * from `user_registration`"
    db=Db()
    res=db.select(query)
    return jsonify(res)

@app.route('/user_send_chat_users')
def user_send_chat_users():
    sender_id=str(session["usid"])
    receiver_id=request.args.get('receiver_id')
    message=request.args.get('message')
    query = "insert into chat(sender_id,receiver_id,message,c_date,c_time)VALUES('" + sender_id + "','" + receiver_id + "','" + message + "',curdate(),curtime())"
    db=Db()
    db.insert(query)
    return  jsonify(status='OK')




@app.route('/training_perform')
def admin_training_perform():
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd

    datasets = pd.read_csv(r'C:\Users\SREEHARI\Downloads\Compressed\heart\heart\static\heart.xls')
    X = datasets.iloc[:,0:13].values
    Y = datasets.iloc[:, 13].values

    from sklearn.model_selection import train_test_split
    X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.25, random_state=0)

    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    X_Train = sc_X.fit_transform(X_Train)
    X_Test = sc_X.transform(X_Test)

    from sklearn.ensemble import RandomForestClassifier
    classifier = RandomForestClassifier(n_estimators=200, criterion='entropy', random_state=0)
    classifier.fit(X_Train, Y_Train)
    Y_Pred = classifier.predict(X_Test)
    from sklearn.metrics import confusion_matrix
    cmrf = confusion_matrix(Y_Test, Y_Pred)
    from sklearn.metrics import accuracy_score
    accrf = accuracy_score(Y_Test, Y_Pred)

    from sklearn.tree import DecisionTreeClassifier
    classifier = DecisionTreeClassifier()
    classifier.fit(X_Train, Y_Train)
    Y_Pred = classifier.predict(X_Test)
    from sklearn.metrics import confusion_matrix
    cmdt = confusion_matrix(Y_Test, Y_Pred)
    from sklearn.metrics import accuracy_score
    accdt = accuracy_score(Y_Test, Y_Pred)



    from sklearn.linear_model import LogisticRegression
    classifier = LogisticRegression()
    classifier.fit(X_Train, Y_Train)
    Y_Pred = classifier.predict(X_Test)
    from sklearn.metrics import confusion_matrix
    cmlr = confusion_matrix(Y_Test, Y_Pred)
    from sklearn.metrics import accuracy_score
    acclr = accuracy_score(Y_Test, Y_Pred)

    from sklearn.naive_bayes import GaussianNB
    classifier = GaussianNB()
    classifier.fit(X_Train, Y_Train)
    Y_Pred = classifier.predict(X_Test)
    from sklearn.metrics import confusion_matrix
    cmnb = confusion_matrix(Y_Test, Y_Pred)
    from sklearn.metrics import accuracy_score
    accnb = accuracy_score(Y_Test, Y_Pred)

    from sklearn.svm import SVC
    classifier = SVC(gamma='auto')
    classifier.fit(X_Train, Y_Train)
    Y_Pred = classifier.predict(X_Test)
    from sklearn.metrics import confusion_matrix
    cmsvm= confusion_matrix(Y_Test, Y_Pred)
    from sklearn.metrics import accuracy_score
    accsvm = accuracy_score(Y_Test, Y_Pred)



    from sklearn.ensemble import GradientBoostingClassifier
    classifier = GradientBoostingClassifier()
    classifier.fit(X_Train, Y_Train)
    Y_Pred = classifier.predict(X_Test)
    from sklearn.metrics import confusion_matrix
    cmgb = confusion_matrix(Y_Test, Y_Pred)
    from sklearn.metrics import accuracy_score
    accgb = accuracy_score(Y_Test, Y_Pred)

    return render_template('/USER/confusionmatrix.html',accnb=accnb, cmrf=cmrf,accrf=accrf,cmdt=cmdt,accdt=accdt,cmgb=cmgb,cmlr=cmlr,cmnb=cmnb,cmsvm=cmsvm,accgb=accgb,acclr=acclr,accsvm=accsvm )

@app.route('/adminputs')
def adminputs():
    return render_template('/USER/inputs.html')


@app.route('/doctorinputs')
def doctorinputs():
    return render_template('/LAB/inputs.html')




@app.route('/adminputpost',methods=['post'])
def adminputpost():
    a1=float(request.form["a1"])
    a2=float(request.form["a2"])
    a3=float(request.form["a3"])
    a4=float(request.form["a4"])
    a5=float(request.form["a5"])
    a6=float(request.form["a6"])
    a7=float(request.form["a7"])
    a8=float(request.form["a8"])
    a9=float(request.form["a9"])
    a10=float(request.form["a10"])
    a11=float(request.form["a11"])
    a12=float(request.form["a12"])
    a13=float(request.form["a13"])

    test=[[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13]]

    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd

    datasets = pd.read_csv(r'D:\backups\pondi_heart\heart\static\heart.xls')
    X = datasets.iloc[:, 0:13].values
    Y = datasets.iloc[:, 13].values

    from sklearn.model_selection import train_test_split
    X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.25, random_state=0)


    from sklearn.tree import DecisionTreeClassifier
    classifier = DecisionTreeClassifier()
    classifier.fit(X_Train, Y_Train)
    Y_Pred_dt = classifier.predict(test)


    from sklearn.ensemble import RandomForestClassifier
    classifier = RandomForestClassifier()
    classifier.fit(X_Train, Y_Train)
    Y_Pred_rf = classifier.predict(test)

    from sklearn.linear_model import LogisticRegression
    classifier = LogisticRegression()
    classifier.fit(X_Train, Y_Train)
    Y_Pred_lr = classifier.predict(test)

    from sklearn.naive_bayes import GaussianNB
    classifier = GaussianNB()
    classifier.fit(X_Train, Y_Train)
    Y_Pred_nb = classifier.predict(test)

    from sklearn.svm import SVC
    classifier = SVC(gamma='auto')
    classifier.fit(X_Train, Y_Train)
    Y_Pred_svm = classifier.predict(test)

    from sklearn.ensemble import GradientBoostingClassifier
    classifier = GradientBoostingClassifier()
    classifier.fit(X_Train, Y_Train)
    Y_Pred_gb = classifier.predict(test)


    db=Db()
    qry="INSERT INTO `medical_report` (`lid`,`date`,`age`,`sex`,`cp`,`trestbps`,`chol`,`fbs`,`resting`,`thalx`,`exang`,`oldpeak`,`slope`,`cab`,`thal`,`num`,`result`) VALUES ('"+str(session["usid"])+"',now(),'"+str(a1)+"','"+str(a2)+"','"+str(a3)+"','"+str(a4)+"','"+str(a5)+"','"+str(a6)+"','"+str(a7)+"','"+str(a8)+"','"+str(a9)+"','"+str(a10)+"','','"+str(a11)+"','"+str(a12)+"','"+str(a13)+"','"+str(Y_Pred_dt[0])+"')"
    recordid=db.insert(qry)


    return render_template('/USER/inputs.html',recordid=recordid,Y_Pred_dt=Y_Pred_dt[0],Y_Pred_rf=Y_Pred_rf[0],Y_Pred_lr=Y_Pred_lr[0],Y_Pred_nb=Y_Pred_nb[0],Y_Pred_svm=Y_Pred_svm[0],Y_Pred_gb=Y_Pred_gb[0])


@app.route('/doctorputpost',methods=['post'])
def doctorputpost():
    a1=float(request.form["a1"])
    a2=float(request.form["a2"])
    a3=float(request.form["a3"])
    a4=float(request.form["a4"])
    a5=float(request.form["a5"])
    a6=float(request.form["a6"])
    a7=float(request.form["a7"])
    a8=float(request.form["a8"])
    a9=float(request.form["a9"])
    a10=float(request.form["a10"])
    a11=float(request.form["a11"])
    a12=float(request.form["a12"])
    a13=float(request.form["a13"])

    test=[[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13]]

    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd

    datasets = pd.read_csv(r'D:\backups\pondi_heart\heart\static\heart.xls')
    X = datasets.iloc[:, 0:13].values
    Y = datasets.iloc[:, 13].values

    from sklearn.model_selection import train_test_split
    X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.25, random_state=0)


    from sklearn.tree import DecisionTreeClassifier
    classifier = DecisionTreeClassifier()
    classifier.fit(X_Train, Y_Train)
    Y_Pred_dt = classifier.predict(test)


    from sklearn.ensemble import RandomForestClassifier
    classifier = RandomForestClassifier()
    classifier.fit(X_Train, Y_Train)
    Y_Pred_rf = classifier.predict(test)

    from sklearn.linear_model import LogisticRegression
    classifier = LogisticRegression()
    classifier.fit(X_Train, Y_Train)
    Y_Pred_lr = classifier.predict(test)

    from sklearn.naive_bayes import GaussianNB
    classifier = GaussianNB()
    classifier.fit(X_Train, Y_Train)
    Y_Pred_nb = classifier.predict(test)

    from sklearn.svm import SVC
    classifier = SVC(gamma='auto')
    classifier.fit(X_Train, Y_Train)
    Y_Pred_svm = classifier.predict(test)

    from sklearn.ensemble import GradientBoostingClassifier
    classifier = GradientBoostingClassifier()
    classifier.fit(X_Train, Y_Train)
    Y_Pred_gb = classifier.predict(test)



















    return render_template('/LAB/inputs.html',Y_Pred_dt=Y_Pred_dt[0],Y_Pred_rf=Y_Pred_rf[0],Y_Pred_lr=Y_Pred_lr[0],Y_Pred_nb=Y_Pred_nb[0],Y_Pred_svm=Y_Pred_svm[0],Y_Pred_gb=Y_Pred_gb[0])









@app.route('/lik')
def lik():
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    from sklearn.feature_selection import SelectFromModel
    from sklearn.metrics import accuracy_score

    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd

    # Importing the datasets
    feat_labels = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope',
                   'ca', 'thal']

    datasets = pd.read_csv(r'D:\backups\pondi_heart\heart\static\heart.xls')
    X = datasets.iloc[:, 0:13].values
    Y = datasets.iloc[:, 13].values

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=0)

    clf = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)

    # lk Train the classifier
    clf.fit(X_train, y_train)

    # lk Print the name and gini importance of each feature

    aa=[]

    for feature in zip(feat_labels, clf.feature_importances_):
        print(feature)
        aa.append(feature)

    sfm = SelectFromModel(clf, threshold=0.04)

    sfm.fit(X_train, y_train)

    X_important_train = sfm.transform(X_train)
    X_important_test = sfm.transform(X_test)

    # print(X_important_test)

    #
    # clf_important = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)
    # #
    # # # Train the new classifier on the new dataset containing the most important features
    # clf_important.fit(X_important_train, y_train)

    from sklearn.linear_model import LogisticRegression
    clf_important=LogisticRegression()
    clf_important.fit(X_important_train, y_train)





    # print("trained")
    #
    y_pred = clf_important.predict(X_important_test)
    print("predicted")
    # # View The Accuracy Of Our Full Feature (4 Features) Model
    s=accuracy_score(y_test, y_pred)
    #
    print(s)
    print("ok")

    #######################

    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)

    print(cm)

    from sklearn.metrics import roc_auc_score, average_precision_score, roc_curve
    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
    rocval = roc_auc_score(y_test, y_pred)

    avc = average_precision_score(y_test, y_pred)

    # Visualising the Training set results

    return render_template('/USER/confusionmatrix.html', cm=cm, rocval=rocval, average_precision_score=avc, fpr=fpr,
                           tpr=tpr,aa=aa)







    return "ok"




@app.route('/adminaddtip')
def adminaddtip():
    return render_template('/ADMIN/addtips.html')


@app.route('/admintippost',methods=['post'])
def admintippost():
    tips=request.form["tips"]
    db=Db()
    qry="INSERT INTO `healthtip` (`healthtip`,`tipdate`) VALUES ('"+tips+"',NOW())"
    db.insert(qry)
    return "<script>alert('Health tip added');window.location='/adminaddtip'</script>"



@app.route('/Suggestionview/<reportid>')
def Suggestionview(reportid):
    db=Db()
    qry="SELECT DISTINCT `doctor_registration`.*,`forward_rec`.* FROM `doctor_registration` INNER JOIN `forward_rec` ON `forward_rec`.`doctorloginid`=`doctor_registration`.`login_id` WHERE `forward_rec`.`recordid`='"+reportid+"'"
    print(qry)
    res=db.select(qry)
    return render_template('/USER/doctor_suggestion.html',data=res)






@app.route('/userhistory')
def userhistory():
    db=Db()
    qry="select * from medical_report where lid='"+str(session["usid"])+"'"
    res=db.select(qry)
    return render_template('USER/history.html',res=res)


@app.route('/doctorhistory/<plogid>')
def doctorhistory(plogid):
    db = Db()
    qry = "select medical_report.*,`forward_rec`.`suggestion`   FROM `medical_report`,`forward_rec` WHERE `forward_rec`.`recordid`=`medical_report`.`report_id` AND `forward_rec`.`doctorloginid`='"+str(session["usid"])+"' and  `medical_report`.`lid`= '" + str(plogid) + "'"
    print(qry)
    res = db.select(qry)

    return render_template('LAB/history.html', res=res)




@app.route('/adminaddnotification')
def adminaddnotification():
    return render_template('/ADMIN/addnoti.html')


@app.route('/adminpostnotification',methods=['post'])
def adminpostnotification():
    title=request.form["title"]
    notification=request.form["notification"]
    db=Db()
    qry="INSERT INTO `notification` (`title`,`notification`,`notdate`) VALUES('"+title+"','"+notification+"',NOW())"
    db.insert(qry)
    return "<script>alert('Notification added');window.location='/adminaddnotification'</script>"

@app.route('/adminviewtip')
def adminviewtip():
    db=Db()
    qry="select * from healthtip"
    data=db.select(qry)
    return render_template('/ADMIN/viewtips.html',data=data)

@app.route('/deletetip/<id>')
def deletetip(id):
    db=Db()
    qry="delete from healthtip where tipid='"+id+"'"
    db.delete(qry)
    return "<script>alert('Tip Deleted');window.location='/adminviewtip'</script>"


@app.route('/adminviewnotification')
def adminviewnotification():
    db=Db()
    qry="select * from notification"
    data=db.select(qry)
    return render_template('/ADMIN/viewnotification.html',data=data)

@app.route('/userviewnotification')
def userviewnotification():
    db=Db()
    qry="select * from notification"
    data=db.select(qry)
    return render_template('/USER/viewnotification.html',data=data)

@app.route('/deletenotification/<id>')
def deletenotification(id):
    db=Db()
    qry="delete from notification where notid='"+id+"'"
    db.delete(qry)
    return "<script>alert('Notification Deleted');window.location='/adminviewnotification'</script>"


@app.route('/viewcomplaints')
def viewcomplaints():
    db=Db()
    qry="SELECT `complaint`.*,`user_registration`.* FROM complaint INNER JOIN `user_registration` WHERE `complaint`.`logid`=`user_registration`.`login_id`"
    data=db.select(qry)
    return render_template('/ADMIN/viewcomplaints.html',data=data)



@app.route('/sentreply/<cid>')
def sentreply(cid):
    return  render_template('/ADMIN/addreply.html',cid=cid)


@app.route('/adminsentreply',methods=['post'])
def adminsentreply():
    cid=request.form["cid"]
    reply=request.form["reply"]
    db=Db()
    qry="UPDATE complaint SET `reply`='"+reply+"' ,STATUS='Done' WHERE cid='"+cid+"'"
    db.insert(qry)
    return "<script>alert('Reply sent');window.location='/viewcomplaints'</script>"


@app.route('/userviewprofile')
def userviewprofile():
    db = Db()
    qry = "SELECT * FROM `user_registration` WHERE `login_id`='" + str(session["usid"]) + "'"
    res = db.selectOne(qry)

    return render_template('USER/ud.html',data=res)



@app.route('/usersentcomplaint')
def usersentcomplaint():
    return render_template('/USER/sentcomplaints.html')

@app.route('/userpostcomplaint',methods=['post'])
def userpostcomplaint():
    subject=request.form["subject"]
    complaint=request.form["complaint"]
    db=Db()
    qry="INSERT INTO `complaint`(`logid`,`subject`,`complaint`,`cdate`,`reply`,`status`) VALUES('"+str(session["usid"])+"','"+subject+"','"+complaint+"',NOW(),'pending','pending')"
    db.insert(qry)
    return "<script>alert('Complaint sent');window.location='/usersentcomplaint'</script>"


@app.route('/userviewcomplaints')
def userviewcomplaints():
    db=Db()
    qry="SELECT `complaint`.*  FROM complaint WHERE `complaint`.`logid`='"+str(session["usid"])+"'"
    data=db.select(qry)
    return render_template('/USER/viewcomplaints.html',data=data)




@app.route('/userviewhealthtip')
def userviewhealthtip():
    db=Db()
    qry="select * from healthtip"
    data=db.select(qry)
    return render_template('/USER/viewtips.html',data=data)


@app.route('/doctor_profile')
def doctor_profile():
    db=Db()
    qry = "SELECT * FROM `lab_registration` WHERE `login_id`='"+str(session["usid"])+"'"
    print(qry)
    res = db.selectOne(qry)

    return render_template('LAB/doctor_profile.html',data=res)

@app.route('/dhomes')
def dhomes():
    return render_template('/LAB/doctorhome.html')

def red(fname):
    file = open(fname,mode='r')
    print("12")
    f=file.read()
    print("13")
    file.close()
    print("14")
    return f

from numpy import *
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tkinter import *
from PIL import ImageTk, Image

if __name__ == '__main__':
    app.run(debug=True)

