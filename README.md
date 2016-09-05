# TECHNEX

# Api Documentation
## Registration Api
<br> <br>
Url: http://technex-ca.herokuapp.com/api/register
<br>
Method: POST
<br>
Json object Expected : 			//(all fields required)<br>
								{<br>
									"email" : emailOfUser,<br>
									"first_name" : firstName,<br>
									"last_name" : lastName,<br>
									"password" : password,<br>
									"college" : collegeName,<br>
									"year" : year(1,2,3,4,5)<br>
									"mobile_number" : mobileNumber<br>
								 }<br><br>

Json Response for Successful registration:<br>
								{<br>
								 	"status" : "Profile created successfully"<br>
								}<br><br>

Json Response for Error in Registration(validation Erorr):<br>
								{<br>
									"status" : "Registration in error",<br>
									"field_name": errorInField //field_name is same as above expected<br>
								}<br><br>

Json Response for Invalid Request(requests other than post):<br>
								{<br>
									"Error" : True,<br>
									"status" : "invalid request,Post request Please!"<br>
								}<br><br><br>

## Login Api
<br><br>
Url: http://technex-ca.herokuapp.com/api/login
<br>
Method: POST
<br>
Json object Expected:<br>			{<br>
									"email" : email,<br>
									"password" : password<br>
								}<br><br>

Json Response for successful Login: <br>
								{<br>
									"status" : "logged in"<br>
								}<br><br>

Json Response for wrong Username/password:<br>
								{<br>
									"Error" : True,<br>
									"status" : "Invalid Credentials!"<br>
								}<br>

Json Response for invalid form submission(empty username/password and other validation errors):<br>
								{<br>
									"Error" : True,<br>
									"status" : "Please Fill the form correctly!"<br>
								}<br><br><br>					
