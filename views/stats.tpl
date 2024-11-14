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
      padding: 20px;
      text-align: center;
      font-family: 'Nunito Sans';
    }

    .button {
      background-color: #000000; /* black */
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
      color: white;
    }

    table {
      margin: 0 auto 45px;
      width: 100%;
      max-width: 800px;
      border-collapse: collapse;
    }

    th, td {
      border: 1px solid #ddd;
      padding: 10px;
      text-align: left;
    }

    th {
      background-color: #000000;
      color: #FFFFFF;
    }

    h2 {
      font-family: 'Nunito Sans';
      text-align: center;
      margin: 0 auto 45px;
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
    @media (max-width: 600px) {
  table, thead, tbody, th, td, tr {
    display: block;
  }
  th {
    display: none; /* Hide table headers */
  }
  td {
    display: block;
    text-align: right; /* Optional */
    padding-left: 50%;
    position: relative;
  }
  td::before {
    content: attr(data-label); /* Add data-label to display headers */
    position: absolute;
    left: 0;
    width: 50%;
    padding-left: 10px;
    font-weight: bold;
    text-align: left;
  }
}
  </style>
</head>
<body>

<h2><h2>Hello {{context['username']}}!<p></h2></h2>
<br>
<div class="table-container">
  <table>
    <thead>
      <tr>
        <th>Task</th>
        <th>Current Month</th>
        <th>Previous Month</th>
        <th>Total Percentage</th>
        <th>Days Assigned</th>
      </tr>
    </thead>
    <tbody>
    % for item in stats_list:
      <tr>
        <td data-label="Task">{{str(item['task'])}}</td>
        <td data-label="Current Month">{{str(item['current month'])}}</td>
        <td data-label="Previous Month">{{str(item['previous month'])}}</td>
        <td data-label="Total Percentage">{{str(item['total percentage'])}}</td>
        <td data-label="Days Assigned">{{str(item['days assigned count'])}}</td>
      </tr>
    % end
    </tbody>
  </table>
</div>

<ul class="footer-links">
  <li><a href="/list/{{context['user_id']}}?timezone={{context['timezone']}}">list</a></li>
  <li><a href="/completed-list/{{context['user_id']}}?timezone={{context['timezone']}}">completed</a></li>
  <li><a href="/regenerate/{{context['user_id']}}?timezone={{context['timezone']}}">regenerate list</a></li>
  <li><a href="/edit-list/{{context['user_id']}}?timezone={{context['timezone']}}">edit list</a></li>
  <li><a href="/logout">logout</a></li>
</ul>

</body>
</html>