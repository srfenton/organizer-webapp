<html>
<head>
 <link rel="manifest" href="/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href='https://fonts.googleapis.com/css?family=Nunito Sans' rel='stylesheet'>
<style>
tr, td {
  border-collapse: collapse;
  font-family: 'Nunito Sans';
  text-align: left;
  padding: 8px;
}

h2 {
  font-family: 'Nunito Sans';
</style>
</head>
<body>
<h2>completed task list</h2>
<hr/>
<table>
% for item in completed_list:
  <tr>
    <td>{{str(item['task'])}}</td>
  </tr>

% end
</table>

<hr/>
<a href="/list">back to list...</a><br>
<a href="/">home</a><br>
</body>
</html>