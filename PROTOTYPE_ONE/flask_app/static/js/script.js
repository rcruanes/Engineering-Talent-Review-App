document.addEventListener('DOMContentLoaded', function() {
    function showCheckedBoxes() {
        var icQuestionsDiv = document.getElementById("individual_contributor_questions");
        var pmQuestionsDiv = document.getElementById("project_manager_questions");
        var pepQuestionsDiv = document.getElementById("people_manager_questions");

        // Hide all question divs
        icQuestionsDiv.style.display = "none";
        pmQuestionsDiv.style.display = "none";
        pepQuestionsDiv.style.display = "none";

        // Collect all checked checkboxes
        var checkedBoxes = document.querySelectorAll('input[name="work_contributions[]"]:checked');
        checkedBoxes.forEach(function(checkbox) {
            switch (checkbox.value) {
                case "individual_contributor":
                    icQuestionsDiv.style.display = "block";
                    break;
                case "project_manager":
                    pmQuestionsDiv.style.display = "block";
                    break;
                case "people_manager":
                    pepQuestionsDiv.style.display = "block";
                    break;
            }
        });

        // Show or hide the questions container
        document.getElementById("questions").style.display = checkedBoxes.length > 0 ? "block" : "none";
    }

    // Initialize the display of checkboxes and attach change event listeners
    showCheckedBoxes();
    document.querySelectorAll('input[name="work_contributions[]"]').forEach(function(checkbox) {
        checkbox.addEventListener('change', showCheckedBoxes);
    });

    // Form submission validation
    document.getElementById('recommendationForm').addEventListener('submit', function(event) {
        var valid = true;
        var checkedBoxes = document.querySelectorAll('input[name="work_contributions[]"]:checked');
        
        if (checkedBoxes.length === 0) {
            alert('Please select at least one work contribution.');
            valid = false;
        } else {
            // Validate the first two questions for each selected role
            checkedBoxes.forEach(function(box) {
                var role = box.value;
                var question1 = document.getElementById(role + '_q1');
                var question2 = document.getElementById(role + '_q2');
                
                // Ensure the first two questions are not empty
                if (!question1.value.trim() || !question2.value.trim()) {
                    alert('Please fill in the first two questions for all selected contributions.');
                    valid = false;
                }
            });
        }

        if (!valid) {
            event.preventDefault(); // Stop form submission
        }
    });
});
