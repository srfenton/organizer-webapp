<!DOCTYPE html>
<html>
<head>

  <link rel="manifest" href="/manifest.json">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href='https://fonts.googleapis.com/css?family=Nunito Sans' rel='stylesheet'>

  <style>

    p {
      color: black;
    }
    a {
      color: black;
      text-decoration: none;
    }


    body {
      padding-top: 45px;
      text-align: center
    }

    .button {
      background-color: #000000; /* electric orange */
      border: none;
      color: white;
      font-family: 'Nunito Sans';
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
    color: white
    }

    table {
      margin: 0 auto 45px;
    }

    .button_text {
    color: white
    }


    tr, td {
      border-collapse: collapse;
      font-family: 'Nunito Sans';
      text-align: left;
      padding: 20px;
    }

    h2 {
      font-family: 'Nunito Sans';
      text-align: center;
      margin: 0 auto 45px
    }

    .footer-links {
      list-style-type: none;
      padding: 0;
      margin: 0;
      text-align: center;
    }

    .footer-links li {
      display: inline-block;
      padding: 30px;
    }

    .footer-links a, .footer-links a:visited {
      color: black;
      text-decoration: none;
    }
  </style>
</head>
<body>

<h2>{{context['username']}}'s account settings<p></h2>
<br>
<p><a href="/account/vacations/{{context['user_id']}}">vacations</a></p>
<!-- <p><a href="/">change password</a></p> -->

<ul class="footer-links">
  <li><a href="/logout">logout</a></li>
  <li><a href="/completed-list/{{context['user_id']}}">completed</a></li>
  <li><a href="/edit-list/{{context['user_id']}}">edit list</a></li>
  <li><a href="/stats/{{context['user_id']}}">stats</a></li>
</ul>

</body>
</html>