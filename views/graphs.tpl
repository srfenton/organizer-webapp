<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</head>

<script>
document.addEventListener("DOMContentLoaded", function() {
    let table = document.getElementById("data-table");
    let labels = [];
    let data = [];

    // Loop through table rows (skip the header row)
    for (let i = 1; i < table.rows.length; i++) {
        labels.push(table.rows[i].cells[0].innerText); // X-axis values
        data.push(parseInt(table.rows[i].cells[1].innerText)); // Y-axis values
    }

    // Create a line chart using Chart.js
    new Chart(document.getElementById("lineChart"), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Sales Data",
                data: data,
                borderColor: "blue",
                fill: false
            }]
        },
        options: {
            responsive: true
        }
    });
});
</script>



<body>


<p>hello</p>

<canvas id="lineChart"></canvas>

<table id="data-table">
    <tr>
        <th>Month</th>
        <th>Sales</th>
    </tr>
    <tr>
        <td>Jan</td>
        <td>100</td>
    </tr>
    <tr>
        <td>Feb</td>
        <td>150</td>
    </tr>
    <tr>
        <td>Mar</td>
        <td>200</td>
    </tr>
</table>



</body>
</html>