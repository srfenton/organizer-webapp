<!DOCTYPE html>
<html>
<head>

  <link rel="manifest" href="/manifest.json">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href='https://fonts.googleapis.com/css?family=Nunito Sans' rel='stylesheet'>

  <style>


    a, a:visited {
      color: black;
      text-decoration: none;
    }

    body {
      padding-top: 45px;
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
    color: white
    }

    table {
      margin: 0 auto 45px;
    }

    .button_text a, a:visited{
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

<h2>Daily List</h2>

<table>
  % for item in task_list:
    <tr>
      <td>{{str(item['task'])}}</td>
      <td><button class="button button2"><a class=button_text href="/complete/{{str(item['id'])}}">complete</a></button></td>
    </tr>

  % end
</table>

<ul class="footer-links">
  <li><a href="/">home</a></li>
  <li><a href="/completed-list">completed</a></li>
  <li><a href="/regenerate">regenerate list</a></li>
</ul>

</body>
</html>