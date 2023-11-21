document.addEventListener('DOMContentLoaded', function() {
    const button = document.createElement('button');
    button.innerHTML = 'More Information';
    button.onclick = function() {
        alert('This is our project');
    };
    document.body.appendChild(button);
});
