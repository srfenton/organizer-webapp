<!DOCTYPE html>
<html>
<head>

  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href='https://fonts.googleapis.com/css?family=Nunito Sans' rel='stylesheet'>

  <style>

    a, a:visited {
      color:black;
      text-decoration: none;
    }

    body {
      padding-top: 45px;
      text-align:center;
      font-family: 'Nunito Sans';
    }

    h1 {
      font-family: 'Nunito Sans';
      text-align: center;
      margin: 0 auto 45px;
    }

    h4 {
      font-family: 'Nunito Sans';
      text-align: center;
      margin: 0 auto 16px;
    }

    .button {
          background-color: #fd5844; /* electric orange */
          border: none;
          color: white;
          box-sizing: border-box;
          padding: 7px 16px;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          visited: inherited;
          font-size: 16px;
          margin: 4px 2px;
          cursor: pointer;
          -webkit-transition-duration: 0.4s; /* Safari */
          transition-duration: 0.4s;
        }

    .button2:hover {
      box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24),0 17px 50px 0 rgba(0,0,0,0.19);
    }

    .button_text {
    color: white;
    }

    .button_text a {
        color: white;

    .button_text a:visited {
        color: white;

    form {
      margin: 0 auto 45px;
      text-align: center;
    }

  </style>

</head>

<body>

<h1>Register</h1>


<script>
  function setTimezone() {
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    document.getElementById('timezone').value = timezone;
  }
</script>

<form action="/register" method="post" onsubmit="setTimezone()">
  <p>username: <input name="username"/></p>
  <p>password: <input name="password" type="password"/></p>
  <p>password confirmation: <input name="password_confirmation" type="password"/></p>
  <p><input type="hidden" name="timezone" id="timezone" value=""></p>
  <p><button class="button button2" type="submit">register</button></p>
</form>

<a href='/'>home</a>

</body>

</html>