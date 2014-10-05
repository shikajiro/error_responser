error responser
===============

指定したエラーを返すサーバー。エラーのレスポンステストなどに。
python、Flaskを利用。herokuにて稼働中。

## design
### URL
http://error-responser.herokuapp.com/{app_name}
### app_name
利用するアプリケーションの名前などを設定する。

## use
http://error-responser.herokuapp.com/{app_name} でアプリ名とstatus_codeを設定した後、http://error-responser.herokuapp.com/{app_name}/(以下任意) にアクセスすると指定したエラーを返す。

## sample
http://error-responser.herokuapp.com/shikajiro
で、404を設定したあと、以下にアクセスする。

http://error-responser.herokuapp.com/shikajiro/hogehoge

```
404 Not Found
```
http://error-responser.herokuapp.com/shikajiro
で、status_codeを404、error_codeを1に設定したあと、以下にアクセスする。

http://error-responser.herokuapp.com/shikajiro/hoge

```json
{
  "error": {
    "code": 1,
    "message": "this is error message"
  }
}
```
