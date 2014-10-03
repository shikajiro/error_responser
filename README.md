error responser
===============

指定したエラーを返すサーバー。エラーのレスポンステストなどに。
python、Flaskを利用。herokuにて稼働中。

## design
### URL
http://error-responser.herokuapp.com/{status_code}/{error_code}
### status_code
httpのstatus codeを指定する
### error_code
status code だけでなく、エラー情報が詰まったjsonも必要な場合利用する。

## sample
http://error-responser.herokuapp.com/404/1

```json
{
  "error": {
    "code": 1,
    "message": "this is error message"
  }
}
```
