## rest-api transfer money
- docker-compose build
- docker-compose up

##### регистрация по адресу: -  /rest-auth/registration/

пример запроса:
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d 'email=<user_email>&password1=<user_password>&password2=<user_password>&balance=<start_balance>&currency=<currency_account>' 'http://127.0.0.1:8000/rest-auth/registration/'
 
где : email - емаил для регистрации, 
password1 - пароль пользователя,
password2 - подтверждение пароля,
balance - начальный баланс(валдация провряет только чтобы сумма была > 0, тип данный не проверяется),
currency - валюта счета.

##### для получения данных пользователя: - /api/v1/myprofile/

пример запроса:
curl -u <user_email>:<user_password> http://127.0.0.1:8000/api/v1/myprofile/

пример ответа:
[{"user":{"email":"test@mail.ru"},"accounts":{"balance":42663.351,"currency":"rub"},"transactions":[{"amount":8717.220000000001,"to_user":{"email":"test@mail.ru"},"from_user":{"email":"another@mail.ru"}},{"amount":30946.131,"to_user":{"email":"test@mail.ru"},"from_user":{"email":"another@mail.ru"}}]}]


##### первод валюты между пользователями: - /api/v1/transfer/

пример запроса:
curl -u <user_email>:<user_password> -H "Content-Type: application/x-www-form-urlencoded" -d 'amount=<some_amount>&to_user=<email_user>' http://127.0.0.1:8000/api/v1/transfer/

где: amount - сумма первода, 
to_user - емаил пользователя, которому будет произведен перевод денег

при переводе, если сумма перевода будет больше суммы баланса то, переводе будет отказанно.
если валюты счетов будет различаться, то будет произведена конвертация в валюту получателя, курс валют
захордкожен в коде.

- аутентификация производится по емаилу и паролю пользователя