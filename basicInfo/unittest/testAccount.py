import requests

def testImg():
    api = "http://127.0.0.1:8000/api/account/img"
    post = {
        "account_id": "3150105000",
    }
    files={
        "file":open("favicon.jpg","rb")
    }

    response = requests.post(url=api, data=post,files=files)
    print(response.text)

def testImgGet():
    api="http://127.0.0.1:8000/api/account/img"
    post={
        "account_id": "3150104497",
    }
    response=requests.get(url=api,params=post)
    print(response.text)

if __name__=="__main__":
    testImgGet()