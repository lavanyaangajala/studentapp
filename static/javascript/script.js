function editstudent(id, name, city, marks) {
    document.getElementById("studentid").value = studentid;
    document.getElementById("name").value = name;
    
    document.getElementById("city").value = city;
    document.getElementById("marks").value = marks;
    document.getElementById("edit-form-container").style.display = "block";
  }
  
function closeEditForm() {
    document.getElementById("edit-form-container").style.display = "none";
  }