source config.txt
curl --location --request POST 'https://api.resy.com/3/auth/password' \
--header 'Authorization: ResyAPI api_key=""' \
--form 'email=' \
--form 'password='