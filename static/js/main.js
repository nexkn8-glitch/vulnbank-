// Minimal UI JS - nothing security related; students can extend.
document.addEventListener("DOMContentLoaded", function(){
  // small nicety: prevent forms from auto-filling by browsers in lab
  document.querySelectorAll("input[type=password]").forEach(i => i.autocomplete = "new-password");
});
