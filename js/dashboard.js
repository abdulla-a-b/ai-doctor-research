const db = JSON.parse(localStorage.getItem("research")||"[]");
let html = "<table><tr><th>Name</th><th>ID</th><th>Condition</th><th>Risk</th><th>BMI</th></tr>";
db.forEach(d => {
  html += `<tr>
    <td>${d.patient.name}</td>
    <td>${d.patient.employee_id}</td>
    <td>${d.condition}</td>
    <td>${d.riskLevel}</td>
    <td>${(d.bmi).toFixed(1)}</td>
  </tr>`;
});
html += "</table>";
document.getElementById("dashboard").innerHTML = html;
