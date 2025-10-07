function showProgressBar() {
    var progressBar = document.getElementById('loading');

        // Remove the 'hidden' attribute to make the progress bar visible
        progressBar.removeAttribute('hidden');
        setInterval(updateProgressBar, 1000);
  
}