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

    .button {
      background-color: inherit;
      border: none;
      cursor: pointer;
      color: black;
      font-family: inherit;
      font-size: inherit;
      line-height: inherit;
      margin: 0;
      padding: 0;
      text-decoration: none;
    }

.button:hover {
  color: #FA2D48;
  background-color: transparent;
}

  </style>
</head>
<body>
<h2>Vacations</h2>

<table>
% for item in vacation_days_list:
  <tr>
    <td>{{str(item['vacation_date'])}}</td>
    <td>
      <form action="/delete-vacation" method="post">
        <input name="user_id" type="hidden" value="{{str(item['user_id'])}}"/>
        <input name="id" type="hidden" value="{{str(item['id'])}}"/>
        <input name="timezone" type="hidden" value="{{context['timezone']}}"/>
        <button class="button" type="submit">delete</button>
      </form>

    </td>
  </tr>

% end
</table>

<ul class="footer-links">
  <li><a href="/logout">logout</a></li>
  <li><a href="/account/{{context['user_id']}}">account</a></li>
  <li><a href="/list/{{context['user_id']}}">list</a></li>
  <li><a href="/edit-list/{{context['user_id']}}">edit list</a></li>
  <!-- <li><a href="/regenerate/{{context['user_id']}}">regenerate list</a></li> -->
  <li><a href="/stats/{{context['user_id']}}">stats</a></li>
  
</ul>

</body>
</html>