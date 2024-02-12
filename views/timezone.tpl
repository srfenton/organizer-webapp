<!DOCTYPE html>
<html>
<body>
   <h1>Timezone</h1>
   <p id="test"></p>
   <script>
      document.getElementById("test").innerHTML =
      Intl.DateTimeFormat().resolvedOptions().timeZone;
   </script>
</body>
</html> 