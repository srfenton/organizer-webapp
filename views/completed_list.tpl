<!DOCTYPE html>
<html>
<head>

 <link rel="manifest" href="/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href='https://fonts.googleapis.com/css?family=Nunito Sans' rel='stylesheet'>

  <style>

    a, a:visited {
      text-decoration: none;
      color: black;
    }

    body {
      padding-top: 45px;
    }


    table {
      margin: 0 auto 45px;
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

    .footer-links a, a:visited {
      color: black;
      text-decoration: none;
    }

    .undo {
    }

    .undo a, a:visited {
      color: #fd5844;
    }


  </style>
</head>
<body>
<h2>Completed Task List</h2>

<table>
% for item in completed_list:
  <tr>
    <td>{{str(item['task'])}}</td>
    <td><a class="undo" href="/undo-complete/{{str(item['id'])}}">undo</a></td>
  </tr>

% end
</table>

<ul class="footer-links">
  <li><a href="/">home</a></li>
  <li><a href="/list">daily list</a></li>
  <li><a href="/regenerate">regenerate list</a></li>
</ul>

</body>
</html>