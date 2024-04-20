document.addEventListener('DOMContentLoaded', function() {
    // Function to show only checked boxes
    function showCheckedBoxes() {
        var checkedBoxes = document.querySelectorAll('input[name="work_contributions[]"]:checked');
        var questionsDiv = document.getElementById("questions");
        var icQuestionsDiv = document.getElementById("individual_contributor_questions");
        var pmQuestionsDiv = document.getElementById("project_manager_questions");
        var pepQuestionsDiv = document.getElementById("people_manager_questions");

        // Hide all question divs
        icQuestionsDiv.style.display = "none";
        pmQuestionsDiv.style.display = "none";
        pepQuestionsDiv.style.display = "none";

        // Show questions based on checked boxes
        checkedBoxes.forEach(function(checkbox) {
            if (checkbox.value === "individual_contributor") {
                icQuestionsDiv.style.display = "block";
            } else if (checkbox.value === "project_manager") {
                pmQuestionsDiv.style.display = "block";
            } else if (checkbox.value === "people_manager") {
                pepQuestionsDiv.style.display = "block";
            }
        });

        // Show questions div if any box is checked
        if (checkedBoxes.length > 0) {
            questionsDiv.style.display = "block";
        } else {
            questionsDiv.style.display = "none";
        }
    }

    // Call the function initially and on checkbox change
    showCheckedBoxes();
    document.querySelectorAll('input[name="work_contributions[]"]').forEach(function(checkbox) {
        checkbox.addEventListener('change', showCheckedBoxes);
    });

});
