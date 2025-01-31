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

<h2>Hello {{context['username']}}!<p></h2>
<br>
<table>
  % for item in uncompleted_task_list:
    <tr>
      <td>{{str(item['task'])}}</td>
      <td>
        <form action="/complete" method="post">
        <input name="user_id" type="hidden" value="{{ str(item['user_id']) }}"/>
        <input name="id" type="hidden" value="{{ str(item['id']) }}"/>
        <input name="timezone" type="hidden" value="{{context['timezone']}}"/>
        <input name="username" type="hidden" value="{{context['username']}}"/>
        <button class="button button2" type="submit">complete</button>
      </form>
      </td>
    </tr>

  % end
</table>

 <label for="date">select a date:</label>

<select name="date" id="date">
  <option value="today">today</option>
  <option value="yesterday">yesterday</option>
</select> 

<ul class="footer-links">
  <li><a href="/logout">logout</a></li>
  <li><a href="/account/{{context['user_id']}}">account</a></li>
  <li><a href="/completed-list/{{context['user_id']}}">completed</a></li>
  <li><a href="/edit-list/{{context['user_id']}}">edit list</a></li>
  <li><a href="/stats/{{context['user_id']}}">stats</a></li>
</ul>

<script>
  const dateSelect = document.getElementById('date');

  // Dynamically set the dropdown to match the current query parameter on page load
  const params = new URLSearchParams(window.location.search);
  const currentDate = params.get('date') || 'today'; // Default to 'today' if no parameter is present
  dateSelect.value = currentDate;

  dateSelect.addEventListener('change', () => {
    const selectedDate = dateSelect.value; // Get the selected date
    const userId = "{{context['user_id']}}"; // Insert user ID dynamically

    // Redirect to the appropriate URL based on the selected date
    if (selectedDate === "yesterday") {
      window.location.href = `/list/${userId}?date=yesterday`;
    } else {
      window.location.href = `/list/${userId}?date=today`;
    }
  });
</script>

</body>
</html>