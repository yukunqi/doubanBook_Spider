from MainRequest import MainRequest


if __name__ == '__main__':
    proxy=MainRequest()
    response=proxy._request_with_proxy('https://httpbin.org/get',use_proxy=True)
    print(response.text)