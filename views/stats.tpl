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

    /* Responsive styling for the table */
    @media (max-width: 600px) {
      table, thead, tbody, th, td, tr {
        display: block;
      }
      thead tr {
        position: absolute;
        top: -9999px;
        left: -9999px;
      }
      tr {
        margin: 0 0 1rem 0;
        border: 1px solid #ccc;
        padding: 0.5rem;
      }
      td {
        border: none;
        padding: 0.5rem;
        position: relative;
        padding-left: 50%;
        text-align: left;
      }
      td::before {
        content: attr(data-label);
        position: absolute;
        left: 0;
        width: 45%;
        padding-left: 10px;
        font-weight: bold;
        text-align: left;
      }
    }
  </style>
</head>
<body>

<h2>Hello {{context['username']}}!<p></h2>
<br>
<div class="table-container">
  <table>
    <thead>
      <tr>
        <th>Task</th>
        <th>Current Month</th>
        <!-- <th>One month</th> -->
        <th>{{context['one_month_string']}}</th> 
        <th>{{context['two_months_string']}}</th>
        <th>Total Percentage</th>
        <th>Days Assigned</th>
      </tr>
    </thead>
    <tbody>
    % for item in stats_list:
      <tr>
        <td data-label="Task">{{str(item['task'])}}</td>
        <td data-label="Current Month">{{str(item['current month'])}}</td>
        <td data-label="{{context['one_month_string']}}">{{str(item['previous month'])}}</td>
        <td data-label="{{context['two_months_string']}}">{{str(item['two months'])}}</td>
        <td data-label="Total Percentage">{{str(item['total percentage'])}}</td>
        <td data-label="Days Assigned">{{str(item['days assigned count'])}}</td>
      </tr>
    % end
    </tbody>
  </table>
</div>

<ul class="footer-links">
  <li><a href="/list/{{context['user_id']}}">list</a></li>
  <li><a href="/account/{{context['user_id']}}">account</a></li>
  <li><a href="/completed-list/{{context['user_id']}}">completed</a></li>
  <li><a href="/edit-list/{{context['user_id']}}">edit list</a></li>
  <li><a href="/logout">logout</a></li>
</ul>


</body>
</html>
