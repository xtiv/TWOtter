import json
from uuid import UUID
import uuid
from typing import Optional, List
from datetime import date, datetime

from pydantic import BaseModel
from pydantic import EmailStr, Field

from fastapi import FastAPI 
from fastapi import status
from fastapi import Body, Query

app = FastAPI()

# Models


class UserBase(BaseModel):
    user_id : UUID = Field(...)
    email : EmailStr = Field(...)

class UserLogin(UserBase):
    password:str=Field(...,
                       min_length=8,
                       max_length=50)

class User(UserBase):
    frist_name : str = Field(...,
                             min_length=2,
                             max_length=20)
    last_name : str = Field(...,
                            min_length=2,
                            max_length=20)
    birth_date : Optional[date] = Field(default=None)
    
class UserRegister(User, UserLogin):
    pass

class Tweet(BaseModel):
    tweet_id : UUID = Field(...)
    content : str = Field(...,
                          max_length=256,
                          min_length=2)
    created_at : datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None) 
    by : User = Field(...)


## Users

### Register a user
@app.post(path="/signup",
          response_model=User,
          status_code = status.HTTP_201_CREATED,
          summary="Register a User",
          tags=["Users"])
def signup(user: UserRegister = Body(...)):
    """
    Signup
    
    This path operation register a user in the app
    
    Parameters:
        -Request body barameter
            -user: UserRegister

    Returns:
        -user_id: UUID
        -email: Emailstr
        -first_name: str
        -last_name: str
        -birth_date: datetime
    """
    # el "r+" quiere decir que lee y escribe
    with open("users.json", "r+", encoding="utf-8") as f:
        #Con json.loads nos permite crear un simil json, en este caso una lista de dicts
        #Los pasos son los siguentes:
        
        # 1- Leemos el json con .read() y lo transformamos en un tipo de dato que podemos trabajar con json.loads
        # 2- Crea un diccionario a partir del request Body (user)
        # 3- Casting de variables que no se pueden manejar a str
        # 4- Y se hace un append del dict
        # 5- Hay que moverse al principio del archivo porque ya se estuvo trabajando abierto, esto para evitar bugs, se realiza con ".seek(0)", nos lleva al primer byte
        # 6- Hay que hacer el write pero en json, se realiza con "json.dumps()"
        # 7- Se hace un return de user, el que viene como parámetro, para decirle al user del API que se escribio correctamente
        
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

        
### Login a user
@app.post(path="/login",
          response_model=User,
          status_code = status.HTTP_200_OK,
          summary="Login a User",
          tags=["Users"])
def login():
    pass

### Show all users
@app.get(path="/users",
          response_model=List[User],
          status_code = status.HTTP_200_OK,
          summary="Show all Users",
          tags=["Users"])
def show_all_users():
    """Show all user

    Parameters:
        -
    Returns a json list with all users in the app, with the following keys
        -user_id: UUID
        -email: Emailstr
        -first_name: str
        -last_name: str
        -birth_date: datetime
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results


### Show a user
@app.get(path="/users/{user_id}",
          response_model=User,
          status_code = status.HTTP_200_OK,
          summary="Show a User",
          tags=["Users"])
def show_a_user():
    pass

### Delete a user
@app.delete(path="/users/{user_id}/delete",
          response_model=User,
          status_code = status.HTTP_200_OK,
          summary="Delete a User",
          tags=["Users"])
def delete_a_user():
    pass

### Update a user
@app.put(path="/users/{user_id}/update",
          response_model=User,
          status_code = status.HTTP_200_OK,
          summary="Update a User",
          tags=["Users"])
def update_a_user():
    pass


## Tweets

### Show all tweets
@app.get(path="/",
        response_model=List[Tweet],
        status_code = status.HTTP_200_OK,
        summary="Show all tweets",
        tags=["Tweets"])
def home():
    """
    Show all tweets

    Parameters:
        -
    Returns:
        -tweet_id: UUID
        -content : str
        -created_at : datetime
        -updated_at : Optional[datetime]
        -by : User
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results


### Post a tweet
@app.post(path="/post",
        response_model=Tweet,
        status_code = status.HTTP_201_CREATED,
        summary="Post a tweet",
        tags=["Tweets"])
def post_tweet(tweet: Tweet = Body(...)):
    
    """
    Post a tweet
    
    This path operation post a tweet in the app
    
    Parameters:
        -Request body barameter
            -tweet: Tweet

    Returns:
        -tweet_id: UUID
        -content : str
        -created_at : datetime
        -updated_at : Optional[datetime]
        -by : User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

### Show a tweet
@app.get(path="/tweets/{tweet_id}",
        response_model=Tweet,
        status_code = status.HTTP_200_OK,
        summary="Show a tweet",
        tags=["Tweets"])
def show_a_tweet():
    pass

### Delete a tweet
@app.delete(path="/tweets/{tweet_id}",
        response_model=Tweet,
        status_code = status.HTTP_200_OK,
        summary="Delete a tweet",
        tags=["Tweets"])
def delete_a_tweet():
    pass

### Update a tweet
@app.put(path="/tweets/{tweet_id}",
        response_model=Tweet,
        status_code = status.HTTP_200_OK,
        summary="Update a tweet",
        tags=["Tweets"])
def update_a_tweet():
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    