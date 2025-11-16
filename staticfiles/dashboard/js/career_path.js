// signup.js

document.addEventListener("DOMContentLoaded", function () {
  // Bind career path dropdown change
  let careerPathSelect = document.getElementById("career_path");
  if (careerPathSelect) {
    careerPathSelect.addEventListener("change", toggleFields);
  }
});

// Toggle fields based on career path
function toggleFields() {
  var value = document.getElementById("career_path").value;

  var jobFields = document.querySelectorAll("#job_fields input");
  var higherFields = document.querySelectorAll("#higher_fields input");
  var startupFields = document.querySelectorAll("#startup_fields input");
  var otherFields = document.querySelectorAll("#other_fields input");

  // Reset
  jobFields.forEach(f => { f.required = false; });
  higherFields.forEach(f => { f.required = false; });
  startupFields.forEach(f => { f.required = false; });
  otherFields.forEach(f => { f.required = false; });

  document.getElementById("job_fields").style.display = "none";
  document.getElementById("higher_fields").style.display = "none";
  document.getElementById("startup_fields").style.display = "none";
  document.getElementById("other_fields").style.display = "none";

  // Show selected
  if (value === "job") {
    document.getElementById("job_fields").style.display = "block";
    jobFields.forEach(f => { f.required = true; });
  } else if (value === "higher_studies") {
    document.getElementById("higher_fields").style.display = "block";
    higherFields.forEach(f => { f.required = true; });
  } else if (value == "startup"){
    document.getElementById("startup_fields").style.display = "block";
    startupFields.forEach(f => { f.required = true; });
  } else if (value === "other") {
    document.getElementById("other_fields").style.display = "block";
    otherFields.forEach(f => { f.required = true; });
  } 
}

