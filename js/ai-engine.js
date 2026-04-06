const patient = JSON.parse(localStorage.getItem("patient"));

fetch("data/harvard_conditions.json")
  .then(res => res.json())
  .then(conditions => {

  // Combine primary + secondary symptom
  const symptomText = (patient.primary_symptom + " " + patient.secondary_symptom).toLowerCase();

  // Match symptom to condition
  let matched = conditions.find(c => symptomText.includes(c.keyword)) || conditions[0];

  // BMI
  const heightM = patient.height / 100;
  const bmi = patient.weight / (heightM * heightM);

  // Risk score calculation
  const riskScore = Math.round(
    (patient.pain_level * 0.4) +
    (patient.stress_level * 0.3) +
    ((patient.overtime_hours || 0) * 0.1) +
    ((patient.repetitive_work || 0) * 0.2)
  );

  let riskLevel = "Low";
  if(riskScore >= 7) riskLevel = "High";
  else if(riskScore >= 4) riskLevel = "Medium";

  const resultHTML = `
    Date: ${new Date().toLocaleDateString()}<br>
    Name: ${patient.name}<br>
    Employee ID: ${patient.employee_id}<br>
    Age: ${patient.age}<br>
    Gender: ${patient.gender}<br>
    BMI: ${bmi.toFixed(1)}<br>
    Symptom: ${symptomText}<br>
    Risk Score: ${riskScore}<br>
    Risk Level: ${riskLevel}<br>
    Condition: ${matched.name}<br>
    Recommended Medicine: ${matched.medicine}<br>
    Recommended Test: ${matched.test}<br>
    Advice Exercise: ${matched.exercise}<br>
    Advice Food: ${matched.food}<br>
    Specialist Doctor: ${matched.doctor}<br>
  `;

  document.getElementById("result").innerHTML = resultHTML;

  // Save to research backup
  const db = JSON.parse(localStorage.getItem("research")||"[]");
  db.push({patient, bmi, riskScore, riskLevel, condition: matched.name});
  localStorage.setItem("research", JSON.stringify(db));

});
