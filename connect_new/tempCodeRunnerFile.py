@app.route("/findTrack", methods=["POST", "GET"])
# def saveDetails():
#     msg = "msg"
#     if request.method == "POST":
#         try:
#             EmployeeId = request.form["EmployeeId"]
#             Title = request.form["Title"]
#             BirthDate = request.form["BirthDate"]
#             HireDate = request.form["HireDate"]
#             Address = request.form["Address"]
#             City = request.form["City"]
#             Phone = request.form["Phone"]
#             Email = request.form["Email"]
#             with sqlite3.connect("instance/MyDataBase.db") as con:
#                 cur = con.cursor()
#                 cur.execute("INSERT into Employee (EmployeeId, Title, BirthDate, HireDate, Address, City, Phone, Email) values (?,?,?,?,?,?,?,?)", (EmployeeId, Title, BirthDate, HireDate, Address, City, Phone, Email))
#                 con.commit()
#                 msg = "Employee successfully Added"
#         except:
#             con.rollback()
#             msg = "We can not add the employee to the list"
#         finally:
#             con.close()
#             return render_template("success.html", msg=msg)