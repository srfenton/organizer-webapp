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
      background-color: #000000; /* black */
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

    table {
      margin: 0 auto 45px;
    }

    .button_text a, a:visited{
    color: white;
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


    form {
      margin: 0 auto 45px;
      text-align: center;
    }

    input[name="new_task"] {
      border: 0 none;
      font: 'Nunito Sans';
      color: #000000;
      width: 150px;
      padding: 6px 15px 6px 35px;
      -webkit-border-radius: 20px;
      -moz-border-radius: 20px;
      border-radius: 20px;
      -webkit-box-shadow: 0 1px 0 rgba(255, 255, 255, 0.1), 0 1px 3px rgba(0, 0, 0, 0.2) inset;
      -moz-box-shadow: 0 1px 0 rgba(255, 255, 255, 0.1), 0 1px 3px rgba(0, 0, 0, 0.2) inset;
      box-shadow: 0 1px 0 rgba(255, 255, 255, 0.1), 0 1px 3px rgba(0, 0, 0, 0.2) inset;
      -webkit-transition: all 0.7s ease 0s;
      -moz-transition: all 0.7s ease 0s;
      -o-transition: all 0.7s ease 0s;
      transition: all 0.7s ease 0s;
    }

  </style>

</head>
<body>

<h2>Edit Daily List</h2>

<table>
  % for item in task_list:
    <tr>
      <td>{{str(item['task'])}}</td>
      <td>
          <form action="/remove-task" method="post">
            <p>
              <input name="id" type="hidden" value="{{str(item['id'])}}"/>
              <input name="user_id" type="hidden" value="{{str(item['user_id'])}}"/>
              <input name="timezone" type="hidden" value="{{context['timezone']}}"/>
              <button class="button button2" type="submit">remove</button>
            </p>
          </form>
    </tr>

  % end
</table>

<form action="/add-task" method="post">
  <p>
    <input name="new_task"/>
    <input name="user_id" type="hidden" value="{{str(item['user_id'])}}"/>
    <input name="timezone" type="hidden" value="{{context['timezone']}}"/>
    <button class="button button2" type="submit">add</button>
  </p>
</form>

<ul class="footer-links">
  <li><a href="/logout">logout</a></li>
  <li><a href="/completed-list/{{context['user_id']}}?timezone={{context['timezone']}}">completed</a></li>
  <li><a href="/regenerate/{{context['user_id']}}?timezone={{context['timezone']}}">regenerate list</a></li>
  <li><a href="/list/{{context['user_id']}}?timezone={{context['timezone']}}">daily list</a></li>
</ul>

</body>
</html>