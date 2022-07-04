#authentication

#login

#view for listing all todos

#view for fetching a specific todos

#list all todos created by authenticated user

#view for updating a specific todos

#view for deleting a specific todos

#logout

from todosapp.models import users,todos

session={}

def signinrequired(fn):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("you Must LogIn")
    return wrapper

def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user=[user for user in users if user["username"]==username and user["password"]==password]
    return user


class SignInView():
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            session["user"]=user[0]
            print("Login Success")
        else:
            print("Invalid Credentials")

class TodoView():       #view for listing all todos
    @signinrequired
    def get(self,*args,**kwargs):
        return todos

    @signinrequired
    def post(self, *args, **kwargs):   #view for fetching a specific todos
        userId = session["user"]["id"]
        kwargs["userId"] = userId
        todos.append(kwargs)  # to add new post to the posts list
        print("todo added")
        print(todos)

class MytodoListView():           #list all todos created by authenticated user
    @signinrequired
    def get(self,*args,**kwargs):
        print(session)
        userId=session["user"]["id"]
        print(userId)
        my_todos=[todo for todo in todos if todo["userId"]==userId]
        print(my_todos)

class TodoDetailsView():
    def get_object(self,id):
        todo=[todo for todo in todos if todo["todoId"]==id]
        return todo


    @signinrequired
    def get(self,*args,**kwargs):
        todo_id=kwargs.get("todo_id")
        todo=self.get_object(todo_id)
        return todo

    @signinrequired
    def __delete__(self,*args,**kwargs):   #view for deleting a specific todos
        todo_id=kwargs.get("todo_id")
        data=self.get_object(todo_id)
        if data:
            todo=data[0]
            todos.remove(todo)
            print("todo removed")
            print(len(todos))

    @signinrequired
    def put(self,*args,**kwargs):   #view for updating a specific todos
        todo_id=kwargs.get("todo_id")
        data = kwargs.get("data")
        instance=self.get_object(todo_id)
        if instance:
            todo_obj=instance[0]
            todo_obj.update(data)
            return todo_obj

@signinrequired
def signout(*args,**kwargs):    #Logout

    user=session.pop("user")
    print(f"The user {user['username']} has been logout")


log=SignInView()
log.post(username="anu",password="Password@123")



# data=TodoView()
# print(data.get())

# data.post(todoId=9,
#           task_name="phonebill",
#           completed="False",
#
# )



# mytodo=MytodoListView()
# mytodo.get()


# todo_detail=TodoDetailsView()
# todo_detail.__delete__(todo_id=6)
# print(todo_detail.get(todo_id=3))

# data={
#     'task_name':"Elecbill"
# }
# tododetails=TodoDetailsView()
# print(tododetails.put(todo_id=4,data=data))



signout()




